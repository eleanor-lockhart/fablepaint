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
