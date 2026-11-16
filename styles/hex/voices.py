"""Hex: the voices. Every instrument the style has, synthesised from sines, saws, noise and filters.

First written for Uptime (uptime/music.py) and moved here so that every piece sings with the same throats.

    new_mix(seconds)                      start a piece
    put(x, t, gain, pan, wet, ev=...)     lay a sound at t seconds; ev=(voice, midi) also writes it in the event list
    finish(ride, wav)                     a hall, the faders, the master; returns the samples
    EVENTS                                [(t, dur, voice, midi, gain)]: what was played, for a picture to be hung on

The event list is the point. Picture and sound are made from the same list of notes, so whoever is seen
playing is playing.
"""
import numpy as np
from scipy import signal
from backlot import sound as sd
SR = sd.SR
rng = np.random.default_rng(16)
BUS = {}; EVENTS = []; N = 0

def new_mix(seconds):
    global N; N = int(seconds * SR); BUS['dry'] = np.zeros((N + 3 * SR, 2)); BUS['wet'] = np.zeros((N + 3 * SR, 2)); EVENTS.clear()

def put(x, t, gain=1.0, pan=0.0, wet=.0, ev=None):
    i = int(round(t * SR)); x = np.asarray(x)
    if ev: EVENTS.append((round(float(t), 4), round(len(x) / SR, 4), ev[0], int(ev[1]), round(float(gain), 3)))
    if x.ndim == 1: x = np.c_[x * min(1, 1 - pan), x * min(1, 1 + pan)]
    n = min(len(x), len(BUS['dry']) - i)
    if n > 0: BUS['dry'][i:i + n] += x[:n] * gain; BUS['wet'][i:i + n] += x[:n] * gain * wet

NOTE = dict(C=0, D=2, E=4, F=5, G=7, A=9, B=11)
def midi(n): return 12 * (int(n[-1]) + 1) + NOTE[n[0]] + ('#' in n)
def hz(m): return 440.0 * 2 ** ((m - 69) / 12)
MINOR, DORIAN, MAJOR = [2, 4, 5, 7, 9, 10, 0], [2, 4, 5, 7, 9, 11, 0], [2, 4, 6, 7, 9, 11, 1]
def third(m, scale, up=True):
    pc = m % 12; i = max(range(7), key=lambda k: (scale[k] == pc, -((pc - scale[k]) % 12)))
    return m + ((scale[(i + 2) % 7] - pc) % 12) if up else m - ((pc - scale[(i - 2) % 7]) % 12)


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


def fiddle(m, dur):
    n = int(dur * SR); t = np.arange(n) / SR; f = hz(m) * (1 + .008 * np.sin(2 * np.pi * 6.1 * t) * np.clip((t - .06) / .1, 0, 1))
    x = saw(f, n) + .3 * saw(f, n, 5); return hp(bp(x, 300, 5200) + .4 * lp(x, 900), 180) * env(n, .025, .04) * .8

def finish(ride, wav, target=-14.0):
    """The hall, the faders (a list of (seconds, dB)), the master. Writes the wav and returns the samples."""
    ir_t = np.arange(int(1.7 * SR)) / SR
    ir = np.c_[lp(rng.normal(size=len(ir_t)), 5200), lp(rng.normal(size=len(ir_t)), 5200)] * np.exp(-ir_t / .42)[:, None]; ir[:int(.012 * SR)] *= 0
    wet = np.c_[signal.fftconvolve(BUS['wet'][:, 0], ir[:, 0])[:len(BUS['wet'])], signal.fftconvolve(BUS['wet'][:, 1], ir[:, 1])[:len(BUS['wet'])]] * .028
    x = (BUS['dry'] + wet)[:N]; tt = np.arange(N) / SR
    x = x * (10 ** (np.interp(tt, [a for a, _ in ride], [b for _, b in ride]) / 20))[:, None]
    x = sd.master(x, target_lufs=target, ceiling=-1.0); sd.write_wav(wav, x); return x
