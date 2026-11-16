"""Tern Point: the Keeper's cue, written to the lighthouse box. The lamp is the clock: one rotation is six
seconds, which is two bars of slow three-in-a-bar at 60 beats a minute, and the bell falls where the lamp
faces the lens. D Dorian. Every pitched sound is struck and dies away; the only continuous things are the sea.

    uv run python world/night-service/music/tern_point.py       (from the repository root)"""
import json
from pathlib import Path
import numpy as np
from backlot import sound as sd, score as sc, ear

HERE = Path(__file__).resolve().parent
s = sc.Seq(bpm=60, beats=3, seed=4)
CH = [('D', 'm'), ('D', 'm'), ('F', 'M'), ('C', 'M'), ('D', 'm'), ('A', 'm'), ('G', 'M'), ('G', 'M')]
BASS = {'D': 'D2', 'F': 'F2', 'C': 'C2', 'A': 'A1', 'G': 'G2'}
COMP = {'D': (('F3', 'A3'), ('A3', 'D4')), 'F': (('A3', 'C4'), ('C4', 'F4')), 'C': (('G3', 'C4'), ('C4', 'E4')), 'A': (('A3', 'C4'), ('C4', 'E4')), 'G': (('G3', 'B3'), ('B3', 'D4'))}
A = [[('A4', 1, 1), ('D5', 2, 1), ('E5', 3, 1)], [('F5', 1, 3)], [('E5', 1, 1), ('C5', 2, 1), ('A4', 3, 1)], [('G4', 1, 3)],
     [('A4', 1, 1), ('D5', 2, 1), ('E5', 3, 1)], [('G5', 1, 2), ('E5', 3, 1)], [('D5', 1, 2), ('B4', 3, 1)], [('D5', 1, 3)]]
B = [[('D5', 1, 1), ('F5', 2, 1), ('A5', 3, 1)], [('A5', 1, 2), ('G5', 3, 1)], [('F5', 1, 1), ('A5', 2, 1), ('C6', 3, 1)], [('G5', 1, 3)],
     [('F5', 1, 1), ('E5', 2, 1), ('D5', 3, 1)], [('E5', 1, 2), ('C5', 3, 1)], [('B4', 1, 1), ('D5', 2, 1), ('G5', 3, 1)], [('D5', 1, 3)]]
BELLS = {2: 'D6', 4: 'A5', 6: 'G5', 8: 'A5', 10: 'D6', 12: 'A5', 14: 'G5', 16: 'A5', 18: 'D6', 20: 'A5'}
for strain, start, vel in ((A, 3, .66), (B, 11, .76)):
    for i, bar in enumerate(strain):
        root, kind = CH[i]; b = start + i
        for pitch, beat, length in bar:
            s.note('lead', pitch, b, beat, length, vel=vel + (.06 if beat == 1 else 0))
        s.note('bass', BASS[root], b, 1, 3, vel=.8)
        for k, dyad in enumerate(COMP[root]):
            for p in dyad:
                s.note('comp', p, b, 2 + k, 1, vel=.5 if strain is A else .58)
for b, p in BELLS.items():
    s.note('bell', p, b, 1, 3, vel=.55 if b in (2,) else .7)
for p, v in (('D5', .8), ('A4', .6), ('F4', .55)):               # the last chord, let ring
    s.note('lead', p, 19, 1, 6, vel=v)
s.note('bass', 'D2', 19, 1, 6, vel=.8)
s.note('glass', 'E6', 19, 2, 5, vel=.6)                           # one high pure note at the end: somebody out on the water
s.humanize(ms=10, vel=.07, tracks=('lead', 'comp'))

DUR = 63.0
m = sd.Mix(DUR, t60=4.6, damp=.5, seed=2)
s.render(m, {
    'lead': dict(inst=lambda f, d, v: sd.pluck(f, d + 3.0, bright=.35 + .4 * v, t60=3.4), gain=-10, send=-9, pan=-.12),
    'comp': dict(inst=lambda f, d, v: sd.epiano(f, d + 1.5, v, t60=2.2), gain=-22, send=-12, pan=.25, spread=.08),
    'bass': dict(inst=lambda f, d, v: .55 * sd.sub(f, d, t60=2.4) + .6 * sd.pluck(2 * f, d, bright=.25, t60=2.6)[:sd._n(d)], gain=-20, send=-18),
    'bell': dict(inst=lambda f, d, v: sd.bell(f, 7.0, t60=5.5, bright=.35, third=.2), gain=-19, send=-5, pan=.3),
    'glass': dict(inst=lambda f, d, v: sd.glass(f, d + 2, t60=5.0), gain=-23, send=-4, pan=-.4),
})
sea = sd.sea(DUR, period=6.0, seed=5)
m.add(sd.highpass(sd.pan(sea, -.2) * .7 + sd.pan(sd.sea(DUR, period=6.0, phase=.5, seed=9), .3) * .5, 70), gain=-25, send=-16)
for t in (0.0, 30.0, 54.0):
    m.add(sd.foghorn(3.4, f=sc.hz('D3')), at=t, gain=-21, pan_=-.5, send=-3)
out = sd.master(m.render(wet=-4.5), target_lufs=-16.0)
wav = sd.write_wav('out/music/tern_point.wav', out)
sd.encode(wav, HERE / 'tern_point.mp3')
sc.piano_roll(s, HERE / 'tern_point_score.png')
r = ear.report(wav, HERE / 'tern_point_report.jpg', 'Tern Point')
r.pop('short_term'); print(json.dumps({k: (round(v, 2) if isinstance(v, float) else v) for k, v in r.items() if k not in ('chroma',)}, default=str))
print('wet to dry', round(m.wet_to_dry_db, 1), 'dB; ffmpeg meter', ear.ffmpeg_loudness(wav))
