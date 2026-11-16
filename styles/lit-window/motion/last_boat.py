"""Last boat, rain, moving. The print's own layers (exported with `studio.py plates p1`) go on the
animation stand; rain, the ferry's light on the water and the rings where drops land are redrawn
for every pose with the same carved shapes the print was made from. Shot on twos.

    uv run python styles/lit-window/motion/last_boat.py        (from the repository root)
"""
import json, math
from pathlib import Path
import numpy as np
from backlot import core, draw, comp, lab, anim, screen, shapes as sh

HERE = Path(__file__).resolve().parent
man = json.load(open(HERE / 'plates_p1/plates.json'))
W, H = man['size']
PL = {p['name']: (core.load(HERE / 'plates_p1' / p['file']), p['blend']) for p in man['plates']}
X0, Y0, X1, Y1, HZ = 80, 70, 1200, 1730, 502          # the print's image window and horizon
N = 72                                                 # poses in the loop (6 s at 12 poses a second)
OUT = 'out/litwindow/last_boat'

def pile(names):
    out = None
    for n in names:
        img, mode = PL[n]
        out = img if out is None else comp.blend(out, img, mode)
    return out

under = pile(['Background', 'paper', 'sky', 'clouds', 'sliver', 'water', 'hullshadow', 'shore', 'shorelights', 'ferry', 'ferrylights'])
front = pile(['stumprefl', 'piles', 'pileplane', 'lash', 'stump', 'heron'])
window = draw.rect(W, H, X0, Y0, X1, Y1)
paper = PL['paper'][0]

def rings(p, seed=5, n=30):
    """Drops landing: each ring is born, widens and fades on its own clock, and every clock divides the loop."""
    r = np.random.default_rng(seed); polys, alphas = [], []
    for _ in range(n):
        f = r.uniform(.15, 1) ** .7
        x, y = r.uniform(420, X1 - 10), HZ + (Y1 - HZ) * f
        life = (p * r.choice([2, 3]) + r.uniform()) % 1.0
        rx = (2 + 30 * f) * life ** .6
        if rx > 1.5:
            polys.append((sh.ring(x, y, rx, w=.9 + .6 * f), 1 - life))
    return polys

def frame(i):
    p = i / N
    img = under.copy()
    # the ferry's light on the water, re-cut for every pose
    sh.seed(1000 + i)
    refl = draw.raster(sh.sheen(710, 1083, 528, 1039, th0=1.8, th1=3.8, breakup=5, keep=.35), W, H)
    img = draw.paint(img, refl, '#ecd596')
    refl2 = draw.raster(sh.sheen(690, 1103, 579, 1279, th0=2.0, th1=4.2, breakup=6, keep=.18), W, H)
    img = draw.paint(img, refl2, '#c9a35c', .9)
    img = comp.over(img, front)
    for poly, a in rings(p):
        img = draw.paint(img, draw.raster([poly], W, H), '#667a82', .75 * a)
    # rain: hairlines in sheaves, new every pose
    sh.seed(5000 + i)
    def sheaves(n, k, **kw):
        out = []
        for _ in range(k):
            cx = sh.rng.uniform(X0 - 100, X1 + 200); wd = sh.rng.uniform(60, 190)
            out += sh.rain(cx - wd, Y0, cx + wd, Y1, n=n, **kw)
        return out
    img = draw.paint(img, draw.raster(sheaves(7, 8, angle=106, w=.9, length=(.25, .75), spread=.9), W, H), '#0a0f15', .5)
    img = draw.paint(img, draw.raster(sheaves(6, 9, angle=106, w=.75, length=(.18, .6), spread=.9), W, H), '#93a3a6', .2)
    # back onto the sheet of paper: margin, border line, paper tooth, seal, title
    img = comp.over(paper, comp.mask(img, window))
    for n in ('border', 'tooth', 'seal', 'title'):
        img = comp.blend(img, PL[n][0], PL[n][1])
    return img

if __name__ == '__main__':
    pat = anim.render(frame, N, OUT + '/frames', workers=10)
    anim.encode(pat, str(HERE / 'last_boat_rain.mp4'), fps=12, loops=1, crf=21, scale='960:-2')
    screen.filmstrip(pat, OUT + '/strip.jpg', n=4, cols=4, cell_w=330)
    a, b = core.load(OUT + '/frames/f_0000.png'), core.load(OUT + '/frames/f_0001.png')
    screen.onion(a, b, OUT + '/onion.png')
    print('seam', {k: round(v, 4) for k, v in screen.loop_seam(pat).items()})
    core.save(str(HERE / 'last_boat_rain_still.png'), core.load(OUT + '/frames/f_0010.png'))
