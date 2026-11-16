"""NIGHT SERVICE opening, unit h_lineup: bars 28-31, 96 poses, 54-62 s.

0-47   THE LINEUP. The dock in front of the Sound. Left to right: the heron on its pile (its eye lit from pose 0: it was
       already watching), Orrin, Red, Dee, Marisol, a Passenger, Vesper Lang. Far out in the water, upper right, No. 4
       stands whole and dark against the moon (the shared placement "No. 4 against the moon", in miniature). Every window
       starts dark and they are struck one a beat: poses 0, 6, 12, 18, 24, 30. On 36 the seventh: No. 4's eye goes green
       and the window in its chest lights, warm. Hold. Only the moon's path on the water moves (on twos).
48-95  THE END CARD. Hard cut on 48 to the cold open in reverse: black; the same seven lights, small, in the same
       arrangement (six in a row low in the frame, No. 4's apart and higher); the sigil; NIGHT SERVICE; SOMEBODY HAS TO
       STAY UP. One plate, built at import, returned unchanged for every pose from 48 to 95.

Everything that does not move is built once, here, at import. frame(i) only composites."""
import numpy as np
import common as C
from backlot import core, draw, comp

N = 96
W, H = C.W, C.H
GROUND, SIZE, HZ = 595, 390, 440
LINE = (('keeper', 211, False), ('red', 358, False), ('dee', 506, False), ('marisol', 653, False), ('passenger', 819, False), ('lang', 1024, True))
HITS = (0, 6, 12, 18, 24, 30)                      # the six windows, one a beat
NO4_HIT, CARD = 36, 48                             # the seventh; the last hit
NO4 = (1160, 452, 380)                             # cx, waterline, height: far out, upper right
MOON = (NO4[0] + .031 * NO4[2], NO4[1] - .892 * NO4[2], .231 * NO4[2])      # where the moon sits behind it in e_no4 / f2_window
HERON = (90, GROUND - 96, .294)                    # feet x, feet y (the top of its pile), scale
# No. 4's two lights, in its own units (copied from common.no4 so they can be struck on the beat and reused on the end card)
EYE = ((.075, .868), (.112, .858), (.112, .848), (.078, .856))
CHEST = ((-.028, .700), (.030, .700), (.030, .628), (-.028, .628))
GLOW, STRIKE = 5.0, 2.0                            # settled glow of a window; how much harder it is struck on its first two poses

def _no4_matte(pts, cx, waterline, height):
    return draw.raster([np.array([C.no4_point(cx, waterline, height, u, v) for u, v in pts])], W, H)

def _window_poly(name, x, ground, size, flip=False):
    """The chest window of a standing member of the cast, in pixels (the polygon backlot.figure.draw_figure cuts)."""
    c = C.CAST[name]; J = c['fig'].joints(c['pose']); sx = -1.0 if flip else 1.0; sc = size * c['height']
    P = c['fig'].on_trunk(J, [(.250, -.002), (.250, .030), (.205, .030), (.205, -.002)])
    return np.c_[x + sx * P[:, 0] * sc, ground - P[:, 1] * sc]

def _crop(img, pad=4):
    ys, xs = np.nonzero(img[..., 3] > 0)
    return (slice(max(ys.min() - pad, 0), min(ys.max() + pad + 1, H)), slice(max(xs.min() - pad, 0), min(xs.max() + pad + 1, W)))

# ------------------------------------------------------------------ plates for the lineup (0-47)
def _build_line():
    """Each figure twice on clear film: dark (no window; lantern, ember and tablet put out too) and lit."""
    out = []
    for name, x, flip in LINE:
        lit = C.figure(core.canvas(W, H), name, x=x, ground=GROUND, size=SIZE, flip=flip, window=True, glow=0)
        lm = C.fg.draw_figure.lit.copy()
        dark = C.figure(core.canvas(W, H), name, x=x, ground=GROUND, size=SIZE, flip=flip, window=False, glow=0)
        dark[..., :3] *= 1 - .9 * C.fg.draw_figure.lit[..., None]          # whatever the figure carries that glows is out until its window is lit
        sl = _crop(lit)
        out.append((sl, dark[sl].copy(), lit[sl].copy(), lm[sl].copy()))
    return out

def _build_front():
    """The dock, the pile and the heron, on clear film."""
    img = core.canvas(W, H)
    img = draw.paint(img, draw.rect(W, H, 0, GROUND, W, H), C.DOCK)
    img = draw.paint(img, draw.rect(W, H, 0, GROUND, W, GROUND + 2), '#2a3550')
    hx, hy, hs = HERON
    img = draw.paint(img, draw.rect(W, H, hx - 26, hy, hx + 26, GROUND), '#0a0e18')
    return C.heron(img, hx, hy, s=hs)

_FIGS = _build_line()
_FRONT = _build_front()
_NO4 = C.no4(core.canvas(W, H), *NO4, cable='cut')
_EYE, _CHEST = _no4_matte(EYE, *NO4), _no4_matte(CHEST, *NO4)

def _lineup(i):
    img = C.harbour(hz=HZ, moon=MOON, shimmer=i // 2)
    img = comp.over(img, _NO4)
    if i >= NO4_HIT:
        k = STRIKE if i - NO4_HIT < 2 else 1.0
        img = C.light(C.light(img, _EYE, C.GREEN, 6.0 * k), _CHEST, C.LAMP, 5.0 * k)
    img = comp.over(img, _FRONT)
    for (sl, dark, lit, lm), hit in zip(_FIGS, HITS):
        if i < hit:
            img[sl] = comp.over(img[sl], dark)
        else:
            f = lit.copy(); f[..., :3] *= 1 + lm[..., None] * GLOW * (STRIKE if i - hit < 2 else 1.0)
            img[sl] = comp.over(img[sl], f)
    return img

# ------------------------------------------------------------------ the end card (48-95): one plate
CARD_K, CARD_CX, CARD_ROW = .75, 640.0, 590.0      # the lineup's lights at 3/4 size, the row of six this low in the frame

def _build_card():
    polys = [(_window_poly(name, x, GROUND, SIZE, flip), C.CAST[name]['window'], 1.0 + GLOW) for name, x, flip in LINE]
    x0 = np.mean([p[:, 0].mean() for p, _, _ in polys]); y0 = np.mean([p[:, 1].mean() for p, _, _ in polys])
    T = lambda P: np.c_[CARD_CX + (np.asarray(P, float)[:, 0] - x0) * CARD_K, CARD_ROW + (np.asarray(P, float)[:, 1] - y0) * CARD_K]
    polys += [(np.array([C.no4_point(*NO4, u, v) for u, v in EYE]), C.GREEN, 6.0), (np.array([C.no4_point(*NO4, u, v) for u, v in CHEST]), C.LAMP, 5.0)]
    img = C.black()
    for P, colour, k in polys:
        img = C.light(img, draw.raster([T(P)], W, H), colour, k)
    hx, hy, hs = HERON                                                     # the heron's eye, where it stood: still watching
    ex, ey = T([(hx + 119 * hs, hy - 509 * hs)])[0]
    img = C.light(img, draw.disc(W, H, ex, ey, 1.7), C.LAMP, 2.5)
    # lettering: the sigil, the title, the tagline
    size = 132; track = size * .12
    m = C.text((0, 0), 'NIGHT SERVICE', size, track=track); ys, xs = np.nonzero(m > .5)
    cap, wd = ys.max() - ys.min() + 1, xs.max() - xs.min() + 1
    gap = 30; left = (W - (cap + gap + wd)) / 2; top = 178
    img = C.sigil(img, left, top, s=cap)
    tx = left + cap + gap - xs.min()
    img = C.write(img, (tx, top - ys.min()), 'NIGHT SERVICE', size, track=track)
    img = C.write(img, (left + cap + gap + 3, top + cap + 34), 'SOMEBODY HAS TO STAY UP.', 34, colour=C.DIM, track=8)
    return img

_CARD = _build_card()

def frame(i):
    if i >= CARD:
        return _CARD.copy()
    return _lineup(i)
