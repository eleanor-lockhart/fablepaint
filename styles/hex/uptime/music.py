"""UPTIME: the score. Seventy-two bars of 6/8 at one bar a second, so the clock on the screen is the metronome.

    uv run python styles/hex/uptime/music.py      writes out/hex/uptime.wav, uptime.mp3 and the listening-room sheet

Everything is synthesised here from sines, saws, noise and filters; nothing is sampled. The plan, bar by bar, is
in BRIEF.md. A jig in D Dorian (whistle, harp, drone, drum) is the place at peace. The same tune over a kick on
every eighth, with two leads a third apart and a choir, is the hive. An organ and a choir climb four chords
four times while everybody waits. Midnight is a hum. Then the jig comes back in D major with everything at once.
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
import numpy as np
from scipy import signal
from backlot import sound as sd, ear
SR = sd.SR; E = 1.0 / 6; BARS = 72; N = BARS * SR
rng = np.random.default_rng(16)
NOTE = dict(C=0, D=2, E=4, F=5, G=7, A=9, B=11)
def midi(n): return 12 * (int(n[-1]) + 1) + NOTE[n[0]] + ('#' in n)
def hz(m): return 440.0 * 2 ** ((m - 69) / 12)
MINOR, DORIAN, MAJOR = [2, 4, 5, 7, 9, 10, 0], [2, 4, 5, 7, 9, 11, 0], [2, 4, 6, 7, 9, 11, 1]
def third(m, scale, up=True):
    pc = m % 12; i = max(range(7), key=lambda k: (scale[k] == pc, -((pc - scale[k]) % 12)))
    return m + ((scale[(i + 2) % 7] - pc) % 12) if up else m - ((pc - scale[(i - 2) % 7]) % 12)

BUS = {k: np.zeros((N + 3 * SR, 2)) for k in ('dry', 'wet')}
def put(x, t, gain=1.0, pan=0.0, wet=.0):
    i = int(round(t * SR)); x = np.asarray(x)
    if x.ndim == 1: x = np.c_[x * min(1, 1 - pan), x * min(1, 1 + pan)]
    n = min(len(x), len(BUS['dry']) - i)
    BUS['dry'][i:i + n] += x[:n] * gain; BUS['wet'][i:i + n] += x[:n] * gain * wet

def env(n, a=.005, r=.03, decay=0.0):
    t = np.arange(n) / SR; e = np.minimum(1, t / a) * np.exp(-decay * t); k = min(int(r * SR), n)
    if k: e[-k:] *= np.linspace(1, 0, k)
    return e
def saw(f, n, det=0.0, ph=0.0): return 2 * (((np.cumsum(np.full(n, f * 2 ** (det / 1200)) if np.isscalar(f) else f * 2 ** (det / 1200)) / SR) + ph) % 1) - 1
def lp(x, fc, o=2): return signal.sosfilt(signal.butter(o, fc, 'low', fs=SR, output='sos'), x)
def hp(x, fc, o=2): return signal.sosfilt(signal.butter(o, fc, 'high', fs=SR, output='sos'), x)
def bp(x, lo, hi): return signal.sosfilt(signal.butter(2, [lo, hi], 'band', fs=SR, output='sos'), x)
def nz(n): return rng.uniform(-1, 1, n)

# ---------------------------------------------------------------- voices
def whistle(m, dur, cut=None):
    n = int(dur * SR); t = np.arange(n) / SR; f = np.full(n, hz(m))
    if cut is not None: f[:int(.03 * SR)] = hz(cut)                                   # the ornament pipers call a cut
    f = f * (1 + .006 * np.sin(2 * np.pi * 5.2 * t) * np.clip((t - .12) / .15, 0, 1)); ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) + .14 * np.sin(2 * ph) + .05 * np.sin(3 * ph) + .06 * bp(nz(n), 2500, 7000)) * env(n, .014, .035)
def harp(m, dur=1.4):
    n = int(dur * SR); t = np.arange(n) / SR; f = hz(m)
    return sum(np.sin(2 * np.pi * k * f * t) / k * np.exp(-t * (1.8 + 1.4 * k)) for k in range(1, 7)) * env(n, .002, .05)
def glass(m, dur=2.2):
    n = int(dur * SR); t = np.arange(n) / SR; f = hz(m)
    return (np.sin(2 * np.pi * f * t) * np.exp(-2.0 * t) + .35 * np.sin(2 * np.pi * 2.76 * f * t) * np.exp(-5 * t) + .15 * np.sin(2 * np.pi * 5.4 * f * t) * np.exp(-9 * t)) * env(n, .002, .1)
def pad(ms, dur, kind='strings', a=.12, r=.25, trem=0.0):
    n = int(dur * SR); t = np.arange(n) / SR; out = np.zeros((n, 2))
    for m in ms:
        if kind == 'organ':
            f = hz(m); x = sum(amp * np.sin(2 * np.pi * h * f * t + h) for h, amp in ((1, 1), (2, .6), (3, .35), (4, .3), (6, .15), (8, .1))) * .35; out += np.c_[x, x]
        else:
            for det, pan in ((-9, -.6), (0, 0), (8, .6)):
                x = saw(hz(m), n, det, rng.random())
                x = lp(x, 1900) if kind == 'strings' else (bp(x, 450, 950) * 1.6 + bp(x, 950, 1500) * 1.1 + lp(x, 300) * .3)       # a choir is a saw with two vowels cut out of it
                out += np.c_[x * (1 - max(pan, 0)), x * (1 + min(pan, 0))] * .33
    e = env(n, a, r) * (1 - trem * .5 * (1 + np.sin(2 * np.pi * 11 * t))); return out * e[:, None]
def guitar(m, dur, palm=False):
    """A power chord, twice, one take in each ear."""
    n = int(dur * SR); takes = []
    for det in (-6, 7):
        x = sum(saw(hz(m + s), n, det + d2, rng.random()) for s, d2 in ((0, 0), (7, 3), (12, -4)))
        x = np.tanh(x * (3.2 if palm else 4.5)); x = hp(lp(x, 1500 if palm else 3300), 85)
        takes.append(x * env(n, .003, .02, 26 if palm else 1.2))
    return np.c_[takes[0], takes[1]] * .5
def lead(m, dur):
    n = int(dur * SR); t = np.arange(n) / SR; f = hz(m) * (1 + .007 * np.sin(2 * np.pi * 5.6 * t) * np.clip((t - .1) / .12, 0, 1))
    x = saw(f, n) + .5 * np.sign(saw(f, n, 3)); return lp(np.tanh(x * 1.8), 3800) * env(n, .008, .03) * .6
def bass(m, dur): n = int(dur * SR); t = np.arange(n) / SR; return (lp(saw(hz(m), n), 380) + .7 * np.sin(2 * np.pi * hz(m) * t)) * env(n, .004, .03, 2.5)
def kick(): n = int(.16 * SR); t = np.arange(n) / SR; return np.sin(2 * np.pi * (45 * t + 75 / 28 * (1 - np.exp(-28 * t)))) * env(n, .001, .03, 14) + .25 * hp(nz(n), 3000) * np.exp(-t * 300)
def snare(): n = int(.16 * SR); t = np.arange(n) / SR; return (bp(nz(n), 900, 6000) * np.exp(-t * 26) + .5 * np.sin(2 * np.pi * 190 * t) * np.exp(-t * 34)) * env(n, .001, .02)
def hat(): n = int(.035 * SR); return hp(nz(n), 7000) * env(n, .0005, .01, 90)
def crash(dur=1.4): n = int(dur * SR); t = np.arange(n) / SR; return hp(nz(n), 3500) * np.exp(-t * 3.2) * env(n, .001, .1)
def timp(m, dur=.9): n = int(dur * SR); t = np.arange(n) / SR; return (np.sin(2 * np.pi * hz(m) * (t + .02 * (1 - np.exp(-t * 30)))) * np.exp(-t * 4.5) + .3 * lp(nz(n), 500) * np.exp(-t * 40)) * env(n, .002, .05)
def bodhran(acc): n = int(.11 * SR); t = np.arange(n) / SR; return (np.sin(2 * np.pi * (88 if acc else 120) * t) * np.exp(-t * (22 if acc else 45)) + .35 * lp(nz(n), 900) * np.exp(-t * 60)) * env(n, .001, .02)
def tick(): n = int(.03 * SR); t = np.arange(n) / SR; return np.sin(2 * np.pi * 1650 * t) * np.exp(-t * 160)
def click(): n = int(.012 * SR); return hp(nz(n), 2000) * env(n, .0003, .004, 200)
def ding(kind='sys'):
    if kind == 'hers': return glass(50, 2.6) + .8 * glass(56, 2.6) + .5 * glass(62, 2.6)                # D, and the tritone above it
    a, b = (93, 98) if kind == 'sys' else (92.4, 97.5); x = np.zeros(int(.6 * SR)); g = glass(a, .25); x[:len(g)] += g; g = glass(b, .45); x[int(.06 * SR):int(.06 * SR) + len(g)] += g; return x
def modem(seed):
    r = np.random.default_rng(seed); out = []
    for _ in range(7): n = int(.035 * SR); t = np.arange(n) / SR; out.append(np.sin(2 * np.pi * r.choice([1070, 1270, 2025, 2225, 1650, 980]) * t) * env(n, .002, .004))
    return np.concatenate(out) + .15 * bp(nz(7 * int(.035 * SR)), 1000, 2600)
def whine(): n = int(.75 * SR); t = np.arange(n) / SR; f = 1200 * (150 / 1200) ** (t / .75); return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, .005, .2)

CH = dict(Dm=(50, [50, 57, 62, 65]), C=(48, [48, 55, 60, 64]), Bb=(46, [46, 53, 58, 62]), A=(45, [45, 52, 57, 61]), F=(41, [53, 57, 60, 65]), Gm=(43, [43, 50, 55, 58]),
          D=(50, [50, 57, 62, 66]), G=(43, [55, 59, 62, 67]))                                         # name -> (bass, voicing), as MIDI
def tune(bar_strings, start, voice, gain, pan=0.0, wet=.3, shift=0, harm=None, cuts=False):
    """Six tokens a bar: a note, '.' for a rest, '-' to hold the note before."""
    for b, s in enumerate(bar_strings):
        tok = s.split(); k = 0
        while k < 6:
            if tok[k] in '.-': k += 1; continue
            L = 1
            while k + L < 6 and tok[k + L] == '-': L += 1
            m = midi(tok[k]) + shift
            if harm: m = third(m, harm[0], harm[1])
            x = voice(m, E * L * .96, cut=m + 3) if (cuts and k in (0, 3)) else voice(m, E * L * .96)
            put(x, start + b + k * E, gain * (1.12 if k in (0, 3) else 1.0), pan, wet); k += L

A = ['A4 D5 D5 F5 D5 D5', 'A4 D5 D5 G5 F5 E5', 'A4 D5 D5 F5 D5 F5', 'G5 E5 C5 D5 - -']
B = ['C5 F5 F5 A5 F5 F5', 'C5 E5 E5 G5 E5 C5', 'D5 F5 A5 D6 A5 F5', 'E5 C#5 A4 D5 - -']
AM = ['A4 D5 D5 F#5 D5 D5', 'A4 D5 D5 G5 F#5 E5', 'A4 D5 D5 F#5 D5 F#5', 'G5 E5 C#5 D5 - -']
M = ['A4 D5 D5 F5 D5 D5', 'A4 D5 D5 G5 F5 E5', 'G4 C5 C5 E5 C5 C5', 'G4 C5 C5 F5 E5 D5', 'F4 A#4 A#4 D5 A#4 A#4', 'F4 A#4 A#4 D5 A#4 D5']

# 0-3: the machine starts
n_ = int(.14 * SR); put(np.sign(np.sin(2 * np.pi * 1000 * np.arange(n_) / SR)) * env(n_, .002, .01) * .5, .25, .22)
for t in np.sort(rng.uniform(1.0, 2.5, 16)): put(click(), t, .25, rng.uniform(-.5, .5))
for k, nt in enumerate('A3 D4 F4 A4 D5 F5'.split()): put(harp(midi(nt)), 2 + k * E, .22 + .05 * k, 0, .4)
put(click(), 3, .5)
for k, nt in enumerate((62, 69, 76, 77, 81, 86)): put(glass(nt), 3 + k * .06, .34, (k - 2.5) / 4, .6)
put(pad(CH['Dm'][1], 1.6, 'strings', .5, .8), 3, .22, 0, .5)
for b in range(3, BARS):                                                                               # the clock, on every bar
    put(tick(), b, .10 if b < 28 else .26 if b < 34 else .16 + .012 * (b - 34) if b < 50 else .3 if b < 56 else .1, .25)
# 4-11: the place at peace
put(pad([38, 45], 8.4, 'strings', 1.0, 1.2), 4, .22, 0, .4)
tune(A + A, 4, whistle, .42, -.1, .45, cuts=True); tune(A, 8, whistle, .22, .3, .45, harm=(DORIAN, False))
for b in range(4, 12):
    ch = CH['C'] if b % 4 == 3 else CH['Dm']
    put(harp(ch[1][0]), b, .2, -.3, .4); put(harp(ch[1][2]), b + E, .16, -.3, .4); put(harp((CH['Dm'] if b % 4 == 3 else ch)[1][1]), b + 3 * E, .18, .3, .4); put(harp(ch[1][3]), b + 4 * E, .15, .3, .4)
    if b >= 8:
        for k in range(6): put(bodhran(k in (0, 3)), b + k * E, .5 if k in (0, 3) else .22, 0, .15)
put(click(), 8, .5)
# 12-19: the crowd
for j, b in enumerate(range(12, 20)):
    nm = ('F', 'C', 'Dm', 'A')[j % 4]; root, vo = CH[nm]; up = 1 + .05 * j
    put(modem(b), b, .13, -.6 if j % 2 else .6)
    for k in range(6): put(pad([vo[0] + 12 if vo[0] < 50 else vo[0]], .15, 'strings', .01, .05), b + k * E, .5 * up, 0, .2)
    put(bass(root - 12, .45), b, .5 * up); put(bass(root - 12, .45), b + 3 * E, .45 * up)
    put(kick(), b, .8); put(snare(), b + 3 * E, .5 * up, 0, .15)
    if j >= 4:
        for k in range(6): put(hat(), b + k * E, .22, .3)
tune(B + B, 12, whistle, .44, -.1, .4, cuts=True); tune(B, 16, lead, .3, .25, .3, shift=-12)
# 20-21: NEWTS
put(click(), 20, .6); put(guitar(38, 1.3), 20, .55, 0, .25); put(crash(), 20, .4, 0, .4); put(kick(), 20, 1.0); put(timp(38), 20, .6, 0, .3)
for k in range(8): put(glass(96 - 2 * k, .12), 20.5 + k * E / 2, .16, (k - 3.5) / 5, .3)
for k in range(12): put(bodhran(False), 21 + k * E / 2, .12 + .05 * (5.5 - abs(k - 5.5)) / 5.5, 0, .15)
# 22-27: the hive
put(ding('hive'), 22, .25, 0, .4)
for j, b in enumerate(range(22, 28)):
    nm = ('Dm', 'Dm', 'C', 'C', 'Bb', 'Bb')[j]; root, vo = CH[nm]
    for k in range(6):
        put(guitar(root - 12, E * (.95 if k in (0, 3) else .8), palm=k not in (0, 3)), b + k * E, .46 if k in (0, 3) else .40)
        put(kick(), b + k * E, .75); put(bass(root - 12, E * .9), b + k * E, .42)
        if k == 3: put(snare(), b + k * E, .62, 0, .15)
    if j % 2 == 0: put(crash(), b, .3, 0, .4)
    put(pad([m + 12 for m in vo[1:]], 1.02, 'choir', .05, .1), b, .26, 0, .5)
tune(M, 22, lead, .34, -.3, .3, shift=12); tune(M, 22, lead, .25, .35, .3, shift=12, harm=(MINOR, True))
# 28-33: the hive tries to close her; stop-time
for b, k in ((28, 'hive'), (30, 'hive'), (32, 'hive')): put(ding(k), b, .3, 0, .45)
for b, nm in ((29, 'A'), (31, 'Bb'), (33, 'A')):
    root, vo = CH[nm]; put(click(), b, .6); put(guitar(root - 12, .5), b, .55, 0, .25); put(pad([m + 12 for m in vo], .5, 'choir', .01, .2), b, .3, 0, .5); put(crash(.6), b, .28, 0, .4); put(timp(root - 12, .7), b, .55, 0, .3); put(kick(), b, .9)
put(timp(38, 1.6), 33.5, .8, 0, .4); put(ding('hers'), 33.5, .22, 0, .5); put(glass(100, .1), 33.85, .12)
# 34-49: the wait
put(ding('sys'), 34, .5, 0, .4)
for j, b in enumerate(range(34, 50)):
    nm = ('Dm', 'Bb', 'Gm', 'A')[j % 4]; root, vo = CH[nm]; lvl = j / 15
    put(pad(vo + ([m + 12 for m in vo[1:]] if j >= 8 else []), 1.04, 'organ', .04, .08), b, .13 + .09 * lvl, 0, .5)
    if j >= 4: put(pad([m + 12 for m in vo[1:]], 1.04, 'choir', .08, .1), b, .14 + .12 * lvl, 0, .55); put(timp(root - 12 if root > 43 else root), b, .4 + .3 * lvl, 0, .35)
    if j >= 8:
        put(pad([vo[0] + 12, vo[2] + 12], 1.02, 'strings', .03, .06, trem=.8), b, .16 + .1 * lvl, 0, .4); put(bass(root - 12, .95), b, .4)
        for k in (range(6) if j >= 12 else (0, 3)): put(snare(), b + k * E, (.2 + .25 * lvl) * (1 if k in (0, 3) else .6), 0, .15)
    if j >= 12:
        put(guitar(root - 12, 1.0), b, .34 + .12 * lvl, 0, .2)
        for k in range(12 if j == 15 else 6): put(kick(), b + k * (E / 2 if j == 15 else E), .6)
put(crash(2.0), 46, .3, 0, .4)
# 50-53: midnight
n_ = 6 * SR; t = np.arange(n_) / SR; put((np.sin(2 * np.pi * 55 * t) + .4 * np.sin(2 * np.pi * 110.4 * t)) * env(n_, .6, 1.0), 50, .2)
for t0 in (50, 51, 52, 53, 53.5): put(whine(), t0, .13, rng.uniform(-.5, .5), .35); put(bodhran(True), t0, .9); put(click(), t0, .5)      # each light goes out with a thump
# 54-55: the decree arrives
put(ding('hers'), 54, .5, 0, .5); put(click(), 54, .6)
for k in range(12): put(timp(38, .3), 55 + k * E / 2, .12 + .05 * k, 0, .3)
# 56-63: OK
put(click(), 56, .6); put(crash(2.0), 56, .45, 0, .4); put(crash(), 60, .35, 0, .4)
for j, b in enumerate(range(56, 64)):
    nm = ('D', 'G', 'D', 'A', 'D', 'G', 'A', 'D')[j]; root, vo = CH[nm]
    for k in range(6):
        put(guitar(root - 12, E * (.95 if k in (0, 3) else .8), palm=k not in (0, 3)), b + k * E, .42 if k in (0, 3) else .34)
        put(kick(), b + k * E, .7 if k in (0, 3) else .45); put(bass(root - 12, E * .9), b + k * E, .4)
        if k == 3: put(snare(), b + k * E, .6, 0, .15)
        put(hat(), b + k * E, .16, .3)
    put(pad([m + 12 for m in vo[1:]], 1.02, 'choir', .05, .1), b, .25, 0, .5); put(pad(vo, 1.02, 'organ', .03, .08), b, .1, 0, .4)
tune(AM + AM, 56, whistle, .46, -.1, .4, cuts=True); tune(AM + AM, 56, lead, .28, -.35, .3); tune(AM + AM, 56, lead, .22, .35, .3, harm=(MAJOR, True))
for b_ in (57, 58, 59, 60, 61): put(glass(86 + (b_ - 57) * 2, .5), b_, .2, 0, .5)                # each light comes back with a note
put(guitar(38, 1.6), 64, .4, 0, .3); put(crash(), 64, .25, 0, .4); put(timp(38), 64, .5, 0, .3)
# 64-71: quiet
put(pad([38, 45], 8.0, 'strings', 1.0, 3.0), 64, .2, 0, .4)
tune(AM, 64, whistle, .3, -.1, .5, cuts=True)
for b in range(64, 68):
    vo = CH['A'][1] if b % 4 == 3 else CH['D'][1]; put(harp(vo[0]), b, .2, -.3, .4); put(harp(vo[2]), b + E, .16, -.3, .4); put(harp(vo[1]), b + 3 * E, .18, .3, .4); put(harp(vo[3]), b + 4 * E, .15, .3, .4)
put(ding('sys'), 68, .5, 0, .4); put(click(), 68, .5)
for k, m in enumerate((50, 57, 62, 66, 69, 74)): put(harp(m, 2.5), 68 + k * 2 * E, .2, (k - 2.5) / 5, .5)
put(click(), 70, .5); put(glass(86, 2.0), 70, .14, 0, .6); put(glass(81, 2.0), 70.02, .1, 0, .6)

# ---------------------------------------------------------------- a hall, and the master
ir_t = np.arange(int(1.7 * SR)) / SR
ir = np.c_[lp(rng.normal(size=len(ir_t)), 5200), lp(rng.normal(size=len(ir_t)), 5200)] * np.exp(-ir_t / .42)[:, None]; ir[:int(.012 * SR)] *= 0
wet = np.c_[signal.fftconvolve(BUS['wet'][:, 0], ir[:, 0])[:len(BUS['wet'])], signal.fftconvolve(BUS['wet'][:, 1], ir[:, 1])[:len(BUS['wet'])]] * .028
x = (BUS['dry'] + wet)[:N]; x[-int(.4 * SR):] *= np.linspace(1, 0, int(.4 * SR))[:, None]
# riding the faders: the place at peace is quiet, midnight is nearly nothing, and the decree is the loudest thing in it
ride = [(0, -4), (4, -8), (12, -7), (16, -4), (20, -1), (20.01, 0), (22, 0), (22.01, 1), (28, 1), (28.05, 0), (34, 0), (34.05, -3), (42, -1), (50, 0), (50.02, -12), (53.93, -12), (53.98, -4), (56, -4), (56.01, 2.5), (64, 2), (64.5, -5), (72, -7)]
tt = np.arange(N) / SR; x = x * (10 ** (np.interp(tt, [a for a, _ in ride], [b for _, b in ride]) / 20))[:, None]
x = sd.master(x, target_lufs=-14.0, ceiling=-1.0)
out = Path('out/hex'); out.mkdir(parents=True, exist_ok=True); sd.write_wav(out / 'uptime.wav', x)
m = ear.measure(x); print({k: round(v, 2) for k, v in m.items() if isinstance(v, float)})
for name, a, b in (('jig 4-12', 4, 12), ('crowd 12-20', 12, 20), ('hive 22-28', 22, 28), ('stop-time 28-34', 28, 34), ('wait 34-42', 34, 42), ('wait 42-50', 42, 50), ('midnight 50-54', 50, 54), ('decree 56-64', 56, 64), ('quiet 64-72', 64, 72)):
    seg = x[a * SR:b * SR]; print(f'  {name:<18} rms {20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-9):6.1f} dB   peak {20 * np.log10(np.abs(seg).max() + 1e-9):6.1f} dB')
ear.report(str(out / 'uptime.wav'), str(HERE / 'uptime_score.jpg'), title='UPTIME: 72 bars of 6/8, one bar a second')
sd.encode(str(out / 'uptime.wav'), str(HERE / 'uptime.mp3'))
