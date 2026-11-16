"""Lighthouse box: layered cut paper, a blue-to-amber back light, one lamp that turns."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import numpy as np
import kit as K
from backlot import core, draw, comp, lab, model, screen, shapes as sh

OUT = 'out/paperlight/lighthouse'
N = 72

def px_to_mm(x, y):
    return ((x - K.W / 2) / K.PPM, (K.H / 2 - y) / K.PPM)

def build(frames=72, animate=True):
    """frames = length of the loop in rendered frames (shot on twos: 72 frames = 6 s)."""
    K.setup(1280, 720, 4.0, 70, seed=5)
    W, H = K.W, K.H
    S = model.Spec((W, H), ppm=K.PPM)
    S.material('back', kind='emit', strength=5.0, axis='Z', stops=[[0, '#ff8a3c'], [.36, '#ffb878'], [.5, '#6aa6c8'], [.72, '#2c58b0'], [1, '#16286e']])
    S.material('paper', kind='paper', color='#f3efe4', translucency=.42, formation=.24, formation_scale=420)
    S.material('thin', kind='paper', color='#f6f2e8', translucency=.62, formation=.2, formation_scale=460)
    S.material('seapaper', kind='paper', color='#e9eef2', translucency=.55, formation=.34, formation_scale=240)
    S.material('card', kind='card', color='#17181b')
    S.material('dark', kind='paper', color='#2c3346', translucency=.06, formation=0)
    S.panel('back', (380, 240), (0, 86, 0), 'back')
    # sky: a whole sheet (it diffuses the back light) with pinhole stars and a crescent cut in it
    moon = comp.subtract(draw.disc(W, H, 965, 190, 44), draw.disc(W, H, 985, 176, 42))
    sky = K.holes(np.ones((H, W), np.float32), K.stars(70, 400, avoid=comp.grow(moon, 8)), moon)
    S.sheet('sky', sky, depth=72, material='thin')
    mmx, mmz = px_to_mm(965, 190)
    S.light('moonlamp', pos=(mmx, 80, mmz), type='point', power=.012, color='#fff1d2', radius=9)      # a ball of light seen through the crescent cut
    S.sheet('far', K.sheet(K.land([(-40, 452), (200, 430), (420, 446), (640, 440), (900, 420), (1100, 436), (1320, 428)])), depth=60)
    # the headland and the light
    head = K.land([(-40, 520), (150, 470), (300, 430), (380, 418), (470, 428), (640, 470), (860, 500), (1320, 510)])
    tower, (lx, ly) = K.lighthouse(372, 424, h=250)
    house = comp.union(draw.rect(W, H, 452, 398, 520, 440), draw.raster([np.array([(444, 400), (486, 372), (528, 400)])], W, H))
    house = K.holes(house, draw.rect(W, H, 470, 410, 484, 426), draw.rect(W, H, 494, 410, 508, 426))
    S.sheet('headland', K.sheet(head, tower, house), depth=46)
    # three sea sheets that slide against each other, toy-theatre fashion, and a boat between them
    S.sheet('sea1', K.sheet(K.waves(516, 12, 92, .0)), depth=36, material='seapaper')
    S.sheet('sea2', K.sheet(K.waves(552, 17, 126, .37)), depth=26, material='seapaper')
    boat = draw.raster([np.array([(596, 368), (610, 394), (672, 394), (694, 364), (662, 372)]), np.array([(634, 296), (642, 296), (642, 372), (634, 372)]),
                        np.array([(640, 304), (688, 364), (640, 364)]), np.array([(636, 318), (636, 364), (602, 364)])], W, H)
    S.sheet('boat', draw.paperize(boat, 3)[0], depth=20, material='dark', thickness=.5, offset=[52, -48.5])
    S.sheet('sea3', K.sheet(K.waves(600, 22, 170, .71)), depth=14, material='seapaper')
    # the shore, drawn for the window the camera actually has on the front sheet (about x 180..1100, y 100..620)
    rocks = K.land([(-40, 600), (150, 586), (250, 560), (330, 578), (470, 604), (700, 616), (900, 606), (1010, 580), (1110, 560), (1320, 566)])
    firs = comp.union(K.fir(1016, 590, 470, 220), K.fir(236, 572, 230, 120))
    shore = K.sheet(rocks, firs, min_width=5)
    core.save(OUT + '/test/shore_matte.png', shore)
    S.sheet('shore', shore, depth=0, material='dark', thickness=.6)
    # lights: the turning lamp, a window, a cold strip under the sea, a little room light from the front
    mx, mz = px_to_mm(lx, ly)
    S.light('lamp', pos=(mx, 52, mz), type='spot', power=1.6, color='#ffc27a', cone=34, blend=.35, radius=1.5, rot=(90, 0, 0))
    hx, hz = px_to_mm(489, 418)
    S.light('window', pos=(hx, 50, hz), type='point', power=.02, color='#ffb060', radius=2)
    S.light('seastrip', pos=(0, 42, -86), type='area', power=.5, color='#58b8d8', size=[300, 6], rot=(180, 0, 0))
    S.light('room', pos=(-260, -420, 260), type='area', power=.9, color='#9db8ff', size=[200, 200], look=(0, 0, 0))
    S.haze((330, 30, 190), pos=(0, 54, 0), density=7.0, anisotropy=.5)
    S.ambient('#1b2334', .06)
    S.camera(pos=(0, -545, 0), look=(0, 40, 0), lens=85, fstop=4.0, focus=(0, 46, 0))
    if animate:
        N = frames
        S.key('lamp', 'rotation_euler', [(1, [90, 0, 0]), (N + 1, [90, 0, 360])])
        ph = [((f - 1) / N) * 2 * math.pi for f in range(1, N + 1)]
        for name, amp, bob, off in (('sea1', 5.0, .8, 0.0), ('sea2', -7.0, 1.2, 1.3), ('sea3', 9.0, 1.6, 2.6)):
            dep = {'sea1': 36, 'sea2': 26, 'sea3': 14}[name]
            S.key(name, 'location', [(f, [amp * math.sin(p + off), dep, bob * math.sin(2 * p + off)]) for f, p in zip(range(1, N + 1), ph)])
        S.key('boat', 'location', [(f, [52 - 7.0 * math.sin(p + 1.3) * .6, 20, -48.5 + 2.2 * math.sin(2 * p + 1.9)]) for f, p in zip(range(1, N + 1), ph)])
        S.key('boat', 'rotation_euler', [(f, [90, 5.0 * math.sin(2 * p + .6), 0]) for f, p in zip(range(1, N + 1), ph)])
        S.key('cam', 'location', [(f, [9.0 * math.sin(p), -545 + 10 * math.cos(p), 3.0 * math.sin(p + .7)]) for f, p in zip(range(1, N + 1), ph)])
        r = np.random.default_rng(11)
        S.key('window', 'data.energy', [(f, float(.02 * (1 + .22 * math.sin(3 * p + 1) + .1 * math.sin(7 * p)))) for f, p in zip(range(1, N + 1), ph)])
    return S

def finish(img, i):
    """The lab pass every frame gets: lens, tone, film."""
    img = lab.exposure(img, -.15)
    img = lab.bloom(img, r=22, strength=.6, threshold=9.0)       # only the lamp seen directly is this bright: the flash
    img = lab.bloom(img, r=14, strength=.16, threshold=2.2)
    img = lab.halation(img, r=9, strength=.22, threshold=3.0)
    img = lab.mist(img, r=36, amount=.10)
    img = lab.tonemap(img, 'filmic', white=7)
    img = lab.vignette(img, .28, radius=.7)
    img = lab.grain(img, .028, size=1.25, frame=i)
    return lab.weave(img, i, .25)

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'test'
    if mode == 'test':
        S = build(N)
        fr = S.render(OUT + '/test', frames=[20], samples=96, res=(1280, 720))
        core.save(OUT + '/test/look.jpg', finish(model.passes(fr[0])['image'], 0))
    elif mode == 'render':
        build(N).render(OUT + '/exr', frames=list(range(1, N + 1)), samples=110, res=(1280, 720))
        print('rendered', N)
    elif mode == 'finish':
        from backlot import anim
        def frame(i):
            return finish(model.passes(f'{OUT}/exr/f_{i + 1:04d}.exr')['image'], i)
        pat = anim.render(frame, N, OUT + '/frames', workers=10)
        anim.encode(pat, 'styles/paperlight/works/lighthouse.mp4', fps=12, loops=3, crf=17)
        screen.filmstrip(pat, OUT + '/strip.jpg', n=12, cols=4)
        _, mm = screen.motion_map(pat, OUT + '/motion.jpg')
        print('motion', {k: round(v, 3) for k, v in mm.items()}, 'seam', {k: round(v, 4) for k, v in screen.loop_seam(pat).items()})
        core.save('styles/paperlight/works/lighthouse_still.png', core.load(f'{OUT}/frames/f_0059.png'))
        pp = model.passes(f'{OUT}/exr/f_0060.exr')
        model.making_of(build(N, animate=False), pp, core.load(f'{OUT}/frames/f_0059.png'), 'styles/paperlight/works/lighthouse_making.jpg')
