"""d_prechorus (bars 13-16, 96 poses): the crossing; the heron; Vesper Lang and light nobody is behind.
0-23  the Kittiwake crossing right to left in rain, Tern Point blinking far off.
24-47 the heron, close and still; rain, twinkling water, one pale figure's window crossing far behind. It blinks on 36.
48-95 Vesper Lang: six minded windows; on 54, 60, 66, 72, 78, 84 she taps and one goes cold, brighter and empty."""
import numpy as np
import common as C

N = 96
W, H = C.W, C.H
draw, sh, comp = C.draw, C.sh, C.comp


def R(polys): return draw.raster(polys, W, H)
def box(x0, y0, x1, y1): return np.array([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], float)
def oval(cx, cy, rx, ry, n=20):
    a = np.linspace(0, 2 * np.pi, n, endpoint=False)
    return np.c_[cx + rx * np.cos(a), cy + ry * np.sin(a)]


def rain(img, seed, n=80, op=.20, y1=H + 60):
    """Ruled rain, leaning the way everything of the boat's goes: down and to the left."""
    sh.setup(W, H, 700 + seed)
    return draw.paint(img, R(sh.rain(0, -60, W, y1, n=n, angle=106, w=1.0, length=(.05, .16))), '#a9bcd2', op)


# ------------------------------------------------------------------ cut 1: the crossing
HZ1, FY, FL = 392, 438, 600


def ferry(img, x, y, L, shimmer=0):
    """The M/V Kittiwake, double-ended, bow at x (she sails left), waterline at y, L pixels long."""
    P = lambda pts: np.array([(x + u * L, y - v * L) for u, v in pts])
    sh.setup(W, H, 300 + shimmer)
    img = draw.paint(img, R(sh.sheen(x - 4, x + L + 4, y + 1, y + .12 * L, th0=2.4, th1=3.4, keep=.9)), '#0b1019', .85)
    img = C.light(img, R(sh.sheen(x + .09 * L, x + .91 * L, y + 5, y + .36 * L, th0=1.8, th1=3.6)), C.LAMP, 1.5)
    dark = [P([(0, .046), (.035, 0), (.965, 0), (1, .046)]), P([(.012, .044), (.988, .044), (.988, .088), (.012, .088)]),
            P([(.07, .086), (.93, .086), (.93, .128), (.07, .128)]), P([(.20, .126), (.80, .126), (.80, .153), (.20, .153)]),
            P([(.115, .126), (.185, .126), (.180, .172), (.120, .172)]), P([(.815, .126), (.885, .126), (.880, .172), (.820, .172)]),
            P([(.455, .15), (.545, .15), (.535, .215), (.465, .215)]),
            P([(.148, .17), (.152, .17), (.152, .24), (.148, .24)]), P([(.848, .17), (.852, .17), (.852, .24), (.848, .24)])]
    img = draw.paint(img, R(dark), '#080b12')
    slots = [P([(u, .054), (u + .048, .054), (u + .048, .078), (u, .078)]) for u in np.arange(.045, .92, .0665)]
    img = C.light(img, R(slots), '#c98f4a', .32)
    wins = [P([(u, .098), (u + .017, .098), (u + .017, .119), (u, .119)]) for u in .085 + np.arange(30) * .0281]
    wins += [P([(u, .133), (u + .016, .133), (u + .016, .147), (u, .147)]) for u in .215 + np.arange(18) * .0327]
    wins += [P([(.125, .150), (.160, .150), (.160, .164), (.125, .164)]), P([(.840, .150), (.875, .150), (.875, .164), (.840, .164)])]
    img = C.light(img, R(wins), C.LAMP, 4.2)
    wake = [sh.lens(x + L - 6 + k * 26, y + 2 + (k % 2) * 3, 30 + 9 * k, 2.2) for k in range(6)]         # she leaves a little water behind her
    return draw.paint(img, R(wake), '#9fb2c2', .55)


def _plate1():
    img = C.harbour(hz=HZ1, moon=None, road=False, seed=3)
    head = [(-10, HZ1 + 2), (-10, HZ1 - 24), (60, HZ1 - 32), (150, HZ1 - 29), (232, HZ1 - 15), (330, HZ1 - 6), (384, HZ1 + 2)]     # Tern Point
    img = draw.paint(img, R([np.array(head), box(146, HZ1 - 64, 153, HZ1 - 28), box(143.5, HZ1 - 72, 155.5, HZ1 - 64)]), '#101824')
    img = draw.paint(img, R([box(1166, 566, 1186, H), oval(1176, 566, 10, 3.5)]), C.DOCK)        # a pile, and who is on it
    return C.heron(img, 1177, 565, s=.10, flip=False)


PLATE1 = _plate1()


def cut1(i):
    img = PLATE1.copy()
    if i % 12 < 3:                                                                               # Tern Point, far off, minded
        k = (7.0, 5.0, 2.5)[i % 12]
        img = C.light(img, R([sh.lens(123, HZ1 - 68, 53, 2.4)]), C.LAMP, k * .45)
        img = C.light(img, draw.disc(W, H, 149.5, HZ1 - 68, 3.2), C.LAMP, k)
    img = ferry(img, 470 - 3.0 * i, FY, FL, shimmer=i // 2)
    return rain(img, i // 2, n=90, op=.22)


# ------------------------------------------------------------------ cut 2: the heron
HX, HY, HS = 430, 650, .90
EYE2 = (HX + 119 * HS, HY - 509 * HS)
JET = 140


def _plate2():
    img = C.harbour(hz=100, moon=None, road=False, seed=5, water=('#586f81', '#3b5165', '#243649'))
    posts = [box(x, JET + 8, x + 5, JET + 24) for x in range(540, W, 62)]
    return draw.paint(img, R([box(520, JET, W + 10, JET + 10)] + posts), '#0b1019')              # a breakwater, far off


def _heron2():
    lay = np.zeros((H, W, 4), np.float32)
    lay = draw.paint(lay, R([box(HX - 52, HY, HX + 44, H), oval(HX - 4, HY, 48, 9)]), C.DOCK)
    return C.heron(lay, HX, HY, s=HS, flip=True, eye=False)


PLATE2, HERON2 = _plate2(), _heron2()
PSIZE = 100
PSPEED = C.walk_speed('passenger', PSIZE)


def cut2(i):
    j = i - 24
    img = PLATE2.copy()
    sh.setup(W, H, 520 + i // 2)
    img = draw.paint(img, R(sh.ripples(0, 128, W, H, n=120, len0=14, len1=120, th0=1.0, th1=3.4)), '#8ea4b6', .5)
    px = 1215 - PSPEED * j                                                                       # the light that left a house, going to the boat
    sh.setup(W, H, 560 + i // 2)
    img = C.light(img, R(sh.sheen(px - 7, px + 7, JET + 14, JET + 150, th0=1.6, th1=3.0, breakup=2.0, spread=.9)), '#fff6cf', 1.5)
    img = C.figure(img, 'passenger', C.walk_pose('passenger', (j % 12) / 12), x=px, ground=JET + 1, size=PSIZE, flip=True, glow=7.0)
    img = rain(img, 40 + i // 2, n=70, op=.20)
    img = comp.over(img, HERON2)                                                                 # the bird does not move
    if i in (36, 37):                                                                            # except this
        img = draw.paint(img, R([sh.lens(EYE2[0] - 9, EYE2[1] + 1, 18, 2.6)]), '#27303d')
    else:
        img = C.light(img, draw.disc(W, H, EYE2[0], EYE2[1], 7.5), C.LAMP, 5.0)
        img = draw.paint(img, draw.disc(W, H, EYE2[0] + 1.5, EYE2[1], 2.8), '#0b0d12')
    return rain(img, 90 + i // 2, n=12, op=.16)


# ------------------------------------------------------------------ cut 3: Vesper Lang
TAPS = (54, 60, 66, 72, 78, 84)
WX = [94 + 108 * k for k in range(6)]                      # window centres
WY0, WY1, WHW = 208, 296, 32                               # each window 64 x 88
LX, LG, LS = 944, 706, 600


def _minder(k):
    """Somebody's head and shoulders, seen from the street."""
    cx = WX[k] + (-7, 6, 0, -5, 8, -2)[k]; hr = (13, 12, 14, 12.5, 13.5, 11.5)[k]; hy = WY0 + 37 + (0, 4, -3, 6, 1, 9)[k]
    t = hy + hr + 4
    polys = [oval(cx, hy, hr * .9, hr), box(cx - 5, hy + hr - 4, cx + 5, t + 6),
             sh.spline([(cx - 29, WY1 + 4), (cx - 27, t + 13), (cx - 15, t + 3), (cx, t), (cx + 15, t + 3), (cx + 27, t + 13), (cx + 29, WY1 + 4)], closed=True)]
    if k == 1: polys.append(oval(cx + 9, hy - 9, 6.5, 6))                       # hair up
    if k == 4: polys.append(box(cx - 15, hy - 10, cx + 19, hy - 6))            # a cap
    if k == 3: polys.append(oval(cx - 2, hy - 2, hr * 1.12, hr * .95))         # a lot of hair
    return R(polys) * draw.rect(W, H, WX[k] - WHW, WY0, WX[k] + WHW, WY1)


def _plate3():
    img = C.harbour(hz=452, moon=None, road=False, seed=11)
    img = draw.paint(img, draw.rect(W, H, 0, 486, W, H), C.DOCK)                                 # the quay
    img = draw.paint(img, draw.rect(W, H, 700, 486, W, 489), '#1c2737')
    img = draw.paint(img, R([box(1189, 446, 1202, 492), oval(1195.5, 446, 6.5, 2.5)]), C.DOCK)   # a bollard, and who is on it
    img = C.heron(img, 1196, 445, s=.09, flip=False)
    img = draw.paint(img, R([box(-70, 168, 700, 490)]), '#141b2a')                               # the terrace
    img = draw.paint(img, R([np.array([(-70, 170), (-70, 138), (690, 138), (706, 170)])] + [box(x - 13, 112, x + 13, 140) for x in range(40, 700, 108)]
                            + [box(x - 9, 106, x - 2, 113) for x in range(40, 700, 108)] + [box(x + 2, 106, x + 9, 113) for x in range(40, 700, 108)]), '#090d16')
    img = draw.paint(img, R([box(x - 1.5, 170, x + 1.5, 490) for x in range(40, 700, 108)] + [box(700, 170, 704, 490)]), '#0b101a')
    for c in WX + [-14]:
        img = draw.paint(img, R([box(c - WHW - 4, WY0 - 4, c + WHW + 4, WY1 + 4), box(c + 12, 388, c + 44, 490), box(c - 42, 372, c - 4, 436)]), '#0a0e17')
        img = draw.paint(img, R([box(c - WHW - 7, WY1 + 4, c + WHW + 7, WY1 + 9)]), '#232c3e')
    img = draw.paint(img, R([box(128, 38, 600, 104), box(180, 104, 186, 140), box(542, 104, 548, 140), box(360, 104, 366, 140)]), '#0a0e16')    # the sign
    return img


SIGN = C.text((364, 28), 'CONTINUITY', 62, track=12, anchor='m')
PLATE3 = _plate3()
WIN = [draw.rect(W, H, c - WHW, WY0, c + WHW, WY1) for c in WX]
MIND = [_minder(k) for k in range(6)]
RAINMASK = np.clip((440 - np.arange(H)) / 60.0, 0, 1).astype(np.float32)[:, None]
BASE = dict(C.CAST['lang']['pose'])
HOVER, ANTIC, TAP = dict(BASE, shF=30, elF=74), dict(BASE, shF=26, elF=62), dict(BASE, shF=37, elF=88)


def cut3(i):
    img = PLATE3.copy()
    d = min([i - t for t in TAPS if i >= t] or [99])           # poses since the last tap
    nxt = min([t - i for t in TAPS if t > i] or [99])          # poses to the next
    hum = C.clamp01((i - 48) / 40.0)                           # the sign comes up as the street goes cold
    img = C.light(img, SIGN, C.COLD, 2.6 + 1.4 * hum + (1.5 if d < 2 else 0))
    for k in range(6):
        since = i - TAPS[k]
        if since < 0:                                          # warm, and somebody is minding it
            img = C.light(img, WIN[k], C.LAMP, 3.2)
            img = draw.paint(img, MIND[k], '#1d1209')
        else:                                                  # cold, brighter, and nobody behind it
            img = C.light(img, WIN[k], C.COLD, 12.0 if since < 2 else 6.5)
    sh.setup(W, H, 880 + i // 2)
    img = draw.paint(img, R(sh.rain(0, -60, W, 470, n=34, angle=106, w=1.0, length=(.05, .14))) * RAINMASK, '#a9bcd2', .15)
    pose = TAP if d < 2 else C.fg.blend(TAP, HOVER, .5) if d == 2 else ANTIC if nxt == 1 else HOVER
    img = C.figure(img, 'lang', pose, x=LX, ground=LG, size=LS, flip=True, glow=12.0 if d < 2 else 5.0)
    # her other hand: the far arm is dark on dark, so the tapping finger is staged where it crosses the tablet's light
    tip = (737, 235) if d < 2 else (751, 254) if d == 2 else (772, 281) if nxt == 1 else (764, 271)
    img = draw.paint(img, R([sh.ribbon([(832, 300), (800, 281), tip], w=17, taper=(0, .55), wob=0, minw=5.5)]), '#0c1019')
    return C.name_card(img, 'lang', C.clamp01((i - 72) / 16), 'l')


def frame(i):
    return cut1(i) if i < 24 else cut2(i) if i < 48 else cut3(i)
