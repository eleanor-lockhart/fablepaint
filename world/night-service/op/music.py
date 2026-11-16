"""NIGHT SERVICE: the opening theme. 62 seconds, 120 beats a minute, 4/4, thirty-one bars of two seconds.

D is home. The verse is D Dorian (B natural); the chorus lifts into F major for B flat, C, A minor, D minor.
The hook is the three lights from Tern Point, A D E rising, and then the interval nobody expects: a leap of a
minor seventh from the E up to the D above. Everything the night shift plays is struck and dies away; the only
held sounds are the power company's (the hum and one cold tone, 28 to 32 s, and the hum very quietly under the
chorus until the cable snaps at 41.5 s). At 32.0 everything, the room included, is cut.

    uv run python world/night-service/op/music.py        (from the repository root)"""
import math
from pathlib import Path
import numpy as np
from scipy import signal
from backlot import sound as sd, score as sc, ear

HERE = Path(__file__).resolve().parent
SR, DUR = sd.SR, 62.0
PI2 = 2 * math.pi

BOLD = [2.0, 2.5, 3.0, 3.5, 4.0, 11.0, 12.5, 13.5, 14.5, 15.5, 16.5, 22.5, 27.0, 32.0, 33.0, 34.0, 36.0, 41.5, 52.0, 57.0, 58.0]
OTHER = ([8.0, 8.5, 9.0, 9.5] + [28.5 + .5 * i for i in range(6)] + [42.0 + .5 * i for i in range(8)]
         + [46.0 + .5 * i for i in range(8)] + [50.5] + [54.0 + .5 * i for i in range(6)])
SYNC = {round(t, 3) for t in BOLD + OTHER}

# ================================================================== new instruments (numpy and scipy only)
def kick(f=None, dur=None, vel=1.0):
    """A drum-machine kick: a sine falling from about 170 Hz to 54, pushed through tanh so it has harmonics a
    small speaker can play, and a beater click."""
    t = sd.tt(.42); ph = PI2 * np.cumsum(54 + 120 * np.exp(-t / .026)) / SR
    x = np.tanh(2.6 * np.sin(ph) * np.exp(-t / .11)) + .55 * np.sin(2 * ph) * np.exp(-t / .06)
    c = sd.bandpass(np.random.default_rng(1).normal(0, 1, sd._n(.006)), 1800, 7000) * np.linspace(1, 0, sd._n(.006)) ** 2
    x[:len(c)] += c * .5
    return sd.fade(x / np.abs(x).max(), .0004, .08)

def snare(f=None, dur=None, vel=1.0, seed=0):
    t = sd.tt(.34); r = np.random.default_rng(seed)
    tone = (np.sin(PI2 * 188 * t) + .5 * np.sin(PI2 * 331 * t)) * np.exp(-t / .05)
    nz = sd.bandpass(r.normal(0, 1, len(t)), 900, 9500) * np.exp(-t / .075)
    x = .8 * tone + nz
    return sd.fade(x / np.abs(x).max(), .0004, .05)

def hat(f=None, dur=None, vel=1.0, open_=False, seed=0):
    t = sd.tt(.42 if open_ else .09); r = np.random.default_rng(seed + int(vel * 1000))
    x = sd.highpass(r.normal(0, 1, len(t)), 6800, 4) * np.exp(-t / (.11 if open_ else .017))
    return sd.fade(x / np.abs(x).max(), .0004, .02)

def crash(f=None, dur=None, vel=1.0, seed=0):
    t = sd.tt(2.4); r = np.random.default_rng(seed)
    x = sd.highpass(r.normal(0, 1, len(t)), 3000, 2) * (.6 * np.exp(-t / .5) + .4 * np.exp(-t / .08))
    for fr in (4120.0, 5370.0, 6830.0, 8110.0):
        x += .12 * np.sin(PI2 * fr * t + r.uniform(0, 6)) * np.exp(-t / .4)
    return sd.fade(x / np.abs(x).max(), .0004, .2)

def tom(f=110.0, dur=None, vel=1.0):
    t = sd.tt(.4); ph = PI2 * np.cumsum(f * (1 + .6 * np.exp(-t / .03))) / SR
    x = np.tanh(1.8 * np.sin(ph) * np.exp(-t / .12))
    c = sd.bandpass(np.random.default_rng(2).normal(0, 1, sd._n(.005)), 1500, 6000) * np.linspace(1, 0, sd._n(.005)) ** 2
    x[:len(c)] += c * .4
    return sd.fade(x / np.abs(x).max(), .0004, .06)

def tick(f=None, dur=None, vel=1.0):
    """A dry tick: Vesper Lang's finger on a window. No room on it."""
    n = sd._n(.035); t = np.arange(n) / SR
    x = sd.bandpass(np.random.default_rng(5).normal(0, 1, n), 2500, 9000) * np.exp(-t / .0022) + .6 * np.sin(PI2 * 3100 * t) * np.exp(-t / .006)
    return sd.fade(x / np.abs(x).max(), .0002, .008)

def rim(f=None, dur=None, vel=1.0):
    n = sd._n(.07); t = np.arange(n) / SR
    x = (np.sin(PI2 * 1730 * t) + .6 * np.sin(PI2 * 470 * t)) * np.exp(-t / .011) + sd.bandpass(np.random.default_rng(6).normal(0, 1, n), 2000, 8000) * np.exp(-t / .002) * .7
    return sd.fade(x / np.abs(x).max(), .0002, .01)

def breaker():
    """The switch thrown at 32.0: 25 ms, dry, and then nothing."""
    n = sd._n(.028); t = np.arange(n) / SR
    x = sd.bandpass(np.random.default_rng(8).normal(0, 1, n), 600, 6000) * np.exp(-t / .0035) + .8 * np.sin(PI2 * 420 * t) * np.exp(-t / .006)
    return x / np.abs(x).max() * np.clip((.028 - t) / .008, 0, 1)

def snap(f=None, dur=None, vel=1.0):
    """The cable parting at 41.5: a crack, and the twang of the loose end falling away."""
    t = sd.tt(.5); r = np.random.default_rng(12)
    crack = sd.highpass(r.normal(0, 1, len(t)), 1500, 2) * np.exp(-t / .02)
    twang = np.sin(PI2 * np.cumsum(180 + 2600 * np.exp(-t / .07)) / SR) * np.exp(-t / .11)
    x = crack + .7 * twang
    return sd.fade(x / np.abs(x).max(), .0003, .05)

def lead(f, dur, vel=.8, t60=1.5):
    """The chorus lead: two slightly detuned sawtooth-like voices, struck, the upper partials dying first."""
    K = int(min(26, SR * .42 / f)); k = np.arange(1, K + 1); x = 0
    for cents, ph in ((-5.0, 0.0), (5.0, 1.3)):
        ff = f * 2 ** (cents / 1200.0)
        x = x + sd.partials(ff, dur, 1.0 / k ** (1.2 - .4 * vel), t60=t60 / (1 + (k * ff / 2600.0) ** 1.3), phases=ph * k)
    c = sd.bandpass(np.random.default_rng(4).normal(0, 1, sd._n(.008)), 1500, 6000) * np.linspace(1, 0, sd._n(.008)) ** 2
    x[:len(c)] += c * .5 * vel
    return sd.fade(x / np.abs(x).max(), .002, .07)

def bassn(f, dur, vel=.8, t60=1.5):
    """A picked bass: every low note carries its harmonics (the fundamental alone is no use on a phone)."""
    d = dur + .2; K = int(min(14, 2600 / f)); k = np.arange(1, K + 1)
    a = 1.0 / k ** .9; a[0] = .55
    x = sd.partials(f, d, a, t60=t60 / (1 + (k * f / 420.0) ** 1.2))
    x = np.tanh(1.6 * x / np.abs(x).max())
    c = sd.bandpass(np.random.default_rng(7).normal(0, 1, sd._n(.006)), 700, 3500) * np.linspace(1, 0, sd._n(.006)) ** 2
    x[:len(c)] += c * .3
    return sd.fade(x / np.abs(x).max(), .002, .05)

def lowtone(f, dur=4.0, vel=1.0):
    """One low struck tone: a string, a sub under it, and a soft bell an octave up."""
    x = sd.pluck(f, dur, bright=.35, t60=3.2)
    x = x + .4 * np.r_[sd.sub(f, min(dur, 3.0), t60=2.4), np.zeros(max(0, len(x) - sd._n(min(dur, 3.0))))][:len(x)]
    x = x + .5 * sd.bell(2 * f, dur, t60=3.4, bright=.3, third=0.0)[:len(x)]
    c = sd.bandpass(np.random.default_rng(9).normal(0, 1, sd._n(.012)), 200, 2500) * np.linspace(1, 0, sd._n(.012)) ** 2      # the mallet
    x[:len(c)] += c * .8
    return sd.fade(x / np.abs(x).max(), .001, .1)

# ================================================================== the score
s = sc.Seq(bpm=120, beats=4, seed=11)
B = s.at
ROW = dict(kick=12, rim=13, snare=14, punch=15, tom=16, tick=17, hat=18, ohat=19, crash=21, snap=22)      # drum rows for the piano roll

def hit(track, t, vel=.8, **kw):
    s.ev.append(dict(track=track, midi=ROW[track], hz=1.0, t=t, dur=.12, vel=vel, kw=kw))

def add(track, bar, notes, scale=1.0, **kw):
    for p, beat, ln, v in notes:
        s.note(track, p, bar, beat, ln, vel=min(1.0, v * scale), **kw)

def stab(track, names, bar, beat, ln, vel, strum=.007):
    for i, p in enumerate(names):
        s.note(track, p, bar, beat, ln, vel=vel); s.ev[-1]['t'] += i * strum

#        bass   comp (electric piano)        arpeggio (plucked)
CH = {'Dm': ('D2', ['A3', 'D4', 'F4'], ['D5', 'F5', 'A5', 'D6']),
      'G': ('G2', ['G3', 'B3', 'D4'], ['D5', 'G5', 'B5', 'D6']),
      'Am': ('A2', ['A3', 'C4', 'E4'], ['C5', 'E5', 'A5', 'C6']),
      'C': ('C3', ['G3', 'C4', 'E4'], ['C5', 'E5', 'G5', 'C6']),
      'Bb': ('Bb1', ['Bb3', 'D4', 'F4', 'A4'], ['D5', 'F5', 'A5', 'D6']),
      'C_': ('C2', ['G3', 'C4', 'E4'], ['E5', 'G5', 'C6', 'E6']),
      'Am_': ('A1', ['A3', 'C4', 'E4', 'G4'], ['C5', 'E5', 'A5', 'C6']),
      'Dm_': ('D2', ['A3', 'D4', 'F4'], ['D5', 'F5', 'A5', 'D6'])}
up = lambda p, n=12: sc.midi(p) + n

# ---- 0-4: sea, four punches, the foghorn swelling into the hit
for i, t in enumerate((2.0, 2.5, 3.0, 3.5)):
    hit('punch', t, .6 + .1 * i)

# ---- 4-8, bars 3-4: the title. Everything enters; the hook plainly, then the leap on the tagline at 6.0
for bar, ch in ((3, 'Dm'), (4, 'G')):
    bs, cp, ar = CH[ch]
    for beat, v in ((1, .95), (2.5, .78), (4, .85)):
        s.note('bass', bs, bar, beat, 1.3, vel=v); stab('comp', cp, bar, beat, 1.4, v * .85); hit('kick', B(bar, beat), v)
    for i in range(8):
        s.note('arp', ar[[0, 1, 2, 3, 2, 1, 2, 1][i]], bar, 1 + i * .5, .5, vel=.5 + (.12 if i % 2 == 0 else 0))
        hit('hat', B(bar, 1 + i * .5), .55 if i % 2 == 0 else .38)
hit('crash', 4.0, .9); s.note('bell', 'D5', 3, 1, 4, vel=.8, third=.5)
hit('ohat', 6.0, .7); s.note('bell', 'D6', 4, 1, 3, vel=.5, third=.0)
TITLE = {3: [('A4', 1, 1, .9), ('D5', 2, 1, .92), ('E5', 3, 2, .97)],
         4: [('D6', 1, 1.5, 1.0), ('B5', 2.5, .5, .78), ('A5', 3, 1.5, .84), ('E5', 4.5, .5, .6)]}
for bar, ns in TITLE.items():
    add('pluck', bar, ns); add('pluck8', bar, [(up(p, -12), b, l, v) for p, b, l, v in ns])

# ---- 8-24, bars 5-12: the verse, D Dorian
VERSE = {5: [('F5', 1, .5, .75), ('E5', 1.5, .5, .64), ('D5', 2, 1, .75), ('A4', 3, .5, .64), ('C5', 3.5, .5, .7), ('D5', 4, 1, .78)],
         6: [('B4', 1, 1, .6), ('A4', 2, .5, .46), ('G4', 2.5, .5, .33), ('A4', 4, .5, .6), ('D5', 4.5, .5, .7)],      # sinks with the lamp; then A, D ...
         7: [('E5', 1, 1.5, .84), ('G5', 2.5, .5, .7), ('A5', 3, 1, .8), ('G5', 4, .5, .68), ('E5', 4.5, .5, .65)],     # ... E: the hook over the bar line
         8: [('D5', 1, .5, .7), ('E5', 1.5, 1, .76), ('C5', 2.5, .5, .66), ('G5', 3, 1.5, .8), ('A5', 4.5, .5, .7)],
         9: [('D6', 1, .5, .8), ('F6', 1.5, .5, .72), ('A6', 2, 1, .86), ('G6', 3, .5, .7), ('F6', 3.5, .5, .68), ('E6', 4, .5, .7), ('D6', 4.5, .5, .66)],
         10: [('B5', 1, 1, .76), ('D6', 2, .5, .7), ('G6', 2.5, 1, .82), ('E6', 3.5, .5, .7), ('D6', 4, .5, .68), ('B5', 4.5, .5, .62)],
         11: [('A4', 2.5, .5, .62), ('C5', 3, .5, .66), ('D5', 3.5, 1.5, .72)],
         12: [('E5', 2, 1, .8), ('D5', 3, .5, .62), ('C5', 3.5, .5, .58), ('A4', 4, 1, .6)]}
for bar, ns in VERSE.items():
    add('pluck', bar, ns)
# bar 5: Orrin walks (a step on every beat); the bass walks with him
for i, p in enumerate(('D2', 'F2', 'A2', 'C3')):
    s.note('bass', p, 5, 1 + i, 1, vel=.64); hit('kick', 8.0 + .5 * i, .46)
    stab('comp', CH['Dm'][1], 5, 1.5 + i, .8, .44)
for i in range(8): hit('hat', B(5, 1 + i * .5), .42 if i % 2 == 0 else .3)
# bar 6: he nods off (thin out, sink), and at 11.0 the lamp flares: a bell
s.note('bass', 'B2', 6, 1, 1.5, vel=.55); stab('comp', CH['G'][1], 6, 1, 1, .42); stab('comp', CH['G'][1], 6, 2, 1, .28)
hit('hat', B(6, 1), .3); hit('hat', B(6, 1.5), .2)
s.note('bell', 'D6', 6, 3, 4, vel=.9, third=.0); s.note('bass', 'G2', 6, 3, 1.5, vel=.7); stab('comp', ['G3', 'B3', 'D4', 'G4'], 6, 3, 2, .66, strum=.012)
hit('ohat', 11.0, .5)
# bars 7-8: Dee. The punch is the backbeat (12.5, 13.5, 14.5, 15.5)
for bar, ch, bl in ((7, 'Am', [('A2', 1), ('A2', 2.5), ('C3', 4), ('E3', 4.5)]), (8, 'C', [('C3', 1), ('C3', 2.5), ('G2', 4), ('B2', 4.5)])):
    for p, beat in bl: s.note('bass', p, bar, beat, 1.0 if beat < 4 else .5, vel=.66 if beat == 1 else .56)
    for beat, v in ((1, .54), (2.5, .46), (4, .5)): stab('comp', CH[ch][1], bar, beat, 1.2, v)
    for beat in (1, 3): hit('kick', B(bar, beat), .55)
    for beat in (2, 4): hit('punch', B(bar, beat), .92)
    for i in range(8): hit('hat', B(bar, 1 + i * .5), .46 if i % 2 == 0 else .32)
# bars 9-10: Marisol. High bright plucked notes; one pure tone on 16.5
s.note('glass', 'A6', 9, 2, 4, vel=.85)
for bar, ch, bl, cp in ((9, 'Dm', [('D2', 1), ('D3', 2.5), ('A2', 4)], ['D4', 'F4', 'A4']), (10, 'G', [('G2', 1), ('G2', 2.5), ('D3', 4)], ['D4', 'G4', 'B4'])):
    for p, beat in bl: s.note('bass', p, bar, beat, 1.0, vel=.62 if beat == 1 else .52)
    for beat, v in ((1, .5), (2.5, .44), (4, .46)): stab('comp', cp, bar, beat, 1.2, v)
    for beat in (1, 3): hit('kick', B(bar, beat), .5)
    for beat in ((4,) if bar == 9 else (2, 4)): hit('rim', B(bar, beat), .6)
    for i in range(8): hit('hat', B(bar, 1 + i * .5), .44 if i % 2 == 0 else .32)
# bars 11-12: Red. One low note, steady, unimpressed; a small accent on 22.5 when the lantern is up
for bar in (11, 12):
    for i in range(8): s.note('ost', 'D2', bar, 1 + i * .5, .5, vel=.66)
hit('kick', 20.0, .5); stab('comp', ['C4', 'F4', 'A4'], 11, 1, 2, .4)
hit('rim', 22.5, .8); s.note('bell', 'A5', 12, 2, 3, vel=.5, third=.0)

# ---- 24-28, bars 13-14: thin out. Three glass tones (the hook again, for the passengers); then the heron blinks
s.note('bass', 'Bb2', 13, 1, 3, vel=.5); stab('comp', ['Bb3', 'D4', 'F4', 'A4'], 13, 1, 3, .38, strum=.02)
for i, (p, v) in enumerate((('A5', .7), ('D6', .66), ('E6', .62))): s.note('glass', p, 13, 1 + i, 3, vel=v)
s.note('pluck', 'A6', 14, 3, .5, vel=.42); hit('tick', 27.0, .3)

# ---- 28-32, bars 15-16: the power company. Hum and a cold tone are added below; six dry ticks, one a beat
for i in range(6): hit('tick', 28.5 + .5 * i, .62 + .075 * i)

# ---- 32-34, bar 17: the break. Silence, then one low struck tone on 33.0
s.note('low', 'D2', 17, 3, 3, vel=.9)

# ---- 34-50, bars 18-25: the chorus. B flat, C, A minor, D minor, twice
CHORUS = {18: [('A4', 1, .5, .92), ('D5', 1.5, 1, .95), ('E5', 2.5, 1.5, 1.0), ('E5', 4, .5, .8), ('E5', 4.5, .5, .86)],
          19: [('D6', 1, 1.5, 1.0), ('C6', 2.5, .5, .82), ('A5', 3, 1, .88), ('G5', 4, .5, .78), ('A5', 4.5, .5, .82)],     # the leap lands on 36.0
          20: [('C6', 1, 1, .92), ('A5', 2, .5, .8), ('G5', 2.5, 1, .86), ('E5', 3.5, .5, .76), ('G5', 4, .5, .8), ('A5', 4.5, .5, .84)],
          21: [('F5', 1, .5, .82), ('G5', 1.5, .5, .84), ('A5', 2, .5, .88), ('C6', 2.5, .5, .92), ('D6', 3, .5, .96), ('F6', 4, 1, 1.0)],   # climbs to 41.5
          22: [('A4', 1, 1.5, .95), ('D5', 2.5, 1.5, .97), ('E5', 4, 1, 1.0)],                                                  # the hook, opened out: 3 + 3 + 2
          23: [('G6', 1, 1.5, 1.0), ('E6', 2.5, .5, .84), ('D6', 3, 1, .9), ('C6', 4, 1, .86)],                                 # a tenth, this time
          24: [('A4', 1, 1, 1.0), ('A6', 2, 1, .9), ('C5', 3, 1, 1.0), ('G6', 4, 1, .9)],                                       # minder, light, minder, light
          25: [('D5', 1, 1, 1.0), ('F6', 2, 1, .92), ('F5', 3, 1, 1.0), ('E6', 4, 1, .94)]}
def lead_pair(bar, ns):
    """One lead, in two octaves: the upper voice doubles an octave above until that would pass E6, then joins in unison."""
    add('lead', bar, ns)
    add('lead8', bar, [(up(p) if up(p) <= 88 else sc.midi(p), b, l, v) for p, b, l, v in ns])
for bar, ns in CHORUS.items(): lead_pair(bar, ns)

def groove(bar, ch, kicks, snares, hats=8, upto=5.0, arp16=True, bassv=.85):
    bs, cp, ar = CH[ch]; r = sc.midi(bs)
    for i, off in enumerate((0, 0, 12, 0, 0, 12, 0, 7)):
        if 1 + i * .5 < upto: s.note('bass', r + off, bar, 1 + i * .5, .5, vel=bassv if i % 2 == 0 else bassv - .13)
    for beat, v in ((1, .9), (2.5, .8), (4, .84)):
        if beat < upto: stab('comp', cp, bar, beat, 1.2, v)
    n = 16 if arp16 else 8
    for i in range(n):
        beat = 1 + i * 4.0 / n
        if beat < upto: s.note('arp', ar[[0, 2, 1, 2, 3, 2, 1, 2][i % 8]], bar, beat, .5, vel=.62 if i % (n // 4) == 0 else .46)
    for beat in kicks: hit('kick', B(bar, beat), .95 if beat == int(beat) else .8)
    for beat in snares: hit('snare', B(bar, beat), .9, seed=bar)
    for i in range(hats):
        beat = 1 + i * 4.0 / hats
        if beat < upto: hit('ohat' if beat == int(beat) else 'hat', B(bar, beat), .62 if beat == int(beat) else .5)
groove(18, 'Bb', (1, 2.5, 3), (2, 4))
groove(19, 'C_', (1, 2.5, 3, 4.5), (2, 4))
groove(20, 'Am_', (1, 2.5, 3), (2, 4))
groove(21, 'Dm_', (1, 2.5), (2,), upto=3.0)
hit('crash', 34.0, 1.0); s.note('bell', 'D5', 18, 1, 4, vel=.75, third=.0)                    # the hit
hit('crash', 36.0, .8, seed=3); s.note('bell', 'D6', 19, 1, 4, vel=.8, third=.0)              # the camera lands
hit('crash', 38.0, .55, seed=5)
for i, f in enumerate((175.0, 131.0, 98.0)): hit('tom', 41.0 + .125 * i, .8 + .08 * i, f=f)   # a fill, a breath ...
# ... and 41.5: the cable snaps. The biggest accent in the piece; the hum (below) stops here for good
hit('kick', 41.5, 1.0); hit('snare', 41.5, 1.0, seed=99); hit('crash', 41.5, 1.0, seed=7); hit('crash', 41.5, 1.0, seed=8); hit('tom', 41.5, 1.0, f=73.0); hit('snap', 41.5, 1.0)
s.note('low', 'Bb1', 21, 4, 2, vel=1.0); s.note('bass', 'Bb1', 21, 4, 1, vel=1.0); s.note('bass', 'Bb2', 21, 4, 1, vel=.9)
stab('comp', ['Bb3', 'D4', 'F4', 'A4', 'D5', 'F5'], 21, 4, 1, 1.0, strum=.0); s.note('bell', 'F5', 21, 4, 2, vel=1.0, third=.0)
# bars 22-23: the four of them on the moon, a kick on every beat, the tune at its most open
for bar, ch in ((22, 'Bb'), (23, 'C_')):
    bs, cp, ar = CH[ch]; r = sc.midi(bs)
    for i in range(8):
        beat = 1 + i * .5
        s.note('bass', r + (12 if i % 2 else 0), bar, beat, .5, vel=.88 if i % 2 == 0 else .74)
        hit('ohat' if i % 2 else 'hat', B(bar, beat), .62 if i % 2 else .6)
        if i % 2 == 0: hit('kick', B(bar, beat), .97)
    for beat in (1, 2, 3, 4): hit('snare', B(bar, beat), .86 if beat % 2 == 0 else .74, seed=bar * 7 + beat)
    for beat, v in ((1, .9), (2.5, .8), (4, .84)): stab('comp', cp, bar, beat, 1.3, v)
    for i in range(16): s.note('arp', ar[[0, 2, 1, 2, 3, 2, 1, 2][i % 8]], bar, 1 + i * .25, .5, vel=.62 if i % 4 == 0 else .46)
hit('crash', 42.0, .7, seed=11); hit('crash', 44.0, .6, seed=12)
# bars 24-25: minder, light, minder, light. Eight hits, each struck and dying
for bar, ch, lows, highs in ((24, 'Am_', ('A1', 'A1'), ('A5', 'G5')), (25, 'Dm_', ('D2', 'D2'), ('F5', 'E5'))):
    for j in range(2):
        tl, th = B(bar, 1 + 2 * j), B(bar, 2 + 2 * j)
        hit('kick', tl, 1.0); hit('crash', tl, .45, seed=20 + bar + j)
        s.note('bass', lows[j], bar, 1 + 2 * j, .9, vel=.95); s.note('bass', up(lows[j]), bar, 1 + 2 * j, .9, vel=.7)
        stab('comp', CH[ch][1], bar, 1 + 2 * j, .9, .95, strum=.0)
        hit('snare', th, .9, seed=30 + bar + j); hit('ohat', th, .7)
        s.note('bell', highs[j], bar, 2 + 2 * j, 1.5, vel=.72, third=.0)
        stab('comp', [up(p) for p in CH[ch][1]], bar, 2 + 2 * j, .9, .6, strum=.0)

# ---- 50-54, bars 26-27: half time, space
add('lead', 26, [('D6', 1, 2, .86), ('A5', 3, 1, .74), ('F5', 4, 1, .7)]); add('lead', 27, [('G5', 1, 2, .8), ('E5', 3, 1, .7), ('C5', 4, 1, .66)])
for bar, ch in ((26, 'Bb'), (27, 'C_')):
    bs, cp, ar = CH[ch]
    s.note('bass', bs, bar, 1, 2.5, vel=.85); s.note('bass', up(bs), bar, 3.5, .5, vel=.6); s.note('bass', bs, bar, 4, 1, vel=.7)
    stab('comp', cp, bar, 1, 3, .7, strum=.015); stab('comp', cp, bar, 3, 1.5, .5, strum=.015)
    for i in range(8): s.note('arp', ar[[0, 1, 2, 3, 2, 1, 2, 1][i]], bar, 1 + i * .5, .5, vel=.5 if i % 2 == 0 else .4)
    hit('kick', B(bar, 1), .92); hit('snare', B(bar, 3), .88, seed=bar)
    for i in range(4): hit('hat', B(bar, 1 + i), .5)
s.note('glass', 'A6', 26, 2, 2, vel=.6); hit('rim', 50.5, .62)                               # the eye turns green
s.note('bell', 'C6', 27, 1, 4, vel=.9, third=.0); s.note('glass', 'G6', 27, 1, 4, vel=.8)     # the window opens in its chest

# ---- 54-58, bars 28-29: six windows, climbing (the hook twice), then a seventh, lower and bigger, far off
for i, (p, bsn, cp) in enumerate((('A4', 'Bb1', ['D4', 'F4', 'A4']), ('D5', None, None), ('E5', 'C2', ['E4', 'G4', 'C5']),
                                  ('A5', None, None), ('D6', 'D2', ['D4', 'A4', 'E5']), ('E6', None, None))):
    bar, beat = 28 + i // 4, 1 + i % 4; v = .78 + .04 * i
    s.note('lead', p, bar, beat, 1.5, vel=v); s.note('lead8', up(p) if up(p) <= 88 else p, bar, beat, 1.5, vel=v)
    s.note('bell', p, bar, beat, 2, vel=.5 + .05 * i, third=.0)
    if bsn:
        s.note('bass', bsn, bar, beat, 2, vel=.8 + .03 * i); s.note('bass', up(bsn), bar, beat, 2, vel=.6)
        stab('comp', cp, bar, beat, 2, .6 + .04 * i, strum=.01); hit('kick', B(bar, beat), .7 + .04 * i)
hit('kick', 57.0, .92); hit('tom', 57.0, .8, f=82.0); hit('crash', 57.0, .5, seed=41)
s.note('low', 'A1', 29, 3, 2, vel=.68); s.note('bass', 'A1', 29, 3, 2, vel=.74); s.note('bass', 'A2', 29, 3, 2, vel=.7)
stab('comp', ['A3', 'E4', 'A4'], 29, 3, 2, .85, strum=.0); s.note('bell', 'A3', 29, 3, 2, vel=.8, third=.0)

# ---- 58-62, bars 30-31: the last chord. D, A, E: the three lights, all lit at once. Let it ring
hit('kick', 58.0, .8); hit('crash', 58.0, .6, seed=43)
s.note('low', 'D2', 30, 1, 8, vel=.68); s.note('bass', 'D2', 30, 1, 8, vel=.7)
stab('comp', ['D3', 'A3', 'D4', 'E4', 'A4'], 30, 1, 8, .8, strum=.014)
for i, p in enumerate(('A4', 'D5', 'E5')):                                                    # the hook, rolled into the chord
    s.note('lead', p, 30, 1, 8, vel=.82); s.ev[-1]['t'] += .05 * i
    s.note('lead8', up(p), 30, 1, 8, vel=.74); s.ev[-1]['t'] += .05 * i
s.note('bell', 'D5', 30, 1, 8, vel=.95, third=.0); s.note('bell', 'D6', 30, 1, 8, vel=.55, third=.0)

# ---- humanise: nobody plays exactly on the grid or equally loud twice; the listed sync times stay exact
HUMAN = dict(pluck=(8, .06), pluck8=(8, .06), lead=(7, .05), lead8=(9, .06), comp=(9, .07), arp=(7, .09), bass=(5, .05), glass=(10, .05),
             hat=(3, .08), ohat=(3, .06), kick=(0, .04), snare=(0, .05), rim=(2, .06), bell=(0, .04), ost=(1.5, .012))
for e in s.ev:
    ms, v = HUMAN.get(e['track'], (0, 0))
    if ms and round(e['t'], 3) not in SYNC: e['t'] = max(0.0, e['t'] + s.rng.normal(0, ms / 1000.0))
    if v: e['vel'] = float(np.clip(e['vel'] * (1 + s.rng.normal(0, v)), .05, 1))

# ================================================================== the mix: two rooms, so the first can be cut dead at 32.0
TRACKS = {
    'pluck': dict(inst=lambda f, d, v: sd.pluck(f, d + 1.8, bright=.4 + .45 * v, t60=2.6), gain=-9, send=-9, pan=-.08),
    'pluck8': dict(inst=lambda f, d, v: sd.pluck(f, d + 1.8, bright=.4 + .3 * v, t60=2.6), gain=-15, send=-12, pan=.1),
    'lead': dict(inst=lambda f, d, v: lead(f, d + .7, v), gain=-8.5, send=-11, pan=.06),
    'lead8': dict(inst=lambda f, d, v: lead(f, d + .7, v * .8, t60=1.3), gain=-14, send=-9, pan=-.14),
    'comp': dict(inst=lambda f, d, v: sd.epiano(f, d + 1.0, v, t60=1.8), gain=-19, send=-12, pan=.25, spread=.06),
    'arp': dict(inst=lambda f, d, v: sd.pluck(f, 1.1, bright=.62, t60=1.2), gain=-21.5, send=-10, pan=-.32, spread=.1),
    'bass': dict(inst=lambda f, d, v: bassn(f, d, v), gain=-13.5, send=-24),
    'ost': dict(inst=lambda f, d, v: bassn(f, d, v, t60=.9) + .4 * sd.pluck(2 * f, d + .2, bright=.5, t60=.8)[:sd._n(d + .2)], gain=-13, send=-20),
    'low': dict(inst=lambda f, d, v: lowtone(f, d + 2.0, v), gain=-9, send=-8),
    'bell': dict(inst=lambda f, d, v, third=.5: sd.bell(f, d + 3.0, t60=4.0, bright=.42, third=third), gain=-16, send=-6, pan=.3),
    'glass': dict(inst=lambda f, d, v: sd.glass(f, d + 2.0, t60=3.4), gain=-19, send=-5, pan=-.36),
    'kick': dict(inst=kick, gain=-9.5, send=None),
    'snare': dict(inst=snare, gain=-11, send=-13, pan=.05),
    'hat': dict(inst=hat, gain=-25, send=-22, pan=.3),
    'ohat': dict(inst=lambda f, d, v: hat(vel=v, open_=True), gain=-24, send=-18, pan=.3),
    'crash': dict(inst=crash, gain=-17, send=-10, pan=-.22),
    'tom': dict(inst=lambda f_, d, v, f=110.0: tom(f), gain=-10, send=-12, pan=-.1),
    'punch': dict(inst=lambda f, d, v: sd.punch(), gain=-10, send=-11, pan=.15),
    'tick': dict(inst=tick, gain=-8, send=None, pan=-.1),
    'snap': dict(inst=snap, gain=-7, send=-8, pan=.1),
    'rim': dict(inst=rim, gain=-15, send=-14, pan=-.2),
}
CUT, BACK = 32.0, 33.0
mA, mB = sd.Mix(DUR, t60=3.4, damp=.5, seed=2), sd.Mix(DUR, t60=3.4, damp=.5, seed=2)
for e in s.ev:
    tr = TRACKS[e['track']]
    x = tr['inst'](e['hz'], e['dur'] + tr.get('ring', 0.0), e['vel'], **e['kw'])
    (mB if e['t'] >= BACK - .25 else mA).add(x * e['vel'], at=e['t'], gain=tr.get('gain', -12.0), pan_=tr.get('pan', 0.0) + s.rng.normal(0, tr.get('spread', 0.0)), send=tr.get('send'))

t = np.arange(mA.n) / SR
# the sea: always there, never noticed. Alone at the start, then under everything; it stops with everything else at 32.0
sea = sd.highpass(sd.pan(sd.sea(DUR, period=6.0, seed=5), -.2) * .7 + sd.pan(sd.sea(DUR, period=6.0, phase=.5, seed=9), .3) * .5, 70)
sea_lvl = np.interp(t, [0, 3.6, 4.4, 57.5, 58.5, 62], [sd.db(-21), sd.db(-21), sd.db(-31), sd.db(-31), sd.db(-27), sd.db(-27)])
mA.add(sea * (sea_lvl * (t < CUT))[:, None], send=-16)
mB.add(sea * (sea_lvl * np.clip((t - 33.6) / .6, 0, 1))[:, None], send=-16)
# the foghorn sounds D: swelling into the hit at 4.0, and under the last chord
fh = sd.foghorn(5.0, f=sc.hz('D3'))[:sd._n(2.9)]; fh = sd.fade(fh * np.linspace(.12, 1, len(fh)) ** 1.6, .01, .02)      # no grunt, no fall: it swells until the hit takes it
mA.add(fh, at=4.0 - 2.9, gain=-13, pan_=-.4, send=-5)
mB.add(sd.foghorn(3.4, f=sc.hz('D3')), at=58.0, gain=-16, pan_=-.4, send=-4)

revA, revB = mA.render(wet=0.0) - mA.dry, mB.render(wet=0.0) - mB.dry
gate = np.clip((CUT - t) / .003, 0, 1)[:, None]                               # 3 ms, and the room goes with it
dry, rev = mA.dry * gate + mB.dry, revA * gate + revB
rms = lambda a: math.sqrt(float((a ** 2).mean()) + 1e-20)
WET = -10.0 - 20 * math.log10(rms(rev) / rms(dry))                            # set the room 10 dB under the dry sound
music = dry + rev * sd.db(WET)
wet_to_dry = 20 * math.log10(rms(rev * sd.db(WET)) / rms(dry))

# the other side: sustained, dry, no room. Hum and one cold tone rising 28 -> 32; the hum, very quietly, under the chorus until 41.5
hum = sd.hum(DUR, buzz=.6); cold = np.sin(PI2 * 720.0 * t) + .25 * np.sin(PI2 * 1440.0 * t)
rise = np.clip((t - 28.0) / 4.0, 0, 1) ** 1.7 * gate[:, 0]
cable = np.clip((t - 34.0) / .05, 0, 1) * np.clip((41.5 - t) / .004, 0, 1)
other = sd.pan(hum * (rise * sd.db(-12) + cable * sd.db(-31)) + cold * rise * sd.db(-22))
bk = breaker(); click = np.zeros(mA.n); click[sd._n(CUT):sd._n(CUT) + len(bk)] = bk * sd.db(-9)
music = music + other + sd.pan(click)
music *= np.clip((DUR - t) / .3, 0, 1)[:, None]

# ================================================================== master: -14 LUFS, true peak under -1
def soften(x, knee_db=-4.0):
    """Round off the tallest drum peaks before the limiter has to."""
    th = sd.db(knee_db); a = np.abs(x); y = x.copy(); o = a > th
    y[o] = np.sign(x[o]) * (th + (1 - th) * np.tanh((a[o] - th) / (1 - th)))
    return y
TARGET = -14.0; tgt = TARGET
for _ in range(4):
    pre = sd.highpass(music, 28.0, 2); pre = soften(pre * sd.db(tgt + 1.0 - sd.loudness(pre)), -3.0)
    out = sd.master(pre, target_lufs=tgt)
    err = sd.loudness(out) - TARGET
    if abs(err) < .08: break
    tgt -= err
pre_pk = 20 * math.log10(np.abs(pre).max()) + (tgt - sd.loudness(sd.highpass(pre, 28.0, 2)))      # how far the limiter has to reach
wav = sd.write_wav('out/op/music/night_service_op.wav', out)
sd.encode(wav, HERE / 'night_service_op.mp3')
sc.piano_roll(s, HERE / 'music_score.png')

# ================================================================== the listening room
r = ear.report(wav, HERE / 'music_report.jpg', 'NIGHT SERVICE: opening theme')
x, _ = sd.read_wav(wav); mono = x.mean(1)
seg = lambda a, b: x[int(a * SR):int(b * SR)]
def rms_db(a, b):
    v = mono[int(a * SR):int(b * SR)]; return 20 * math.log10(max(math.sqrt(float((v ** 2).mean())), 1e-9))

print(f"seconds {r['seconds']:.2f}   LUFS {r['lufs']:.2f} (ffmpeg {ear.ffmpeg_loudness(wav)})   true peak {r['true_peak_db']:.2f} dB   clipped {r['clipped_samples']}   crest {r['crest_db']:.1f} dB   loudness range {r['loudness_range']:.1f}")
print(f"key {r['key_candidates']}   pitch classes {sorted(r['chroma'].items(), key=lambda kv: -kv[1])[:6]}")
print(f"pulse {r.get('pulse_seconds', 0):.3f} s ({r.get('pulse_bpm', 0):.0f} bpm)   onsets {r['onsets_per_second']:.2f}/s   stereo corr {r['stereo_correlation']:.2f}   side/mid {r['side_to_mid_db']:.1f} dB")
print('bands (dB of total):', {k: round(v, 1) for k, v in r['bands'].items()}, f"centroid {r['centroid_hz']:.0f} Hz")
print(f'reverb: wet to dry {wet_to_dry:.1f} dB (wet gain {WET:.1f})   limiter: tallest peak before it {pre_pk:.1f} dB, ceiling -1.5')
def line_db(fr, a, b):
    v = mono[int(a * SR):int(b * SR)] * np.hanning(int(b * SR) - int(a * SR)); X = np.abs(np.fft.rfft(v)); ff = np.fft.rfftfreq(len(v), 1 / SR)
    return 20 * math.log10(max(X[np.abs(ff - fr) < .3].max() / len(v) * 4, 1e-9))
print('the cable (hum harmonics, dB): ' + '   '.join(f'{fr:.0f} Hz: {line_db(fr, 34.1, 41.4):.1f} before 41.5, {line_db(fr, 42.0, 49.3):.1f} after' for fr in (180.0, 300.0, 420.0, 540.0)))
SECT = [('intro', 0, 4), ('title', 4, 8), ('verse', 8, 24), ('pre', 24, 28), ('hum', 28, 32), ('tone', 33, 34), ('chorus', 34, 50), ('half', 50, 54), ('climb', 54, 58), ('end', 58, 62)]
L = {n: sd.loudness(seg(a, b)) for n, a, b in SECT}
print('loudness by section (LUFS):', {k: round(v, 1) for k, v in L.items()})
print(f"chorus - verse = {L['chorus'] - L['verse']:.1f} LU   (verse halves: {sd.loudness(seg(8, 16)):.1f}, {sd.loudness(seg(16, 24)):.1f}; chorus halves: {sd.loudness(seg(34, 42)):.1f}, {sd.loudness(seg(42, 50)):.1f})")
print(f'the break: RMS 32.05-32.95 = {rms_db(32.05, 32.95):.1f} dB   (31.90-31.99: {rms_db(31.9, 31.99):.1f} dB;  32.05-32.15: {rms_db(32.05, 32.15):.1f} dB)')

# sync: a spectral-flux onset envelope at 5 ms resolution; an onset is a peak 1.5 standard deviations over the local median
f_, tf, Z = signal.stft(mono, SR, nperseg=1024, noverlap=1024 - 240, window='hann', padded=False, boundary=None)
flux = np.maximum(np.diff(np.log1p(np.abs(Z) * 50), axis=1), 0).sum(0); tf = tf[1:]
flux = flux - signal.medfilt(flux, 81); thr = 1.5 * flux.std()
pk, _ = signal.find_peaks(flux, height=thr, distance=5)
def onset(T):
    near = pk[np.abs(tf[pk] - T) <= .040]
    rise = rms_db(T, T + .03) - rms_db(T - .05, T - .01)
    if not len(near): return None, 0.0, rise
    i = near[np.argmax(flux[near])]; return (tf[i] - T) * 1000, flux[i] / thr, rise
ok = True
for label, times in (('BOLD', BOLD), ('other', OTHER)):
    print(f'sync, {label}:  time  offset  strength (x threshold)  level rise over the 40 ms before')
    for T in times:
        off, st, rise = onset(T)
        good = off is not None
        if label == 'BOLD' and not good: ok = False
        print(f"   {T:5.1f}  {'  none' if off is None else f'{off:+5.0f} ms'}  {st:5.1f}  {rise:+6.1f} dB  {'ok' if good else 'MISSING'}")
big = sorted(((onset(T)[1], T) for T in sorted(SYNC)), reverse=True)[:5]
print('strongest onsets at listed times:', [(round(T, 1), round(st, 1)) for st, T in big])
loud = sorted(((rms_db(T, T + .25), T) for T in sorted(SYNC)), reverse=True)[:5]
print('loudest quarter-seconds after a listed time:', [(round(T, 1), round(v, 1)) for v, T in loud])
print('all bold sync times have an onset within 40 ms:', ok)
fa = flux - flux.mean(); ac = signal.fftconvolve(fa, fa[::-1])[len(fa) - 1:]; lo_, hi_ = int(.3 / .005), int(2.2 / .005); lag = lo_ + int(np.argmax(ac[lo_:hi_]))
print(f'pulse again at 5 ms resolution (0.5 s is a whole number of hops here): {lag * .005:.3f} s;  autocorrelation at 0.5 s {ac[100] / ac[0]:.3f}, 1.0 s {ac[200] / ac[0]:.3f}, 2.0 s {ac[400] / ac[0]:.3f}')
F = np.abs(np.fft.rfft((flux - flux.mean()) * np.hanning(len(flux)))); ff = np.fft.rfftfreq(len(flux), .005); band = (ff >= 1 / 2.2) & (ff <= 1 / .3)
top = sorted(((F[i], ff[i]) for i in signal.find_peaks(np.where(band, F, 0))[0]), reverse=True)[:3]
print('tempo lines in the onset envelope (period s, relative strength):', [(round(1 / fr, 3), round(v / top[0][0], 2)) for v, fr in top])
b_ = int(.4 * SR); ml = sorted(((10 * math.log10(max(float((x[i:i + b_] ** 2).mean()), 1e-12)), i / SR) for i in range(0, len(x) - b_, int(.05 * SR))), reverse=True)
print('loudest 400 ms windows (dB, start):', [(round(v, 1), round(tm, 2)) for v, tm in ml[:6]])
