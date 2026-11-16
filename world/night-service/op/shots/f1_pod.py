"""f1_pod (bars 20-21, 48 poses): the pod goes in; the cable is cut.
0-23  wide, at water level: three dorsal fins cut right to left through the moon's path toward No. 4's shins; its cable, a
      hose as thick as a ferry's funnel, hangs down beside them and trails slack into the water, a cold pulse climbing INSIDE it
      on every beat (the power goes up the cable into its back).
24-47 closer: an orca leaps in a low arc from the right and takes the hose in its teeth (36); the hose bows toward it under
      its weight and the bow deepens as it shakes (37-41); on 42 the hose snaps (near-white flash, 42-43); the upper end
      recoils up and out of frame, the lower stays in the orca's mouth as it falls back; no more pulses, the hose dead dark.
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


HOSE, RIMC, RIBC = '#191622', '#4d5b73', '#0c0a13'


def hose(img, P, w, live=True, pulses=(), light=(.4, -1.0), body=HOSE, rim=RIMC, k=3.6, sigma=34.0, clip=None):
    """A thick hose along the centreline P (the machine's end first), jointed with collars, one edge rim-lit so that it
    separates from the night. live: the faintest cold light inside it. pulses: distances along P (pixels from P[0]) at which a
    lit section is travelling INSIDE it: narrower than the hose, soft at its sides and at both ends, the collars dark across it.
    clip: a matte to keep it inside (the waterline)."""
    P = np.asarray(P, float)
    if len(P) < 4:
        return img
    m = 1.0 if clip is None else clip
    tg = np.gradient(P, axis=0); tg /= np.maximum(np.hypot(tg[:, 0], tg[:, 1]), 1e-9)[:, None]
    n = np.c_[-tg[:, 1], tg[:, 0]]
    if float((n @ np.asarray(light, float)).mean()) < 0:
        n = -n
    hw = w / 2.0
    band = lambda a, b: np.r_[P + n * a, (P + n * b)[::-1]]
    img = draw.paint(img, R([band(hw, -hw)]) * m, body)
    d = np.r_[0, np.cumsum(np.hypot(*np.diff(P, axis=0).T))]
    if live:
        field = np.full((H, W), .010, np.float32)
        for c in pulses:
            if 0 <= c <= d[-1]:
                px, py = float(np.interp(c, d, P[:, 0])), float(np.interp(c, d, P[:, 1]))
                x0, x1, y0, y1 = int(max(px - 3 * sigma, 0)), int(min(px + 3 * sigma, W)), int(max(py - 3 * sigma, 0)), int(min(py + 3 * sigma, H))
                if x1 > x0 and y1 > y0:
                    yy, xx = np.mgrid[y0:y1, x0:x1]
                    field[y0:y1, x0:x1] += np.exp(-((xx - px) ** 2 + (yy - py) ** 2) / (2 * sigma ** 2))
        core = np.clip(C.comp.feather(R([band(hw * .30, -hw * .30)]), w * .09) * 1.2, 0, 1)
        img = C.light(img, core * np.clip(field, 0, 1) * m, C.COLD, k)
    rw = max(2.0, w * .09)
    if rim:
        img = draw.paint(img, R([band(hw, hw - rw)]) * m, rim)
    cl, ch, joints, edges = w * .14, hw * 1.17, [], []                         # a collar every three widths
    for q in np.searchsorted(d, np.arange(w * 1.7, d[-1], w * 3.0)):
        q = min(int(q), len(P) - 1)
        c0, t0, n0 = P[q], tg[q], n[q]
        joints.append(np.array([c0 + n0 * ch - t0 * cl, c0 + n0 * ch + t0 * cl, c0 - n0 * ch + t0 * cl, c0 - n0 * ch - t0 * cl]))
        edges.append(np.array([c0 + n0 * ch - t0 * cl, c0 + n0 * ch + t0 * cl, c0 + n0 * (ch - rw) + t0 * cl, c0 + n0 * (ch - rw) - t0 * cl]))
    if joints:
        img = draw.paint(img, R(joints) * m, '#211e2d' if rim else body)
        if rim:
            img = draw.paint(img, R(edges) * m, rim)
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
# the hose, in No. 4's units, as e_no4 draws it (the part that is in this picture): it hangs, then trails away along the water
HOSE_UV = [(-.270, .487), (-.292, .405), (-.306, .32), (-.322, .235), (-.345, .165), (-.376, .105), (-.414, .055), (-.46, .015), (-.52, -.012), (-.60, -.035)]
HOSE_A = path(*MA(HOSE_UV))
WA, YA = A4['h'] * .027, 381.0                                                  # its width; the water where it goes in
ABOVE_A = np.clip(YA - ROWS + .5, 0, 1)
ENTRY_A = np.array([float(np.interp(YA, HOSE_A[:, 1], HOSE_A[:, 0])), YA])


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
    L = float(np.hypot(*np.diff(HOSE_A, axis=0).T).sum())
    sh.setup(W, H, 47 + i // 2)
    img = draw.paint(img, R(sh.sheen(ENTRY_A[0] - 44, ENTRY_A[0] + 40, YA + 3, YA + 46, th0=2.5, th1=4, keep=.85)), '#0c1018', .85)
    img = hose(img, HOSE_A, WA, True, [L * (1 - ((i % 6) + .5) / 12.0 - k / 2.0) for k in range(2)], clip=ABOVE_A, sigma=28.0)
    img = C.light(img, R([sh.lens(ENTRY_A[0] - 62, YA, 96, 3.2), sh.lens(ENTRY_A[0] - 20, YA + 5, 84, 2.6)]) * (.9 if i % 6 == 0 else .55), PALE, 1.3)
    dive = C.ease(C.clamp01((i - 15) / 8.0), 'in')                              # the leader goes under as it reaches the cable
    f = FINS[1]; img = fin(img, f['x0'] - f['v'] * i, f['y'], f['h'], sink=f['h'] * 1.05 * dive, seed=f['seed'] * 100 + i // 2, wake=1 - .5 * dive)
    f = FINS[2]; img = fin(img, f['x0'] - f['v'] * i, f['y'] + ((i + 1) // 2 % 2), f['h'], seed=f['seed'] * 100 + i // 2)
    return img


# ------------------------------------------------------------------ 24-47: the orca and the cable
HZB, MOONB = 470, (800, 330, 330)
B4 = dict(cx=-122, wl=505, h=1760)
C0 = np.array([600.0, 352.0])                                                   # where its teeth meet the hose
REST = [(572.0, -40.0), (560.0, 80.0), (566.0, 210.0), (600.0, 352.0), (630.0, 452.0), (652.0, 530.0), (666.0, 600.0)]   # the hose, hanging slack: it bellies away from the pod
A0, EB = np.array(REST[0]), np.array([662.0, 580.0])
WB, YB = 36.0, 548.0                                                            # the hose's width here; the water where it goes in
ABOVE_B = np.clip(YB - ROWS + .5, 0, 1)
WLB, OS, ROT = 553, 1.3, -17.0
BASE_F = C0 - orca_T(0, 0, OS, True, ROT)([MOUTH])[0]                           # where its tail stock leaves the water when its teeth meet the hose
BOW = (0.0, 22.0, 42.0, 60.0, 76.0, 92.0)                                       # 36-41: how far its weight has pulled the hose over
SHAKE = (0.0, 3.5, .5, 4.5, 1.0, 5.5)                                           # and how it shakes: it swings about its teeth, so its tail goes down and up
AFTER = {18: (696, 390, -12.0), 19: (716, 402, -14.0), 20: (752, 420, -16.5), 21: (806, 446, -19.5), 22: (880, 480, -23.0), 23: (972, 520, -27.0)}   # its mouth, its tilt, falling back
RECOIL = {18: [(572, -40), (590, 115), (630, 250), (666, 348)], 19: [(572, -40), (560, 90), (534, 190), (494, 238)],
          20: [(572, -40), (548, 36), (510, 92), (468, 98)], 21: [(572, -40), (556, -8), (530, 10), (508, 6)]}     # the upper end, springing back up and out
BRK = np.array([676.0, 368.0])                                                  # where it parts


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


def orca_at(j):
    """(base, rotation, jaw, mouth) at pose j of the cut."""
    if j < 12:                                                                   # the leap: up its own line, tipping over toward the hose
        d, rot, jaw = 640.0 * (1 - C.ease(j / 12.0, 'out')), C.lerp(9.0, ROT, C.ease(j / 12.0, 'inout')), 4.0 + 30.0 * C.clamp01((j - 4) / 6.0)
        T0 = orca_T(0, 0, OS, True, rot)
        down = -T0([(8.1, 1.7)])[0]; down /= np.hypot(*down)
        base = BASE_F + d * down
        return base, rot, jaw, base + T0([MOUTH])[0]
    if j < 18:                                                                   # hanging on the hose: its teeth are the fixed point
        T0 = orca_T(0, 0, OS, True, ROT)
        down = -T0([(8.1, 1.7)])[0]; down /= np.hypot(*down)
        mouth = C0 + BOW[j - 12] * down + np.array([-down[1], down[0]]) * (0, 5, -4, 6, -5, 7)[j - 12]
        rot, jaw = ROT + SHAKE[j - 12], 20.0
    else:
        mouth, rot, jaw = np.array(AFTER[j][:2], float), AFTER[j][2], 17.0
    return mouth - orca_T(0, 0, OS, True, rot)([MOUTH])[0], rot, jaw, mouth


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
    base, rot, jaw, mouth = orca_at(j)
    flash = j == 18
    if flash:                                                                    # the snap: one drawing in black on white
        img = C.light(clear(), np.ones((H, W), np.float32), FLASH, 3.4)
        img = draw.paint(img, np.clip((ROWS - HZB) / 4.0, 0, 1) * np.ones((1, W), np.float32), '#aebfd6', .22)
        img = draw.paint(img, LEG_B, '#05070a')
    else:
        img = road(PLATE_B.copy(), MOONB, HZB, i)
    img = comp.over(img, LAYER_B)
    dead = dict(live=False, body='#05070a', rim=None) if flash else dict(live=False)
    b = i % 6
    front = None                                                                 # the part of the hose that passes in front of its face
    if j < 12:                                                                   # hanging slack; two pulses in the picture, one out of the water on each beat
        P = path(*REST)
        L = float(np.hypot(*np.diff(P, axis=0).T).sum())
        img = hose(img, P, WB, True, [L * (1 - (b + .5) / 12.0 - k / 2.0) for k in range(2)], light=(1, -.25), clip=ABOVE_B, sigma=30.0)
    elif j < 18:                                                                 # taken: it bows toward the orca, and the bow deepens
        bow = BOW[j - 12]
        up = path(A0, A0 + (mouth - A0) * .34 + np.array([-.22 * bow, 0.0]), A0 + (mouth - A0) * .68 + np.array([-.30 * bow, 0.0]), mouth)
        low = path(mouth, mouth + (EB - mouth) * .5 + np.array([.10 * bow + 6, 0.0]), EB)
        Lu, Ll = (float(np.hypot(*np.diff(q, axis=0).T).sum()) for q in (up, low))
        pulses = [(Lu + Ll) * (1 - (b + .5) / 12.0 - k / 2.0) for k in range(2)]
        img = hose(img, low, WB, True, [c - Lu for c in pulses], light=(1, -.25), clip=ABOVE_B, sigma=30.0)
        front = (up, dict(live=True, pulses=pulses, sigma=30.0))
    else:                                                                        # parted: dead, dark; the upper end springs back up and out of the picture
        if j in RECOIL:
            img = hose(img, path(*RECOIL[j]), WB, light=(1, -.25), **dead)
        if mouth[1] < WLB - 8:                                                   # the lower end stays in its teeth and goes down with it
            e2 = EB + np.array([14.0 * (j - 18), 0.0])
            img = hose(img, path(mouth, (mouth + e2) / 2 + np.array([-10.0, 24.0]), e2), WB, light=(1, -.25), clip=ABOVE_B, **dead)
            back = (BRK - mouth) / max(np.hypot(*(BRK - mouth)), 1e-6) if j == 18 else np.array([-.5, -.87])
            front = (path(mouth + back * 52.0, mouth + back * 26.0 + np.array([2.0, 0.0]), mouth), dead)
    if not flash:
        img = C.light(img, R([sh.lens(612, YB, 96, 3.4), sh.lens(640, YB + 6, 80, 2.8)]) * (.9 if b == 0 and j < 18 else .5), PALE, 1.3)
    pre = img.copy()
    img = orca(img, base[0], base[1], s=OS, flip=True, rot=rot, jaw=jaw, flash=flash)
    img[WLB:] = pre[WLB:]                                                        # the sea in front of it
    if front is not None:                                                        # the hose goes in at the side of its mouth
        img = hose(img, front[0], WB, light=(1, -.25), **front[1])
    # white water where it breaks the surface
    xs = np.nonzero(np.abs(img[WLB - 1] - pre[WLB - 1]).max(-1) > 1e-4)[0]
    if len(xs) and not flash:
        rng = np.random.default_rng(4000 + i)
        x0, x1 = xs.min() - 36, xs.max() + 36
        speed = C.clamp01(float(np.hypot(*(orca_at(min(j + 1, 23))[0] - base))) / 90.0)
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
            spikes.append(sh.seg(BRK + u * r0, BRK + u * r1, w=rng.uniform(3, 7), taper=(0, .9), wob=0))
        img = draw.paint(img, R(spikes), '#05070a')
    elif j >= 19:
        age = j - 18
        if j == 19:
            g = np.exp(-((np.arange(W)[None, :] - BRK[0]) ** 2 + (ROWS - BRK[1]) ** 2) / (2 * 190.0 ** 2)).astype(np.float32)
            img[..., :3] += C.core.col(C.COLD) * 3.2 * g[..., None]
        img = sparks(img, BRK, age)
        ends = [np.array(RECOIL[j][-1], float)] if j in RECOIL else []
        if front is not None:
            ends.append(front[0][0])
        rng = np.random.default_rng(600 + i)
        drip = [sh.chip(e[0] + rng.uniform(-14, 14), e[1] + rng.uniform(-10, 30), rng.uniform(2, 4)) for e in ends for _ in range(max(0, 6 - age))]
        if drip:
            img = C.light(img, R(drip), C.COLD, 6.0)
    return img


def frame(i):
    return frame_a(i) if i < 24 else frame_b(i)
