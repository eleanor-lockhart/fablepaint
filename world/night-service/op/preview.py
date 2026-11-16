"""Preview one unit of the opening:   uv run python world/night-service/op/preview.py <unit>     (from the repository root)
Renders world/night-service/op/shots/<unit>.py (which must define N and frame(i)) through the master's finishing pass
into out/op/<unit>/: frames, strip.jpg (a filmstrip to LOOK at), motion.jpg, preview.mp4. Prints a few numbers."""
import sys, importlib, json
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE / 'shots'))
import numpy as np
import common as C
from backlot import anim, screen, core
unit = sys.argv[1]
mod = importlib.import_module(unit)
out = f'out/op/{unit}'
def fr(i):
    img = mod.frame(i)
    assert img.shape == (C.H, C.W, 4), f'frame {i}: shape {img.shape}, wanted {(C.H, C.W, 4)}'
    return C.finish(img, i)
pat = anim.render(fr, mod.N, out + '/frames', workers=4)
anim.encode(pat, out + '/preview.mp4', fps=C.FPS, crf=22)
n = min(mod.N, 16)
screen.filmstrip(pat, out + '/strip.jpg', n=n, cols=8 if n > 8 else n, cell_w=320 if n > 8 else 420)
_, mm = screen.motion_map(pat, out + '/motion.jpg')
fl = screen.flicker(pat)[1]
print(json.dumps(dict(unit=unit, poses=mod.N, seconds=mod.N / C.FPS, strip=out + '/strip.jpg', motion={k: round(v, 3) for k, v in mm.items()},
                      brightness_min=round(min(fl['series']), 3), brightness_max=round(max(fl['series']), 3), largest_jump=round(fl['max_jump'], 3))))
