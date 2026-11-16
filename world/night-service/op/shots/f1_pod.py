"""f1_pod (bars 20-21, 48 poses): the pod goes in; the cable is cut.
0-23  wide, at water level: three dorsal fins cut right to left through the moon's path toward No. 4's shins; its cable
      comes down into the water beside them, a cold pulse climbing it on every beat (the power goes up the cable into its back).
24-47 closer: an orca leaps in a low arc from the right and takes the cable in its teeth (36); it hangs on it; on 42 the
      cable snaps (near-white flash, 42-43); after that the cable is dark, the ends apart, no more pulses.
No. 4 is seen here from its other side (mirrored), so that the cable, which hangs from its back, falls on the pod's side.
The orca is ported from styles/lit-window/subjects/orca.py (landmarks measured on a photograph of a breach)."""
import math
import numpy as np
import common as C

N = 48
W, H = C.W, C.H
draw, sh, comp = C.draw, C.sh, C.comp
N4COL, PALE, FLASH = '#13101b', '#dfe8ee', '#eef4ff'
ROWS = np.arange(H, dtype=np.float32)[:, None]


def R(polys): return draw.raster(polys, W, H)
def box(x0, y0, x1, y1): return np.array([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], float)
def path(*pts): return sh.resample(sh.spline(np.array(pts, float)), 4.0)
def clear(): return np.zeros((H, W, 4), np.float32)


def road(img, moon, hz, i):
    sh.setup(W, H, 9000 + i // 2)
    return C.light(img, R(sh.moonroad(moon[0], hz + 3, H - 4, w0=moon[2] * 1.1, w1=520, th0=1.4, th1=4.2)), '#efe6cc', 1.6)


def cable(img, P, w, live=True, frac=None, colour=N4COL, taper=(0, 0)):
    """P runs from the machine's end down to the water. live: a cold core. frac: where the pulse is, 0 at the water, 1 at the top."""
    if len(P) < 3:
        return img
    img = draw.paint(img, R([sh.ribbon(P, w=w, taper=taper, wob=0, smooth=False)]), colour)
    if live:
        img = C.light(img, R([sh.ribbon(P, w=max(1.8, w * .22), taper=(0, 0), wob=0, smooth=False)]) * .55, C.COLD, 1.0)
        if frac is not None:
            d = np.r_[0, np.cumsum(np.hypot(*np.diff(P, axis=0).T))]
            sel = np.abs(d - d[-1] * (1 - frac)) < 46
            if sel.sum() > 3:
                img = C.light(img, R([sh.ribbon(P[sel], w=w * 1.3, taper=(.4, .4), wob=0, smooth=False)]), C.COLD, 7.0)
    return img


def fin(img, x, y, h, sink=0.0, seed=0, wake=1.0):
    """A dorsal fin travelling left: (x, y) is the middle of its base on the water; sink pushes it under. A pale wake behind it."""
    rng = np.random.default_rng(seed)
    dashes = [sh.lens(x - .8 * h, y + 2, 1.4 * h, max(2.4, h * .07))]
    for k in range(10):
        t = (k + rng.uniform(0, .6)) / 10
        ln = h * rng.uniform(.5, 1.1) * (1 - .35 * t)
        dashes.append(sh.lens(x + h * (.45 + 7.0 * t), y + 3 + (1 if k % 2 else -1) * h * (.03 + .15 * t), ln, max(1.6, h * .05) * (1 - .45 * t)))
    vee = [sh.ribbon([(x - .25 * h, y + 2), (x + 3.2 * h, y + 2 + k * h * .5), (x + 7.5 * h, y + 2 + k * h)], w=max(2.2, h * .05), taper=(.05, .7), wob=0) for k in (-.17, .26)]
    img = C.light(img, R(dashes + vee) * wake, PALE, 1.35)
    o = np.array([x, y + sink])
    lead = sh.spline(np.array([(-.42, 0), (-.27, -.42), (-.09, -.80), (.09, -1.0)]) * h + o)
    trail = sh.spline(np.array([(.09, -1.0), (.17, -.72), (.22, -.38), (.36, 0)]) * h + o)
    above = np.clip(y - ROWS + .5, 0, 1)
    img = draw.paint(img, R([np.r_[lead, trail], sh.lens(x - 1.25 * h, y + sink, 2.9 * h, .36 * h)]) * above, '#0a0d12')
    return draw.paint(img, R([sh.lens(x + .30 * h, y + sink - .07 * h, .55 * h, .11 * h)]) * above, '#46525c')


# ------------------------------------------------------------------ the orca (after subjects/orca.py)
UX, UY = 73.2, 50.3


def orca_T(ox, oy, s, flip, rot):
    bx, by = 2.8 * UX, 7.6 * UY
    ca, sa = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    def T(pts):
        P = np.asarray(pts, float).reshape(-1, 2)
        dx, dy = P[:, 0] * UX - bx, P[:, 1] * UY - by
        x_, y_ = dx * ca + dy * sa, -dx * sa + dy * ca
        return np.c_[ox + (-x_ if flip else x_) * s, oy + y_ * s]
    return T


MOUTH = (7.62, 2.24)


def orca(img, ox, oy, s=1.0, flip=True, rot=0.0, jaw=14.0, flash=False):
    """Stocky, blunt-headed, the dorsal fin well back, a broad paddle of a flipper, white jaw and belly, a slanted eye patch."""
    T = orca_T(ox, oy, s, flip, rot)
    def J(pts, pivot=(7.1, 2.6)):                 # swing the lower jaw open about the corner of the mouth
        a = math.radians(jaw); out = []
        for ux, uy in pts:
            dx, dy = (ux - pivot[0]) * UX, (uy - pivot[1]) * UY
            out.append((pivot[0] + (dx * math.cos(a) - dy * math.sin(a)) / UX, pivot[1] + (dx * math.sin(a) + dy * math.cos(a)) / UY))
        return out
    black = '#05070a' if flash else '#0d1013'
    def white(im, polys):
        return C.light(im, R(polys), FLASH, 3.4) if flash else draw.paint(im, R(polys), '#e9e2cf')
    back = [(8.1, 1.7), (7.95, 1.45), (7.5, 1.38), (6.9, 1.6), (6.2, 2.05), (5.5, 2.6), (4.6, 3.4), (4.05, 4.2), (3.6, 5.0), (3.15, 6.0), (2.85, 7.0), (2.7, 7.7)]
    belly = [(3.0, 7.8), (3.6, 7.3), (4.3, 6.7), (5.2, 5.9), (6.0, 5.15), (6.6, 4.5), (7.1, 3.7)]
    lowjaw = J([(7.1, 3.7), (7.6, 2.9), (7.95, 2.25), (8.12, 1.95), (7.6, 2.2)])
    dorsal = sh.spline(T([(4.7, 3.3), (4.2, 3.18), (3.5, 3.33), (3.72, 3.75), (4.0, 4.3), (4.4, 3.9)]), closed=True)
    img = draw.paint(img, R([sh.spline(T(back + belly + lowjaw[:4] + [(7.1, 2.6), (7.7, 2.05)]), closed=True), dorsal]), black)
    wh = lowjaw[3:4] + lowjaw[4:5] + [(7.1, 2.62), (6.75, 3.3), (6.45, 4.0), (6.0, 4.6), (5.3, 5.25), (4.6, 5.68), (3.95, 5.8), (3.4, 6.2), (3.3, 6.6),
         (3.5, 6.95), (3.2, 7.5), (3.0, 7.8), (3.6, 7.3), (4.3, 6.7), (5.2, 5.9), (6.0, 5.15), (6.6, 4.5), (7.1, 3.7)] + lowjaw[1:3]
    img = white(img, [T(wh), sh.spline(T([(6.45, 1.86), (6.75, 1.66), (7.2, 1.62), (7.4, 1.74), (7.1, 1.9), (6.7, 1.98)]), closed=True)])
    if not flash:
        img = draw.paint(img, R([sh.spline(T([(3.95, 4.5), (3.75, 4.75), (3.4, 5.5), (3.55, 5.45), (3.9, 4.85)]), closed=True)]), '#3a4650')
    img = draw.paint(img, R([T([(8.08, 1.78), (7.1, 2.6)] + lowjaw[3:4])]), black if flash else '#3b171a')
    teeth = []
    for t in np.linspace(.12, .8, 8):
        ux, uy = 8.08 + (7.1 - 8.08) * t, 1.78 + (2.6 - 1.78) * t
        teeth.append(T([(ux - .035, uy - .02), (ux + .035, uy + .04), (ux - .05, uy + .14)]))
        lx, ly = lowjaw[3][0] + (7.1 - lowjaw[3][0]) * t, lowjaw[3][1] + (2.6 - lowjaw[3][1]) * t
        teeth.append(T([(lx - .04, ly - .02), (lx + .04, ly + .03), (lx + .0, ly - .13)]))
    img = white(img, teeth)
    return draw.paint(img, R([sh.spline(T([(6.75, 4.1), (7.35, 4.6), (7.6, 5.6), (7.4, 6.6), (6.9, 6.5), (6.65, 5.6), (6.55, 4.8)]), closed=True)]), black)


# ------------------------------------------------------------------ 0-23: the fins
HZA, MOONA = 330, (900, 190, 270)
A4 = dict(cx=190, wl=372, h=1100)
def MA(pts): return np.array([(A4['cx'] - u * A4['h'], A4['wl'] - v * A4['h']) for u, v in pts])
CABLE_A = path(*MA([(-.03, .63), (-.2, .46), (-.36, .2), (-.5, -.01)]))
ENTRY_A = CABLE_A[-1]


def _plate_a():
    img = C.harbour(hz=HZA, moon=MOONA, road=False, seed=2)
    img = draw.paint(img, R([MA(p) for p in C._NO4[:3]]), N4COL)
    sh.setup(W, H, 41)
    return draw.paint(img, R(sh.sheen(70, 160, 376, 500, th0=3, th1=5, keep=.85) + sh.sheen(256, 318, 376, 500, th0=3, th1=5, keep=.85)), '#0c1018', .9)


def _layer_a():
    lay = draw.paint(clear(), R([box(1054, 300, 1067, 354)]), C.DOCK)
    return C.heron(lay, 1060.5, 300, s=.075, flip=False)


PLATE_A, LAYER_A = _plate_a(), _layer_a()
FINS = [dict(x0=1300, v=11.0, y=396, h=48, seed=1), dict(x0=1066, v=13.0, y=428, h=74, seed=2), dict(x0=1262, v=15.0, y=486, h=112, seed=3)]


def frame_a(i):
    img = comp.over(road(PLATE_A.copy(), MOONA, HZA, i), LAYER_A)
    f = FINS[0]; img = fin(img, f['x0'] - f['v'] * i, f['y'] + (i // 2 % 2), f['h'], seed=f['seed'] * 100 + i // 2)
    img = cable(img, CABLE_A, 9.5, True, ((i % 6) + .5) / 6)
    img = C.light(img, R([sh.lens(ENTRY_A[0] - 26, ENTRY_A[1] - 4, 52, 3.4)]) * (.9 if i % 6 == 0 else .5), PALE, 1.3)
    dive = C.ease(C.clamp01((i - 15) / 8.0), 'in')                              # the leader goes under as it reaches the cable
    f = FINS[1]; img = fin(img, f['x0'] - f['v'] * i, f['y'], f['h'], sink=f['h'] * 1.05 * dive, seed=f['seed'] * 100 + i // 2, wake=1 - .5 * dive)
    f = FINS[2]; img = fin(img, f['x0'] - f['v'] * i, f['y'] + ((i + 1) // 2 % 2), f['h'], seed=f['seed'] * 100 + i // 2)
    return img


# ------------------------------------------------------------------ 24-47: the orca and the cable
HZB, MOONB = 470, (800, 330, 330)
B4 = dict(cx=-122, wl=505, h=1760)
A0, C0, E = np.array([575.0, -20.0]), np.array([600.0, 352.0]), np.array([628.0, 540.0])
WLB, OS, ROT = 553, 1.3, -17.0
BASE_F = C0 - orca_T(0, 0, OS, True, ROT)([MOUTH])[0]                           # where its tail stock leaves the water when its teeth meet the cable
LC = float(np.hypot(*(C0 - A0)))


def _plate_b():
    img = C.harbour(hz=HZB, moon=MOONB, road=False, seed=2)
    img = draw.paint(img, R([np.array([(B4['cx'] - u * B4['h'], B4['wl'] - v * B4['h']) for u, v in C._NO4[0]])]), N4COL)
    sh.setup(W, H, 43)
    return draw.paint(img, R(sh.sheen(-10, 82, 509, 700, th0=4, th1=7, keep=.85)), '#0c1018', .9)


def _layer_b():
    lay = draw.paint(clear(), R([box(480, 455, 496, 506)]), C.DOCK)
    return C.heron(lay, 488, 455, s=.10, flip=True)


PLATE_B, LAYER_B = _plate_b(), _layer_b()
LEG_B = R([np.array([(B4['cx'] - u * B4['h'], B4['wl'] - v * B4['h']) for u, v in C._NO4[0]])])
_r = np.random.default_rng(42)
SP_ANG, SP_SPD, SP_LIFE = _r.uniform(0, 2 * np.pi, 44), _r.uniform(20, 74, 44), _r.integers(1, 6, 44)
SWING = {18: (6, 10), 19: (-10, -2), 20: (-22, -14), 21: (-30, -24), 22: (-31, -29), 23: (-26, -28)}    # the loose end: (end, middle) degrees from plumb


def orca_state(j):
    """(distance back down its own line, rotation, jaw) at pose j of the cut."""
    if j < 12:
        return 640.0 * (1 - C.ease(j / 12.0, 'out')), C.lerp(9.0, ROT, C.ease(j / 12.0, 'inout')), 4.0 + 30.0 * C.clamp01((j - 4) / 6.0)
    if j < 18:
        return 7.0 * (j - 12), ROT + (0, 2.2, -1.8, 2.4, -1.6, 2.8)[j - 12], 7.0
    return (44, 66, 110, 180, 275, 395)[j - 18], ROT + (1.0, 0, -2, -5, -8, -11)[j - 18], 7.0


def sparks(img, origin, age, n=44, k=8.0):
    polys = []
    for q in range(n):
        if age <= SP_LIFE[q]:
            v = np.array([math.cos(SP_ANG[q]), math.sin(SP_ANG[q])]) * SP_SPD[q]
            p = origin + v * (age + .4) + np.array([0, 3.4 * age * age])
            polys.append(sh.seg(p - v * .34, p, w=2.6, taper=(.5, 0), wob=0))
    return C.light(img, R(polys), C.COLD, k) if polys else img


def frame_b(i):
    j = i - 24
    d, rot, jaw = orca_state(j)
    T0 = orca_T(0, 0, OS, True, rot)
    down = -T0([(8.1, 1.7)])[0]; down /= np.hypot(*down)                        # back along its own line, into the water
    base = BASE_F + d * down
    mouth = base + T0([MOUTH])[0]
    flash = j == 18
    if flash:                                                                    # the snap: one drawing in black on white
        img = C.light(clear(), np.ones((H, W), np.float32), FLASH, 3.4)
        img = draw.paint(img, np.clip((ROWS - HZB) / 4.0, 0, 1) * np.ones((1, W), np.float32), '#aebfd6', .22)
        img = draw.paint(img, LEG_B, '#05070a')
        dark = '#05070a'
    else:
        img = road(PLATE_B.copy(), MOONB, HZB, i)
        dark = N4COL
    img = comp.over(img, LAYER_B)
    # the cable
    if j < 12:
        img = cable(img, path(A0, C0, E), 13, True, ((i % 6) + .5) / 6)
    elif j < 18:
        img = cable(img, np.r_[path(A0, mouth), path(mouth, E)], 13, True, ((i % 6) + .5) / 6)
    else:
        a, m = (math.radians(v) for v in SWING[j])
        end = A0 + LC * np.array([math.sin(a), math.cos(a)])
        mid = A0 + .52 * LC * np.array([math.sin(m), math.cos(m)])
        img = cable(img, path(A0, mid, end), 13, False, colour=dark)
        sag = (mouth + E) / 2 + np.array([-6.0 * (j - 18), 10.0 + 9.0 * (j - 18)])
        if mouth[1] < WLB - 6:
            img = cable(img, path(mouth, sag, E + np.array([8.0 * (j - 18), 14.0])), 13, False, colour=dark, taper=(0, .3))
    pre = img.copy()
    img = orca(img, base[0], base[1], s=OS, flip=True, rot=rot, jaw=jaw, flash=flash)
    img[WLB:] = pre[WLB:]                                                        # the sea in front of it
    if 12 <= j < 18:                                                             # the cable goes in at the side of its mouth
        img = cable(img, path(A0, mouth), 13, True, None)
    # white water where it breaks the surface
    xs = np.nonzero(np.abs(img[WLB - 1] - pre[WLB - 1]).max(-1) > 1e-4)[0]
    if len(xs) and not flash:
        rng = np.random.default_rng(4000 + i)
        x0, x1 = xs.min() - 36, xs.max() + 36
        speed = C.clamp01(abs(orca_state(min(j + 1, 23))[0] - d) / 90.0)
        foam = [sh.lens(rng.uniform(x0, x1 - 40), WLB + rng.uniform(-4, 12), rng.uniform(26, 90), rng.uniform(2.5, 5.5)) for _ in range(16)]
        foam += [box(px, py, px + sz, py + sz * .8) for px, py, sz in zip(rng.uniform(x0, x1, int(34 * speed)), WLB - rng.uniform(0, 6.2, int(34 * speed)) ** 2, rng.uniform(2, 4.5, int(34 * speed)))]
        img = C.light(img, R(foam), PALE, 1.35)
    # the break
    if j == 12 or j == 13:
        img = sparks(img, mouth, j - 12 + .3, n=9, k=7.0)                        # its teeth close on a live cable
    if flash:
        rng = np.random.default_rng(7)
        spikes = []
        for a in np.linspace(0, 2 * np.pi, 19, endpoint=False) + rng.uniform(-.12, .12, 19):
            u = np.array([math.cos(a), math.sin(a)]); r0, r1 = rng.uniform(46, 70), rng.uniform(150, 420)
            spikes.append(sh.seg(C0 + u * r0, C0 + u * r1, w=rng.uniform(3, 7), taper=(0, .9), wob=0))
        img = draw.paint(img, R(spikes), '#05070a')
    elif j >= 19:
        age = j - 18
        if j == 19:
            g = np.exp(-((np.arange(W)[None, :] - C0[0]) ** 2 + (ROWS - C0[1]) ** 2) / (2 * 190.0 ** 2)).astype(np.float32)
            img[..., :3] += C.core.col(C.COLD) * 3.2 * g[..., None]
        img = sparks(img, C0, age)
        a = math.radians(SWING[j][0]); end = A0 + LC * np.array([math.sin(a), math.cos(a)])
        rng = np.random.default_rng(600 + i)
        drip = [sh.chip(end[0] + rng.uniform(-9, 9), end[1] + rng.uniform(0, 34), rng.uniform(2, 4)) for _ in range(max(0, 6 - age))]
        if drip:
            img = C.light(img, R(drip), C.COLD, 6.0)
    return img


def frame(i):
    return frame_a(i) if i < 24 else frame_b(i)
