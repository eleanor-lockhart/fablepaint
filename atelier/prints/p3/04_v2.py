exec(open('../atelier/prints/p3/common.py').read())
window(X0, Y0, X1, Y1)
# ---- sky again: on a clear night the board grain read as rain. Re-lay the gradation with almost none.
use('sky'); select_rect(X0 - 4, Y0 - 4, X1 + 4, HZ + 6)
gradient('linear', (0, Y0), (0, HZ), ramp(NIGHT, ('#1b2b3b', .45), ('#3a5062', .85), '#506878'))
woodgrain(.006, 'v', seed=6); select_none()
# ---- splash again: the first was shards of ice on an ice floe. Foam is lumps, like the snow pillows.
use('splash'); clear()
bx, by = 955, 1596
def plume(pth, r0, r1, n):
    """Thrown water: a chain of lumps shrinking along a curved path, with loose drops past the tip."""
    Pth = resample(spline(pth), step=4)
    out = []
    for i in range(n):
        t = (i / (n - 1)) ** .85
        j = int(t * (len(Pth) - 1)); r = r0 + (r1 - r0) * t
        out.append(blob(Pth[j][0] + rng.normal(0, r * .15), Pth[j][1] + rng.normal(0, r * .15), r * rng.uniform(.8, 1.2), r * rng.uniform(.8, 1.25), n=int(rng.integers(8, 12)), rough=.24))
    tip = Pth[-1]; d = Pth[-1] - Pth[-8]; d = d / max(np.hypot(*d), 1e-6)
    for k in range(7):
        q = tip + d * rng.uniform(8, 70) + rng.normal(0, 9, 2)
        out.append(chip(q[0], q[1], rng.uniform(1.6, 4.6)))
    return out
foam = []
for dx in np.arange(-330, 340, 34):                      # the mound round the whale: lumps along an arc
    yy = by + 34 - 58 * math.exp(-(dx / 190.0) ** 2) + rng.normal(0, 7)
    foam.append(blob(bx + dx, yy, rng.uniform(32, 56), rng.uniform(22, 36), n=11, rough=.22))
for dx in np.arange(-380, 400, 46):
    foam.append(blob(bx + dx + rng.normal(0, 12), by + 86 + rng.normal(0, 9), rng.uniform(40, 70), rng.uniform(20, 32), n=11, rough=.22))
foam.append(np.array([(bx - 330, by + 60), (bx + 340, by + 60), (bx + 340, by + 170), (bx - 330, by + 170)]))
marks(foam, PAPERW)
pl = []
for pth, r0, r1, n in (([(bx - 150, by + 6), (bx - 196, by - 86), (bx - 262, by - 150)], 26, 6, 9), ([(bx - 96, by - 6), (bx - 120, by - 120), (bx - 168, by - 232)], 30, 6, 11),
                        ([(bx - 40, by + 10), (bx - 46, by - 50), (bx - 60, by - 92)], 20, 6, 6), ([(bx + 96, by - 4), (bx + 124, by - 126), (bx + 178, by - 250)], 32, 6, 12),
                        ([(bx + 160, by + 4), (bx + 212, by - 80), (bx + 286, by - 136)], 26, 6, 9), ([(bx + 40, by + 8), (bx + 52, by - 44), (bx + 76, by - 84)], 18, 6, 6)):
    pl += plume(pth, r0, r1, n)
marks(pl, PAPERW)
drops = []
for _ in range(200):
    a = math.radians(rng.uniform(-70, 70)); r = 120 + 380 * rng.uniform() ** 1.8
    drops.append(chip(bx + r * math.sin(a), by - 40 - r * math.cos(a) * rng.uniform(.5, 1), max(1.1, 4.2 - r / 120)))
marks(drops, PAPERW)
# hollows in the foam, and dark water showing through it
marks([lens(bx + dx, by + dy, ln, th) for dx, dy, ln, th in ((-270, 70, 150, 12), (-80, 54, 120, 10), (90, 82, 170, 13), (-180, 120, 230, 11), (140, 128, 170, 9), (-10, 104, 110, 8))], MIDL)
cut([lens(bx + dx, by + dy, ln, th) for dx, dy, ln, th in ((-330, 96, 90, 9), (250, 60, 80, 8), (-240, 150, 120, 9), (40, 150, 150, 9), (-390, 60, 60, 7))], depth=1)
marks([lens(bx + rng.uniform(-600, 260), by + rng.uniform(-50, 120), rng.uniform(50, 170), rng.uniform(2.4, 4.6)) for _ in range(22)], PALE)
# water running off flipper and chin: unequal, not a comb
w = dict(fliptip=(485, 1314), chin=(508, 955))
fx, fy = w['fliptip']; cx_, cy_ = w['chin']
run = [ribbon([(fx + d, fy - 8), (fx + d + rng.normal(0, 2), fy + ln)], w=wd, taper=(.05, .85), wob=.15) for d, ln, wd in ((-14, 132, 3.0), (2, 58, 2.2), (17, 96, 2.6))]
run += [ribbon([(cx_ + d, cy_ + 4), (cx_ + d + rng.normal(0, 2), cy_ + ln)], w=wd, taper=(.05, .85), wob=.15) for d, ln, wd in ((0, 84, 2.2), (14, 40, 1.8))]
run += [chip(fx + d + rng.normal(0, 3), fy + ln + rng.uniform(10, 60), rng.uniform(1.5, 3)) for d, ln in ((-14, 132), (-14, 150), (2, 58), (17, 96), (17, 120))]
marks(run, PAPERW)
