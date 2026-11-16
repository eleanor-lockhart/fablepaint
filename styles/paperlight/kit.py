"""Paperlight kit: patterns for cut paper. Everything returns a matte (white = paper) on a W x H
design canvas; a sheet is the union of its border and whatever stands on it, made cuttable."""
import math
import numpy as np
from backlot import draw, comp, shapes as sh

W, H, PPM, BORDER = 1280, 720, 4.0, 70
def setup(w=1280, h=720, ppm=4.0, border=70, seed=1):
    global W, H, PPM, BORDER
    W, H, PPM, BORDER = w, h, ppm, border; sh.setup(w, h, seed)

def border():
    return comp.subtract(np.ones((H, W), np.float32), draw.rect(W, H, BORDER, BORDER, W - BORDER, H - BORDER))

def land(pts, smooth=True):
    """Ground: everything below a line through the points (x, y)."""
    line = sh.spline(pts) if smooth else np.asarray(pts, float)
    return draw.raster([np.vstack([line, [(W + 40, H + 40), (-40, H + 40)]])], W, H)

def waves(y, amp=14, length=110, phase=0.0, lean=.35):
    """A sea sheet: a row of cusped crests, each leaning forward."""
    xs = np.arange(-length, W + length, 3.0)
    u = ((xs / length + phase) % 1.0)
    crest = np.sin(np.pi * u ** (1 - lean)) ** .8
    return land(np.c_[xs, y - amp * crest], smooth=False)

def sheet(*mattes, min_width=4.0):
    """Border plus shapes, made cuttable. Prints what was lost if it is more than a little."""
    m = border()
    for a in mattes: m = comp.union(m, a)
    out, lost = draw.paperize(m, min_width, anchor=border())
    if lost > .01: print(f'  paperize dropped {lost * 100:.1f}% of a sheet')
    return out

def holes(m, *cuts):
    for c in cuts: m = comp.subtract(m, c)
    return m

def fir(x, base, height, width, seed=None):
    """A conifer bold enough to cut: the kit's tree, fattened."""
    t_, f_ = sh.conifer(x, base, height, width, crown=.88, tuft=(11, 28), trunk_w=max(7, width * .07))
    return comp.grow(draw.raster(t_ + f_, W, H), 1)

def stars(n, y1, seed=4, rmin=1.4, rmax=3.2, avoid=None):
    """Pinholes for a sky sheet (returned as a matte of the HOLES)."""
    r = np.random.default_rng(seed); m = np.zeros((H, W), np.float32)
    for _ in range(n):
        x, y = r.uniform(BORDER + 10, W - BORDER - 10), r.uniform(BORDER + 10, y1)
        m = np.maximum(m, draw.disc(W, H, x, y, r.uniform(rmin, rmax) * (1.8 if r.uniform() < .08 else 1), soft=.8))
    return m if avoid is None else m * (1 - avoid)

def lighthouse(x, base, h=250):
    """Tower, gallery, lantern room with glazing bars, cap. Returns (paper matte, lantern centre (x, y))."""
    wb, wt = h * .2, h * .12
    top = base - h * .74
    tower = draw.raster([np.array([(x - wb / 2, base + 4), (x - wt / 2, top), (x + wt / 2, top), (x + wb / 2, base + 4)])], W, H)
    gal = draw.rect(W, H, x - wt * .95, top - 7, x + wt * .95, top + 2)
    lw, lh = wt * .78, h * .15
    lant = draw.rect(W, H, x - lw / 2, top - 7 - lh, x + lw / 2, top - 6)
    glass = np.zeros((H, W), np.float32)
    n = 3
    for i in range(n):
        gx0 = x - lw / 2 + 5 + i * (lw - 10) / n + 2.2; gx1 = x - lw / 2 + 5 + (i + 1) * (lw - 10) / n - 2.2
        glass = np.maximum(glass, draw.rect(W, H, gx0, top - 7 - lh + 6, gx1, top - 12))
    cap = draw.raster([np.array([(x - lw * .68, top - 6 - lh), (x, top - 6 - lh - h * .09), (x + lw * .68, top - 6 - lh)])], W, H)
    rod = draw.rect(W, H, x - 2.5, top - 6 - lh - h * .15, x + 2.5, top - 6 - lh - h * .05)
    door = draw.rect(W, H, x - wb * .13, base - h * .1, x + wb * .13, base + 4)
    wins = sum(draw.rect(W, H, x - 5, base - h * f, x + 5, base - h * f + 14) for f in (.34, .56))
    m = comp.union(comp.union(comp.union(tower, gal), comp.union(lant, cap)), rod)
    return holes(m, glass, wins), (x, top - 6 - lh / 2)

def visible(depth, cam_dist=545.0, lens=85.0, aspect=16 / 9, margin=0.0):
    """The part of a sheet the camera can see, in design pixels (x0, y0, x1, y1). A sheet nearer the
    lens shows less of itself: design each sheet for its own window, not for the whole canvas."""
    w_mm = 36.0 / lens * (cam_dist + depth) * (1 - margin); h_mm = w_mm / aspect
    return (W / 2 - w_mm / 2 * PPM, H / 2 - h_mm / 2 * PPM, W / 2 + w_mm / 2 * PPM, H / 2 + h_mm / 2 * PPM)

def lookout(cx, base, h=250):
    """A fire lookout cut for paper: front elevation, every member thick enough to hold.
    Returns (paper matte, centre of the cab windows (x, y))."""
    R = lambda *p: draw.raster([np.array(p)], W, H)
    def bar(a, b, w):
        a, b = np.array(a, float), np.array(b, float); d = b - a; n = np.array([-d[1], d[0]]) / max(np.hypot(*d), 1e-6) * w / 2
        return R(a + n, b + n, b - n, a - n)
    lw, tw = h * .34, h * .27                       # leg spread at the ground and under the deck
    deck = base - h * .58
    m = np.zeros((H, W), np.float32)
    for s in (-1, 1):
        m = np.maximum(m, bar((cx + s * lw / 2, base + 6), (cx + s * tw / 2, deck), 9))
    for (ya, yb) in ((base - 2, base - h * .29), (base - h * .29, deck)):
        fa = (ya - deck) / (base - deck); fb = (yb - deck) / (base - deck)
        xa, xb = (tw + (lw - tw) * fa) / 2, (tw + (lw - tw) * fb) / 2
        m = np.maximum(m, bar((cx - xa, ya), (cx + xb, yb), 6)); m = np.maximum(m, bar((cx + xa, ya), (cx - xb, yb), 6))
        m = np.maximum(m, bar((cx - xb, yb), (cx + xb, yb), 6))
    dw = h * .52
    m = np.maximum(m, draw.rect(W, H, cx - dw / 2, deck - 6, cx + dw / 2, deck + 4))                    # deck
    for x in np.linspace(cx - dw / 2 + 3, cx + dw / 2 - 3, 7):                                          # rail posts
        m = np.maximum(m, draw.rect(W, H, x - 2.5, deck - 26, x + 2.5, deck - 4))
    m = np.maximum(m, draw.rect(W, H, cx - dw / 2, deck - 30, cx + dw / 2, deck - 24))                  # rail
    cw, chh = h * .36, h * .2
    cab = draw.rect(W, H, cx - cw / 2, deck - 6 - chh, cx + cw / 2, deck - 4)
    roof = R((cx - cw * .68, deck - 6 - chh), (cx, deck - 6 - chh - h * .13), (cx + cw * .68, deck - 6 - chh))
    pipe = draw.rect(W, H, cx + cw * .2, deck - 6 - chh - h * .16, cx + cw * .2 + 6, deck - 6 - chh - 4)
    m = np.maximum(np.maximum(m, cab), np.maximum(roof, pipe))
    glass = np.zeros((H, W), np.float32); n = 4
    for i in range(n):
        x0 = cx - cw / 2 + 6 + i * (cw - 12) / n + 2.5; x1 = cx - cw / 2 + 6 + (i + 1) * (cw - 12) / n - 2.5
        glass = np.maximum(glass, draw.rect(W, H, x0, deck - chh + 4, x1, deck - 6 - chh * .34))
    return holes(m, glass), (cx, deck - 6 - chh * .6)
