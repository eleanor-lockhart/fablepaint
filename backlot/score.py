"""backlot.score: writing music down. Pitches, scales, chords, and a sequence of notes in bars and beats
that renders through instruments into a Mix.

    s = Seq(bpm=60, beats=3)                              # slow three-in-a-bar
    s.note('lead', 'A4', bar=1, beat=1, length=1, vel=.7)
    s.chord('pad', 'D3', 'm9', bar=1, length=6)
    s.render(mix, {'lead': dict(inst=pluck, gain=-12, send=-8), 'pad': dict(inst=..., gain=-24)})
"""
import math
import numpy as np

A4 = 440.0
_SEMI = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
NAMES = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']

def midi(n):
    """'D4', 'F#3', 'Bb2' -> MIDI note number (A4 = 69). Numbers pass through."""
    if not isinstance(n, str): return float(n)
    acc = n[1:-1] if not n[-2].lstrip('-').isdigit() else n[1:-2]
    octv = int(n[len(acc) + 1:])
    return 12 * (octv + 1) + _SEMI[n[0].upper()] + acc.count('#') - acc.count('b')

def hz(n, a4=A4):
    return a4 * 2 ** ((midi(n) - 69) / 12.0)

def name(m):
    m = int(round(m)); return f'{NAMES[m % 12]}{m // 12 - 1}'

MODES = dict(major=[0, 2, 4, 5, 7, 9, 11], dorian=[0, 2, 3, 5, 7, 9, 10], aeolian=[0, 2, 3, 5, 7, 8, 10], mixolydian=[0, 2, 4, 5, 7, 9, 10],
             lydian=[0, 2, 4, 6, 7, 9, 11], pentatonic=[0, 2, 4, 7, 9], minor_pentatonic=[0, 3, 5, 7, 10])
CHORDS = {'M': [0, 4, 7], 'm': [0, 3, 7], 'M7': [0, 4, 7, 11], 'm7': [0, 3, 7, 10], 'm9': [0, 3, 7, 10, 14], 'add9': [0, 4, 7, 14], 'sus2': [0, 2, 7],
          'sus4': [0, 5, 7], '6': [0, 4, 7, 9], '5': [0, 7], 'M9': [0, 4, 7, 11, 14]}

def scale(root, mode, lo, hi):
    r = midi(root) % 12
    return [m for m in range(int(midi(lo)), int(midi(hi)) + 1) if (m - r) % 12 in MODES[mode]]

def chord(root, kind='m', spread=False):
    """MIDI notes of a chord on `root`. spread=True opens it out (root, fifth, then the rest an octave up)."""
    r = midi(root); ns = [r + i for i in CHORDS[kind]]
    return [ns[0]] + [ns[2]] + [n + 12 for n in ns[1:2] + ns[3:]] if spread and len(ns) >= 3 else ns

def harmonic(n, f0=60.0):
    """The n-th harmonic of a fundamental, in Hz: for music made out of a hum."""
    return f0 * n

class Seq:
    """Notes placed by bar and beat (both counted from 1). Tracks are just names."""
    def __init__(self, bpm=60.0, beats=4, seed=0):
        self.bpm, self.beats, self.ev, self.rng = bpm, beats, [], np.random.default_rng(seed)
    def at(self, bar, beat=1.0):
        return ((bar - 1) * self.beats + (beat - 1)) * 60.0 / self.bpm
    def note(self, track, pitch, bar, beat=1.0, length=1.0, vel=.7, hz_=None, **kw):
        """pitch: a name, a MIDI number, or pass hz_= for an exact frequency. length in beats."""
        self.ev.append(dict(track=track, midi=None if hz_ else midi(pitch), hz=hz_ or hz(pitch), t=self.at(bar, beat), dur=length * 60.0 / self.bpm, vel=vel, kw=kw))
    def chord(self, track, root, kind, bar, beat=1.0, length=1.0, vel=.6, spread=False, strum=0.0, **kw):
        for i, m in enumerate(chord(root, kind, spread)):
            self.ev.append(dict(track=track, midi=m, hz=hz(m), t=self.at(bar, beat) + i * strum, dur=length * 60.0 / self.bpm, vel=vel, kw=kw))
    def humanize(self, ms=8.0, vel=.06, tracks=None):
        """Nobody plays exactly on the beat or exactly as loud twice."""
        for e in self.ev:
            if tracks is None or e['track'] in tracks:
                e['t'] = max(0.0, e['t'] + self.rng.normal(0, ms / 1000.0)); e['vel'] = float(np.clip(e['vel'] * (1 + self.rng.normal(0, vel)), .05, 1))
    def length(self):
        return max(e['t'] + e['dur'] for e in self.ev)
    def render(self, mix, tracks):
        """tracks: {name: dict(inst=fn(freq, dur, vel, **kw) -> mono, gain=dB, pan=-1..1, send=dB or None, ring=extra seconds a note may ring past its length)}"""
        for e in self.ev:
            tr = tracks[e['track']]
            x = tr['inst'](e['hz'], e['dur'] + tr.get('ring', 0.0), e['vel'], **e['kw'])
            mix.add(x * e['vel'], at=e['t'], gain=tr.get('gain', -12.0), pan_=tr.get('pan', 0.0) + self.rng.normal(0, tr.get('spread', 0.0)), send=tr.get('send'))

def piano_roll(seq, out, width=1500, row=7, lo=None, hi=None):
    """The score as a picture: time across, pitch up, one colour per track. What was meant, to set beside what was heard."""
    import cv2
    ev = [e for e in seq.ev if e['midi'] is not None]
    lo = lo or int(min(e['midi'] for e in ev)) - 2; hi = hi or int(max(e['midi'] for e in ev)) + 2
    T = seq.length(); H = (hi - lo + 1) * row + 30
    img = np.full((H, width, 3), 22, np.uint8)
    for m in range(lo, hi + 1):
        y = H - 20 - (m - lo + 1) * row
        if m % 12 in (1, 3, 6, 8, 10): cv2.rectangle(img, (40, y), (width, y + row - 1), (30, 30, 30), -1)
        if m % 12 == 0: cv2.putText(img, name(m), (2, y + row), cv2.FONT_HERSHEY_SIMPLEX, .35, (170, 170, 160), 1, cv2.LINE_AA)
    bar = seq.beats * 60.0 / seq.bpm
    for b in range(int(T / bar) + 1):
        x = 40 + int((width - 44) * b * bar / T); cv2.line(img, (x, 0), (x, H - 20), (48, 48, 48), 1)
        cv2.putText(img, str(b + 1), (x + 2, H - 6), cv2.FONT_HERSHEY_SIMPLEX, .32, (150, 150, 140), 1, cv2.LINE_AA)
    cols = [(120, 200, 255), (120, 255, 160), (255, 170, 120), (230, 130, 230), (140, 230, 230), (200, 200, 120)]
    names = sorted({e['track'] for e in ev})
    for e in ev:
        c = cols[names.index(e['track']) % len(cols)]; y = H - 20 - int((e['midi'] - lo + 1) * row)
        x0, x1 = 40 + int((width - 44) * e['t'] / T), 40 + int((width - 44) * (e['t'] + e['dur']) / T)
        cv2.rectangle(img, (x0, y + 1), (max(x1 - 1, x0 + 2), y + row - 2), tuple(int(v * (.45 + .55 * e['vel'])) for v in c), -1)
    for i, nme in enumerate(names):
        cv2.putText(img, nme, (50 + i * 120, 12), cv2.FONT_HERSHEY_SIMPLEX, .4, cols[i % len(cols)], 1, cv2.LINE_AA)
    cv2.imwrite(str(out), img); return str(out)
