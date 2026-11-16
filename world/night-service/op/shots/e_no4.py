"""e_no4 (bars 17-19, 72 poses): the break, then No. 4 revealed.
0-11  black.  12-23 black, and one slit of COLD light exactly where No. 4's eye will be.
24-47 the Sound under a huge moon; No. 4 knee-deep; a tilt from the waterline up to its head (lands on 48), a cold pulse
      running up the cable into its back on every beat.  48-71 hold on the FINAL placement, with the caption."""
import numpy as np
import common as C

N = 72
W, H = C.W, C.H
draw, sh = C.draw, C.sh
FINAL = dict(cx=600, waterline=1560, height=1300, moon=(640, 400, 300))
CX, WL, HT = FINAL['cx'], FINAL['waterline'], FINAL['height']
EYE = [(.075, .868), (.112, .858), (.112, .848), (.078, .856)]              # the eye, as common.no4 draws it
CABLE = [(-.03, .63), (-.2, .46), (-.36, .2), (-.5, -.01)]                  # the cable, as common.no4 draws it: back -> water
HERON = (-.110, .7725)                                                      # on its shoulder, against the moon


def R(polys): return draw.raster(polys, W, H)
def M(pts, off=0.0): return np.array([(CX + u * HT, WL - off - v * HT) for u, v in pts])


EYE_M = R([M(EYE)])


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
        img = draw.paint(img, R(sh.sheen(446, 523, wl + 2, wl + 150, th0=3, th1=5, keep=.85) + sh.sheen(636, 744, wl + 2, wl + 150, th0=3, th1=5, keep=.85)), '#0d1018', .9)
    img = C.no4(img, CX, wl, HT, eye=None, cable=True)
    P = sh.resample(sh.spline(M(CABLE, off)), 4.0)
    cw = HT * .009
    if P[:, 1].min() < H + 40:                                               # the cable is in the picture: it is live
        img = C.light(img, R([sh.ribbon(P, w=cw * .22, taper=(0, 0), wob=0, smooth=False)]) * .5, C.COLD, 1.0)
        d = np.r_[0, np.cumsum(np.hypot(*np.diff(P, axis=0).T))]
        b = i % 6
        for k in range(3):                                                   # three pulses a cable-length; one reaches its back on each beat
            c = d[-1] * (((6 - b) % 6) / 18.0 + k / 3.0)
            sel = np.abs(d - c) < 58
            if sel.sum() > 3:
                img = C.light(img, R([sh.ribbon(P[sel], w=cw * 1.25, taper=(.4, .4), wob=0, smooth=False)]), C.COLD, 7.0)
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
