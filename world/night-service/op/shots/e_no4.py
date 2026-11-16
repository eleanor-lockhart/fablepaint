"""e_no4 (bars 17-19, 72 poses): the break, then No. 4 revealed.
0-11  black.  12-23 black, and one slit of COLD light exactly where No. 4's eye will be.
24-47 the Sound under a huge moon; No. 4 knee-deep; a tilt from the waterline up to its head (lands on 48). Its cable is a
      hose as thick as a ferry's funnel, hanging slack from a coupling in its back down into the water; a cold pulse
      travels up INSIDE it and reaches the coupling on every beat.  48-71 hold on the FINAL placement, with the caption."""
import math
import numpy as np
import common as C

N = 72
W, H = C.W, C.H
draw, sh = C.draw, C.sh
FINAL = dict(cx=600, waterline=1560, height=1300, moon=(640, 400, 300))
CX, WL, HT = FINAL['cx'], FINAL['waterline'], FINAL['height']
EYE = [(.075, .868), (.112, .858), (.112, .848), (.078, .856)]              # the eye, as common.no4 draws it
# the cable, drawn here (not by common.no4) so that it reads as a cable: out of a socket in its back, over, down, and away along the water
HOSE_UV = [(-.115, .612), (-.18, .585), (-.235, .545), (-.270, .487), (-.292, .405), (-.306, .32), (-.322, .235), (-.345, .165),
           (-.376, .105), (-.414, .055), (-.46, .015), (-.52, -.012)]
HOSE_W = HT * .027                                                          # three times the kit's line
HOSE, RIMC, RIBC = '#191622', '#4d5b73', '#0c0a13'
ROWS = np.arange(H, dtype=np.float32)[:, None]
HERON = (-.110, .7725)                                                      # on its shoulder, against the moon


def R(polys): return draw.raster(polys, W, H)
def M(pts, off=0.0): return np.array([(CX + u * HT, WL - off - v * HT) for u, v in pts])


EYE_M = R([M(EYE)])


def hose(img, P, w, live=True, pulses=(), light=(-.4, -1.0), body=HOSE, rim=RIMC, k=3.6, sigma=34.0, clip=None):
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


def coupling(img, P, w):
    """Where the hose goes into its back: a flange bolted to the plate, and two collars on the hose."""
    c0 = P[0]; t = P[3] - P[0]; t = t / np.hypot(*t); n = np.array([-t[1], t[0]])
    quad = lambda a, b, h: np.array([c0 + t * a + n * h, c0 + t * b + n * h, c0 + t * b - n * h, c0 + t * a - n * h])
    octa = lambda r, o=0.0: np.array([c0 - t * .15 * w + r * np.array([math.cos(a), math.sin(a)]) for a in np.linspace(0, 2 * np.pi, 8, endpoint=False) + np.pi / 8 + o])
    img = draw.paint(img, R([octa(w * .98)]), '#34314b')
    img = draw.paint(img, R([octa(w * .86)]), '#1f1c2b')
    img = draw.paint(img, R([octa(w * .92, o)[:1].repeat(3, 0) + np.array([(-2.5, -2.5), (2.5, -2.5), (0, 3.0)]) for o in np.linspace(0, 2 * np.pi, 8, endpoint=False)]), '#34314b')
    img = draw.paint(img, R([quad(.30 * w, .78 * w, .74 * w), quad(1.08 * w, 1.40 * w, .64 * w)]), '#34314b')
    return draw.paint(img, R([quad(.50 * w, .58 * w, .74 * w), quad(1.21 * w, 1.27 * w, .64 * w)]), '#15121d')


def ferry(img, x, y, L):
    """The Kittiwake, tiny."""
    P = lambda pts: np.array([(x + u * L, y - v * L) for u, v in pts])
    dark = [P([(0, .046), (.035, 0), (.965, 0), (1, .046)]), P([(.012, .044), (.988, .044), (.988, .088), (.012, .088)]),
            P([(.07, .086), (.93, .086), (.93, .128), (.07, .128)]), P([(.20, .126), (.80, .126), (.80, .153), (.20, .153)]),
            P([(.455, .15), (.545, .15), (.535, .215), (.465, .215)])]
    img = draw.paint(img, R(dark), '#080b12')
    img = C.light(img, R([P([(.085, .096), (.915, .096), (.915, .120), (.085, .120)]), P([(.215, .132), (.785, .132), (.785, .147), (.215, .147)])]), C.LAMP, 3.2)
    return C.light(img, R([sh.lens(x + .1 * L + 9 * k, y + 4 + 4 * k, L * (.8 - .13 * k), 1.6) for k in range(4)]), C.LAMP, 1.2)


def scene(off, i, eye_k, live=True):
    """The whole scene slid `off` pixels up from FINAL (off = 1000: its legs at the waterline; 0: FINAL)."""
    hz, wl = 1540 - off, WL - off
    img = C.harbour(hz=hz, moon=(640, 400 - off, 300), road=False)
    if hz < H:
        sh.setup(W, H, 9000 + i // 2)
        img = C.light(img, R(sh.moonroad(640, hz + 3, hz + 190, w0=330, w1=520, th0=1.4, th1=4.2)), '#efe6cc', 1.6)
        img = ferry(img, 842, hz + 9, 92)
        sh.setup(W, H, 77 + i // 2)
        img = draw.paint(img, R(sh.sheen(446, 523, wl + 2, wl + 150, th0=3, th1=5, keep=.85) + sh.sheen(636, 744, wl + 2, wl + 150, th0=3, th1=5, keep=.85) + sh.sheen(-30, 64, wl + 3, wl + 90, th0=3, th1=5, keep=.85)), '#0d1018', .9)
    img = C.no4(img, CX, wl, HT, eye=None, cable=False)
    P = sh.resample(sh.spline(M(HOSE_UV, off)), 4.0)
    if P[:, 1].min() - HOSE_W * 1.2 < H:                                     # the hose is in the picture: it is live
        d = float(np.hypot(*np.diff(P, axis=0).T).sum())
        b = i % 6                                                            # three pulses a hose-length; one reaches the coupling on each beat
        img = hose(img, P, HOSE_W, True, [d * (((6 - b) % 6) / 18.0 + k / 3.0) for k in range(3)], clip=np.clip(wl + 3 - ROWS, 0, 1))
        img = coupling(img, P, HOSE_W)
    hx, hy = CX + HERON[0] * HT, wl - HERON[1] * HT
    if -60 < hy < H + 60:
        img = C.heron(img, hx, hy, s=.075, flip=True)
    if eye_k:
        img = C.light(img, R([M(EYE, off)]), C.COLD, eye_k)
    return img


def eye_k(i):
    """Cold, and a little brighter each time a pulse arrives."""
    return (9.5, 7.5)[i % 6] if i % 6 < 2 else 6.0


def card(img, t):
    """The standard card, on the right, for someone who is not in the cast list: no window, an eye."""
    x0 = W - 84
    a = C.ease(C.clamp01(t / .22), 'out'); b = C.ease(C.clamp01((t - .10) / .25), 'out')
    img = draw.paint(img, draw.rect(W, H, x0 - 244 * a, 566, x0, 572), C.RED)
    wipe = draw.rect(W, H, x0 - 700 * b, 0, W, H)
    img = draw.paint(img, C.text((x0 + 7, 458), 'NO. 4', 96, track=7, anchor='r') * wipe, C.INK)
    img = draw.paint(img, C.text((x0 + 4, 584), 'THE LINEMAN', 28, track=6, anchor='r') * wipe, C.DIM)
    wx = x0 - 262 * a - 30
    return C.light(img, R([np.array([(wx, 564), (wx + 30, 567), (wx + 30, 574), (wx + 2, 572)])]) * a, C.COLD, 5.0)


HOLD = scene(0, 0, None)


def frame(i):
    if i < 12:
        return C.black()
    if i < 24:
        return C.light(C.black(), EYE_M, C.COLD, 11.0 if i < 14 else 6.0)
    if i < 48:
        off = 1000.0 * (1 - C.ease((i - 24) / 24.0, 'inout'))
        return scene(off, i, eye_k(i))
    k = (26.0, 16.0)[i - 48] if i < 50 else eye_k(i)             # director's pass: the camera arrives ON the hit, so the eye is struck
    img = C.light(HOLD.copy(), EYE_M, C.COLD, k)
    return card(img, C.clamp01((i - 48) / 16.0))
