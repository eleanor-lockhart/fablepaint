# Study 2b: the same heron and ferry as 2a, and the fir from study 1, redrawn AFTER studying photographs.
exec(open('../atelier/kit.py').read())
exec(open('../atelier/subjects/heron.py').read())
exec(open('../atelier/subjects/ferry.py').read())
layer('paper'); fill(PAPER)
PAN = [(20, 20, 653, 620), (673, 20, 1306, 620), (20, 640, 1306, 1060)]
layer('base'); layer('far'); layer('mid'); layer('dark'); layer('light'); layer('key', blend='multiply')

# ---------------- heron
x0, y0, x1, y1 = window(*PAN[0])
use('base'); select_rect(x0, y0, x1, y1); gradient('linear', (0, y0), (0, y1), ramp('#5d7478', '#93a49d', '#b9bca8')); select_none()
marks([np.array([(x0, y1), (x0, y1 - 62), (x1, y1 - 54), (x1, y1)])], '#48606a')
use('dark')
px_, py_ = x0 + 300, y1 - 66                                  # the top of a piling for it to stand on
marks([wobble([(px_ - 46, y1 + 4), (px_ - 44, py_ + 8), (px_ - 30, py_), (px_ + 34, py_), (px_ + 46, py_ + 9), (px_ + 48, y1 + 4)], .6)], '#22282b')
cut([seg((px_ + d, py_ + 10), (px_ + d + 1, y1), w=1.4) for d in (-28, -12, 6, 24)], depth=.35)
use('mid'); heron(x0 + 300, y1 - 66, s=.74)

# ---------------- ferry at night, three-quarter view off the starboard bow
x0, y0, x1, y1 = window(*PAN[1])
use('base'); select_rect(x0, y0, x1, y1)
gradient('linear', (0, y0), (0, y1), ramp('#121a24', ('#1c2a38', .30), ('#33485a', .52), ('#263848', .535), ('#19242f', .75), '#111921')); select_none()
eye = (150, 125, 4)
P = camera(eye=eye, look=(0, 0, 8), fov=62, centre=((x0 + x1) / 2, y0 + 300))
use('mid'); info = ferry(P, eye, night=True)
use('light')
c = info['pal']
for x in np.arange(-41, 42, 4.6):
    wx, wy = P(x, 13.7, 0)
    marks(ticks(wx, wy + 5, wy + 60 + 150 * rng.uniform(.3, 1), 7, grow=1.5, th=1.9, gap=.6), c['lamp'], opacity=.9)
for (lx, ly) in info['mast_lights']:
    marks([blob(lx, ly, 2.2, 2.2, n=8, rough=.05)], c['nav_w'])
sx_, sy_ = info['side_light']; marks([blob(sx_, sy_, 2.4, 2.4, n=8, rough=.05)], c['nav_g'])

# ---------------- firs
x0, y0, x1, y1 = window(*PAN[2])
use('base'); select_rect(x0, y0, x1, y1); gradient('linear', (0, y0), (0, y1), ramp('#6c8083', '#9aa9a2', '#c2c2ae')); select_none()
baren(.05, seed=3)
use('far')
tr, fo = [], []
for x in np.arange(x0 - 20, x1 + 30, 34):
    t_, f_ = conifer(x + rng.normal(0, 8), y1 - 60 + rng.uniform(-14, 10), rng.uniform(130, 230), rng.uniform(34, 52), crown=.8)
    tr += t_; fo += f_
marks(tr + fo, '#8b9f9d')
lock(True); gradient('linear', (0, y1 - 190), (0, y1 - 40), [(0, '#c2c2ae', 0), (.6, '#c2c2ae', .3), (1, '#c2c2ae', .9)]); lock(False)
use('mid')
tr, fo = [], []
for x in (x0 + 90, x0 + 230, x0 + 300, x0 + 520, x0 + 800, x0 + 880, x0 + 1150):
    t_, f_ = conifer(x, y1 - 26 + rng.uniform(-8, 8), rng.uniform(250, 360), rng.uniform(84, 120), crown=rng.uniform(.6, .8), lean=rng.normal(0, .012))
    tr += t_; fo += f_
marks(tr + fo, '#4b6264')
use('dark')
t_, f_ = conifer(x0 + 640, y1 + 40, 560, 230, crown=.74, lean=.01, trunk_w=17)
marks(t_ + f_, '#171e20')
t_, f_ = conifer(x0 + 1040, y1 + 60, 760, 300, crown=.62, lean=-.008, trunk_w=24)
marks(t_ + f_, '#171e20')
marks([np.array([(x0, y1), (x0, y1 - 30), (x0 + 400, y1 - 44), (x0 + 900, y1 - 28), (x1, y1 - 40), (x1, y1)])], '#171e20')

finish(0, 0, W, H, border=False, tooth=.3)
use('key'); _CLIP[0] = None
marks([seg(a, b, w=1.6) for (a0, b0, a1, b1) in PAN for a, b in (((a0, b0), (a1, b0)), ((a1, b0), (a1, b1)), ((a1, b1), (a0, b1)), ((a0, b1), (a0, b0)))], KEY)
layer('gutter', below='key'); fill(PAPER)
m = np.ones((H, W), np.float32)
for (a0, b0, a1, b1) in PAN: m[b0:b1, a0:a1] = 0
modulate(m)
