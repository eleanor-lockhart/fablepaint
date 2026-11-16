"""backlot.draw: mattes and fills in memory. No session, no files: fast enough to redraw every frame.

    m = raster(polys, w, h)            polygons -> matte
    img = paint(img, m, '#223344')     lay a pigment through a matte
    g = gradient(w, h, p0, p1, stops)  an even gradation as an image
"""
import numpy as np
import cv2
from .core import F, col, s2l

def raster(polys, w, h, ss=2):
    """Float matte (h, w) of the polygons, each filled on its own, anti-aliased by supersampling."""
    m = np.zeros((h * ss, w * ss), np.uint8)
    for p in polys:
        q = np.asarray(p, np.float64)[:, :2]
        if len(q) >= 3:
            cv2.fillPoly(m, [np.round(q * (ss * 16)).astype(np.int32)], 255, lineType=cv2.LINE_8, shift=4)
    return cv2.resize(m, (w, h), interpolation=cv2.INTER_AREA).astype(F) / 255

def rect(w, h, x0, y0, x1, y1):
    m = np.zeros((h, w), F); m[int(max(y0, 0)):int(y1), int(max(x0, 0)):int(x1)] = 1
    return m

def disc(w, h, cx, cy, r, soft=1.0):
    y, x = np.mgrid[:h, :w].astype(F)
    return np.clip((r - np.hypot(x - cx, y - cy)) / soft + .5, 0, 1)

def paint(img, matte, color, opacity=1.0):
    """Lay one flat colour over the image through a matte (normal blend, premultiplied)."""
    a = (np.asarray(matte, F) * opacity)[..., None]
    c = np.concatenate([col(color), [1]]).astype(F)
    return img * (1 - a) + c * a

def erase(img, matte, depth=1.0):
    """Cut the matte out of the image (what is underneath will show)."""
    return img * (1 - np.asarray(matte, F) * depth)[..., None]

def stops(*cols, n=24, ease=1.0):
    """Even-looking gradient stops: (position, linear rgb), interpolated in display space."""
    cs = [(c, i / (len(cols) - 1)) if isinstance(c, str) else c for i, c in enumerate(cols)]
    rgb = np.array([[int(c[0].lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)] for c in cs], float) / 255
    pos = np.array([c[1] for c in cs], float)
    t = np.linspace(0, 1, n + 1)
    return t, s2l(np.stack([np.interp(t ** ease, pos, rgb[:, k]) for k in range(3)], 1))

def gradient(w, h, p0, p1, *cols, kind='linear', ease=1.0):
    """An opaque gradation image from p0 to p1 through the colours (or (colour, position) pairs)."""
    y, x = np.mgrid[:h, :w].astype(F)
    if kind == 'radial':
        t = np.hypot(x - p0[0], y - p0[1]) / max(np.hypot(p1[0] - p0[0], p1[1] - p0[1]), 1e-6)
    else:
        d = np.array(p1, float) - np.array(p0, float)
        t = ((x - p0[0]) * d[0] + (y - p0[1]) * d[1]) / max(float(d @ d), 1e-6)
    ts, cs = stops(*cols, ease=ease)
    t = np.clip(t, 0, 1)
    out = np.empty((h, w, 4), F); out[..., 3] = 1
    for k in range(3):
        out[..., k] = np.interp(t, ts, cs[:, k])
    return out

def fbm(w, h, scale=6.0, octaves=5, seed=0, stretch=(1.0, 1.0), ridged=False):
    """Fractal value noise in 0..1. `scale` = cells across the width; stretch multiplies frequency per axis."""
    r = np.random.default_rng(seed)
    out = np.zeros((h, w), F); amp, tot, f = 1.0, 0.0, float(scale)
    for _ in range(octaves):
        gx = min(w, max(2, int(round(f * stretch[0])) + 1)); gy = min(h, max(2, int(round(f * stretch[1] * h / w)) + 1))
        n = cv2.resize(r.random((gy, gx), dtype=F), (w, h), interpolation=cv2.INTER_CUBIC)
        out += amp * (1 - np.abs(2 * n - 1) if ridged else n); tot += amp; amp *= .5; f *= 2
    out /= tot
    lo, hi = np.percentile(out[::4, ::4], [.5, 99.5])
    return np.clip((out - lo) / max(hi - lo, 1e-6), 0, 1)

def trace(matte, tol=.6, min_area=6.0, level=.5):
    """Turn a matte into cut lines: a list of {'pts': [[x, y], ...], 'hole': bool}, in pixels.
    This is how a 2D design becomes a pattern the model shop can cut out of paper."""
    m = (np.asarray(matte) >= level).astype(np.uint8)
    cs, hier = cv2.findContours(m, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    out = []
    if hier is None:
        return out
    for c, hi in zip(cs, hier[0]):
        if cv2.contourArea(c) < min_area:
            continue
        c = cv2.approxPolyDP(c, tol, True)
        if len(c) >= 3:
            out.append({'pts': c[:, 0, :].astype(float).tolist(), 'hole': bool(hi[3] >= 0)})
    return out

def paperize(matte, min_width=4.0, anchor=None, level=.5):
    """Make a design cuttable. Paper cannot hold a strip thinner than about a millimetre, and a piece
    that is not joined to the rest falls out. Removes strips narrower than `min_width` pixels and every
    island not connected to `anchor` (a matte, e.g. the sheet's border; default: the largest piece).
    Returns (clean matte, fraction of the design that was lost)."""
    m = (np.asarray(matte) >= level).astype(np.uint8)
    k = max(1, int(round(min_width)))
    opened = cv2.morphologyEx(m, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
    n, lab = cv2.connectedComponents(opened, connectivity=4)
    if n <= 1:
        return opened.astype(F), 1.0
    if anchor is not None:
        keep = np.unique(lab[(np.asarray(anchor) >= level) & (opened > 0)])
    else:
        keep = [1 + int(np.argmax(np.bincount(lab[lab > 0].ravel())[1:]))]
    out = np.isin(lab, [v for v in keep if v != 0]).astype(F)
    lost = 1 - float(out.sum()) / max(float(m.sum()), 1)
    return out, lost
