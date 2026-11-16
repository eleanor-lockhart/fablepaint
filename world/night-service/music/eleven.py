"""Eleven: No. 4's cue. Mains hum; the cable is cut; silence; then the machine works something out, in bars of
eleven, using only the harmonics of the 60 Hz it runs on (it can only make music out of what powers it).
It learns one note a bar. On the eleventh bar the hum comes back and takes the notes away mid-phrase.

    uv run python world/night-service/music/eleven.py"""
import json
from pathlib import Path
import numpy as np
from backlot import sound as sd, score as sc, ear

HERE = Path(__file__).resolve().parent
T0 = 7.5                                         # hum for six seconds, a second and a half of nothing, then bar 1
s = sc.Seq(bpm=132, beats=11, seed=7)            # a beat is an eighth note: a bar of eleven lasts five seconds
H = lambda n: sc.harmonic(n, 60.0)
# (beat, harmonic) per bar: grouped 3 + 3 + 3 + 2, accents on 1, 4, 7, 10
BARS = [[(1, 8)],
        [(1, 8), (4, 9)],
        [(1, 8), (4, 9), (7, 10)],
        [(1, 8), (4, 9), (7, 10), (10, 12)],
        [(1, 8), (3, 9), (4, 10), (7, 12), (9, 11), (10, 9)],
        [(1, 8), (3, 9), (4, 10), (6, 12), (7, 13), (9, 12), (10, 10)],
        [(1, 12), (7, 9)],                                                   # it stops, and looks at the light
        [(1, 8), (3, 9), (4, 10), (6, 12), (7, 13), (9, 12), (10, 10), (11, 9)],
        [(1, 8), (2, 9), (3, 10), (4, 12), (6, 13), (7, 14), (9, 12), (10, 10), (11, 9)],
        [(1, 8), (2, 9), (3, 10), (4, 12), (5, 13), (6, 14), (7, 16), (9, 14), (10, 12), (11, 10)],      # the top: it waves
        [(1, 8), (4, 9), (7, 10)]]
for b, bar in enumerate(BARS, 1):
    for beat, n in bar:
        long = 9 if b == 7 else 3
        s.note('voice', None, b, beat, long, vel=.55 + (.14 if beat in (1, 4, 7, 10) else 0) + .012 * b, hz_=H(n))
    if b >= 3: s.note('body', None, b, 1, 8, vel=.8, hz_=H(2))
    if b >= 6: s.note('body', None, b, 7, 5, vel=.6, hz_=H(3))
s.humanize(ms=14, vel=.08, tracks=('voice',))
END = T0 + 11 * 5.0                              # the bar line where it is cut off
DUR = END + 4.0
m = sd.Mix(DUR, t60=5.5, damp=.45, seed=3)
for e in s.ev: e['t'] += T0
s.render(m, {'voice': dict(inst=lambda f, d, v: sd.bell(f, d + 3, t60=3.2, bright=.5, third=.0), gain=-12, send=-6, spread=.25),
             'body': dict(inst=lambda f, d, v: sd.highpass(sd.bell(f, d + 3, t60=4.5, bright=.5, third=.3), 85), gain=-18, send=-8)})
m.add(sd.highpass(sd.sea(DUR, period=7.0, seed=11), 90), at=6.3, gain=-30, send=-14)
music = m.render(wet=-5.0)
gate = np.ones(len(music)); i = sd._n(END)
gate[i:] = 0; gate[i - sd._n(.02):i] = np.linspace(1, 0, sd._n(.02))            # taken away at the bar line
hum = sd.hum(DUR, buzz=.7)
env = np.zeros(len(hum)); t = np.arange(len(hum)) / sd.SR
env[t < 6.0] = 1.0; env[(t >= 6.0) & (t < 6.006)] = np.linspace(1, 0, ((t >= 6.0) & (t < 6.006)).sum())     # the cable is cut
back = END - 4 * 60.0 / 132                                                         # it returns four beats before the end
env = np.maximum(env, np.clip((t - back) / 1.6, 0, 1) ** 2)
env[t > DUR - .004] = 0
out = sd.master(music * gate[:, None] + sd.pan(hum * env) * sd.db(-13), target_lufs=-17.0)
wav = sd.write_wav('out/music/eleven.wav', out)
sd.encode(wav, HERE / 'eleven.mp3')
r = ear.report(wav, HERE / 'eleven_report.jpg', 'Eleven (No. 4)')
r.pop('short_term'); print(json.dumps({k: (round(v, 2) if isinstance(v, float) else v) for k, v in r.items() if k not in ('chroma', 'bands')}, default=str))
print('bands', {k: round(v, 1) for k, v in r['bands'].items()}, 'wet to dry', round(m.wet_to_dry_db, 1))
