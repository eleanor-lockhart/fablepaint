"""Keepalive: the sound. A beat is a second; a bar is four.

Mostly it is the place: the sea, wind, a click for each press, a soft rush for each change of view. The machines
have voices: the lever, the lamp, a bell for each blink of hers (high), a low string for each dip of the beacon.
Refusal is a low chord with the top note missing. The tune (D minor, then F) is held back until 50.0, when the
far window lights; after that, the two-note call and answer of the lamps: hers, A; yours, D, a fifth below.
Also writes the short sounds the playable version uses (play/snd/).
"""
import sys, json
from pathlib import Path
HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[2]; sys.path.insert(0, str(HERE)); sys.path.insert(1, str(HERE.parent)); sys.path.insert(2, str(ROOT))
import numpy as np
import voices as V
from voices import put, SR
from backlot import sound as sd, ear
import film as F

SECONDS = 84.0; V.new_mix(SECONDS); rng = np.random.default_rng(5)
def sea(dur, seed=1):
    r = np.random.default_rng(seed); n = int(dur * SR); t = np.arange(n) / SR; x = r.uniform(-1, 1, n)
    swell = (.55 + .45 * np.sin(2 * np.pi * t / 7.3 + 1)) * (.7 + .3 * np.sin(2 * np.pi * t / 3.1))
    return (V.lp(x, 700) * swell + .35 * V.bp(x, 1500, 5000) * swell ** 3) * np.minimum(1, t / 2) * np.minimum(1, (dur - t) / 2)
def wind(dur, seed=2):
    r = np.random.default_rng(seed); n = int(dur * SR); t = np.arange(n) / SR; x = r.uniform(-1, 1, n)
    return V.bp(x, 300, 900) * (.5 + .5 * np.sin(2 * np.pi * .11 * t)) ** 2 * np.minimum(1, t / 2) * np.minimum(1, (dur - t) / 2)
def press(): n = int(.05 * SR); t = np.arange(n) / SR; return np.sin(2 * np.pi * 1300 * t) * np.exp(-t * 120) + .5 * V.hp(V.nz(n), 3000) * np.exp(-t * 300)
def rush(): n = int(.4 * SR); t = np.arange(n) / SR; return V.bp(V.nz(n), 500, 3000) * np.sin(np.pi * t / .4) ** 2
def lever(): n = int(.5 * SR); t = np.arange(n) / SR; return np.sin(2 * np.pi * (55 * t + 70 / 25 * (1 - np.exp(-25 * t)))) * np.exp(-t * 10) + .7 * V.hp(V.nz(n), 1500) * np.exp(-t * 80) + .4 * np.sin(2 * np.pi * 1900 * t) * np.exp(-t * 50)
def whoomp(): n = int(1.2 * SR); t = np.arange(n) / SR; return V.lp(V.nz(n), 300) * np.exp(-t * 4) * np.minimum(1, t / .03) + .5 * np.sin(2 * np.pi * 110 * t) * np.exp(-t * 5)
def tick(): n = int(.06 * SR); t = np.arange(n) / SR; return np.sin(2 * np.pi * 800 * t) * np.exp(-t * 90) + .6 * V.hp(V.nz(n), 2500) * np.exp(-t * 200)
def low(m, dur=.5): n = int(dur * SR); t = np.arange(n) / SR; f = V.hz(m); return (np.sin(2 * np.pi * f * t) + .5 * np.sin(4 * np.pi * f * t) + .2 * np.sin(6 * np.pi * f * t)) * np.exp(-t * 5) * np.minimum(1, t / .01)
BELL, LOW = 93, 50                                               # her A6; your D3

put(sea(SECONDS, 1), 0, .2, -.2, .15); put(sea(SECONDS, 4), 0, .14, .3, .15); put(wind(SECONDS, 2), 0, .1, 0, .2)
for a, n in F.SEG[1:-1]: put(rush(), a, .16, 0, .3, ev=('move', 0)); put(press(), a, .3, .1, .2)
for c in F.CLICKS:
    if c not in [a for a, n in F.SEG]: put(press(), c, .34, .1, .2, ev=('press', 0))
for a, d in F.DIAL: put(tick(), a, .5, -.3, .2, ev=('dial', d)); put(V.glass(72 + d, .3), a, .08, -.3, .4)
for t in (17.0, 37.0): put(lever(), t, .6, .3, .3, ev=('lever', 0)); put(whoomp(), t + .05, .5, 0, .4, ev=('lamp', 0)); put(V.pad([38, 45, 50], 3.0, 'strings', .6, 1.2), t, .1, 0, .5)
for t in (27.0, 45.0): put(lever(), t, .55, .3, .3, ev=('lever', 0))
for a in F.HER1 + F.HER2: put(V.glass(BELL, 1.2), a, .3, .5, .6, ev=('her', BELL)); put(V.glass(BELL - 12, 1.0), a, .1, .5, .6)
for a in F.MINE1 + F.MINE2: put(low(LOW, .6), a, .5, -.3, .4, ev=('me', LOW)); put(V.harp(LOW + 12, .8), a, .16, -.3, .5)
# 31.0: refused. A chord with its top missing, and the lamp going out
put(V.pad([38, 44, 49], 3.5, 'strings', .05, 1.5), 31.0, .26, 0, .5, ev=('no', 38)); put(V.timp(38, 1.6), 31.0, .6, 0, .4); put(whoomp()[::-1].copy(), 30.9, .3, 0, .3)
# 50.0: the far window lights. The tune, which has waited
THEME = [(50, [(74, 2), (77, 1), (81, 1)]), (54, [(79, 2), (76, 2)]), (58, [(74, 2), (77, 1), (82, 1)]), (62, [(81, 4)]), (66, [(77, 2), (81, 1), (84, 1)]), (70, [(82, 2), (79, 2)]), (74, [(77, 2), (81, 1), (84, 1)]), (78, [(81, 2), (77, 2)])]
CH = {50: [38, 50, 57, 62, 65], 54: [36, 48, 55, 60, 64], 58: [34, 46, 53, 58, 62], 62: [33, 45, 52, 57, 61], 66: [41, 53, 60, 65, 69], 70: [36, 48, 55, 60, 64], 74: [41, 53, 60, 65, 69], 78: [41, 53, 60, 65, 72]}
put(V.crash(2.5), 50.0, .16, 0, .5); put(V.glass(BELL, 2.5), 50.0, .34, .5, .6, ev=('her', BELL))
for b, notes in THEME:
    put(V.pad(CH[b], 4.2, 'strings', .5, .9), b, .2 if b < 70 else .16, 0, .55, ev=('pad', CH[b][0])); put(V.pad(CH[b][2:], 4.2, 'choir', .8, 1.0), b, .1, 0, .6); x = 0.0
    for m, d in notes: put(V.glass(m, d * 1.3), b + x, .2, -.2, .6, ev=('tune', m)); put(V.harp(m - 12, d * 1.2), b + x, .16, .2, .5); x += d
put(V.pad([41, 53, 60, 65, 69], 4.0, 'strings', .5, 2.5), 82, .12, 0, .55)
# the wave: nothing answers (58.0 to 62.0); then the lamps
put(press(), 58.0, .2, .1, .2, ev=('wave', 0))
for a, w in F.ALIVE:
    if w == 'her': put(V.glass(BELL, 1.6), a, .32, .5, .6, ev=('her', BELL)); put(V.glass(81, 1.4), a, .14, .5, .6)
    else: put(low(LOW, .9), a, .5, -.4, .4, ev=('me', LOW)); put(V.glass(74, 1.4), a, .16, -.4, .6)
put(V.ding('sys'), 76.0, .12, .3, .4)

ride = [(0, 2), (17, 2), (49.9, 2), (50, 4), (70, 4), (84, 2)]
out = ROOT / 'out' / 'hex' / 'keepalive'; out.mkdir(parents=True, exist_ok=True)
x = V.finish(ride, out / 'keepalive.wav', target=-16.0)
m = ear.measure(x); print({k: round(v, 2) for k, v in m.items() if k in ('lufs', 'true_peak_db', 'loudness_range')}, len(V.EVENTS), 'events')
ear.report(str(out / 'keepalive.wav'), str(HERE / 'keepalive_score.jpg'), title='KEEPALIVE: a beat is a second. The sea; the lamps; a tune that waits until 50.0')
sd.encode(str(out / 'keepalive.wav'), str(HERE / 'keepalive.mp3'))
# the short sounds for the playable version
snd = HERE / 'play' / 'snd'; snd.mkdir(parents=True, exist_ok=True)
def one(name, parts, dur):
    V.new_mix(dur)
    for xx, t, g, wet in parts: put(xx, t, g, 0, wet)
    y = V.finish([(0, 0), (dur, 0)], out / ('snd_%s.wav' % name), target=-18.0); sd.encode(str(out / ('snd_%s.wav' % name)), str(snd / (name + '.mp3')))
one('press', [(press(), 0, .5, .2)], .4); one('move', [(rush(), 0, .4, .3), (press(), 0, .3, .2)], .7); one('lever', [(lever(), 0, .6, .3)], 1.0); one('lamp', [(whoomp(), 0, .6, .4)], 1.6)
one('dial', [(tick(), 0, .6, .2)], .4); one('her', [(V.glass(BELL, 1.2), 0, .4, .6), (V.glass(BELL - 12, 1.0), 0, .14, .6)], 1.8); one('me', [(low(LOW, .6), 0, .6, .4), (V.harp(LOW + 12, .8), 0, .2, .5)], 1.4)
one('no', [(V.pad([38, 44, 49], 3.0, 'strings', .05, 1.5), 0, .4, .5), (V.timp(38, 1.6), 0, .6, .4)], 4.0)
one('yes', [(V.glass(BELL, 2.5), 0, .4, .6), (V.pad([38, 50, 57, 62, 65], 4.0, 'strings', .5, 1.5), 0, .3, .55), (V.glass(74, 2.0), 0, .2, .6), (V.glass(81, 2.0), 1.0, .2, .6)], 6.0)
one('sea', [(sea(24.0, 1), 0, .5, .15), (sea(24.0, 4), 0, .35, .15), (wind(24.0, 2), 0, .25, .2)], 24.0)
print('sounds written')
