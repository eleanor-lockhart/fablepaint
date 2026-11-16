exec(open('paint/common.py').read())
use('fringe'); gaussian_blur(3); props('fringe', opacity=.22)
# The spruces came out as paper cut-outs: every bough the same, snow wall to wall. Again, properly:
# a dark ragged mass of needles first, then snow only where it would actually lodge.
delete('trees_back'); delete('trees_front')

def spruce(x, base, h, seed):
    r = np.random.default_rng(seed)
    dark = mix('#020709', '#06141a', r.random())
    n = int(12 + h / 13)
    B(size=max(2.5, h * .02), hardness=.7, spacing=.15, taper=(0, .9))
    stroke([(x, base), (x + r.uniform(-.01, .01) * h, base - h)], color='#030504')
    for i in range(n):
        t = (i + r.uniform(.2, .8)) / n
        y = base - h * (1 - t) * .96 - h * .03
        reach = h * (.03 + .24 * t ** .85)
        thick = max(2.0, h * (.010 + .022 * t))
        for side in (-1, 1):
            for _ in range(2 if h > 300 else 1):
                L = reach * r.uniform(.6, 1.1)
                droop = L * r.uniform(.2, .6)
                y0 = y + r.uniform(-.5, .5) * h / n
                bough = [(x, y0), (x + side * L * .5, y0 + droop * .25), (x + side * L, y0 + droop)]
                B(tip='needle', size=thick * 5, flow=.9, spacing=.18, follow=True, angle_jitter=.06, psize=False, size_jitter=.3)
                stroke(bough, color=dark)
                B(tip='chalk', size=thick * 1.8, flow=.9, spacing=.15, angle_jitter=1, taper=(0, .6))
                stroke(bough, color=dark)
                clumps = []
                for _ in range(int(2 + L / (thick * 2.2))):
                    u = r.uniform(.08, .82)
                    clumps.append((x + side * L * u, y0 + droop * u * u - thick * r.uniform(.5, .9), r.uniform(.55, 1.25)))
                B(size=thick * 1.5, hardness=.35, flow=.85)
                dabs(clumps, color=mix('#2b6360', '#57a892', r.uniform(0, 1) * (.9 if side * (x - 1280) < 0 else .35)))

use('snow_ridges')
layer('trees_back')
for x, b, h, sd in ((1945, 958, 120, 1), (1990, 952, 150, 2), (2030, 946, 190, 3), (2290, 955, 210, 4), (2345, 962, 170, 5),
                    (2400, 975, 250, 6), (2460, 985, 220, 7), (2520, 1000, 300, 8)):
    spruce(x, b, h, sd)

# ---------------- the snow: only the gentlest hollows (hard-edged crest stripes looked airbrushed), then dead grass
use('snow')
lock(True)
B(size=260, hardness=0, flow=.05, spacing=.1, psize=False)
for c in ([(900, 1330), (1500, 1340), (2100, 1290)], [(1500, 1420), (2100, 1410), (2600, 1380)], [(2050, 1110), (2400, 1090)]):
    stroke(c, color='#071824')
for c in ([(1000, 1262), (1500, 1268), (2000, 1200), (2500, 1120)], [(600, 1380), (1200, 1400)]):
    stroke(c, color='#4fae94')
lock(False)
layer('grass')
B(tip='blade', size=30, flow=.9, angle=-90, angle_jitter=.07, size_jitter=.4, psize=False)
for cx, cy in ((900, 1210), (1380, 1216), (1750, 1152), (330, 1190), (1100, 1260), (2180, 1100)):
    dabs([(cx + rng.normal(0, 22), cy + rng.normal(0, 5) - 13) for _ in range(16)], color='#0a1410')

# ---------------- cold mist along the far shore
use('treeline')
layer('mist', opacity=.25)
B(size=110, hardness=0, flow=.05, spacing=.1, psize=False)
for yy_ in (884, 896, 906):
    stroke([(-50, yy_), (700, yy_ + 6), (1400, yy_ - 4), (2000, yy_ + 4)], color='#4a9c94')
gaussian_blur(18)

# ---------------- foreground trees
use('figure')
layer('trees_front')
spruce(2545, 1190, 520, 21)
spruce(300, 1420, 560, 22)
spruce(70, 1500, 940, 23)
