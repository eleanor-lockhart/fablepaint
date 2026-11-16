"""Calibrate the listening room against sounds whose answers are known. Run: uv run python backlot/tests/eartest.py"""
import numpy as np
from backlot import sound as sd, score as sc, ear
def mix(notes, dur=6):
    m = sd.Mix(dur)
    for n in notes: m.add(sd.pluck(sc.hz(n), dur), gain=-12)
    return sd.master(m.render(wet=-60), -16)
for label, notes, want in (('A4 alone', ['A4'], 'A'), ('D minor triad with a low D', ['D2', 'D3', 'F3', 'A3', 'D4'], 'D minor'), ('C major triad', ['C3', 'E3', 'G3', 'C4'], 'C major'),
                           ('D Dorian scale', ['D3', 'E3', 'F3', 'G3', 'A3', 'B3', 'C4', 'D4'], 'D minor / C major / A minor')):
    r = ear.measure(mix(notes))
    top = [k for k, v in sorted(r['chroma'].items(), key=lambda kv: -kv[1])[:3]]
    print(f'{label:28s} wanted {want:28s} got key {r["key"]:10s} strongest {top}  lufs {r["lufs"]:.1f}')
x = sd.pan(sd.sine(1000, 5)) * sd.db(-20)
print('1 kHz sine, centre-panned from -20 dBFS (so -23 dBFS in each channel): lufs', round(sd.loudness(x), 2), '(BS.1770 says exactly -23.0)')
