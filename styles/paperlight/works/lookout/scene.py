"""Lookout box: snow slopes of white paper under a cold front light, one stove-lit cab, and snow
falling THROUGH the box: 2D flakes composited at their own depths against the render's depth pass."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import numpy as np
import cv2
import kit as K
from backlot import core, draw, comp, lab, model, screen, anim, shapes as sh

OUT = 'out/paperlight/lookout'
N = 72
CAM = 545.0

def mm(x, y):
    return ((x - K.W / 2) / K.PPM, (K.H / 2 - y) / K.PPM)

def build(animate=True):
    K.setup(1280, 720, 4.0, 70, seed=9)
    W, H = K.W, K.H
    S = model.Spec((W, H), ppm=K.PPM)
    S.material('back', kind='emit', strength=2.1, axis='Z', stops=[[0, '#7fb0d0'], [.4, '#2f5a9e'], [1, '#08123c']])
    S.material('card', kind='card', color='#17181b')
    S.material('paper', kind='paper', color='#f4f1ea', translucency=.36, formation=.22, formation_scale=420)
    S.material('thin', kind='paper', color='#f6f2e8', translucency=.6, formation=.2, formation_scale=460)
    S.material('dark', kind='paper', color='#262c3c', translucency=.05, formation=0)
    S.panel('back', (380, 240), (0, 88, 0), 'back')
    sky = K.holes(np.ones((H, W), np.float32), K.stars(90, 380, seed=6))
    S.sheet('sky', sky, depth=74, material='thin')
    S.sheet('ridge', K.sheet(K.land([(-40, 430), (180, 404), (360, 420), (560, 396), (800, 414), (1040, 392), (1320, 410)])), depth=62)
    ground = K.land([(-40, 470), (200, 452), (420, 462), (700, 448), (960, 458), (1320, 444)])
    trees = np.zeros((H, W), np.float32)
    for x, hh, ww in ((150, 190, 96), (262, 150, 80), (700, 170, 88), (800, 230, 110), (905, 160, 84), (1010, 210, 104), (1118, 170, 90)):
        trees = np.maximum(trees, K.fir(x, 462, hh, ww))
    S.sheet('trees', K.sheet(ground, trees, min_width=4), depth=50)
    knoll = K.land([(-40, 500), (180, 470), (330, 420), (440, 398), (540, 400), (660, 440), (860, 486), (1320, 500)])
    tower, (wx, wy) = K.lookout(488, 402, h=250)
    S.sheet('knoll', K.sheet(knoll, tower, min_width=4), depth=38)
    # tracing paper behind the cab windows, the stove behind that, and a card behind the stove so it does not flood the box
    S.sheet('glazing', draw.rect(W, H, wx - 41, wy - 20, wx + 41, wy + 20), depth=39.6, material='thin', thickness=.12)
    S.sheet('baffle', draw.rect(W, H, wx - 40, wy - 22, wx + 40, wy + 22), depth=46.5, material='card', thickness=.4)
    S.sheet('drift1', K.sheet(K.land([(-40, 520), (160, 532), (380, 500), (600, 512), (840, 540), (1060, 522), (1320, 536)])), depth=26)
    S.sheet('drift2', K.sheet(K.land([(-40, 584), (220, 560), (460, 578), (700, 556), (920, 574), (1120, 596), (1320, 580)])), depth=14)
    near = comp.union(K.land([(-40, 600), (170, 606), (330, 616), (520, 640), (1320, 660)]), comp.union(K.fir(238, 612, 520, 250), K.fir(1060, 640, 300, 150)))
    S.sheet('near', K.sheet(near, min_width=5), depth=0, material='dark', thickness=.6)
    sx, sz = mm(wx, wy)
    S.light('stove', pos=(sx, 43.5, sz), type='point', power=.045, color='#ffab52', radius=2.5)
    # footlights, as in a toy theatre: a cold strip below the front edge, so the snow is brightest at the foot of each sheet
    S.light('foot', pos=(0, -46, -74), type='area', power=.62, color='#8fb0ff', size=[300, 8], look=(0, 34, -18))
    S.light('room', pos=(-280, -380, 300), type='area', power=.22, color='#9db8ff', size=[160, 160], look=(0, 30, 0))
    S.ambient('#141c30', .05)
    S.camera(pos=(0, -CAM, 0), look=(0, 40, 0), lens=85, fstop=4.0, focus=(0, 38, 0))
    if animate:
        ph = [((f - 1) / N) * 2 * math.pi for f in range(1, N + 1)]
        S.key('stove', 'data.energy', [(f, float(.045 * (1 + .25 * anim.loop_noise((f - 1) / N, seed=3, harmonics=6)))) for f in range(1, N + 1)])
        S.key('cam', 'location', [(f, [6.0 * math.sin(p), -CAM, 2.0 * math.sin(2 * p)]) for f, p in zip(range(1, N + 1), ph)])
    return S, (wx, wy)

# ------------------------------------------------------------------ snow, on the compositing desk
RES = (1280, 720)
def make_flakes(seed=2, n=420):
    r = np.random.default_rng(seed)
    return dict(x=r.uniform(-.05, 1.05, n), y=r.uniform(0, 1, n), z=r.choice([6.0, 20.0, 32.0, 44.0, 56.0], n, p=[.16, .22, .22, .22, .18]),
                turns=r.choice([1, 2], n, p=[.6, .4]), sway=r.uniform(.004, .014, n), ph=r.uniform(0, 6.283, n), size=r.uniform(.8, 1.5, n))
FL = make_flakes()

def snow(image, depth, i, window_xy=None):
    """Lay the flakes into a rendered frame. Each flake has its own depth in the box (mm behind the front):
    it is hidden wherever the render's depth pass says a sheet is nearer, it is larger and softer the
    further it is from the plane of focus, and it catches the stove's colour when it passes the window."""
    Wd, Hd = RES; p = i / N
    out = image.copy()
    for z in (56.0, 44.0, 32.0, 20.0, 6.0):                       # far to near
        sel = FL['z'] == z
        scale = (CAM + 38) / (CAM + z)                             # nearer things are bigger
        x = (FL['x'][sel] + FL['sway'][sel] * np.sin(2 * math.pi * 2 * p + FL['ph'][sel])) * Wd
        y = ((FL['y'][sel] + FL['turns'][sel] * p) % 1.0) * (Hd + 40) - 20
        rad = 1.5 * FL['size'][sel] * scale
        blur = abs(z - 38) / 38 * 3.2                              # circle of confusion, in pixels
        m = np.zeros((Hd, Wd), np.float32)
        for xi, yi, ri in zip(x, y, rad):
            cv2.circle(m, (int(round(xi * 16)), int(round(yi * 16))), int(round((ri + blur * .5) * 16)), 1.0, -1, cv2.LINE_AA, 4)
        if blur > .3:
            m = cv2.GaussianBlur(m, (0, 0), blur) * (1 + blur * .9)
        behind = comp.feather((depth > (CAM + z) / 1000.0).astype(np.float32), 1.0)       # only where nothing nearer is in the way
        m = np.clip(m, 0, 1) * behind
        tint = np.broadcast_to(core.col('#cfe0ff') * 1.5, (Hd, Wd, 3)).copy()
        if window_xy is not None and abs(z - 38) < 16:
            yy, xx = np.mgrid[:Hd, :Wd].astype(np.float32)
            g = np.exp(-((xx - window_xy[0]) ** 2 + (yy - window_xy[1]) ** 2) / (2 * 80.0 ** 2))[..., None]
            tint = tint * (1 - g) + core.col('#ffb060') * 2.6 * g
        out[..., :3] = out[..., :3] * (1 - m[..., None] * .85) + tint * m[..., None]
    return out

def finish(img, i):
    img = lab.exposure(img, .35)
    img = lab.bloom(img, r=12, strength=.2, threshold=1.6)
    img = lab.halation(img, r=8, strength=.2, threshold=2.6)
    img = lab.mist(img, r=34, amount=.09)
    img = lab.tonemap(img, 'filmic', white=6)
    img = lab.vignette(img, .3, radius=.7)
    img = lab.grain(img, .028, size=1.25, frame=i)
    return lab.weave(img, i, .25)

def window_px(wxy):
    """Where the cab window lands in the rendered frame (the knoll sheet is the plane of focus)."""
    x0, y0, x1, y1 = K.visible(38, CAM)
    return ((wxy[0] - x0) / (x1 - x0) * RES[0], (wxy[1] - y0) / (y1 - y0) * RES[1])

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'test'
    S, wxy = build()
    wp = window_px(wxy)
    if mode == 'test':
        fr = S.render(OUT + '/test', frames=[20], samples=96, res=RES)
        p = model.passes(fr[0])
        core.save(OUT + '/test/plain.jpg', finish(p['image'], 0))
        core.save(OUT + '/test/look.jpg', finish(snow(p['image'], p['depth'], 19, wp), 0))
        d = p['depth']; print('depth range m', round(float(d.min()), 4), round(float(np.percentile(d, 99)), 4), 'window px', [round(v) for v in wp])
    elif mode == 'render':
        S.render(OUT + '/exr', frames=list(range(1, N + 1)), samples=110, res=RES)
    elif mode == 'finish':
        def frame(i):
            p = model.passes(f'{OUT}/exr/f_{i + 1:04d}.exr')
            return finish(snow(p['image'], p['depth'], i, wp), i)
        pat = anim.render(frame, N, OUT + '/frames', workers=10)
        anim.encode(pat, 'styles/paperlight/works/lookout.mp4', fps=12, loops=3, crf=17)
        screen.filmstrip(pat, OUT + '/strip.jpg', n=8, cols=4)
        _, mmap = screen.motion_map(pat, OUT + '/motion.jpg')
        print('motion', {k: round(v, 3) for k, v in mmap.items()}, 'seam', {k: round(v, 4) for k, v in screen.loop_seam(pat).items()})
        core.save('styles/paperlight/works/lookout_still.png', core.load(f'{OUT}/frames/f_0030.png'))
        pp = model.passes(f'{OUT}/exr/f_0031.exr')
        model.making_of(S, pp, core.load(f'{OUT}/frames/f_0030.png'), 'styles/paperlight/works/lookout_making.jpg')
