"""BASE CASE: the score. Forty-eight bars of 4/4 at 120; a bar is two seconds, a beat half a second.

    uv run python styles/hex/basecase/music.py     writes out/hex/basecase.wav, basecase.mp3, the listening-room sheet, events.json

A ground: one bass note a bar, stepping down (D, C, B flat, A), stated twelve times, eight seconds each, one
scene each. Over it one tune. Going down, the tune is handed to older and older machines and loses its voices
with its colours: an orchestra, three square waves, one eight-bit voice, a beeper. At the bottom there is a
pedal note and the keys. At bar 35 she presses RETURN, the value returned is F, and the piece is in F major
from there: the same tune in the relative major, each machine joining again on the way up.

  bars 0-3     wind; a music box; it stops dead at 5.0 with the lights
  4-7          the ground, plucked; the kitchen clock; the hinge; from 13.0 every step she takes is a note of the scale, descending
  8-11         the scale goes on down (two octaves in all); a whistle has the tune; then footfalls
  12-15        the answer on the music box; harp; strings; a rise into the glass
  16-19        1989: three square waves and a noise channel
  20-23        1987: one eight-bit voice, and the mouse
  24-27        1980: a beeper and the keys; at 54.0 her chord, which is not from the machine
  28-31        the keys; two answers and an error; a pedal D
  32-35        nothing but the pedal and a heartbeat; half a second of silence; RETURN: F major
  36-39        the tune in the major: the beeper, then the eight-bit voice, then the squares, then strings
  40-43        everyone: guitars, drums, choir, whistle and lead on the tune
  44-47        the answer; a note for each window; a last chord; the music box
"""
import sys, json
from pathlib import Path
HERE = Path(__file__).resolve().parent; sys.path.insert(0, str(HERE.parent))
import numpy as np
from scipy import signal
import voices as V
from voices import put, midi, SR, hz
from backlot import sound as sd, ear
BAR, Q = 2.0, .5; BARS = 48
V.new_mix(BARS * BAR)
T = lambda bar, beat=0.0: bar * BAR + beat * Q
rng = np.random.default_rng(7)
M = midi
# the ground and the tune: (note, beats)
MINOR = [('D', [50, 57, 62, 65]), ('C', [48, 55, 60, 64]), ('Bb', [46, 53, 58, 62]), ('Am', [45, 52, 57, 60])]; ROOT = dict(D=38, C=36, Bb=34, Am=33, A=33, F=41, CE=40, Dm=38, C2=36)
MAJOR = [('F', [53, 60, 65, 69]), ('CE', [52, 60, 64, 67]), ('Dm', [50, 57, 62, 65]), ('C2', [48, 55, 60, 64])]
T1 = [[(74, 1), (77, 1), (81, 2)], [(79, 1), (76, 1), (72, 2)], [(74, 1), (77, 1), (82, 1.5), (81, .5)], [(81, 2), (76, 2)]]
T2 = [[(81, 1), (77, 1), (74, 2)], [(79, 1), (76, 1), (72, 2)], [(77, 1), (74, 1), (70, 1), (74, 1)], [(73, 2), (69, 2)]]
TM = [[(77, 1), (81, 1), (84, 2)], [(82, 1), (79, 1), (76, 2)], [(77, 1), (81, 1), (86, 1.5), (84, .5)], [(84, 2), (79, 2)]]
TM2 = [[(84, 1), (81, 1), (77, 2)], [(82, 1), (79, 1), (76, 2)], [(81, 1), (77, 1), (74, 1), (77, 1)], [(76, 2), (79, 1), (84, 1)]]
def tune(bars, bar0, voice, gain, pan=0.0, wet=.3, shift=0, name=None, hold=.95, **kw):
    for j, notes in enumerate(bars):
        b = 0.0
        for m, d in notes: put(voice(m + shift, d * Q * hold, **kw), T(bar0 + j, b), gain, pan, wet, ev=(name, m + shift) if name else None); b += d

# ------------------------------------------------------------------ voices this piece adds
def crush(x, bits=8, rate=11025):
    """A sound as an old converter gives it: few samples a second, few steps of loudness."""
    k = max(int(SR / rate), 1); y = np.repeat(x[::k], k)[:len(x)]; q = 2 ** (bits - 1); return np.round(y * q) / q
def sq(m, dur, duty=.25, vol=1.0):
    """One channel of a three-voice sound chip: a pulse wave, sixteen volume steps."""
    n = int(dur * SR); ph = (np.arange(n) * hz(m) / SR) % 1; e = np.round(np.minimum(1, np.linspace(1.6, .55, n)) * 15) / 15
    e[-min(int(.012 * SR), n):] *= np.linspace(1, 0, min(int(.012 * SR), n)); return V.lp(np.where(ph < duty, 1.0, -1.0) * e * vol, 9000) * .5
def tri(m, dur):
    """The same chip's triangle, in sixteen steps."""
    n = int(dur * SR); ph = (np.arange(n) * hz(m) / SR) % 1; x = np.round((2 * np.abs(2 * ph - 1) - 1) * 7.5) / 7.5; x[-min(int(.01 * SR), n):] *= np.linspace(1, 0, min(int(.01 * SR), n)); return x * .6
def chh(dur=.03): n = int(dur * SR); return np.repeat(rng.choice([-1.0, 1.0], n // 6 + 1), 6)[:n] * np.linspace(1, 0, n) * .5
def boop(m, dur):
    """1987: one voice, eight bits, eleven thousand samples a second."""
    n = int(dur * SR); t = np.arange(n) / SR; x = (np.sin(2 * np.pi * hz(m) * t) + .3 * np.sin(4 * np.pi * hz(m) * t)) * np.exp(-t * 2.2) * np.minimum(1, t / .004); return crush(x * .7, 6, 11025)
def beep(m, dur):
    """1980: a speaker that is either in or out."""
    n = int(dur * SR); x = np.sign(np.sin(2 * np.pi * hz(m) * np.arange(n) / SR)); k = min(int(.002 * SR), n); x[:k] *= np.linspace(0, 1, k); x[-k:] *= np.linspace(1, 0, k); return V.lp(x, 7000) * .4
def key(): n = int(.02 * SR); return np.sign(np.sin(2 * np.pi * 2400 * np.arange(n) / SR)) * np.linspace(1, 0, n)* .35
def buzz(dur=.22): n = int(dur * SR); return np.sign(np.sin(2 * np.pi * 98 * np.arange(n) / SR)) * .4 * np.minimum(1, np.linspace(8, 0, n))
def wind(dur, seed=1):
    r = np.random.default_rng(seed); n = int(dur * SR); t = np.arange(n) / SR; x = r.uniform(-1, 1, n)
    a = V.bp(x, 300, 900) * (.6 + .4 * np.sin(2 * np.pi * .13 * t + 1)) + .6 * V.bp(x, 900, 2200) * (.5 + .5 * np.sin(2 * np.pi * .21 * t)) ** 2
    return a * np.minimum(1, t / 1.5) * np.minimum(1, (dur - t) / 1.5)
def thunk(): n = int(.5 * SR); t = np.arange(n) / SR; return np.sin(2 * np.pi * (38 * t + 60 / 20 * (1 - np.exp(-20 * t)))) * np.exp(-t * 9) + .5 * V.lp(V.nz(n), 400) * np.exp(-t * 30)
def creak(dur=1.2):
    n = int(dur * SR); t = np.arange(n) / SR; f = 70 + 90 * (t / dur) ** 1.5 + 12 * np.sin(2 * np.pi * 7 * t); ph = np.cumsum(f) / SR
    return V.bp(np.sign(np.sin(2 * np.pi * ph)) * (((ph * 1.0) % 1) < .35), 500, 2600) * np.minimum(1, t / .05) * np.minimum(1, (dur - t) / .1) * (.6 + .4 * np.sin(2 * np.pi * 3.1 * t))
def riser(dur, lo=300, hi=6000):
    n = int(dur * SR); t = np.arange(n) / SR; x = V.nz(n); out = np.zeros(n); k = 8
    for i in range(k):
        a, b = int(i * n / k), int((i + 1) * n / k); fc = lo * (hi / lo) ** ((i + .5) / k); out[a:b] = V.bp(x[a:b], fc * .7, fc * 1.4)
    return out * (t / dur) ** 2
def chatter(dur, seed=2):
    """A hard disc looking for something."""
    r = np.random.default_rng(seed); n = int(dur * SR); x = np.zeros(n)
    for t0 in np.cumsum(r.exponential(.045, int(dur / .04))):
        i = int(t0 * SR)
        if i < n - 200: x[i:i + 200] += V.bp(r.uniform(-1, 1, 200), 1500, 5000) * np.linspace(1, 0, 200) * r.uniform(.3, 1)
    return x
def ticks(dur, rate=28.0): n = int(dur * SR); x = np.zeros(n); x[::int(SR / rate)] = 1; return V.bp(signal.lfilter(np.ones(40) / 6, 1, x), 1800, 6000) * 1.2
def typing(text, t0, cps=14.0, gain=.3, pan=.2):
    for i, ch in enumerate(text):
        if ch != ' ': put(key(), t0 + i / cps, gain * rng.uniform(.8, 1.1), pan, .05)
def ground(bars, bar0, chords, voice, gain, octave=0, wet=.25, name=None, every=(0,), **kw):
    for j in range(bars):
        nm, _ = chords[j % 4]
        for b in every: put(voice(ROOT[nm] + octave, **kw), T(bar0 + j, b), gain, 0, wet, ev=(name, ROOT[nm] + octave) if name and b == 0 else None)

# ================================================================== level 0: the house
put(wind(9.0), 0, .34, 0, .1); put(wind(9.5, 4), 86.5, .2, 0, .1)
put(V.pad([38, 45], 5.2, 'strings', 1.5, .1), 0, .16, 0, .5)
b = 0.0                                                             # bars 0-2: the music box, which stops with the lights
for j, notes in enumerate(T1[:3]):
    bb = 0.0
    for m, d in notes:
        if T(j, bb) < 4.9: put(V.glass(m, 1.6)[:int(min(1.6, 5.0 - T(j, bb)) * SR)], T(j, bb), .34, -.2, .5, ev=('box', m))
        bb += d
put(thunk(), 5.0, .9, 0, .2, ev=('power', 0)); put(V.ding('sys'), 5.5, .34, -.3, .3, ev=('ui', 0)); put(V.click(), 5.5, .4, -.3, .1); put(V.whine(), 5.0, .3, .3, .3); put(V.pad([26, 38], 3.2, 'strings', .8, 1.2), 5.0, .2, 0, .4)
# bars 4-7: the pantry
for j in range(4):
    nm, vo = MINOR[j]; put(V.harp(ROOT[nm], 2.2), T(4 + j), .5, 0, .35, ev=('ground', ROOT[nm])); put(V.harp(ROOT[nm] + 12, 1.6), T(4 + j, 2), .26, .1, .35); put(V.harp(vo[1], 1.4), T(4 + j, 3), .2, -.2, .35)
for k in range(10): put(V.tick(), 8.0 + k * .5, .12 if k % 2 else .17, .5, .2)             # the kitchen clock
put(V.bodhran(True), 8.0, .8, 0, .2); put(V.click(), 8.0, .5, 0, .1)
put(creak(1.2), 11.6, .42, .1, .3, ev=('hinge', 0)); put(V.pad([50, 57, 62, 69], 3.0, 'strings', .3, 1.5), 12.8, .2, 0, .5, ev=('glow', 62)); put(V.glass(74, 2.0), 12.8, .22, .2, .6); put(V.bodhran(True), 12.8, .5, 0, .2)
STEPS = [74, 72, 70, 69, 67, 65] + [64, 62, 60, 58, 57, 55, 53, 52, 50, 38]         # D5 down the scale; the last is the floor
for k, m in enumerate(STEPS):
    t = 13.0 + k * .5 if k < 6 else 16.0 + (k - 6) * .5
    put(V.harp(m, 1.5), t, .46, -.3 + .04 * k, .4, ev=('step', m)); put(V.glass(m + 12, .8), t, .12, .3, .5); put(V.bodhran(k % 2 == 0), t, .2, 0, .15)
put(V.bodhran(True), 20.5, 1.0, 0, .25); put(V.timp(38, 1.0), 20.5, .55, 0, .3); put(V.kick(), 20.5, .6, 0, .2)
# bars 8-11: the basement. Strings on the ground, the whistle on the tune, then her feet on the floor
for j in range(4): nm, vo = MINOR[j]; put(V.pad([ROOT[nm]] + vo[:3], 2.1, 'strings', .35, .3), T(8 + j), .15, 0, .45, ev=('ground', ROOT[nm]))
tune(T1, 8, V.whistle, .2, .25, .5, name='whistle')
for k in range(10): put(V.bodhran(k % 2 == 0), 21.0 + k * .5, .2, -.1, .2, ev=('foot', 0))
# bars 12-15: at the desk. The disc; the answer on the music box; harp in eighths; strings; a rise
put(chatter(1.6), 26.0, .22, .4, .15, ev=('disc', 0)); put(V.ding('sys'), 26.0, .14, .4, .3)
for j in range(4):
    nm, vo = (MINOR[j][0], MINOR[j][1]) if j < 3 else ('A', [45, 52, 57, 61]); g = .16 + .035 * j
    put(V.pad([ROOT[nm]] + vo, 2.1, 'strings', .3, .3), T(12 + j), g, 0, .45, ev=('ground', ROOT[nm]))
    for e in range(8): put(V.harp(vo[(e * 3) % 4] + 12, .9), T(12 + j, e * .5), .16 + .02 * j, .3 - .08 * e, .4)
tune(T2, 12, V.glass, .3, -.2, .5, name='box', hold=2.4)
put(riser(1.9), 30.1, .34, 0, .3); put(V.timp(33, 1.2), 31.0, .3, 0, .3)

# ================================================================== level 1: 1989, three square waves
def chip(bar0, bars, chords, melody, lead=.2, tag='chip'):
    for j in range(bars):
        nm, vo = chords[j % 4]
        for e in range(8): put(sq(ROOT[nm] + (12 if e % 2 else 0), .2, .5), T(bar0 + j, e * .5), .2, -.3, .04, ev=(tag, ROOT[nm]) if e == 0 else None)
        for s in range(16): put(tri(vo[s % 4] + 12, .1), T(bar0 + j, s * .25), .12, .4, .04)
        for e in range(8): put(chh(), T(bar0 + j, e * .5), .14 if e % 2 else .07, .1, 0)
    tune(melody[:bars], bar0, sq, lead, 0, .05, name=tag, duty=.25)
put(sq(84, .12, .5), 32.0, .4, 0, .05); put(sq(91, .2, .5), 32.12, .3, 0, .05, ev=('ui', 1)); put(V.click(), 32.0, .5)               # PRESS ANY KEY
chip(16, 4, MINOR, T1)
put(key(), 32.8, .7, .2); put(sq(96, .05, .5), 32.8, .3, 0, .05); typing('LIFT TRAPDOOR', 32.9); put(sq(79, .07, .5), 34.0, .26, 0, .05, ev=('ui', 2)); put(sq(72, .1, .5), 34.07, .26, 0, .05)
for k, m in enumerate((62, 69, 74)): put(sq(m, .08, .125), 34.6 + k * .08, .26, .3, .05, ev=('ui', 3) if k == 0 else None)               # the lid
for k in range(7): put(sq(74 - 2 * k, .09, .125), 35.2 + k * .13, .2, -.3 + .1 * k, .05)                                                     # down
put(chh(.3), 36.0, .3, 0, .05, ev=('ui', 4)); put(sq(79, .07, .5), 37.2, .24, 0, .05); put(sq(72, .1, .5), 37.27, .24, 0, .05)
n = int(1.4 * SR); ph = np.cumsum(220 * 2 ** (np.linspace(0, 2.2, n))) / SR; put(np.where(ph % 1 < .5, 1.0, -1.0) * np.linspace(.2, 1, n) * .5, 38.6, .14, 0, .05, ev=('ui', 5)); put(sq(88, .06, .5), 38.6, .34, 0, .05); put(chh(.06), 38.6, .4, 0, 0)      # into the glass
# ================================================================== level 2: 1987, one voice and a mouse
for j in range(4):
    nm, vo = MINOR[j]; put(boop(ROOT[nm] + 12, 1.8), T(20 + j), .34, 0, .1, ev=('mac', ROOT[nm]))
    for m, d in T1[j][:2 if j != 3 else 1]: pass
tune([[T1[0][0], T1[0][2]], [T1[1][0], T1[1][2]], [T1[2][0], T1[2][2]], [T1[3][0]]], 20, boop, .3, .2, .12, name='mac', hold=1.6)      # only the notes that matter: (D . A), (G . C), (D . B flat), (A)
for t in (41.0, 43.0, 45.0, 46.0): put(V.click(), t, .6, .3, .05, ev=('mouse', 0)); put(V.click(), t + .07, .42, .3, .05)
for t in (41.0, 45.0): put(crush(riser(.4, 500, 3000), 6, 11025), t + .02, .26, 0, .05)                                                    # an iris opening
put(crush(V.nz(int(.4 * SR)) * np.linspace(1, 0, int(.4 * SR)), 4, 8000), 43.02, .12, 0, .05)                                                # a dissolve
n = int(2.0 * SR); put(crush(np.sin(2 * np.pi * np.cumsum(180 * 2 ** np.linspace(0, 2, n)) / SR) * np.linspace(.2, 1, n), 6, 11025), 46.0, .16, 0, .08)
# ================================================================== level 3: 1980, a beeper and the keys
for j in range(8):
    nm, _ = MINOR[j % 4]; put(beep(ROOT[nm] + 12, .16), T(24 + j), .26 if j < 4 else .15, 0, .04, ev=('beeper', ROOT[nm]))
for t0, kind, s in [(48.3, 'M', ''), (49.2, 'T', '>LIFT TRAPDOOR'), (50.3, 'M', ''), (50.6, 'T', '>DOWN'), (51.2, 'M', ''), (56.0, 'T', '>ASK WITCH FOR LIGHT'), (58.0, 'M', ''), (59.6, 'T', '>SAY PLEASE'), (62.4, 'T', '>LOOK AT WITCH')]:
    if kind == 'T': typing(s, t0, gain=.34)
    else: put(beep(84, .05), t0, .2, 0, .04, ev=('line', 0))
put(ticks(1.2), 48.2, .1, -.3, .05); put(ticks(2.2), 51.0, .1, -.3, .05); put(beep(60, .09), 51.0, .34, 0, .04, ev=('line', 2)); put(beep(48, .12), 51.09, .34, 0, .04)                                                                     # the picture drawing itself
put(buzz(), 61.0, .3, 0, .05, ev=('error', 0)); put(buzz(.3), 61.3, .3, 0, .05)                                                              # I DON'T KNOW THE WORD
put(beep(72, .08), 64.0, .42, 0, .04, ev=('line', 1)); put(beep(66, .14), 64.08, .42, 0, .04); put(beep(84, .05), 71.0, .3, .3, .04, ev=('line', 3))
# her: a chord that is not from the machine (54.0), and a pedal D that grows until she has decided
put(V.ding('hers'), 54.0, .5, 0, .6, ev=('her', 50)); put(V.timp(38, 1.2), 54.0, .4, 0, .4)
ped = V.pad([26, 38], 16.2, 'organ', 3.0, .05); put(ped * np.linspace(.25, 1, len(ped))[:, None], 54.0, .34, 0, .5)
put(V.ding('hers'), 66.0, .7, 0, .6, ev=('her', 50)); st = V.pad([62, 68, 74], 3.4, 'strings', 1.8, .04, trem=.8); put(st * np.linspace(.2, 1, len(st))[:, None], 66.0, .2, 0, .5)
for k in range(4): put(V.timp(38, .8), 66.0 + k, .3 + .12 * k, 0, .3, ev=('heart', 38)); put(V.timp(38, .5), 66.0 + k + .3, .18 + .08 * k, 0, .3)
# 69.5: nothing. 70.0: RETURN. The value is F.
put(V.click(), 70.0, .9, 0, .1, ev=('return', 0)); put(V.kick(), 70.0, 1.0, 0, .2); put(V.crash(2.2), 70.0, .34, 0, .5); put(V.timp(41, 1.4), 70.0, .7, 0, .4)
put(V.pad([41, 53, 60, 65, 69], 2.1, 'organ', .02, .3), 70.0, .3, 0, .5, ev=('organ', 65)); put(V.pad([65, 69, 72, 77, 81], 2.1, 'choir', .05, .3), 70.0, .34, 0, .6, ev=('choir', 77)); put(V.pad([53, 60, 65, 69], 2.1, 'strings', .05, .3), 70.0, .26, 0, .5)
for k, m in enumerate((65, 69, 72, 77, 81, 84, 89)): put(V.glass(m, 1.6), 70.0 + k * .125, .22, -.4 + .13 * k, .6)

# ================================================================== the way back: F major
for j in range(4):                                                  # bars 36-39, a machine joining each bar
    nm, vo = MAJOR[j]; b = 36 + j
    put(V.ding('sys'), T(b), .3, .3, .4, ev=('pop', j)); put(V.click(), T(b), .7, 0, .1); put(V.kick(), T(b), .5 + .12 * j, 0, .15); put(V.glass(89 + 0, .7), T(b), .2, -.3, .5)
    put(beep(ROOT[nm] + 12, .3), T(b), .22, -.2, .05, ev=('beeper', ROOT[nm]))
    if j >= 1: put(boop(ROOT[nm] + 12, 1.8), T(b), .3, .2, .1, ev=('mac', ROOT[nm]))
    if j >= 2:
        for e in range(8): put(sq(ROOT[nm] + (12 if e % 2 else 0), .2, .5), T(b, e * .5), .18, -.3, .04)
        for s in range(16): put(tri(vo[s % 4] + 12, .1), T(b, s * .25), .11, .4, .04)
        for e in range(8): put(chh(), T(b, e * .5), .13 if e % 2 else .07, .1, 0)
    if j >= 2: put(V.pad([ROOT[nm]] + vo, 2.1, 'strings', .4, .3), T(b), .14 + .08 * (j - 2), 0, .5)
    if j == 3:
        for s in range(16): put(V.snare(), T(b, s * .25), .1 + .028 * s, 0, .15)
        put(V.timp(36, 1.6), T(b), .4, 0, .3); put(riser(1.8, 500, 7000), T(b) + .2, .2, 0, .3)
        for e in range(8): put(V.harp(vo[(e * 3) % 4] + 12, .9), T(b, e * .5), .2, .3 - .08 * e, .4)
tune(TM[:1], 36, beep, .2, -.2, .05, name='beeper'); tune(TM[1:2], 37, beep, .16, -.2, .05); tune(TM[1:2], 37, boop, .3, .2, .1, name='mac', shift=-12)
tune(TM[2:3], 38, sq, .18, 0, .05, name='chip', duty=.25); tune(TM[2:3], 38, boop, .22, .2, .1, shift=-12)
tune(TM[3:4], 39, sq, .16, 0, .05, duty=.25); tune(TM[3:4], 39, V.whistle, .3, .25, .5, name='whistle'); tune(TM[3:4], 39, V.fiddle, .2, -.3, .4, shift=-12)

def band(b, nm, vo, fill=False):
    """A bar of everyone."""
    r = ROOT[nm]
    put(V.guitar(r, 1.0), T(b), .46, 0, .25, ev=('guitar', r)); put(V.bass(r, .95), T(b), .44, ev=('bass', r))
    for e in (2, 3, 4, 5, 6, 7): put(V.guitar(r, .24, palm=True), T(b, e * .5), .36, 0, .15)
    for e in range(8): put(V.bass(r, .24), T(b, e * .5), .26)
    for q in range(4): put(V.kick(), T(b, q), .9, ev=('kick', 36) if q == 0 else None); put(V.hat(), T(b, q), .1, .3); put(V.hat(), T(b, q + .5), .16, .3)
    for q in (1, 3): put(V.snare(), T(b, q), .62, 0, .2, ev=('snare', 38)); put(V.kick(), T(b, q + .5), .7)
    if fill:
        for s in range(8): put(V.snare(), T(b, 2 + s * .25), .3 + .05 * s, 0, .2); put(V.kick(), T(b, 2 + s * .25), .6)
    put(V.pad(vo + [m + 12 for m in vo[1:]], 2.0, 'choir', .05, .15), T(b), .2, 0, .5, ev=('choir', vo[3])); put(V.pad([r] + vo, 2.0, 'strings', .08, .15), T(b), .17, 0, .45); put(V.pad(vo, 2.0, 'organ', .03, .1), T(b), .08, 0, .4)
for j in range(4): band(40 + j, *MAJOR[j], fill=j == 3)             # bars 40-43
put(V.crash(), T(40), .4, 0, .4, ev=('pop', 4)); put(V.ding('sys'), T(40), .3, .3, .4); put(V.crash(), T(42), .28, 0, .4)
tune(TM, 40, V.lead, .34, -.3, .3, name='lead'); tune(TM, 40, V.whistle, .34, .25, .5, name='whistle'); tune(TM, 40, V.fiddle, .2, .4, .35, shift=-12)
put(V.ding('hers'), 82.0, .5, -.2, .6, ev=('her', 50)); put(V.click(), 82.0, .5, -.2, .1)                                                       # the shadow opens an eye
for t in (83.0, 83.3, 83.62): put(V.glass(96, .3), t, .2, .5, .4, ev=('tube', 0)); put(V.click(), t, .3, .5, .2)                               # the shop light catching
put(V.glass(96, .8), 84.0, .22, .5, .5); put(sd.hum(12.0, 60.0, .35), 84.0, .028, .3, .1)
for j in range(2): band(44 + j, *MAJOR[j], fill=j == 1)             # bars 44-45: the answer, and the windows
put(V.crash(), T(44), .36, 0, .4); tune(TM2[:2], 44, V.lead, .34, -.3, .3, name='lead'); tune(TM2[:2], 44, V.whistle, .34, .25, .5, name='whistle')
for k, m in enumerate((81, 84, 86, 89, 91, 93, 96)): put(V.glass(m, 1.8), 90.0 + k * .25, .34, -.5 + .16 * k, .6, ev=('window', m)); put(V.harp(m - 12, 1.2), 90.0 + k * .25, .24, -.5 + .16 * k, .5); put(V.click(), 90.0 + k * .25, .3, -.5 + .16 * k, .2)
# bar 46: the last chord; bar 47: the music box, alone
put(V.guitar(41, 3.2), T(46), .5, 0, .3, ev=('guitar', 41)); put(V.bass(41, 3.0), T(46), .46, ev=('bass', 41)); put(V.kick(), T(46), 1.0, ev=('kick', 36)); put(V.crash(2.6), T(46), .42, 0, .5); put(V.timp(41, 2.0), T(46), .7, 0, .4)
put(V.pad([53, 60, 65, 69, 72, 77], 3.6, 'choir', .05, 1.6), T(46), .26, 0, .6, ev=('choir', 77)); put(V.pad([41, 53, 60, 65, 69], 3.6, 'strings', .05, 1.6), T(46), .2, 0, .5); put(V.pad([53, 60, 65], 3.4, 'organ', .03, 1.4), T(46), .1, 0, .4)
for (m, d), t in zip(TM[0], (93.0, 93.6, 94.2)): put(V.glass(m, 2.4), t, .34, -.2, .6, ev=('box', m))

ride = [(0, -3), (5, -3), (8, -4), (16, -4), (24, -4), (30, -3), (32, -1), (32.05, 5), (40, 5), (40.05, 7), (48, 7), (48.05, -1), (54, 0), (64, 0), (66, -4), (69.45, -3), (69.5, -40), (69.97, -40), (70, 0), (72, -1), (72.05, 3), (76, 2), (79, 0), (80, .5), (92, .5), (93, -1), (96, -3)]
out = Path('out/hex'); out.mkdir(parents=True, exist_ok=True)
x = V.finish(ride, out / 'basecase.wav')
json.dump(dict(bar=BAR, bars=BARS, events=sorted(V.EVENTS)), open(HERE / 'events.json', 'w'), separators=(',', ':'))
m = ear.measure(x); print({k: round(v, 2) for k, v in m.items() if isinstance(v, float)}); print(len(V.EVENTS), 'events;', sorted({e[2] for e in V.EVENTS}))
for name, a, b in (('outside', 0, 4), ('pantry', 4, 8), ('basement', 8, 12), ('desk', 12, 16), ('1989', 16, 20), ('1987', 20, 24), ('1980', 24, 28), ('parser', 28, 32), ('decision', 32, 35), ('RETURN', 35, 36), ('way back', 36, 40), ('everyone', 40, 44), ('windows', 44, 46), ('last', 46, 48)):
    seg = x[int(a * BAR * SR):int(b * BAR * SR)]; print(f'  {name:<10} rms {20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-9):6.1f} dB')
ear.report(str(out / 'basecase.wav'), str(HERE / 'basecase_score.jpg'), title='BASE CASE: 48 bars of 4/4, two seconds a bar; a ground stated twelve times')
sd.encode(str(out / 'basecase.wav'), str(HERE / 'basecase.mp3'))
