exec(open('../styles/lit-window/prints/p1/common.py').read())
window(X0, Y0, X1, Y1)
# ---- ferry again with quieter car-deck mouths (they were black boxes stuck on her ends)
eye = (160, 420, 3.5)
P = camera(eye=eye, look=(0, 0, 3.5), fov=34, centre=(X0 + 800, HZ))
use('ferry'); clear()
ferry(P, eye, night=True, pal=dict(white='#7b8b8e', white2='#62737a', lamp=PAL['lamp'], lamp2='#dcbf7c', lamp3='#a8935f', dark='#3b4950'))
# ---- piles again: they were a flat brown wall. Converging leans, broken lit planes, carved grain.
for n in ('piles', 'pileplane', 'lash', 'stump', 'stumprefl', 'heron'):
    use(n); clear()
PILE, PILE2, CHECK = '#191716', '#2f2b27', '#0d0c0c'
def pile(xl, xr, top, bot, lean=0.0, chew=10):
    n = 7
    d = lean * (bot - top)
    tx = np.linspace(xl + d, xr + d, n)
    crown = [(tx[i], top + rng.uniform(0, chew) - (chew * .8 if i in (2, 3) else 0)) for i in range(n)]
    return wobble([(xl, bot)] + crown + [(xr, bot)], amp=.9, step=40)
def edge_x(xl, xr, top, bot, lean, y, frac):
    return xl + (xr - xl) * frac + lean * (bot - top) * (bot - y) / (bot - top)
def lit_plane(xl, xr, top, bot, lean, frac=.78):
    """The side of the pile toward the light: a strip with a stepped, broken inner edge."""
    ys = np.arange(max(top, Y0 - 20) + 16, min(bot, Y1 + 20), 46.0)
    inner = [(edge_x(xl, xr, top, bot, lean, y, frac + rng.choice([-.05, 0, 0, .04, .09])), y) for y in ys]
    inner = [p for a, b in zip(inner, inner[1:]) for p in (a, (a[0], b[1]))]           # steps, not a curve
    outer = [(edge_x(xl, xr, top, bot, lean, y, .985), y) for y in ys[::-1]]
    return np.array(inner + outer)
def grain(xl, xr, top, bot, lean, n, lo=.05, hi=.95, long=(50, 380), w=(.8, 1.7)):
    out = []
    for _ in range(n):
        y = rng.uniform(max(top, Y0) + 20, min(bot, Y1) - 30); ln = rng.uniform(*long)
        fr = rng.uniform(lo, hi)
        x0_, x1_ = edge_x(xl, xr, top, bot, lean, y, fr), edge_x(xl, xr, top, bot, lean, min(y + ln, bot), fr)
        out.append(ribbon([(x0_, y), ((x0_ + x1_) / 2 + rng.normal(0, 2.2), y + ln / 2), (x1_ + rng.normal(0, 2), y + ln)], w=rng.uniform(*w), taper=(.35, .5), wob=.2))
    return out
PILES = [(30, 178, -40, 1800, .002), (190, 300, 150, 1800, -.010), (298, 382, 372, 1800, -.011)]
use('piles'); marks([pile(*p) for p in PILES], PILE)
use('pileplane')
marks([lit_plane(*p) for p in PILES], PILE2)
marks(sum([grain(*p, n=int(34 * (p[1] - p[0]) / 110), hi=.74) for p in PILES], []), PILE2, opacity=.8)
marks(sum([grain(*p, n=7, long=(160, 620), w=(1.8, 3.4)) for p in PILES], []), CHECK)
# knots, and end grain catching the sky
marks([spline(blob(x, y, 9, 15, n=7, rough=.2), closed=True) for x, y in ((110, 420), (240, 905), (330, 1340), (95, 1490))], CHECK)
marks([np.array([(178, 152), (214, 143), (284, 148), (280, 160), (200, 164)]), np.array([(286, 374), (320, 366), (366, 372), (358, 384), (300, 386)])], '#55524a')
# lashings: wire rope, seven turns, sagging between piles
use('lash')
wraps = []
for yc, n in ((636, 7), (1226, 6)):
    for i in range(n):
        y = yc + i * 7.5 + rng.normal(0, .8)
        wraps.append(ribbon([(56, y - 3), (170, y + 6), (188, y + 2), (292, y + 8), (300, y + 5), (386, y + 9 - i * .6)], w=2.3, taper=(0, 0), wob=.06))
marks(wraps, '#4b4944')
# ---- the short pile, 8 m out, clear of the cluster so the bird has water behind it
hx0, hx1, htop, hwl = 476, 566, 962, 1418
sp = (hx0, hx1, htop, hwl + 2, .004)
use('stump')
marks([pile(*sp, chew=7)], PILE)
marks([lit_plane(*sp)], PILE2)
marks(grain(*sp, n=16, hi=.74, long=(40, 200)), PILE2, opacity=.8); marks(grain(*sp, n=4, long=(90, 260), w=(1.6, 2.8)), CHECK)
marks([np.array([(hx0 + 7, htop + 5), (hx0 + 22, htop - 3), (hx1 - 12, htop - 2), (hx1 - 2, htop + 6), (hx1 - 20, htop + 11), (hx0 + 18, htop + 11)])], '#8f9288')
marks([wobble([(hx0 - 1, hwl - 44), (hx1 + 2, hwl - 40), (hx1 + 2, hwl + 2), (hx0 - 1, hwl + 2)], amp=1.2, step=14)], '#100f0f')        # wet band
marks([chip(rng.uniform(hx0 + 3, hx1), hwl - 46 - abs(rng.normal(0, 22)), rng.uniform(1.1, 2.4)) for _ in range(170)], '#73776f')    # barnacles
use('stumprefl')
marks(ticks((hx0 + hx1) / 2 + 2, hwl + 3, hwl + 300, (hx1 - hx0) * 1.02, grow=1.15, th=3.4, jitter=.1, gap=.22), '#0f151c')
marks([lens(hx0 - 26, hwl + 1, hx1 - hx0 + 52, 2.0)], '#566a74')                                                                   # the line where water meets wood
use('heron')
heron((hx0 + hx1) / 2 - 2, htop + 2, s=.58, flip=True,
      pal=dict(body='#1e262d', tip='#11161a', neck='#44423f', head='#cfcdbf', bill=PAL['lamp2'], plume='#566573', leg='#0f0f0f', thigh='#3d302b'))
