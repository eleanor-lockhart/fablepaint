# Study 1: materials sheet. Six panels, one material problem each, after looking at real prints.
exec(open('../atelier/kit.py').read())
layer('paper'); fill(PAPER)
PAN = [(20 + 433 * i, 20 + 440 * j, 440 + 433 * i, 440 + 440 * j) for j in range(2) for i in range(3)]
def panel(k):
    r = PAN[k]; window(*r); return r
def flat(r, stops, y0=None, y1=None):
    select_rect(r[0], r[1] if y0 is None else y0, r[2], r[3] if y1 is None else y1)
    gradient('linear', (0, r[1] if y0 is None else y0), (0, r[3] if y1 is None else y1), stops)
def band(x, y, ln, th, n=7):
    xs = np.linspace(x, x + ln, n)
    top = [(xs[i], y - th * (.5 if 0 < i < n - 1 else 0) * rng.uniform(.6, 1.1)) for i in range(n)]
    bot = [(xs[i], y + th * (.5 if 0 < i < n - 1 else 0) * rng.uniform(.5, 1.2)) for i in range(n - 2, 0, -1)]
    return spline(top + bot, closed=True)

layer('base'); layer('mid'); layer('dark'); layer('light'); layer('key', blend='multiply'); layer('weather')

# ---------- 1. dusk sky: gradation, grain, stepped cloud bands
x0, y0, x1, y1 = r = panel(0)
use('base'); flat(r, ramp('#1b2738', '#2c4257', '#5f7c84', '#a9b1a0', '#d9cbb0'))
woodgrain(.10, 'v', seed=1); baren(.05, seed=2); select_none()
use('mid')
marks([band(x0 - 30, y0 + 215, 300, 26), band(x0 + 150, y0 + 250, 330, 20), band(x0 + 40, y0 + 160, 180, 12)], '#33485b')
marks([band(x0 + 10, y0 + 232, 250, 9), band(x0 + 190, y0 + 262, 260, 7)], '#8c9f99')
use('light')
marks([band(x0 + 60, y0 + 290, 400, 22), band(x0 - 40, y0 + 318, 260, 12)], '#e2d2b4')
use('dark'); marks([np.array([(x0, y1), (x0, y1 - 46), (x0 + 120, y1 - 52), (x0 + 260, y1 - 40), (x1, y1 - 48), (x1, y1)])], '#1a2226')

# ---------- 2. water: light at the far edge, dark at the feet; reflections as ticks
x0, y0, x1, y1 = r = panel(1)
use('base'); flat(r, ramp('#aab2a2', '#d9cbb0'), y1=y0 + 62)
flat(r, ramp('#b9bca8', '#7f9698', '#48637a', '#243648', '#18222e'), y0=y0 + 62)
woodgrain(.08, 'h', seed=3); select_none()
use('dark')
marks([np.array([(x0, y0 + 64), (x0, y0 + 40), (x0 + 90, y0 + 30), (x0 + 150, y0 + 44), (x0 + 250, y0 + 38), (x0 + 330, y0 + 48), (x1, y0 + 42), (x1, y0 + 64)])], '#1c262c')
marks(sum([ticks(x, y0 + 68, y0 + 150 + 60 * rng.uniform(), 34, th=2.0, gap=.6) for x in range(x0 + 20, x1, 38)], []), '#2c3e4c', opacity=.9)
use('light')
marks([np.array([(x0 + 118, y0 + 50), (x0 + 124, y0 + 50), (x0 + 124, y0 + 58), (x0 + 118, y0 + 58)])], '#ecd08e')
marks(ticks(x0 + 121, y0 + 68, y0 + 300, 9, grow=2.2, th=1.8), '#e3bf78')
marks(ticks(x0 + 300, y0 + 70, y1 - 20, 16, grow=5.0, th=2.2, gap=.5), '#e6dcc2')       # a moon road
use('base'); cut(ripples(x0, y0 + 90, x1, y1, n=70, len0=14, len1=90, th0=.8, th1=1.8), depth=.45)
use('dark'); marks(ripples(x0, y0 + 240, x1, y1, n=22, len0=40, len1=150, th0=1.5, th1=3.2), '#121a24')

# ---------- 3. night rain: values close together, slit windows with no glow, puddles
x0, y0, x1, y1 = r = panel(2)
use('base'); flat(r, ramp('#121820', '#1a2632', '#2c4050'), y1=y0 + 270)
woodgrain(.09, 'v', seed=5); select_none()
flat(r, ramp('#2c2a27', '#201e1c'), y0=y0 + 268); select_none()
use('dark')
houses = [[(x1 - 190, y0 + 280), (x1 - 190, y0 + 150), (x1 - 100, y0 + 90), (x1 + 10, y0 + 150), (x1 + 10, y0 + 280)],
          [(x1 - 290, y0 + 280), (x1 - 290, y0 + 190), (x1 - 235, y0 + 150), (x1 - 180, y0 + 190), (x1 - 180, y0 + 280)],
          [(x0 + 40, y0 + 280), (x0 + 40, y0 + 222), (x0 + 82, y0 + 196), (x0 + 130, y0 + 222), (x0 + 130, y0 + 280)]]
marks([wobble(h, .6) for h in houses], '#1b1918')
use('mid')
pud = [blob(x0 + 150, y0 + 318, 95, 9, n=12, rough=.3, rot=0), blob(x0 + 300, y0 + 352, 110, 14, n=12, rough=.3, rot=0), blob(x0 + 120, y0 + 398, 150, 20, n=13, rough=.3, rot=0)]
marks([spline(p, closed=True) for p in pud], '#34485a')
use('light')
wins = [(x1 - 150, y0 + 205, 7, 34), (x1 - 250, y0 + 222, 5, 22), (x0 + 84, y0 + 240, 5, 16)]
marks([np.array([(x, y), (x + w, y), (x + w, y + h), (x, y + h)]) for x, y, w, h in wins], '#ead59c')
_CLIP[0] = _CLIP[0] * raster([spline(p, closed=True) for p in pud])           # reflections only where there is water
marks(sum([ticks(x + w / 2, y0 + 300, y1, w + 3, grow=1.4, th=2.0, gap=.4) for x, y, w, h in wins], []), '#e0c27e')
panel(2)
use('mid')
fx, fy = x0 + 215, y0 + 300                                                    # walker under an umbrella
marks([np.array([(fx - 5, fy + 6), (fx + 5, fy + 6), (fx + 7, fy + 34), (fx + 2, fy + 34), (fx, fy + 22), (fx - 2, fy + 34), (fx - 7, fy + 34)])], '#15171a')
marks([np.array([(fx - 22, fy + 8), (fx - 12, fy - 4), (fx, fy - 8), (fx + 12, fy - 4), (fx + 22, fy + 8)])], '#b08a4a')
use('key'); marks([seg((fx, fy - 8), (fx, fy + 10), w=1.2)], KEY)
use('weather')
marks(rain(x0, y0, x1, y1, n=120, angle=66, w=1.0), '#0b0f14', opacity=.7)
marks(rain(x0, y0, x1, y1, n=45, angle=63, w=.9), '#93a5ab', opacity=.32)

# ---------- 4. snow: white paper sitting on black, a speckled shadow tone, chips falling
x0, y0, x1, y1 = r = panel(3)
use('base'); flat(r, ramp('#22323b', '#3a515b', '#56707a'))
baren(.10, seed=8); select_none()
use('dark')
hut = [(x0 + 60, y1 - 60), (x0 + 60, y0 + 200), (x0 + 180, y0 + 120), (x0 + 300, y0 + 200), (x0 + 300, y1 - 60)]
marks([wobble(hut, .6)], '#191b1d')
cut([seg((x, y0 + 150), (x, y1 - 60), w=1.2) for x in range(x0 + 72, x0 + 300, 15)], depth=.3)
use('light')
roofL = spline([(x0 + 36, y0 + 214), (x0 + 110, y0 + 150), (x0 + 180, y0 + 96), (x0 + 250, y0 + 150), (x0 + 326, y0 + 214), (x0 + 318, y0 + 236), (x0 + 250, y0 + 190), (x0 + 180, y0 + 142), (x0 + 110, y0 + 190), (x0 + 44, y0 + 238)], closed=True)
ground = spline([(x0 - 20, y1 + 20), (x0 - 20, y1 - 52), (x0 + 90, y1 - 66), (x0 + 200, y1 - 54), (x0 + 320, y1 - 70), (x1 + 20, y1 - 58), (x1 + 20, y1 + 20)], closed=True)
marks([roofL, ground], '#edeadc')
marks([np.array([(x0 + 170, y0 + 250), (x0 + 196, y0 + 250), (x0 + 196, y0 + 290), (x0 + 170, y0 + 290)])], '#e0a55e')
layer('snowshade', blend='multiply', above='light')
marks([band(x0 + 60, y0 + 196, 110, 26), band(x0 + 200, y0 + 196, 110, 24), band(x0 - 10, y1 - 26, 250, 26), band(x0 + 240, y1 - 34, 200, 20)], '#9fb2b8')
select_rect(*r); baren(.0, seed=4, goma=.34); select_none()
use('weather')
marks(snowfall(x0, y0, x1, y1, n=520), '#edeadc')

# ---------- 5. broadleaf mass against the light band
x0, y0, x1, y1 = r = panel(4)
use('base'); flat(r, ramp('#253a4e', '#4c6a78', '#93a59c', ('#dccdb0', .72), ('#b9bba6', .8), '#7d9596'))
woodgrain(.08, 'v', seed=9); select_none()
use('dark')
marks([np.array([(x0, y1), (x0, y1 - 70), (x0 + 200, y1 - 78), (x1, y1 - 66), (x1, y1)])], '#27363a')
trees = [(x0 + 95, 250, 1.0), (x0 + 160, 300, 1.15), (x0 + 228, 215, .9), (x0 + 330, 120, .6)]
fol, trunks = [], []
for tx, th, sc in trees:
    by = y1 - 72
    trunks.append(ribbon([(tx, by), (tx + rng.normal(0, 3), by - th * .5), (tx + rng.normal(0, 4), by - th)], w=5 * sc, taper=(0, .9), wob=.1))
    yy = by - th * .22
    while yy > by - th * 1.02:
        f = (by - yy) / th
        wd = (16 + 30 * math.sin(math.pi * min(f * 1.1, 1)) ** .7) * sc
        ox = rng.normal(0, 7 * sc)
        fol += foliage(tx + ox, yy, wd * rng.uniform(.6, 1.1), 20 * sc, n=int(46 * sc), leaf=5.5 * sc)
        if rng.uniform() < .5:
            s_ = rng.choice([-1, 1])
            trunks.append(ribbon([(tx, yy + 14), (tx + s_ * wd * .9, yy - 4)], w=1.6 * sc, taper=(0, .8)))
        yy -= rng.uniform(22, 40) * sc
marks(trunks, '#151a1c'); marks(fol, '#151a1c')
use('mid'); cut([]) 
marks([blob(x0 + rng.uniform(60, 250), y1 - rng.uniform(100, 330), 5, 3.5, n=6) for _ in range(46)], '#33504e')
marks(sum([blades(x, y1 - 68 + rng.uniform(-3, 8), n=5, length=20, w=1.5) for x in range(x0, x1, 9)], []), '#151a1c')

# ---------- 6. firs in three distances, reeds in front
x0, y0, x1, y1 = r = panel(5)
use('base'); flat(r, ramp('#62787c', '#8fa19c', '#b7bba9'))
baren(.06, seed=11); select_none()
use('mid')
far = sum([fir(x, y1 - 150 + rng.uniform(-8, 8), rng.uniform(90, 150), rng.uniform(40, 56)) for x in range(x0 - 10, x1 + 20, 26)], [])
marks(far, '#7d9392')
lock(True); gradient('linear', (0, y1 - 250), (0, y1 - 140), fade('#b7bba9', 0, .9, power=1)[::-1] if False else [(0, '#b7bba9', 0), (.6, '#b7bba9', .25), (1, '#b7bba9', .85)]); lock(False)
layer('mid2', above='mid')
marks(sum([fir(x, y1 - 96 + rng.uniform(-10, 10), rng.uniform(170, 250), rng.uniform(70, 96)) for x in (x0 + 40, x0 + 150, x0 + 215, x0 + 372)], []), '#3d5557')
use('dark')
marks(fir(x0 + 300, y1 + 30, 470, 190, droop=.4), '#161d1f')
marks([np.array([(x0, y1), (x0, y1 - 74), (x0 + 140, y1 - 92), (x0 + 250, y1 - 70), (x1, y1 - 84), (x1, y1)])], '#161d1f')
marks(sum([blades(x, y1 - 76 + 10 * math.sin(x / 40.0), n=6, length=46, w=2.2, spread=44) for x in range(x0, x1, 11)], []), '#161d1f')
use('light')
marks(sum([blades(x, y1 - 30 + rng.uniform(-20, 20), n=3, length=38, w=1.6, spread=50) for x in range(x0, x1, 17)], []), '#51686a')

finish(0, 0, W, H, border=False, tooth=.3)
use('key'); _CLIP[0] = None
marks([seg(a, b, w=1.6) for (px0, py0, px1, py1) in PAN for a, b in (((px0, py0), (px1, py0)), ((px1, py0), (px1, py1)), ((px1, py1), (px0, py1)), ((px0, py1), (px0, py0)))], KEY)
layer('gutter', below='key'); fill(PAPER)
m = np.ones((H, W), np.float32)
for (px0, py0, px1, py1) in PAN: m[py0:py1, px0:px1] = 0
modulate(m)
