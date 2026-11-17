"""Persistence: the score. One beat is half a second from beginning to end.

    0-36     a waltz (three beats; a bar is 1.5 s): a music box far off, then silence in the dark shed, then at 12.0
             the band organ, complete. At 27.0 the lights go out and it stops dead. Under the lamp: 24 ticks a second.
    36-60    a galop (four beats; a bar is 2 s): Dm, B flat, F, C, three times, each time with more of the band. The
             hooves are where the plate puts them: four in a beat, then air.
    60-72    the waltz again on one pipe, the organ when the lights come back, and the music box, alone, last.

The ride makes a sound of its own: a flutter, once for every horse that passes. At six turns a minute it is
1.2 a second; locked, it is 24 a second, which is a note (the G below the bass stave, near enough).
"""
import sys, json, math
from pathlib import Path
HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[2]; sys.path.insert(0, str(HERE)); sys.path.insert(1, str(HERE.parent)); sys.path.insert(2, str(ROOT))
import numpy as np
from scipy import signal
import voices as V
from voices import put, SR
from backlot import sound as sd, ear

SECONDS = 72.0; Q = .5; FPS = 24
V.new_mix(SECONDS); rng = np.random.default_rng(7)
def omega(t):                                                    # the same curve the picture turns by (film.py)
    e = lambda u: (lambda u: u * u * (3 - 2 * u))(min(max(u, 0.0), 1.0))
    if t < 12: return 0.0
    if t < 14: return 1.5 * e((t - 12) / 2)
    if t < 28.5: return 1.5
    if t < 30: return 1.5 + 2.5 * e((t - 28.5) / 1.5)
    if t < 32.5: return 4 + 22 * (t - 30) / 2.5
    if t < 36: return 30 - 4 * (1 - (t - 32.5) / 3.5) ** 2
    if t < 60: return 30.0
    if t < 62: return 30 - 3 * ((t - 60) / 2) ** 2
    if t < 64: return 27 - 25.5 * e((t - 62) / 2)
    if t < 66: return 1.5 * (1 - e((t - 64) / 2))
    return 0.0

# ------------------------------------------------------------------ voices this piece adds
def pipe(m, dur, bright=.5):
    """An organ pipe: a few harmonics, a chiff at the front, a tremulant."""
    n = int(dur * SR); t = np.arange(n) / SR; f = V.hz(m); x = np.sin(2 * np.pi * f * t) + bright * np.sin(4 * np.pi * f * t) + .3 * bright * np.sin(6 * np.pi * f * t) + .12 * np.sin(8 * np.pi * f * t)
    x = x * (1 + .06 * np.sin(2 * np.pi * 6.2 * t)) + .5 * V.bp(V.nz(n), f * 2, f * 6) * np.exp(-t * 60)
    return x * V.env(n, .012, .05) * .5
def hoof(acc=False): n = int(.07 * SR); t = np.arange(n) / SR; return (np.sin(2 * np.pi * (150 if acc else 190) * t) * np.exp(-t * 55) + .8 * V.bp(V.nz(n), 900, 3200) * np.exp(-t * 140)) * (1.0 if acc else .8)
def crunch(): n = int(.12 * SR); t = np.arange(n) / SR; return V.bp(V.nz(n), 500, 4200) * np.exp(-t * 28) * (.6 + .4 * rng.random())
def tread(): n = int(.1 * SR); t = np.arange(n) / SR; return np.sin(2 * np.pi * 110 * t) * np.exp(-t * 45) + .4 * V.bp(V.nz(n), 400, 1800) * np.exp(-t * 60)
def clack(): n = int(.25 * SR); t = np.arange(n) / SR; return np.sin(2 * np.pi * (60 * t + 80 / 30 * (1 - np.exp(-30 * t)))) * np.exp(-t * 14) + .9 * V.hp(V.nz(n), 1800) * np.exp(-t * 90) + .5 * np.sin(2 * np.pi * 2300 * t) * np.exp(-t * 70)
def wind(dur, seed=1):
    r = np.random.default_rng(seed); n = int(dur * SR); t = np.arange(n) / SR; x = r.uniform(-1, 1, n)
    a = V.bp(x, 300, 900) * (.6 + .4 * np.sin(2 * np.pi * .13 * t + 1)) + .6 * V.bp(x, 900, 2200) * (.5 + .5 * np.sin(2 * np.pi * .21 * t)) ** 2
    return a * np.minimum(1, t / 1.2) * np.minimum(1, (dur - t) / 1.2)
def creak(dur=1.2):
    n = int(dur * SR); t = np.arange(n) / SR; f = 420 + 160 * np.sin(2 * np.pi * 2.3 * t); ph = np.cumsum(f) / SR
    return V.bp(np.sign(np.sin(2 * np.pi * ph)), 700, 2600) * np.minimum(1, t / .05) * np.minimum(1, (dur - t) / .1) * (.5 + .5 * np.sin(2 * np.pi * 2.3 * t)) ** 2 * .5
def flutter(t0, t1):
    """The ride's own sound: a puff of air for every horse that passes any one place."""
    n = int((t1 - t0) * SR); tt = t0 + np.arange(n) / SR; rate = np.array([omega(float(t)) for t in tt[::441]]) * FPS / 30.0; rate = np.interp(np.arange(n), np.arange(len(rate)) * 441, rate)
    ph = np.cumsum(rate) / SR; puff = np.clip(np.cos(2 * np.pi * ph), 0, 1) ** 6
    return V.bp(V.nz(n), 180, 1400) * puff * np.minimum(1, rate / 3.0 + .25) + .5 * np.sin(2 * np.pi * ph) * np.clip((rate - 14) / 10, 0, 1)
def riser(dur, lo=300, hi=6000):
    n = int(dur * SR); t = np.arange(n) / SR; x = V.nz(n); out = np.zeros(n); k = 8
    for i in range(k):
        a, b = int(i * n / k), int((i + 1) * n / k); fc = lo * (hi / lo) ** ((i + .5) / k); out[a:b] = V.bp(x[a:b], fc * .7, fc * 1.4)
    return out * (t / dur) ** 2
def ticks(dur, rate=24.0): n = int(dur * SR); x = np.zeros(n); x[(np.arange(int(dur * rate)) * SR / rate).astype(int)] = 1; return V.bp(signal.lfilter(np.ones(30) / 5, 1, x), 1500, 6000)

# ------------------------------------------------------------------ the tunes
WA = [('F', [(72, 1), (77, 1), (81, 1)]), ('F', [(84, 2), (81, 1)]), ('C7', [(82, 1), (79, 1), (76, 1)]), ('C7', [(79, 3)]),
      ('C7', [(72, 1), (76, 1), (79, 1)]), ('C7', [(82, 2), (79, 1)]), ('F', [(81, 1), (77, 1), (72, 1)]), ('F', [(77, 3)])]
WB = [('Bb', [(86, 1), (82, 1), (77, 1)]), ('Bb', [(86, 2), (82, 1)]), ('F', [(84, 1), (81, 1), (77, 1)]), ('F', [(84, 3)]),
      ('C7', [(82, 1), (79, 1), (76, 1)]), ('C7', [(84, 2), (82, 1)]), ('F', [(81, 1), (84, 1), (81, 1)]), ('F', [(77, 3)])]
CH = dict(F=(41, [60, 65, 69]), C7=(36, [58, 64, 67]), Bb=(34, [58, 62, 65]), Dm=(38, [57, 62, 65]), C=(36, [55, 60, 64]))
def waltz(bars, t0, full=True, gain=1.0, box=False, mel=True):
    for j, (ch, notes) in enumerate(bars):
        t = t0 + j * 3 * Q; b = 0.0; root, tri = CH[ch]
        for m, d in notes:
            if box: put(V.glass(m, 1.6), t + b * Q, .2 * gain, -.2, .7, ev=('box', m))
            elif mel:
                put(pipe(m, d * Q * .92, .6), t + b * Q, .2 * gain, -.15, .3, ev=('pipe', m)); put(pipe(m + 12, d * Q * .92, .3), t + b * Q, .07 * gain, .2, .3)
                if full: put(V.glass(m + 12, .5), t + b * Q, .1 * gain, .3, .4)
            b += d
        if full and not box:
            put(pipe(root, Q * .9, .9), t, .3 * gain, 0, .2, ev=('oom', root)); put(V.kick(), t, .5 * gain)
            for k in (1, 2):
                for m in tri: put(pipe(m, Q * .45, .4), t + k * Q, .1 * gain, .25, .25)
                put(V.snare(), t + k * Q, .12 * gain, .2, .2)

# 0-6: outside. Wind, his steps in the snow on the beat, the tune far off on a music box
put(wind(7.5, 1), 0.0, .22, 0, .2); put(V.ding('sys'), 1.0, .22, .3, .4, ev=('type', 0)); waltz(WA[:4], 0.0, box=True, gain=.6)
for k in range(10): put(crunch(), k * Q, .42, -.3 + .05 * k, .1, ev=('step', 0))
put(creak(.9), 5.0, .2, .1, .3); put(V.lp(V.nz(int(.9 * SR)), 180) * np.hanning(int(.9 * SR)), 5.0, .5, .1, .2, ev=('door', 0))             # the door, slid open
# 6-12: inside, dark. A door, three steps, the lamp, two steps, his hand on the switch
put(clack(), 6.0, .3, .3, .3, ev=('door', 0)); put(creak(.9), 6.0, .16, .3, .3); put(sd.hum(6.0, 50.0, .3), 6.0, .02, 0, .1)
for t in (6.0, 6.5, 7.0, 9.5, 10.0): put(tread(), t, .42, .2, .3, ev=('step', 0))
put(V.pad([38, 45], 6.0, 'strings', 1.5, .6), 6.0, .1, 0, .5)
for t, m in ((7.5, 69), (8.5, 65), (9.5, 62)): put(V.glass(m, 2.0), t, .1, -.3, .7)
# 12-24: the lights and the organ. The waltz, complete: first strain 12-24
put(clack(), 12.0, .6, .3, .3, ev=('switch', 0)); put(V.crash(1.6), 12.0, .3, 0, .4); put(V.ding('sys'), 12.0, .3, .3, .4)
waltz(WA, 12.0, full=True); put(V.crash(1.0), 18.0, .2, 0, .4, ev=('cut', 0)); put(flutter(12.0, 66.5), 12.0, .16, 0, .15)
# a bell for every numbered horse that goes by the lens, 18-24 (one every twenty frames)
th = np.cumsum([omega(i / FPS) for i in range(int(36 * FPS))]); th = th - th[-1]
for i in range(18 * FPS, 24 * FPS):
    if math.floor((th[i] + 30) / 30) != math.floor((th[i - 1] + 30) / 30): put(V.glass(96, .5), i / FPS, .16, .4, .5, ev=('pass', 96))
# 24-27: the organ thins to one pipe (second strain, two bars); the stroboscope is wheeled up
waltz(WB[:2], 24.0, full=False, gain=.8); put(V.crash(.8), 24.0, .12, 0, .3, ev=('cut', 0))
for t in (24.1, 24.9, 25.6): put(creak(.6), t, .2, .5, .2)
# 27.0: lights out. The organ stops dead; the lamp ticks, 24 a second, until 63.0
put(clack(), 27.0, .65, .3, .3, ev=('switch', 0)); put(ticks(35.875), 27.125, .05, .4, .05); put(V.click(), 27.125, .3, .4, .1); put(V.pad([38, 50], 9.0, 'strings', 2.0, .4), 27.0, .12, 0, .5)
# 28.5-30: the regulator, six notches
for k in range(6): put(V.click(), 28.5 + k * .25, .45, .3, .2, ev=('lever', 0) if k == 0 else None); put(tread(), 28.5 + k * .25, .2, .3, .2)
# 30-36: faster. A rise; a drum that cannot keep up; the waltz's first three notes, climbing
put(riser(6.0), 30.0, .34, 0, .3); put(V.timp(38, 1.0), 30.0, .7, 0, .4, ev=('cut', 0)); put(V.crash(1.0), 30.0, .3, 0, .4)
tt = 30.0; gap = .5
while tt < 35.95: put(V.kick(), tt, .35 + .5 * (tt - 30) / 6); put(V.snare(), tt, .08 + .3 * (tt - 30) / 6, 0, .2); gap = max(gap * .9, 1 / 24); tt += gap
for k, t in enumerate((30.0, 31.5, 33.0, 34.5)):
    for j, m in enumerate((72, 77, 81)): put(pipe(m + 2 * k, .4, .7), t + j * Q, .16 + .03 * k, -.2 + .1 * k, .4)
put(V.timp(38, 1.2), 33.0, .5, 0, .4)
# 36-60: locked. The galop
GAL = ['Dm', 'Bb', 'F', 'C']; GROOT = dict(Dm=38, Bb=34, F=41, C=36); GTRI = dict(Dm=[62, 65, 69, 74], Bb=[58, 62, 65, 70], F=[60, 65, 69, 72], C=[60, 64, 67, 72])
ARP = dict(Dm=[74, 77, 81, 86, 81, 77, 81, 86], Bb=[82, 86, 89, 86, 82, 77, 82, 86], F=[81, 84, 89, 84, 81, 77, 81, 84], C=[79, 84, 88, 84, 79, 76, 79, 84])
THEME = [[(74, 1.5), (77, .5), (81, 2)], [(82, 1.5), (81, .5), (77, 2)], [(81, 1.5), (84, .5), (89, 2)], [(88, 1.5), (86, .5), (84, 1), (79, 1)]]
ANSWER = [[(86, 1.5), (84, .5), (81, 2)], [(82, 1.5), (86, .5), (89, 2)], [(89, 1), (88, 1), (84, 1), (81, 1)], [(84, 1), (88, 1), (91, 2)]]
HOOF = (2, 4, 5, 8)                                              # frames after the beat at which a foot comes down (off the plate)
def gbar(b, nm, level):
    t = 36.0 + b * 2.0; r = GROOT[nm]; vo = GTRI[nm]
    put(V.guitar(r, .45), t, .42, 0, .25, ev=('guitar', r)); put(V.bass(r, .45), t, .42, ev=('bass', r))
    for q in range(4):
        for k, (o, g) in enumerate(((0, 1.0), (.25, .7), (.375, .8))):          # the gallop: long, short, short
            if q or k: put(V.guitar(r, .11, palm=True), t + q * Q + o, .34 * g, -.1, .15)
            put(V.bass(r, .11), t + q * Q + o, .26 * g); put(V.kick(), t + q * Q + o, .8 * g if k == 0 else .5 * g, ev=('kick', 36) if (q == 0 and k == 0) else None)
        if q in (1, 3): put(V.snare(), t + q * Q, .6, 0, .2, ev=('snare', 38))
        put(V.hat(), t + q * Q, .12, .3); put(V.hat(), t + q * Q + .25, .1, .3)
        for k, f in enumerate(HOOF): put(hoof(k == 3), t + q * Q + f / FPS, .36, -.3 + .2 * k, .15, ev=('hoof', k))
    if level >= 1: put(V.pad(vo + [m + 12 for m in vo[1:]], 2.0, 'choir', .05, .15), t, .2, 0, .5, ev=('choir', vo[3])); put(V.pad([r] + vo, 2.0, 'strings', .08, .15), t, .17, 0, .45)
    if level >= 2: put(V.pad(vo, 2.0, 'organ', .03, .1), t, .1, 0, .4)
    for q in range(4): put(V.guitar(r + 12 if level else r, .22, palm=level == 0), t + q * Q + .25, .0 if level == 0 else .14, .2, .2)
def line(notes, t, voice, gain, pan=0.0, wet=.3, shift=0, name=None):
    b = 0.0
    for m, d in notes: put(voice(m + shift, d * Q * .95), t + b * Q, gain, pan, wet, ev=(name, m + shift) if name else None); b += d
for b in range(12):
    nm = GAL[b % 4]; lv = b // 4; gbar(b, nm, lv); t = 36.0 + b * 2.0
    if lv == 0:
        for k, m in enumerate(ARP[nm]): put(V.lead(m, .24), t + k * .25, .26, -.3, .3, ev=('lead', m))
    elif lv == 1: line(THEME[b % 4], t, V.lead, .32, -.3, .3, name='lead'); line(THEME[b % 4], t, V.whistle, .32, .25, .5, name='whistle')
    else:
        line(ANSWER[b % 4], t, V.lead, .32, -.3, .3, name='lead'); line(ANSWER[b % 4], t, V.whistle, .32, .25, .5, name='whistle'); line(ANSWER[b % 4], t, V.fiddle, .18, .4, .35, shift=-12)
        line(ANSWER[b % 4], t, lambda m, d: pipe(m, d, .6), .14, 0, .4, shift=-12)
for t, g in ((36.0, .46), (40.0, .22), (44.0, .4), (48.0, .24), (52.0, .42), (56.0, .26)): put(V.crash(1.8), t, g, 0, .4, ev=('crash', 0)); put(V.timp(38, 1.0), t, .5, 0, .4)
put(V.ding('sys'), 36.0, .3, .3, .4)
# 60-66: the regulator closed. A held F, the waltz on one pipe (second strain, bars 5-8), the organ at 63.0, the end of the tune
put(V.pad([41, 53, 60, 65, 69], 3.2, 'strings', .05, 2.2), 60.0, .26, 0, .5); put(V.pad([53, 60, 65, 69, 72], 3.0, 'choir', .05, 2.0), 60.0, .2, 0, .6); put(V.timp(41, 2.0), 60.0, .6, 0, .4, ev=('close', 0)); put(V.crash(2.4), 60.0, .3, 0, .5)
for k in range(6): put(V.click(), 60.0 + k * .25, .4, .3, .2)
waltz(WB[4:6], 60.0, full=False, gain=.8); waltz(WB[6:8], 63.0, full=True, gain=.95)
put(clack(), 63.0, .6, .3, .3, ev=('switch', 0)); put(V.crash(1.2), 63.0, .2, 0, .4)
# 66-72: outside. Wind, his steps, the music box
put(wind(6.4, 3), 65.6, .22, 0, .2); put(clack(), 66.0, .3, .3, .3, ev=('door', 0))
put(creak(.9), 66.0, .2, .1, .3); put(V.lp(V.nz(int(.9 * SR)), 180) * np.hanning(int(.9 * SR)), 66.0, .5, .1, .2)                                 # and shut
for k in range(10): put(crunch(), 67.0 + k * Q, .4, .3 - .05 * k, .1, ev=('step', 0))
for m, t in ((81, 69.0), (77, 69.5), (72, 70.0)): put(V.glass(m, 2.2), t, .3, -.2, .6, ev=('box', m))
put(V.glass(77, 3.0), 70.5, .36, 0, .7, ev=('box', 77)); put(V.glass(65, 3.0), 70.5, .2, 0, .7); put(V.ding('sys'), 69.0, .14, .3, .4)

ride = [(0, 1), (6, 1), (6.05, 2), (12, 2), (12.05, 4.5), (24, 4.5), (27, 4), (27.05, 2), (30, 0), (35.9, 1), (36, 5), (44, 5), (44.05, 3), (60, 3), (60.1, 0), (63, 1), (63.05, 5.5), (66, 5.5), (66.1, 0), (72, 0)]
out = ROOT / 'out' / 'hex' / 'persistence'; out.mkdir(parents=True, exist_ok=True)
x = V.finish(ride, out / 'persistence.wav')
json.dump(dict(beat=Q, events=sorted(V.EVENTS)), open(HERE / 'events.json', 'w'), separators=(',', ':'))
m = ear.measure(x); print({k: round(v, 2) for k, v in m.items() if isinstance(v, float)}); print(len(V.EVENTS), 'events;', sorted({e[2] for e in V.EVENTS}))
for name, a, b in (('outside', 0, 6), ('dark', 6, 12), ('organ', 12, 24), ('one pipe', 24, 27), ('lamp', 27, 30), ('faster', 30, 36), ('galop 1', 36, 44), ('galop 2', 44, 52), ('galop 3', 52, 60), ('closing', 60, 63), ('organ', 63, 66), ('outside', 66, 72)):
    seg = x[int(a * SR):int(b * SR)]; print(f'  {name:<10} rms {20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-9):6.1f} dB')
ear.report(str(out / 'persistence.wav'), str(HERE / 'persistence_score.jpg'), title='PERSISTENCE: a beat is half a second. A waltz, a galop, the waltz')
sd.encode(str(out / 'persistence.wav'), str(HERE / 'persistence.mp3'))
