"""End-to-end check of the 2D departments: shapes -> draw -> comp (multiplane) -> lab -> anim -> screen.
Run:  uv run python backlot/tests/selftest.py   (writes out/selftest/)"""
import math, sys
import numpy as np
from backlot import core, draw, shapes as sh, comp, lab, anim, screen

W, H, N = 640, 360, 48
OUT = 'out/selftest'
sh.setup(W, H, seed=3)
# plates, far to near (built once)
sky = draw.gradient(W, H, (0, 0), (0, H), '#101a2a', '#27405a', '#6c8794')
moon = comp.stencil(draw.disc(W, H, 430, 110, 46), '#efe6cc')
hills = comp.stencil(draw.raster([np.array([(-40, H), (-40, 250), (120, 215), (300, 240), (470, 205), (700, 235), (700, H)])], W, H), '#1f3346')
tr, fo = [], []
for x in range(-20, W + 60, 70):
    t_, f_ = sh.conifer(x + sh.rng.normal(0, 10), H + 20, sh.rng.uniform(170, 260), sh.rng.uniform(70, 100), crown=.85)
    tr += t_; fo += f_
trees_m = draw.raster(tr + fo, W, H)
trees = comp.stencil(trees_m, '#0b1118')
window = comp.stencil(draw.rect(W, H, 300, 262, 306, 272), '#ffcf7a')

def frame(i):
    p = anim.phase(i, N)
    cam = (40 * math.sin(2 * math.pi * p), 6 * math.sin(4 * math.pi * p))
    img = comp.multiplane([(sky, 50), (moon, 30), (hills, 6), (window, 6), (trees, 1.0)], cam=cam)
    img = comp.over(img, comp.drop_shadow(trees_m, 0, 0, 10, '#000000', .0))
    img = lab.bloom(img, r=10, strength=.5, threshold=.7)
    img = lab.vignette(img, .4)
    img = lab.tonemap(img, 'filmic', white=3)
    return lab.grain(img, .04, frame=i)

pattern = anim.render(frame, N, OUT + '/frames', workers=8)
anim.encode(pattern, OUT + '/loop.mp4', fps=24, loops=2)
anim.encode(pattern, OUT + '/loop.gif', fps=24, scale='320:-1')
screen.filmstrip(pattern, OUT + '/strip.jpg', n=8)
_, mm = screen.motion_map(pattern, OUT + '/motion.jpg')
f0 = core.load(OUT + '/frames/f_0000.png')
screen.scopes(f0, OUT + '/scopes.jpg')
screen.onion(f0, core.load(OUT + '/frames/f_0006.png'), OUT + '/onion.png')
# print and screen finishes on one frame
fin = [f0, lab.halftone(f0, cell=5), lab.quantize(f0, 'ega', pixel=2), lab.quantize(f0, 'gameboy', pixel=3), lab.crt(f0, lines=180), lab.misregister(lab.paper(f0), ((2, 0), (0, 0), (-1.5, 1.5)))]
screen.sheet(fin, OUT + '/finishes.jpg', ['plain', 'halftone', 'ega dither', 'gameboy', 'crt', 'paper + misregister'], cols=3)
print('motion', {k: round(v, 3) for k, v in mm.items()})
print('seam', {k: round(v, 4) for k, v in screen.loop_seam(pattern).items()})
print('flicker', {k: round(v, 4) for k, v in screen.flicker(pattern)[1].items() if k != 'series'})
print('stats', {k: round(v, 3) for k, v in screen.stats(f0).items()})


# draw.rect must clip, not wrap: a rectangle wholly off the left or top edge is empty (it used to fill most of the frame)
assert draw.rect(64, 48, -30, 10, -5, 20).sum() == 0 and draw.rect(64, 48, 10, -30, 20, -5).sum() == 0, 'draw.rect wraps negative far edges'
assert draw.rect(64, 48, -10, -10, 8, 6).sum() == 48 and draw.rect(64, 48, 60, 40, 200, 200).sum() == 32, 'draw.rect clips wrongly'
print('draw.rect clips at every edge')

# lab.bloom(protect=) keeps a silhouette dark in front of a large light, and still lets a light inside it glow
import numpy as np
from backlot import core as _core
_img = _core.canvas(96, 64, '#000000'); _img[..., :3] = 0; _img[:, 48:, :3] = 4.0                       # a wall of light on the right
_sil = draw.rect(96, 64, 40, 8, 46, 56); _img[..., :3] *= (1 - _sil[..., None])                         # a thin dark post just in front of it
_plain = lab.bloom(_img, r=6, strength=.5, threshold=1.0)[20, 43, 0]; _kept = lab.bloom(_img, r=6, strength=.5, threshold=1.0, protect=_sil)[20, 43, 0]
assert _plain > .2 and _kept == 0, f'lab.bloom(protect=) does not protect: {_plain} {_kept}'
print('lab.bloom keeps silhouettes dark')
# draw.font is strict: a typeface that fontconfig would silently substitute is an error
try:
    draw.font(20, 'No Such Typeface Anywhere:style=Ultra'); raise AssertionError('draw.font accepted a substituted face')
except RuntimeError:
    print('draw.font refuses a substituted typeface')
# sync.pops sees a one-frame slab; sync.travel measures a pan
from backlot import sync as _sync
import cv2 as _cv2, os as _os
_d = OUT + '/synctest'; _os.makedirs(_d, exist_ok=True)
_rng = np.random.default_rng(1); _tex = _cv2.GaussianBlur(_rng.uniform(0, 255, (360, 1400)).astype(np.float32), (0, 0), 6)
_tex = ((_tex - _tex.min()) / (_tex.max() - _tex.min()) * 255).astype(np.uint8)
for _i in range(24):
    _f = _cv2.cvtColor(_tex[:, _i * 5:_i * 5 + 640].copy(), _cv2.COLOR_GRAY2BGR)
    if _i == 13: _f[200:300, 100:500] = 0
    _cv2.imwrite(f'{_d}/f_{_i:04d}.png', _f)
_p = _sync.pops([], _d, fps=12); _a, _st = _sync.travel(_d)
assert [q['frame'] for q in _p] == [13], f'sync.pops should find exactly the slab on frame 13: {_p}'
assert abs(_st['max_step'] - 5.0) < 1.0, f'sync.travel measured {_st}'
print('sync.pops and sync.travel measure what they should')
