# Study 0: "Night ferry", painted from memory BEFORE any research or reference.
# Self-contained on purpose: this is the baseline.
RESET = dict(tip='round', size=20, hardness=.8, opacity=1, flow=1, spacing=.1, angle=0, roundness=1, follow=False,
             scatter=0, count=1, size_jitter=0, angle_jitter=0, flow_jitter=0, hue_jitter=0, sat_jitter=0,
             val_jitter=0, psize=True, pflow=False, taper=(0, 0), blend='normal', mix=0, grain=0, smooth=True)
def B(**kw):
    brush(**{**RESET, **kw})
KEY = '#161b2e'
def kline(pts, w=3.0, taper=(.15, .15), wob=.18, color=KEY, smooth=True):
    P = np.array(path(pts) if (smooth and len(pts) > 2) else pts, dtype=float)
    if len(P) < 8:
        P = np.concatenate([np.linspace(P[i], P[i + 1], 8, endpoint=False) for i in range(len(P) - 1)] + [P[-1:]])
    d = np.r_[0, np.cumsum(np.hypot(*np.diff(P, axis=0).T))]
    t = d / max(d[-1], 1e-6)
    prof = np.ones_like(t)
    if taper[0] > 0: prof *= np.clip(t / taper[0], 0, 1) ** .7
    if taper[1] > 0: prof *= np.clip((1 - t) / taper[1], 0, 1) ** .7
    ph = rng.uniform(0, 6.28, 3)
    wv = sum(np.sin((i + 1) * 3.1 * t * (1 + d[-1] / 300) + ph[i]) / (i + 1) for i in range(3))
    wd = np.maximum(w * prof * (1 + wob * wv), .5)
    tg = np.gradient(P, axis=0)
    n = np.c_[-tg[:, 1], tg[:, 0]]
    n /= np.maximum(np.hypot(n[:, 0], n[:, 1]), 1e-6)[:, None]
    L, R = P + n * wd[:, None] / 2, P - n * wd[:, None] / 2
    fill_poly([tuple(p) for p in np.r_[L, R[::-1]]], color)

X0, Y0, X1, Y1 = 50, 50, 850, 1230          # image area inside the paper margin
HZ = 560
PAPER = '#ebe2ce'
layer('paper'); fill(PAPER)

# --- sky block with a gradation: indigo at the top, afterglow at the horizon
layer('sky'); select_rect(X0, Y0, X1, HZ + 4)
gradient('linear', (0, Y0), (0, HZ), [(0, '#18244a'), (.35, '#2b4573'), (.7, '#5f8a9c'), (.9, '#b9c3a8'), (1, '#e3cfa6')])
select_none()
B(size=3, hardness=.9, psize=False)
dabs([(rng.uniform(X0 + 20, X1 - 20), rng.uniform(Y0 + 15, 330), rng.uniform(.5, 1.2)) for _ in range(34)], color='#e8e4d0')

# --- far shore: two ranges, each lighter at its foot (mist)
layer('hills_far')
pts = [(X0, HZ)] + [(x, HZ - 34 - 26 * math.sin(x / 97.0) - 16 * math.sin(x / 41.0 + 1)) for x in range(X0, X1 + 1, 20)] + [(X1, HZ)]
fill_poly(pts, '#6c8aa0', smooth=False)
layer('hills_near')
pts = [(X0, HZ)] + [(x, HZ - 14 - 20 * max(0, math.sin(x / 130.0 + 2)) - 7 * math.sin(x / 33.0)) for x in range(X0, X1 + 1, 16)] + [(X1, HZ)]
fill_poly(pts, '#2c4467')
lock(True); gradient('linear', (0, HZ - 40), (0, HZ), [(0, '#2c4467', 0), (1, '#7f9cab', .7)]); lock(False)

# --- water
layer('water'); select_rect(X0, HZ, X1, Y1)
gradient('linear', (0, HZ), (0, Y1), [(0, '#d5c9a6'), (.06, '#8fa9ad'), (.3, '#3f6288'), (1, '#131e40')])
select_none()

# --- the ferry, from memory: double-ended, two pilot houses, a central stack
fx0, fx1, wl = 300, 680, 552
layer('ferry')
fill_poly([(fx0 + 8, wl), (fx0, wl - 14), (fx0 + 6, wl - 20), (fx1 - 6, wl - 20), (fx1, wl - 14), (fx1 - 8, wl)], '#16283a')     # hull
fill_poly([(fx0 + 10, wl - 20), (fx0 + 16, wl - 40), (fx1 - 16, wl - 40), (fx1 - 10, wl - 20)], '#a9bcc4')                    # car deck
fill_rect(fx0 + 40, wl - 58, fx1 - 40, wl - 40, color='#b7c8cd')                                                              # passenger deck
fill_rect(fx0 + 54, wl - 64, fx1 - 54, wl - 58, color='#8ea5b0')                                                              # sun deck edge
for cx in (fx0 + 78, fx1 - 78):
    fill_poly([(cx - 17, wl - 64), (cx - 14, wl - 80), (cx + 14, wl - 80), (cx + 17, wl - 64)], '#b7c8cd')                    # pilot houses
fill_poly([(468, wl - 64), (472, wl - 92), (508, wl - 92), (512, wl - 64)], '#9db2bb')                                        # stack
fill_rect(471, wl - 86, 509, wl - 79, color='#2c6a55')
layer('lights')
for x in range(fx0 + 48, fx1 - 46, 9):
    fill_rect(x, wl - 54, x + 5, wl - 45, color='#f8cf73')
for x in range(fx0 + 30, fx1 - 30, 22):
    fill_rect(x, wl - 35, x + 13, wl - 25, color='#f1b755')
for cx in (fx0 + 78, fx1 - 78):
    fill_rect(cx - 11, wl - 76, cx + 11, wl - 70, color='#f8cf73')
# reflections: broken warm streaks
layer('refl')
for x in range(fx0 + 30, fx1 - 30, 11):
    y = wl + 6
    while y < wl + 150 + rng.uniform(-40, 60):
        ln = rng.uniform(5, 14)
        fill_rect(x + rng.uniform(-2, 2), y, x + rng.uniform(4, 7), y + ln, color='#f0b85a', opacity=max(.12, .8 - (y - wl) / 190))
        y += ln + rng.uniform(4, 12)

# --- key block: selective line
layer('key', blend='multiply')
for cx in (fx0 + 78, fx1 - 78):
    kline([(cx, wl - 80), (cx, wl - 108)], w=1.4, taper=(0, .5), smooth=False)
kline([(fx0, wl - 14), (fx0 + 6, wl - 20), (fx1 - 6, wl - 20), (fx1, wl - 14)], w=1.5, smooth=False)
kline([(fx0 + 8, wl + 1), (fx1 - 8, wl + 1)], w=2.2, smooth=False)
# wave lines, wider apart and longer toward the bottom
y = HZ + 16
while y < Y1 - 6:
    f = (y - HZ) / (Y1 - HZ)
    for _ in range(int(9 - 5 * f)):
        x = rng.uniform(X0, X1); ln = rng.uniform(20, 50) * (1 + 3 * f)
        kline([(x, y), (x + ln / 2, y - 1.5 - 3 * f), (x + ln, y)], w=1.0 + 2.2 * f, taper=(.45, .45), color='#0f1838')
    y += 7 + 30 * f

# --- foreground: dock pilings with a gull
layer('piles')
for (x, top, wd) in ((120, 760, 34), (168, 700, 38), (214, 800, 32)):
    fill_poly([(x - wd / 2, Y1), (x - wd / 2 + 3, top + 8), (x - wd / 4, top), (x + wd / 4, top), (x + wd / 2 - 3, top + 8), (x + wd / 2, Y1)], '#0e1428')
fill_rect(96, 890, 240, 912, color='#0e1428')
fill_poly([(150, 700), (160, 688), (176, 684), (188, 690), (196, 686), (190, 697), (176, 700)], '#d9dccf')   # gull
use('key')
kline([(176, 700), (176, 708)], w=1.2, smooth=False, color='#d09a4a')

# --- paper margin back on top, border, tooth
layer('margin'); fill(PAPER); select_rect(X0, Y0, X1, Y1); clear(); select_none()
use('key')
for a, b in (((X0, Y0), (X1, Y0)), ((X1, Y0), (X1, Y1)), ((X1, Y1), (X0, Y1)), ((X0, Y1), (X0, Y0))):
    kline([a, b], w=2.0, taper=(0, 0), wob=.1, smooth=False)
layer('tooth', blend='multiply')
clouds('#d8d8d8', '#ffffff', scale=1.2, octaves=3, seed=4, opacity=1)
props('tooth', opacity=.35)
