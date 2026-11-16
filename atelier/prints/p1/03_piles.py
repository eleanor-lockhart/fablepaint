exec(open('../atelier/prints/p1/common.py').read())
window(X0, Y0, X1, Y1)
# quieter car-deck mouths on the ferry, and a longer sliver of last light to her left
use('sliver')
marks([cloudband(X0 + 180, HZ - 30, 640, 15, ragged=.3)], PAL['pale'])

# ---- the dolphin: a cluster of timber piles, nearest ones running out of the frame
def pile(xl, xr, top, bot, lean=0.0, chew=10):
    n = 7
    tx = np.linspace(xl + lean * (bot - top), xr + lean * (bot - top), n)
    crown = [(tx[i], top + rng.uniform(0, chew) - (chew * .8 if i in (2, 3) else 0)) for i in range(n)]
    return wobble([(xl, bot)] + crown + [(xr, bot)], amp=.9, step=40)
def plane(xl, xr, top, bot, lean=0.0, frac=.2):
    d = lean * (bot - top)
    return wobble([(xr - (xr - xl) * frac, bot), (xr - (xr - xl) * frac + d, top + 14), (xr + d - 2, top + 16), (xr - 1, bot)], amp=.7, step=50)
PILES = [(40, 196, -40, 1800, .0), (176, 318, 176, 1800, .004), (300, 420, 404, 1800, -.006)]
block('piles')
marks([pile(*p) for p in PILES], PAL['pile'])
block('pileplane')
marks([plane(*p) for p in PILES], PAL['pile2'])
use('piles')
cracks = []
for (xl, xr, top, bot, lean) in PILES:
    for _ in range(9):
        x = rng.uniform(xl + 8, xr - 30); y = rng.uniform(max(top, Y0) + 20, Y1 - 200); ln = rng.uniform(120, 520)
        cracks.append(ribbon([(x, y), (x + rng.normal(0, 3), y + ln * .5), (x + rng.normal(0, 5), y + ln)], w=rng.uniform(1.2, 2.4), taper=(.3, .5), wob=.2))
cut(cracks, depth=.22)
# wire-rope lashings round the cluster
block('lash')
wraps = []
for yc, n in ((640, 6), (1210, 5)):
    for i in range(n):
        y = yc + i * 9 + rng.normal(0, 1)
        wraps.append(ribbon([(60, y - 4), (200, y + 5), (330, y + 1), (424, y + 7 - i)], w=3.4, taper=(0, 0), wob=.08))
marks(wraps, '#3b3a38')
# ---- the short pile the heron stands on, 8 m out: top 1.75 m above the water, waterline in view
hx0, hx1, htop, hwl = 452, 546, 962, 1418
block('stump')
marks([pile(hx0, hx1, htop, hwl + 3, lean=.004, chew=7)], PAL['pile'])
marks([plane(hx0, hx1, htop, hwl + 3, lean=.004, frac=.22)], PAL['pile2'])
cut([ribbon([(x, y), (x + rng.normal(0, 3), y + ln)], w=1.6, taper=(.3, .5), wob=.2) for x, y, ln in ((470, 1000, 220), (492, 1110, 180), (512, 990, 150), (478, 1260, 120))], depth=.22)
marks([np.array([(hx0 + 6, htop + 5), (hx0 + 20, htop - 3), (hx1 - 14, htop - 2), (hx1 - 4, htop + 6), (hx1 - 20, htop + 10), (hx0 + 18, htop + 11)])], '#8f9288')   # weathered cap
# tide zone: wet dark band and barnacles just above the water
marks([wobble([(hx0 - 1, hwl - 96), (hx1 + 3, hwl - 90), (hx1 + 3, hwl + 3), (hx0 - 1, hwl + 3)], amp=.8, step=20)], '#121110')
marks([chip(rng.uniform(hx0 + 3, hx1), hwl - 96 - abs(rng.normal(0, 16)), rng.uniform(1.2, 2.6)) for _ in range(130)], '#6f736c')
# its reflection: dark dashes that wander
block('stumprefl', above='water')
marks(ticks((hx0 + hx1) / 2 + 2, hwl + 6, hwl + 250, hx1 - hx0, grow=1.1, th=3.2, jitter=.12, gap=.35), '#10161d')
# ---- heron, facing the light
block('heron')
heron((hx0 + hx1) / 2 - 2, htop + 2, s=.58, flip=True,
      pal=dict(body='#1e262d', tip='#11161a', neck='#40403f', head='#cfcdbf', bill=PAL['lamp2'], plume='#536270', leg='#0f0f0f', thigh='#3d302b'))
