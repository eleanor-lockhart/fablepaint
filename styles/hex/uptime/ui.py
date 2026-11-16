"""Hex, stage 3: a desktop of about the year 2000, drawn at full resolution.

The finish is contemporary (smooth gradients, gloss, soft shadows, a glow) and the colours are not: everything is
one of the sixteen registers or a blend between two of them. Type is the 8 x 8 ROM font at whole multiples, so
the letters stay hard while the chrome goes soft. Only register F glows.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
import cv2
from kit import RGB, glyph
C = RGB.astype(np.float32) / 255
W, H = 1280, 720

def mix(a, b, t): return C[a] * (1 - t) + C[b] * t
def vgrad(h, c0, c1): t = np.linspace(0, 1, max(h, 1), dtype=np.float32)[:, None, None]; return c0[None, None, :] * (1 - t) + c1[None, None, :] * t

def rect(img, x0, y0, x1, y1, c, a=1.0):
    x0, y0, x1, y1 = max(int(x0), 0), max(int(y0), 0), min(int(x1), img.shape[1]), min(int(y1), img.shape[0])
    if x1 > x0 and y1 > y0:
        if isinstance(c, np.ndarray) and c.ndim == 3 and len(c) != y1 - y0: c = c[np.linspace(0, len(c) - 1, y1 - y0).astype(int)]      # a gradient is stretched to fit
        img[y0:y1, x0:x1] = img[y0:y1, x0:x1] * (1 - a) + c * a

def rrect(img, x0, y0, x1, y1, r, c, a=1.0, top_only=False):
    """A rounded rectangle, anti-aliased. c is a colour or a (h, 1, 3) gradient. top_only rounds just the top corners."""
    X0, Y0, X1, Y1 = max(int(x0), 0), max(int(y0), 0), min(int(x1), img.shape[1]), min(int(y1), img.shape[0])
    if X1 <= X0 or Y1 <= Y0: return
    y, x = np.mgrid[Y0:Y1, X0:X1].astype(np.float32) + .5; yb = y1 + (r + 2 if top_only else 0)          # top_only: push the bottom corners out of sight
    dx = np.maximum(np.abs(x - (x0 + x1) / 2) - ((x1 - x0) / 2 - r), 0); dy = np.maximum(np.abs(y - (y0 + yb) / 2) - ((yb - y0) / 2 - r), 0)
    al = (np.clip(r + .5 - np.hypot(dx, dy), 0, 1) * a)[..., None]
    if isinstance(c, np.ndarray) and c.ndim == 3: c = c[Y0 - int(y0):Y1 - int(y0)]
    img[Y0:Y1, X0:X1] = img[Y0:Y1, X0:X1] * (1 - al) + c * al

_G = {}
def text(img, x, y, s, c, scale=2, shadow=None):
    for k, ch in enumerate(s):
        if ch == ' ': continue
        if (ch, scale) not in _G: _G[(ch, scale)] = np.kron(glyph(ch), np.ones((scale, scale), bool))
        g = _G[(ch, scale)]; gx, gy = int(x) + k * 8 * scale, int(y)
        for off, cc in (((scale, scale), shadow), ((0, 0), c)):
            if cc is None: continue
            X0, Y0 = gx + off[0], gy + off[1]; X1, Y1 = X0 + g.shape[1], Y0 + g.shape[0]
            a0, b0, a1, b1 = max(X0, 0), max(Y0, 0), min(X1, img.shape[1]), min(Y1, img.shape[0])
            if a1 > a0 and b1 > b0: img[b0:b1, a0:a1][g[b0 - Y0:b1 - Y0, a0 - X0:a1 - X0]] = cc
def tw(s, scale=2): return len(s) * 8 * scale

def blit(img, small, x, y, scale=2, key=None):
    """Paste an index canvas (h, w uint8) or an RGB array, scaled up with hard pixels. key: an index to leave out."""
    idx = small if small.ndim == 2 else None
    big = np.repeat(np.repeat(small, scale, 0), scale, 1); x, y = int(x), int(y)
    X0, Y0, X1, Y1 = max(x, 0), max(y, 0), min(x + big.shape[1], img.shape[1]), min(y + big.shape[0], img.shape[0])
    if X1 <= X0 or Y1 <= Y0: return
    part = big[Y0 - y:Y1 - y, X0 - x:X1 - x]
    if idx is not None:
        rgb = C[part]
        if key is None: img[Y0:Y1, X0:X1] = rgb
        else: m = part != key; img[Y0:Y1, X0:X1][m] = rgb[m]
    else: img[Y0:Y1, X0:X1] = part

_S = {}
def sprite(img, rows, x, y, scale=3, swap=None, flip=False):
    key = (id(rows), scale, tuple(sorted(swap.items())) if swap else None, flip)
    if key not in _S:
        wd = max(len(r) for r in rows); a = np.full((len(rows), wd), 255, np.uint8)
        for j, r in enumerate(rows):
            r = r.ljust(wd, '.'); r = r[::-1] if flip else r
            for i, ch in enumerate(r):
                if ch != '.': k = int(ch, 16); a[j, i] = swap.get(k, k) if swap else k
        _S[key] = a
    a = _S[key]; big = np.repeat(np.repeat(a, scale, 0), scale, 1); x, y = int(x), int(y)
    X0, Y0, X1, Y1 = max(x, 0), max(y, 0), min(x + big.shape[1], img.shape[1]), min(y + big.shape[0], img.shape[0])
    if X1 <= X0 or Y1 <= Y0: return
    part = big[Y0 - y:Y1 - y, X0 - x:X1 - x]; m = part != 255; img[Y0:Y1, X0:X1][m] = C[np.minimum(part, 15)][m]

BARS = dict(sys=(0xB, 0xC), hers=(5, 6), hive=(0xD, 0xE), off=(8, 9))
def window(img, x, y, w, h, title, bar='sys', close=True):
    """A window of the period: soft shadow, rounded top, a glossy title bar. Returns its content box (x, y, w, h)."""
    for k, a in ((14, .10), (9, .14), (5, .18)): rrect(img, x - k + 6, y - k + 10, x + w + k + 6, y + h + k + 10, 10 + k, C[0], a)
    rrect(img, x, y, x + w, y + h, 9, vgrad(h, C[0xA], C[9]))
    b0, b1 = BARS[bar]
    rrect(img, x + 2, y + 2, x + w - 2, y + 26, 8, vgrad(24, mix(b1, 0xA, .25), C[b0]), top_only=True)
    rrect(img, x + 6, y + 3, x + w - 6, y + 12, 5, C[0xA], .28)                                   # the gloss
    text(img, x + 12, y + 6, title, C[0xA], 2, shadow=mix(b0, 0, .5))
    if close: rrect(img, x + w - 26, y + 6, x + w - 8, y + 22, 8, vgrad(16, C[0xA], C[9])); text(img, x + w - 21, y + 10, 'x', C[0], 1)
    rect(img, x + 4, y + 28, x + w - 4, y + h - 4, C[0])
    return x + 4, y + 28, w - 8, h - 32

def button(img, x, y, w, h, label, pressed=False, tint=(0xC, 0xB)):
    """A pill of clear plastic."""
    c0, c1 = (mix(tint[1], 0, .2), C[tint[0]]) if pressed else (mix(tint[0], 0xA, .45), C[tint[1]])
    rrect(img, x, y + 1, x + w, y + h + 1, h / 2, C[0], .35); rrect(img, x, y, x + w, y + h, h / 2, vgrad(h, c0, c1))
    if not pressed: rrect(img, x + 5, y + 2, x + w - 5, y + h * .48, h * .22, C[0xA], .45)
    text(img, x + (w - tw(label)) // 2 + (1 if pressed else 0), y + (h - 14) // 2 + (1 if pressed else 0), label, C[0xA], 2, shadow=mix(tint[1], 0, .6))

def dialog(img, x, y, w, title, lines, buttons=(), bar='sys', pressed=None, body=None):
    """A dialog box. Returns the button boxes [(x, y, w, h)] so that a pointer can find them."""
    h = 28 + 16 + len(lines) * 24 + (46 if buttons else 6) + 8
    cx, cy, cw, ch = window(img, x, y, w, h, title, bar)
    rect(img, cx, cy, cx + cw, cy + ch, C[9] if body is None else body)
    for k, ln in enumerate(lines): text(img, cx + 14, cy + 14 + k * 24, ln, C[0], 2)
    out = []; bx = cx + 14
    for k, b in enumerate(buttons):
        bw = tw(b) + 30; by = cy + ch - 40
        button(img, bx, by, bw, 30, b, pressed == k, (6, 5) if bar == 'hers' else (0xC, 0xB)); out.append((bx, by, bw, 30)); bx += bw + 10
    return out

ARROW = np.array([(0, 0), (0, 17), (4, 13), (7, 20), (10, 19), (7, 12), (12, 12)], np.float32)
def pointer(img, x, y, k=6, scale=1.6):
    pts = (ARROW * scale + (x, y)).astype(np.int32)
    cv2.fillPoly(img, [pts], [float(v) for v in C[k]], cv2.LINE_AA); cv2.polylines(img, [pts], True, [float(v) for v in C[0]], 2, cv2.LINE_AA)

def strip(img, x, y, s=10, gap=2):
    rect(img, x - 4, y - 4, x + 16 * (s + gap) + 2, y + s + 4, C[0])
    for k in range(16): rect(img, x + k * (s + gap), y, x + k * (s + gap) + s, y + s, C[k])

def glow(img, strength=.55):
    """Only register F glows: find it, blur it, add it back."""
    d = np.abs(img - C[0xF]).sum(-1); m = np.clip(1 - d / .12, 0, 1).astype(np.float32)
    if m.max() <= 0: return img
    g = cv2.GaussianBlur(m, (0, 0), 7) * .9 + cv2.GaussianBlur(m, (0, 0), 28) * 1.6
    return np.clip(img + g[..., None] * C[0xF] * strength, 0, 1)
