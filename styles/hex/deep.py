"""Hex in depth: how the sixteen registers behave in a place with light in it.

`backlot.depth` works out what is seen and how much light falls on it. This file decides what that looks like in
Hex, and the rule is short: **light has no colour. It only moves a thing between the void and itself.**

    PAINT            the registers 0..F, then the blends a material needs (wood, brick, rust): each a fixed
                     mixture of two registers, made with blend(a, b, t) and used like any other index
    colour(g, level) the picture: every texel is its own paint, darkened toward register 0 by how little light
                     it gets, in a few steps, dithered between steps on the texel grid (so the dither is part
                     of the wall and does not crawl when the camera moves)
    sprite(rows)     a text sprite as an index array for depth.card
    tile helpers     bricks, planks, blocks, speckle: procedural skins on the 5 cm grid

Register F is still reserved, and it is still the only thing that glows.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent)); sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import numpy as np
import cv2
from kit import RGB, BAYER
from backlot.depth import HOLE

PAINT = [tuple(c) for c in (RGB.astype(np.float64) / 255)]; _B = {}
def blend(a, b, t):
    """A new paint: register a, mixed t of the way toward register b. Returns its index."""
    k = (a, b, round(t, 3))
    if k not in _B: _B[k] = len(PAINT); PAINT.append(tuple(np.array(PAINT[a]) * (1 - t) + np.array(PAINT[b]) * t))
    return _B[k]
def table(): return np.array(PAINT + [(0, 0, 0)] * (256 - len(PAINT)), np.float32)

def colour(g, level, steps=6, gamma=.8, dark=0, over=.0, dither=1.0):
    """(h, w, 3) float32 in 0..1. level: from depth.lighting. steps: how many tones each paint has between the
    void and itself. A solid with glow shows that much of its own colour whatever the light."""
    T = table(); base = T[g['index']]; lv = np.maximum(np.clip(level, 0, 1) ** gamma, g['glow'])
    t = lv * steps; lo = np.floor(t); d = BAYER[g['v'] % 4, g['u'] % 4]
    q = np.clip((lo + ((t - lo) > .5 + (d - .5) * dither)) / steps, 0, 1)[..., None]
    img = T[dark][None, None, :] * (1 - q) + base * q
    if over: img = img + (T[0xA][None, None, :] - img) * (np.clip(level - 1, 0, 1) * over)[..., None]
    img[~g['hit']] = T[dark]
    return img.astype(np.float32)

def sprite(rows, swap=None, flip=False):
    """Text rows (one hex digit a pixel, '.' nothing; letters above F via `swap`) -> an index array with HOLEs."""
    wd = max(len(r) for r in rows); a = np.full((len(rows), wd), HOLE, np.uint8)
    for j, r in enumerate(rows):
        r = r.ljust(wd, '.'); r = r[::-1] if flip else r
        for i, ch in enumerate(r):
            if ch == '.': continue
            k = swap[ch] if swap and ch in swap else int(ch, 16); a[j, i] = swap.get(k, k) if swap else k
    return a

# ------------------------------------------------------------------ skins, on the 5 cm grid
def speckle(h, w, base, others, p=.12, seed=1):
    r = np.random.default_rng(seed); a = np.full((h, w), base, np.uint8); m = r.random((h, w))
    for k, o in enumerate(others): a[(m > k * p / len(others)) & (m <= (k + 1) * p / len(others))] = o
    return a
def bricks(brick, mortar, bw=7, bh=3, odd=None, seed=2, rows=8, cols=8):
    """Running bond: bricks bw x bh texels with one texel of mortar. `odd`: paints for the occasional brick."""
    r = np.random.default_rng(seed); W_, H_ = (bw + 1) * cols, (bh + 1) * rows; a = np.full((H_, W_), mortar, np.uint8)
    for j in range(rows):
        for i in range(cols):
            c = brick if odd is None or r.random() > .3 else odd[int(r.integers(len(odd)))]; x0 = i * (bw + 1) + (j % 2) * ((bw + 1) // 2)
            for x in range(bw): a[j * (bh + 1):j * (bh + 1) + bh, (x0 + x) % W_] = c
    return a
def planks(a_, b_, gap, width=4, length=48, along='u', seed=3, n=8):
    """Boards: `width` texels wide with a one-texel joint of `gap`, butt joints staggered, two tones."""
    r = np.random.default_rng(seed); H_, W_ = (width + 1) * n, length; t = np.full((H_, W_), a_, np.uint8)
    for j in range(n):
        y0 = j * (width + 1); t[y0:y0 + width] = a_ if r.random() > .45 else b_; t[y0 + width] = gap
        t[y0:y0 + width, int(r.integers(W_))] = gap
        for _ in range(3): x = int(r.integers(W_ - 5)); t[y0 + int(r.integers(width)), x:x + int(r.integers(2, 5))] = b_ if t[y0, (x + 7) % W_] == a_ else a_
    return t if along == 'u' else t.T.copy()
def blocks(face, joint, bw=8, bh=4, seed=4, chips=()):
    """Concrete block, painted: a joint line every bh texels and a staggered upright every bw."""
    r = np.random.default_rng(seed); H_, W_ = bh * 8, bw * 8; a = np.full((H_, W_), face, np.uint8)
    for j in range(8):
        a[j * bh] = joint
        for i in range(8): a[j * bh:(j + 1) * bh, (i * bw + (j % 2) * bw // 2) % W_] = joint
    for c in chips:
        for _ in range(40): a[int(r.integers(H_)), int(r.integers(W_))] = c
    return a

def glow(img, strength=.55, r0=6, r1=24):
    """Only register F glows: find it, blur it, add it back."""
    F = table()[0xF]; d = np.abs(img - F).sum(-1); m = np.clip(1 - d / .12, 0, 1).astype(np.float32)
    if m.max() <= 0: return img
    k = cv2.GaussianBlur(m, (0, 0), r0) * .9 + cv2.GaussianBlur(m, (0, 0), r1) * 1.6
    return np.clip(img + k[..., None] * F * strength, 0, 1)

def save(path, img):
    Path(path).parent.mkdir(parents=True, exist_ok=True); cv2.imwrite(str(path), (np.clip(img, 0, 1)[..., ::-1] * 255 + .5).astype(np.uint8)); return str(path)
