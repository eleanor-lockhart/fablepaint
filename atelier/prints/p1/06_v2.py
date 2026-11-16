exec(open('../atelier/prints/p1/common.py').read())
window(X0, Y0, X1, Y1)
PILE, PILE2, CHECK = '#191716', '#2f2b27', '#0d0c0c'
def edge_x(xl, xr, top, bot, lean, y, frac):
    return xl + (xr - xl) * frac + lean * (bot - top) * (bot - y) / (bot - top)
def lit_plane(xl, xr, top, bot, lean, frac=.78):
    """Lit side of a pile: mostly a straight edge, with a few long shallow notches."""
    ys, y = [], max(top, Y0 - 20) + 16
    while y < min(bot, Y1 + 20):
        ys.append(y); y += rng.uniform(110, 330)
    ys.append(min(bot, Y1 + 20))
    inner, off = [], 0.0
    for a, b in zip(ys, ys[1:]):
        inner += [(edge_x(xl, xr, top, bot, lean, a + 14, frac + off), a + 14), (edge_x(xl, xr, top, bot, lean, b, frac + off), b)]
        off = rng.choice([-.045, 0, 0, .035])
    outer = [(edge_x(xl, xr, top, bot, lean, y, .985), y) for y in ys[::-1]]
    return np.array(inner + outer)
def grain(xl, xr, top, bot, lean, n, lo=.05, hi=.95, long=(50, 380), w=(.8, 1.7)):
    out = []
    for _ in range(n):
        y = rng.uniform(max(top, Y0) + 20, min(bot, Y1) - 30); ln = rng.uniform(*long)
        fr = rng.uniform(lo, hi)
        a, b = edge_x(xl, xr, top, bot, lean, y, fr), edge_x(xl, xr, top, bot, lean, min(y + ln, bot), fr)
        out.append(ribbon([(a, y), ((a + b) / 2 + rng.normal(0, 2.2), y + ln / 2), (b + rng.normal(0, 2), y + ln)], w=rng.uniform(*w), taper=(.35, .5), wob=.2))
    return out
PILES = [(30, 178, -40, 1800, .002), (190, 300, 150, 1800, -.010), (298, 382, 372, 1800, -.011)]
hx0, hx1, htop, hwl = 476, 566, 962, 1418
sp = (hx0, hx1, htop, hwl + 2, .004)
# ---- pile planes again: the stepped edge read as crenellations
use('pileplane'); clear()
marks([lit_plane(*p) for p in PILES], PILE2)
marks(sum([grain(*p, n=int(40 * (p[1] - p[0]) / 110), hi=.74) for p in PILES], []), PILE2, opacity=.8)
marks(sum([grain(*p, n=7, long=(160, 620), w=(1.8, 3.4)) for p in PILES], []), CHECK)
marks([spline(blob(x, y, 8, 14, n=7, rough=.2), closed=True) for x, y in ((110, 420), (240, 905), (330, 1340), (95, 1490))], CHECK)
marks([np.array([(178, 152), (214, 143), (284, 148), (280, 160), (200, 164)]), np.array([(286, 374), (320, 366), (366, 372), (358, 384), (300, 386)])], '#55524a')
# ---- lashings again: rope goes ROUND each pile, so it sags across each one separately
use('lash'); clear()
wraps = []
for yc, n in ((640, 7), (1228, 6)):
    for (xl, xr, top, bot, lean) in PILES:
        if top > yc - 30: continue
        dy = rng.normal(0, 2.5)
        for i in range(n):
            y = yc + i * 6.6 + dy
            a, b = edge_x(xl, xr, top, bot, lean, y, 0) + 1, edge_x(xl, xr, top, bot, lean, y, 1) - 1
            wraps.append(ribbon([(a, y - 5), ((a + b) / 2, y + 4), (b, y - 5)], w=2.0, taper=(0, 0), wob=.06))
marks(wraps, '#3d3b38')
# ---- the stump's plane too
use('stump'); clear()
def pile(xl, xr, top, bot, lean=0.0, chew=10):
    d = lean * (bot - top); tx = np.linspace(xl + d, xr + d, 7)
    crown = [(tx[i], top + rng.uniform(0, chew) - (chew * .8 if i in (2, 3) else 0)) for i in range(7)]
    return wobble([(xl, bot)] + crown + [(xr, bot)], amp=.9, step=40)
marks([pile(*sp, chew=7)], PILE)
marks([lit_plane(*sp)], PILE2)
marks(grain(*sp, n=18, hi=.74, long=(40, 200)), PILE2, opacity=.8); marks(grain(*sp, n=4, long=(90, 260), w=(1.6, 2.8)), CHECK)
marks([np.array([(hx0 + 7, htop + 5), (hx0 + 22, htop - 3), (hx1 - 12, htop - 2), (hx1 - 2, htop + 6), (hx1 - 20, htop + 11), (hx0 + 18, htop + 11)])], '#8f9288')
marks([wobble([(hx0 - 1, hwl - 44), (hx1 + 2, hwl - 40), (hx1 + 2, hwl + 2), (hx0 - 1, hwl + 2)], amp=1.2, step=14)], '#100f0f')
marks([chip(rng.uniform(hx0 + 3, hx1), hwl - 46 - abs(rng.normal(0, 22)), rng.uniform(1.1, 2.4)) for _ in range(170)], '#73776f')
# ---- heron: its neck was a separate brown blob; bring it into the bird
use('heron'); clear()
heron((hx0 + hx1) / 2 - 2, htop + 2, s=.58, flip=True,
      pal=dict(body='#1e262d', tip='#11161a', neck='#353b41', head='#cfcdbf', bill=PAL['lamp2'], plume='#566573', leg='#0f0f0f', thigh='#3d302b'))
# ---- the pale sliver: keep it only to the left of the ferry, behind the far shore
use('sliver'); clear()
marks([cloudband(X0 + 250, HZ - 40, 420, 22, ragged=.3), cloudband(X0 + 300, HZ - 16, 330, 11, ragged=.3)], PAL['pale'])
marks([cloudband(X0 + 330, HZ - 60, 300, 8, ragged=.3)], '#7f9193')
# ---- rain again: a third as much, hairline, in sheaves with gaps between
for nm in ('rain_dark', 'rain_pale', 'rings'):
    use(nm); clear()
def sheaves(n, k, **kw):
    out = []
    for _ in range(k):
        cx = rng.uniform(X0 - 100, X1 + 200); w_ = rng.uniform(60, 190)
        out += rain(cx - w_, Y0, cx + w_, Y1, n=n, **kw)
    return out
use('rain_dark'); marks(sheaves(7, 8, angle=106, w=.9, length=(.25, .75), spread=.9), '#0a0f15', opacity=.5)
use('rain_pale'); marks(sheaves(6, 9, angle=106, w=.75, length=(.18, .6), spread=.9), '#93a3a6', opacity=.2)
use('rings')
rr = []
for _ in range(24):
    f = rng.uniform(.15, 1) ** .7
    y = HZ + (Y1 - HZ) * f; x = rng.uniform(420, X1 - 10)
    rx = 3 + 24 * f * rng.uniform(.5, 1.25)
    full = rng.uniform() < .55
    rr.append(ring(x, y, rx, w=.9 + .5 * f, arc=(0, 360) if full else (rng.uniform(150, 200), rng.uniform(330, 400))))
    if rng.uniform() < .35:
        rr.append(ring(x, y, rx * .45, w=.8 + .3 * f))
marks(rr, '#667a82', opacity=.7)
