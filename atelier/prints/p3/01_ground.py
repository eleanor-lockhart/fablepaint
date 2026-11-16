exec(open('../atelier/prints/p3/common.py').read())
window(X0, Y0, X1, Y1)
mx, my, mr = MOON
layer('paper'); fill(PAPER)
block('sky'); select_rect(X0 - 4, Y0 - 4, X1 + 4, HZ + 6)
gradient('linear', (0, Y0), (0, HZ), ramp(NIGHT, ('#1b2b3b', .45), ('#3a5062', .85), '#506878'))
woodgrain(.02, 'v', seed=6); select_none()
# ---- the moon: a plain disc of bare paper, no halo
block('moon')
a = np.linspace(0, 2 * np.pi, 90)
marks([np.c_[mx + mr * np.cos(a), my + mr * np.sin(a)]], PAPERW)
marks([spline(blob(mx - 34, my - 40, 34, 22, n=8, rough=.3), closed=True), spline(blob(mx + 30, my - 10, 22, 30, n=8, rough=.3), closed=True), spline(blob(mx - 10, my + 46, 30, 16, n=8, rough=.3), closed=True)], '#dcd6c4')
block('clouds')
marks([cloudband(X0 + 640, 250, 520, 22), cloudband(X0 + 760, 300, 380, 14), cloudband(X0 - 40, 470, 330, 18)], '#1d2d3c')
# ---- Rainier, a ghost under the moon
block('rainier')
marks([wobble(np.array([(1010, HZ), (1070, 548), (1108, 520), (1124, 512), (1140, 522), (1180, 556), (1230, HZ)]), .6, 18)], '#465c6c')
marks([wobble(np.array([(1092, 532), (1108, 520), (1124, 512), (1140, 522), (1154, 534), (1138, 530), (1126, 540), (1112, 529)]), .4, 10)], '#7f949c')
# ---- water
block('water'); select_rect(X0 - 4, HZ, X1 + 4, Y1 + 4)
gradient('linear', (0, HZ), (0, Y1), ramp('#6f8792', ('#4b6274', .12), ('#2c4155', .4), ('#1a2838', .7), NIGHT))
woodgrain(.02, 'h', seed=8); select_none()
# ---- the city on the far shore, burning in three places
block('city')
sky_pts = [(X0 - 10, HZ + 2)]
x = X0 - 10
while x < X1 + 20:
    wd = rng.uniform(8, 26)
    downtown = math.exp(-((x - 800) / 150.0) ** 2)
    h = 6 + rng.uniform(0, 10) + 44 * downtown * rng.uniform(.3, 1)
    if 430 < x < 630: h = min(h, 9)                       # keep the skyline low behind the machine's legs
    sky_pts += [(x, HZ - h), (x + wd, HZ - h)]
    x += wd
sky_pts.append((X1 + 20, HZ + 2))
marks([np.array(sky_pts)], CITY)
nx = 694                                                   # the Space Needle
marks([np.array([(nx - 3, HZ), (nx - 1.5, HZ - 40), (nx - 9, HZ - 47), (nx - 13, HZ - 50), (nx - 9, HZ - 54), (nx - 1, HZ - 56), (nx, HZ - 72),
                 (nx + 1, HZ - 56), (nx + 9, HZ - 54), (nx + 13, HZ - 50), (nx + 9, HZ - 47), (nx + 1.5, HZ - 40), (nx + 3, HZ)])], CITY)
block('citylights')
wl = [np.array([(x, y), (x + 2, y), (x + 2, y + 2), (x, y + 2)]) for x, y in [(rng.uniform(640, 980), HZ - rng.uniform(4, 34)) for _ in range(60)] + [(rng.uniform(100, 400), HZ - rng.uniform(3, 9)) for _ in range(14)]]
marks(wl, '#d9c184')
fires = [(318, HZ - 8, 1.0), (752, HZ - 30, 1.3), (1004, HZ - 12, .9)]
marks([np.array([(fx - 9 * k, fy + 6), (fx - 5 * k, fy - 8 * k), (fx - 1 * k, fy - 2 * k), (fx + 2 * k, fy - 15 * k), (fx + 6 * k, fy - 4 * k), (fx + 10 * k, fy + 6)]) for fx, fy, k in fires], FIRE)
block('smoke', below='city')
for fx, fy, k in fires:
    marks([cloudband(fx - 10, fy - 30 * k - i * 26, 150 + i * 90, 20 + i * 5, ragged=.6) for i in range(3)], '#1a2733')
# ---- the moon road
block('road')
marks(sheen(mx - 70, mx + 70, HZ + 4, HZ + 170, th0=1.6, th1=3.0, breakup=3, keep=.5), PAPERW)
marks(ticks(mx, HZ + 120, Y1 - 10, 170, grow=4.2, th=2.6, jitter=.3, gap=.45), PAPERW)
marks(ticks(mx + 40, HZ + 400, Y1 - 10, 260, grow=2.6, th=3.0, jitter=.5, gap=1.2), PAPERW)
