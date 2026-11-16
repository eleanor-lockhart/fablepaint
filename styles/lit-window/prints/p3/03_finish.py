exec(open('../styles/lit-window/prints/p3/common.py').read())
window(X0, Y0, X1, Y1)
mx, my, mr = MOON
# ---- moon road again: broken, thickening toward us
use('road'); clear()
marks(moonroad(mx, HZ + 4, Y1 - 6, w0=130, w1=700, th0=1.7, th1=5.2), PAPERW)
# ---- whale again (flank patch was notched; no saddle)
use('whale'); clear()
w = orca(950, 1575, s=1.6, flip=True, rot=20.6, pal=dict(black=BLACK, white=PALE, saddle=None, tooth=PAPERW))
# ---- the splash: stepped foam, tongues thrown up beside the body, chips of spray, water running off
block('splash')
bx, by = 955, 1590
base = [(bx - 320, by + 64), (bx - 262, by + 22), (bx - 190, by + 6), (bx - 128, by - 20), (bx - 70, by - 12), (bx - 20, by + 4), (bx + 44, by - 6), (bx + 96, by - 30),
        (bx + 150, by - 14), (bx + 214, by + 10), (bx + 280, by + 44), (bx + 330, by + 76), (bx + 330, by + 170), (bx - 320, by + 170)]
marks([wobble(np.array(base), 1.3, 16)], PAPERW)
tongues = []
for dx, h, lean in ((-235, 60, -.7), (-185, 130, -.5), (-140, 215, -.34), (-98, 120, -.2), (-30, 46, -.05), (36, 58, .1), (104, 150, .22), (150, 250, .36), (200, 150, .5), (250, 70, .7)):
    wd = rng.uniform(15, 27)
    tongues.append(np.array([(bx + dx - wd, by + 14), (bx + dx - wd * .5 + lean * h * .45, by - 8 - h * .55), (bx + dx + lean * h, by - 10 - h),
                             (bx + dx + wd * .45 + lean * h * .62, by - 8 - h * .5), (bx + dx + wd, by + 14)]))
marks(tongues, PAPERW)
drops = []
for _ in range(260):
    a = math.radians(rng.uniform(-78, 78)); r = 70 + 430 * rng.uniform() ** 1.7
    drops.append(chip(bx + r * math.sin(a), by - 30 - r * math.cos(a) * rng.uniform(.45, 1), max(1.1, 4.6 - r / 110)))
marks(drops, PAPERW)
marks([lens(bx + dx, by + dy, ln, th) for dx, dy, ln, th in ((-250, 60, 190, 14), (-60, 34, 150, 12), (70, 70, 200, 16), (-160, 104, 260, 12), (120, 116, 190, 10))], MIDL)
marks([lens(bx + rng.uniform(-560, 240), by + rng.uniform(-40, 130), rng.uniform(50, 170), rng.uniform(2.4, 4.6)) for _ in range(26)], PALE)
fx, fy = w['fliptip']; cx_, cy_ = w['chin']
run = [ribbon([(fx + d, fy - 6), (fx + d + rng.normal(0, 2), fy + ln)], w=rng.uniform(1.6, 3.0), taper=(.05, .8), wob=.1) for d, ln in ((-18, 60), (-8, 120), (2, 80), (12, 150), (22, 50))]
run += [ribbon([(cx_ + d, cy_ + 4), (cx_ + d + rng.normal(0, 2), cy_ + ln)], w=rng.uniform(1.4, 2.4), taper=(.05, .8), wob=.1) for d, ln in ((-4, 50), (8, 90), (20, 40))]
marks(run, PAPERW)
# ---- the battle, small and far: searchlights, tracers, two hits, two jets, a destroyer
block('beams', below='mech')
marks([np.array([(232, HZ - 8), (240, HZ - 8), (mx - 46, 470), (mx - 70, 462)]), np.array([(1096, HZ - 10), (1104, HZ - 10), (mx + 90, 432), (mx + 66, 446)])], '#7890a0', opacity=.36)
block('tracers')
tr = []
for (xa, ya), (xb, yb), pk in (((842, HZ - 34), (606, 432), 60), ((962, HZ - 16), (624, 396), 120), ((300, HZ - 10), (468, 446), 50)):
    for t in np.linspace(.06, .94, 13) + rng.uniform(-.02, .02, 13):
        p = lambda t_: (xa + (xb - xa) * t_, ya + (yb - ya) * t_ - pk * math.sin(math.pi * t_))
        tr.append(seg(p(t), p(t + .018), w=1.7, wob=0))
marks(tr, FIRE)
def star(x, y, r):
    a = np.linspace(0, 2 * np.pi, 9)[:-1]
    return np.c_[x + np.where(np.arange(8) % 2 == 0, r, r * .32) * np.cos(a), y + np.where(np.arange(8) % 2 == 0, r, r * .32) * np.sin(a)]
marks([star(616, 402, 9), star(458, 450, 7)], FIRE); marks([star(616, 402, 3.4), star(458, 450, 2.6)], PAPERW)
block('jets')
for jx, jy in ((936, 196), (1012, 162)):
    marks([np.array([(jx - 12, jy), (jx + 2, jy - 2.4), (jx + 9, jy - 6), (jx + 7, jy - 1), (jx + 10, jy + 1.5), (jx + 2, jy + 2)])], '#8fa3aa')
    marks([seg((jx + 12, jy), (jx + 150, jy + 9), w=1.1, taper=(0, .8), wob=0)], '#5f7686', opacity=.7)
block('ship', below='road')
sx_, sy_ = 196, HZ + 13
marks([np.array([(sx_, sy_), (sx_ + 6, sy_ - 7), (sx_ + 34, sy_ - 8), (sx_ + 36, sy_ - 15), (sx_ + 48, sy_ - 15), (sx_ + 50, sy_ - 22), (sx_ + 60, sy_ - 22), (sx_ + 62, sy_ - 12),
                 (sx_ + 76, sy_ - 12), (sx_ + 78, sy_ - 8), (sx_ + 118, sy_ - 8), (sx_ + 132, sy_ - 2), (sx_ + 128, sy_ + 1), (sx_ + 4, sy_ + 1)]),
       seg((sx_ + 55, sy_ - 22), (sx_ + 55, sy_ - 40), w=1.2, wob=0), seg((sx_ + 96, sy_ - 9), (sx_ + 116, sy_ - 15), w=1.6, wob=0)], CITY)
marks([star(sx_ + 121, sy_ - 17, 6)], FIRE)
marks([lens(sx_ - 30, sy_ + 4, 190, 2.2)], PALE)
# ---- flames less like traffic cones: redraw them ragged
use('citylights')
fires = [(318, HZ - 8, 1.0), (752, HZ - 30, 1.3), (1004, HZ - 12, .9)]
marks([np.array([(fx - 11 * k, fy + 6), (fx - 8 * k, fy - 5 * k), (fx - 5 * k, fy - 1 * k), (fx - 3 * k, fy - 12 * k), (fx + 0 * k, fy - 5 * k), (fx + 3 * k, fy - 19 * k),
                 (fx + 6 * k, fy - 7 * k), (fx + 9 * k, fy - 10 * k), (fx + 12 * k, fy + 6)]) for fx, fy, k in fires], FIRE)
finish(X0, Y0, X1, Y1, tooth=.3)
seal(X0 + 30, Y1 - 66, 36)
block('title')
text(X0 + 2, Y1 + 30, 'Full moon over the Sound', size=30, font='Liberation Serif', color='#4b4438', anchor='la')
text(X1 - 2, Y1 + 34, 'Fable', size=24, font='Liberation Serif', color='#4b4438', anchor='ra')
