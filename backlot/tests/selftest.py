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

# backlot.space: the horizon is the eye; size goes as one over distance; the almanac finds an eclipse
from backlot import space as _sp
from datetime import datetime as _dt
import math as _m
_c = _sp.Camera(eye=(0, 0, 1.7), az=270, lens=35)
assert abs(_c.horizon() - 360) < 1e-6 and abs(_c.place((-20, 0, 0), 1.7)['top'] - 360) < 1e-6, 'a level camera should put the horizon through the head of someone its own height'
assert abs(_c.place((-10, 0, 0), 1.7)['px'] / _c.place((-20, 0, 0), 1.7)['px'] - 2) < 1e-6, 'twice as far should be half as tall'
_mn = _sp.moon(_dt(2024, 4, 8, 18, 17, 16), 25.29, -104.14)
_sep = _m.degrees(_m.acos(float(_sp.direction(_mn['az'], _mn['alt']) @ _sp.direction(_mn['sun']['az'], _mn['sun']['alt']))))
assert _sep < .5 and _mn['lit'] < .01, f'the almanac should put the moon on the sun at the 2024 eclipse: {_sep}'
_S = _sp.Set('test'); _S.box('near', (-10, -9), (-1, 1), (0, 2)); _S.box('far', (-30, -29), (-3, 3), (0, 6))
_p = _sp.render(_S, _c, ss=1); _mid = _p['solid'][340, 640]
assert _p['names'][_mid] == 'near' and abs(_p['depth'][340, 640] - 9.0) < .05, 'the nearer box should hide the farther one, nine metres off'
print('space: horizon, scale, hidden surfaces and the almanac are right')

# backlot.depth: parallax is one over distance; a texel is a place in the world; a wall blocks a lamp; a card is a cut-out
from backlot import depth as _dp
_cam = _sp.Camera(eye=(0, 0, 1.5), az=0, lens=35); _cam2 = _sp.Camera(eye=(.2, 0, 1.5), az=0, lens=35)
_sq = np.full((10, 10), 3, np.uint8); _near = _dp.card('near', _sq, (-.2, 2, 1.2), (1, 0, 0)); _far = _dp.card('far', _sq, (.6, 4, 1.2), (1, 0, 0))
_cx = lambda g, i: float(np.nonzero(g['solid'] == i)[1].mean())
_g1, _g2 = _dp.gbuffer([_near, _far], _cam), _dp.gbuffer([_near, _far], _cam2)
_ratio = (_cx(_g1, 0) - _cx(_g2, 0)) / (_cx(_g1, 1) - _cx(_g2, 1))
assert abs(_ratio - 2) < .05, f'a card twice as near should slide twice as far when the camera steps aside: {_ratio}'
_F = _sp.Set('floor'); _fl = _dp.paint(_F.box('floor', (-5, 5), (0, 10), (-.1, 0)), skin=(np.indices((8, 8)).sum(0) % 2 * 9).astype(np.uint8)); _F.box('wall', (-5, 5), (4, 4.1), (0, 3))
_cam3 = _sp.Camera(eye=(0, 0, 1.5), look=(0, 3, 0), lens=35); _g = _dp.gbuffer(_F.solids, _cam3); _P = _g['pos'][500, 700]
assert _g['u'][500, 700] == int(np.floor(_P[0] / .05)) and _g['v'][500, 700] == int(np.floor(-_P[1] / .05)), 'the texel under a pixel should be the 5 cm square of floor the pixel looks at'
assert np.allclose(_g['centre'][500, 700], ((_g['u'][500, 700] + .5) * .05, -(_g['v'][500, 700] + .5) * .05, 0), atol=1e-6), "a texel's middle should be a point on the floor"
_same = (_g['u'] == _g['u'][500, 700]) & (_g['v'] == _g['v'][500, 700]) & (_g['solid'] == 0)
_lamp = _dp.Light((0, 6, 1.0), 1.0, 3.0).bake(_F.solids); _lv = _dp.lighting(_g, [_lamp], ambient=.1); _open = _dp.lighting(_g, [_dp.Light((0, 2, 1.0), 1.0, 3.0).bake(_F.solids)], ambient=.1)
assert abs(_lv[500, 700] - .1) < 1e-6 and _open[500, 700] > .3, 'a lamp behind a wall should light nothing on this side of it; a lamp on this side should'
assert _same.sum() > 20 and np.ptp(_open[_same]) < 1e-6, 'every pixel of one texel should get one level of light'
_hole = _sq.copy(); _hole[3:7, 3:7] = _dp.HOLE; _g = _dp.gbuffer([_dp.card('front', _hole, (0, 2, 1.25), (1, 0, 0)), _dp.card('back', _sq, (0, 3, 1.0), (1, 0, 0), texel=.1)], _cam)
assert _g['names'][_g['solid'][360, 640]] == 'back' and (_g['solid'] == 0).sum() > 100, 'a hole in a card should show what stands behind it'
print('depth: parallax, texels, cast shadows and cut-outs are right')
