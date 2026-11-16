"""f2_window (bars 26-27, 48 poses): the eye turns green; a window opens in No. 4's chest.
0-5   the FINAL placement e_no4 ended on; the eye is dark (the cable is cut), a few last sparks come up from its back.
6     the eye opens GREEN.   8-22 an eased tilt and push from the eye down to the chest plate and its stencil.
24    a slit of warm light in the chest plate; it opens like a pair of shutters over six poses.
30-47 hold: the window, and in it, among scratched lines, I AM TOLD I WROTE THE LAST ENTRY."""
import math
import numpy as np
import cv2
import common as C

N = 48
W, H = C.W, C.H
draw, sh, comp = C.draw, C.sh, C.comp
FINAL = dict(cx=600, waterline=1560, height=1300, moon=(640, 400, 300))
CX, WL, HT = FINAL['cx'], FINAL['waterline'], FINAL['height']
EYE = [(.075, .868), (.112, .858), (.112, .848), (.078, .856)]              # the eye, as common.no4 draws it
CHEST = (-.028, .030, .628, .700)                                           # the chest window, as common.no4 draws it (u0, u1, v0, v1)
HERON = (-.110, .7725)                                                      # where e_no4 left it
ZEND = 3.6
F0, F1 = (.0935, .858), (.001, .664)                                        # what the camera looks at: the eye, then the window
P0, P1 = C.no4_eye(CX, WL, HT), (640.0, 440.0)                              # and where on the screen that is


def R(polys): return draw.raster(polys, W, H)
def ngon(cx, cy, r, n=12):
    a = np.linspace(0, 2 * np.pi, n, endpoint=False)
    return np.c_[cx + r * np.cos(a), cy + r * np.sin(a)]


def place(t):
    """No. 4's placement (cx, waterline, height) and the zoom, t = 0 (FINAL) .. 1 (the chest)."""
    z = math.exp(math.log(ZEND) * t); h = HT * z
    return C.lerp(P0[0], P1[0], t) - C.lerp(F0[0], F1[0], t) * h, C.lerp(P0[1], P1[1], t) + C.lerp(F0[1], F1[1], t) * h, h, z


# plates, seams and bolts of the chest, in No. 4's own units
SEAM_H = [(.722, -.178, .178), (.612, -.158, .158)]
SEAM_V = [(-.078, .565, .722), (.080, .565, .722)]
HATCH = (-.040, .042, .616, .712)
BOLTS = [(u, .722 - .0065) for u in np.arange(-.169, .17, .026)] + [(u, .612 - .0065) for u in np.arange(-.143, .15, .026)]
BOLTS += [(su * .0725 + .001, v) for su in (-1, 1) for v in np.arange(.578, .71, .026)]
BOLTS += [(u, v) for u in (-.034, .001, .036) for v in (.622, .706)] + [(u, .664) for u in (-.034, .036)]


def plates(cx, wl, h):
    """(groove matte, lip matte): seams cut into the chest and the edges and bolt heads that catch light."""
    P = lambda u, v: (cx + u * h, wl - v * h)
    lw = max(1.1, .0011 * h); br = .0023 * h
    def hline(v, u0, u1, dy):
        (x0, y), (x1, _) = P(u0, v), P(u1, v)
        return np.array([(x0, y + dy), (x1, y + dy), (x1, y + dy + lw), (x0, y + dy + lw)])
    def vline(u, v0, v1, dx):
        (x, y0), (_, y1) = P(u, v1), P(u, v0)
        return np.array([(x + dx, y0), (x + dx + lw, y0), (x + dx + lw, y1), (x + dx, y1)])
    u0, u1, v0, v1 = HATCH
    hs = SEAM_H + [(v0, u0, u1), (v1, u0, u1)]; vs = SEAM_V + [(u0, v0, v1), (u1, v0, v1)]
    groove = [hline(v, a, b, 0) for v, a, b in hs] + [vline(u, a, b, 0) for u, a, b in vs]
    lip = [hline(v, a, b, lw) for v, a, b in hs] + [vline(u, a, b, lw) for u, a, b in vs]
    groove += [ngon(P(u, v)[0] + br * .28, P(u, v)[1] + br * .32, br) for u, v in BOLTS]
    lip += [ngon(*P(u, v), br * .86) for u, v in BOLTS]
    return R(groove), R(lip)


def scene(t, eye=None, eye_k=6.0):
    cx, wl, h, z = place(t)
    img = C.harbour(hz=wl - 20 * z, moon=(cx + 40 * z, wl - 1160 * z, 300 * z), road=False)
    img = C.no4(img, cx, wl, h, eye=None, cable='cut')
    hx, hy = cx + HERON[0] * h, wl - HERON[1] * h
    if -80 * z < hy < H + 80 * z and hx > -80 * z:
        img = C.heron(img, hx, hy, s=.075 * z, flip=True)
    if t > 0:
        groove, lip = plates(cx, wl, h)
        img = draw.paint(img, groove, '#07060b', t)
        img = draw.paint(img, lip, '#2b2942', t)
    em = R([np.array([(cx + u * h, wl - v * h) for u, v in EYE])])
    return C.light(img, em, eye, eye_k) if eye else draw.paint(img, em, '#262338')      # unlit, the eye is only a socket


# ------------------------------------------------------------------ the two ends of the move, and what is in the window
PLATE0 = scene(0.0)
PLATE0G = scene(0.0, C.GREEN, 6.0)
PLATE1 = scene(1.0)
CX1, WL1, H1, _ = place(1.0)
WX0, WX1, WY0, WY1 = CX1 + CHEST[0] * H1, CX1 + CHEST[1] * H1, WL1 - CHEST[3] * H1, WL1 - CHEST[2] * H1
WXC = (WX0 + WX1) / 2
LIP1 = plates(CX1, WL1, H1)[1]
_sz = int(H1 * .034)
STEN1 = C.text((CX1, WL1 - .745 * H1 - _sz * .6), 'CONTINUITY', _sz, track=_sz * .12, anchor='m')
LINES = ('I AM TOLD', 'I WROTE THE', 'LAST ENTRY.')


def _writing():
    """The page behind the shutters: scratched lines nobody can read, and one that can be."""
    rng = np.random.default_rng(11)
    x0, x1 = WX0 + 22, WX1 - 20
    polys = []
    def scratch(y, xa, xb):
        x = xa
        while x < xb - 18:
            ln = min(rng.uniform(18, 58), xb - x); pts = []; px = x
            while px < x + ln:
                pts.append((px, y + rng.uniform(-10, -1) if len(pts) % 2 else y + rng.uniform(-3, 3))); px += rng.uniform(3.5, 6.5)
            if len(pts) > 2:
                polys.append(sh.ribbon(pts, w=3.0, taper=(.1, .1), wob=0))
            x += ln + rng.uniform(9, 15)
    size = 46
    while max(C.font(size).getlength(s) + 2 * len(s) for s in LINES) > x1 - x0 - 6:
        size -= 1
    top = (WY0 + WY1) / 2 - 1.62 * size
    for k, y in enumerate((WY0 + 30, WY0 + 55)):
        scratch(y, x0, x1 - (0, 36)[k])
    y = top + 3.42 * size + 26
    k = 0
    while y < WY1 - 12:
        scratch(y, x0, x1 - (10, 0, 52, 120)[k % 4]); y += 25; k += 1
    m = R(polys)
    for k, s in enumerate(LINES):
        m = np.maximum(m, C.text((x0 + (0, 5, 2)[k], top + k * size * 1.08), s, size, track=2))
    shear = -.13                                                               # written with the hand leaning
    yc = (WY0 + WY1) / 2
    return cv2.warpAffine(m, np.float32([[1, shear, -shear * yc], [0, 1, 0]]), (W, H), flags=cv2.INTER_LINEAR)


WRITING = _writing()
OPEN = {24: .05, 25: .14, 26: .32, 27: .56, 28: .80, 29: .95}
GLOW = {24: 7.0, 25: 6.0, 26: 4.8, 27: 3.8, 28: 3.1, 29: 2.6}
_r = np.random.default_rng(5)
SPARKS = [(_r.uniform(486, 566), _r.uniform(700, 726), _r.uniform(-5, 5), _r.uniform(-17, -8), int(_r.integers(2, 7))) for _ in range(12)]


def window(img, o, k):
    """The chest window, the shutters a fraction o open, the light k strong."""
    hw = (WX1 - WX0) / 2 * o
    vis = draw.rect(W, H, WXC - hw, WY0, WXC + hw, WY1)
    img = C.light(img, vis, C.LAMP, k)
    img = draw.paint(img, WRITING * vis, '#1c0c02', 1.0)
    lamp = C.core.col(C.LAMP)
    near, far = comp.feather(vis, 42), comp.feather(vis, 130)
    img[..., :3] += lamp * (np.clip(near * 1.2, 0, 1) * (1 - vis) * .20 * k / 3.0)[..., None]                   # warm light on the plate round it
    img[..., :3] += lamp * ((LIP1 * 1.1 + STEN1 * .30) * np.clip(far * 2.4, 0, 1) * (1 - vis) * k / 2.4)[..., None]   # and on every edge that faces it
    return img


HOLD = window(PLATE1.copy(), 1.0, 2.3)


def frame(i):
    if i < 6:                                                                    # dark: the cable is cut
        img = PLATE0.copy()
        polys = [sh.seg((x + vx * i, y + vy * i + .9 * i * i), (x + vx * (i + .45), y + vy * (i + .45) + .9 * (i + .45) ** 2), w=2.6, taper=(.4, 0), wob=0)
                 for x, y, vx, vy, life in SPARKS if i < life]
        return C.light(img, R(polys), C.COLD, 6.0) if polys else img
    if i < 8:                                                                    # green: it is itself
        return C.light(PLATE0.copy(), R([np.array([(CX + u * HT, WL - v * HT) for u, v in EYE])]), C.GREEN, 12.0)
    if i < 22:
        t = C.ease((i - 8) / 14.0, 'inout')
        return PLATE0G.copy() if t <= 0 else scene(t, C.GREEN, 6.0)
    if i < 24:
        return PLATE1.copy()
    if i < 30:
        return window(PLATE1.copy(), OPEN[i], GLOW[i])
    return HOLD.copy()
