"""Assemble the opening:   uv run python world/night-service/op/build.py      (from the repository root)
Renders every unit in order through the finishing pass, encodes, puts the theme under it, and writes the
review sheets (one frame every half second) that the critics and I look at."""
import sys, importlib, json
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE / 'shots'))
import common as C
from backlot import anim, screen, core, sound as sd
ORDER = ['a_open', 'b_keeper_dee', 'c_marisol_red', 'd_prechorus', 'e_no4', 'f1_pod', 'f15_eye_out', 'g1_walk', 'g2_lights', 'f2_window', 'h_lineup']
mods = [importlib.import_module(m) for m in ORDER]
starts, n = [], 0
for m in mods:
    starts.append(n); n += m.N
assert n == 744, f'{n} poses, wanted 744: ' + ', '.join(f'{o}={m.N}' for o, m in zip(ORDER, mods))
def frame(i):
    k = max(j for j, s in enumerate(starts) if s <= i)
    C.begin()
    return C.finish(mods[k].frame(i - starts[k]), i)
if __name__ == '__main__':
    pat = anim.render(frame, n, 'out/op/full/frames', workers=14)
    silent = anim.encode(pat, 'out/op/full/silent.mp4', fps=C.FPS, crf=20)
    wav = Path('out/op/music/night_service_op.wav')
    out = HERE / 'night_service_op.mp4'
    if wav.exists():
        sd.mux(silent, wav, out, loop_video=False, crf=23)
    else:
        anim.encode(pat, str(out), fps=C.FPS, crf=23); print('no music found at', wav)
    (HERE / 'review').mkdir(exist_ok=True)
    frames = [core.load(f'out/op/full/frames/f_{i:04d}.png') for i in range(0, n, 6)]
    for k in range(0, len(frames), 30):
        screen.sheet(frames[k:k + 30], str(HERE / 'review' / f'strip_{k // 30 + 1}.jpg'), [f'{(k + j) * .5:.1f}s  pose {(k + j) * 6}' for j in range(len(frames[k:k + 30]))], cols=6, cell_w=256)
    print('built', out, n, 'poses')
