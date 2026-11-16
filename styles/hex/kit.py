"""Hex: the kit. A picture is a grid of hex digits. Sixteen colours, numbered 0 to F, and nothing in between.

    c = Canvas()                      320 x 180, every pixel one palette index
    c.rect / poly / line / disc       hard-edged, no anti-aliasing: a pixel is one colour or another
    c.grad(y0, y1, [0, 1, 2, 3])      a gradation the only way sixteen colours allow: ordered dither between neighbours
    c.sprite(rows, x, y, swap={})     a sprite is text: one hex digit per pixel, '.' for nothing
    c.text(x, y, 'ABORT, RETRY, HEX?', 0xA)      the 8 x 8 ROM font (font8x8.hex, public domain)
    c.window(x, y, w, h, 'GATE.EXE', lines, buttons)      a system dialog, because the system has something to say
    c.save(path)                      scaled up four times with hard pixels: 1280 x 720

Register F is reserved. It is the colour of a tended light (a lit window, a kept watch) and nothing else may use it.
"""
from pathlib import Path
import numpy as np
import cv2

W, H, SCALE = 320, 180, 4
PAL = ['#0a0a12', '#1a1c3a', '#2e2a5e', '#4b3f8f',      # 0 void   1 midnight  2 violet     3 twilight
       '#18404a', '#2a7f6f', '#6fd08c', '#c8f08f',      # 4 engine 5 hex green 6 her green  7 phosphor
       '#5a5f72', '#9aa3b8', '#e8ecf4', '#3a78d8',      # 8 steel  9 chrome    A white      B title-bar blue
       '#59d8f0', '#e0407a', '#f08a30', '#ffd870']      # C aqua   D hostile   E torch      F the lit window (reserved)
RGB = np.array([[int(h[i:i + 2], 16) for i in (1, 3, 5)] for h in PAL], np.uint8)
BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]], np.float32) / 16 + 1 / 32
_FONT = bytes.fromhex((Path(__file__).resolve().parents[2] / 'font8x8.hex').read_text().strip())

def glyph(ch):
    k = (ord(ch) - 32) * 8
    rows = _FONT[k:k + 8] if 0 <= k < len(_FONT) - 7 else bytes(8)
    return np.array([[(r >> (7 - b)) & 1 for b in range(8)] for r in rows], bool)

def bayer(h, w, y0=0, x0=0):
    yy, xx = np.mgrid[y0:y0 + h, x0:x0 + w]; return BAYER[yy % 4, xx % 4]

class Canvas:
    def __init__(s, w=W, h=H, fill=0): s.a = np.full((h, w), fill, np.uint8); s.w, s.h = w, h
    def copy(s): c = Canvas(s.w, s.h); c.a = s.a.copy(); return c
    def rect(s, x0, y0, x1, y1, c): s.a[max(int(y0), 0):max(int(y1), 0), max(int(x0), 0):max(int(x1), 0)] = c; return s
    def poly(s, pts, c): cv2.fillPoly(s.a, [np.round(np.asarray(pts)).astype(np.int32)], int(c), lineType=cv2.LINE_8); return s
    def line(s, a, b, c, t=1): cv2.line(s.a, (int(round(a[0])), int(round(a[1]))), (int(round(b[0])), int(round(b[1]))), int(c), t, cv2.LINE_8); return s
    def disc(s, cx, cy, r, c): cv2.circle(s.a, (int(round(cx)), int(round(cy))), int(r), int(c), -1, cv2.LINE_8); return s
    def ring(s, cx, cy, r, c, t=1): cv2.circle(s.a, (int(round(cx)), int(round(cy))), int(r), int(c), t, cv2.LINE_8); return s
    def px(s, x, y, c):
        if 0 <= x < s.w and 0 <= y < s.h: s.a[int(y), int(x)] = c
        return s
    def mask(s, m, c): s.a[m] = c; return s
    def mix(s, m, c0, c1, t):
        """Inside mask m, a dither of c0 and c1: t = 0 is all c0, 1 is all c1 (t may be an array)."""
        d = bayer(s.h, s.w) < t; s.a[m & d] = c1; s.a[m & ~d] = c0; return s
    def grad(s, y0, y1, cols, x0=0, x1=None, power=1.0):
        """A vertical gradation through a list of palette indices, dithered between neighbours."""
        x1 = s.w if x1 is None else x1; n = len(cols) - 1
        for y in range(max(int(y0), 0), min(int(y1), s.h)):
            u = ((y - y0) / max(y1 - y0 - 1, 1)) ** power * n; k = min(int(u), n - 1); t = u - k
            row = bayer(1, x1 - x0, y, x0)[0] < t
            s.a[y, x0:x1] = np.where(row, cols[k + 1], cols[k])
        return s
    def sprite(s, rows, x, y, flip=False, swap=None):
        """rows: strings of hex digits, '.' transparent. swap: {from: to} palette swap, the oldest trick there is."""
        wd = max(len(r) for r in rows)
        for j, r in enumerate(rows):
            r = r.ljust(wd, '.'); r = r[::-1] if flip else r
            for i, ch in enumerate(r):
                if ch == '.': continue
                c = int(ch, 16); c = swap.get(c, c) if swap else c
                s.px(int(x) + i, int(y) + j, c)
        return s
    def text(s, x, y, string, c, shadow=None, gap=0):
        for k, ch in enumerate(string):
            g = glyph(ch); ys, xs = np.nonzero(g)
            for yy, xx in zip(ys, xs):
                if shadow is not None: s.px(x + k * (8 + gap) + xx + 1, y + yy + 1, shadow)
            for yy, xx in zip(ys, xs): s.px(x + k * (8 + gap) + xx, y + yy, c)
        return s
    def bevel(s, x0, y0, x1, y1, face=9, hi=0xA, lo=8):
        s.rect(x0, y0, x1, y1, face); s.rect(x0, y0, x1, y0 + 1, hi); s.rect(x0, y0, x0 + 1, y1, hi); s.rect(x0, y1 - 1, x1, y1, lo); s.rect(x1 - 1, y0, x1, y1, lo); return s
    def window(s, x, y, w, h, title, lines=(), buttons=(), bar=0xB):
        """A dialog box of the period: bevelled chrome, a title bar, a close box, and buttons that mean it."""
        s.rect(x + 2, y + 2, x + w + 2, y + h + 2, 0); s.bevel(x, y, x + w, y + h)
        s.rect(x + 2, y + 2, x + w - 2, y + 12, bar); s.text(x + 4, y + 3, title, 0xA)
        s.bevel(x + w - 12, y + 3, x + w - 3, y + 11); s.text(x + w - 11, y + 3, 'x', 0)
        for k, ln in enumerate(lines): s.text(x + 6, y + 17 + k * 10, ln, 0)
        bx = x + 6
        for b in buttons:
            bw = len(b) * 8 + 8; s.bevel(bx, y + h - 16, bx + bw, y + h - 4); s.text(bx + 4, y + h - 14, b, 0); bx += bw + 4
        return s
    def rgb(s, scale=SCALE): return np.repeat(np.repeat(RGB[s.a], scale, 0), scale, 1)
    def save(s, path, scale=SCALE):
        Path(path).parent.mkdir(parents=True, exist_ok=True); cv2.imwrite(str(path), s.rgb(scale)[..., ::-1]); return str(path)

def hexmap(size, w=W, h=H, ox=0.0, oy=0.0):
    """Which hexagon every pixel belongs to: (q, r) axial coordinates of pointy-topped hexagons `size` pixels from
    centre to corner, and a mask of the pixels that lie on a boundary between two of them."""
    y, x = np.mgrid[:h, :w].astype(np.float64); x = x - ox; y = y - oy
    q = (np.sqrt(3) / 3 * x - y / 3) / size; r = (2 / 3 * y) / size
    xx, zz = q, r; yy = -xx - zz; rx, ry, rz = np.round(xx), np.round(yy), np.round(zz)
    dx, dy, dz = np.abs(rx - xx), np.abs(ry - yy), np.abs(rz - zz)
    fx = (dx > dy) & (dx > dz); fy = ~fx & (dy > dz); rx = np.where(fx, -ry - rz, rx); rz = np.where(~fx & ~fy, -rx - ry, rz)
    Q, R = rx.astype(int), rz.astype(int); edge = np.zeros((h, w), bool)
    edge[:, 1:] |= (Q[:, 1:] != Q[:, :-1]) | (R[:, 1:] != R[:, :-1]); edge[1:, :] |= (Q[1:, :] != Q[:-1, :]) | (R[1:, :] != R[:-1, :])
    return Q, R, edge

def stars(c, y1, seed=3, step=9, cols=(8, 9, 9, 0xA, 0xC), skip=None):
    """A sky that is full: one star in every cell of a lattice, pushed off its mark, so it is dense and never ruled."""
    r = np.random.default_rng(seed)
    for gy in range(0, y1, step):
        for gx in range(0, c.w, step):
            x, y = gx + int(r.integers(0, step)), gy + int(r.integers(0, step))
            if y < y1 and (skip is None or not skip[min(y, c.h - 1), min(x, c.w - 1)]): c.px(x, y, cols[int(r.integers(0, len(cols)))])
    return c

def movie(frames, out, fps=12, scale=SCALE, crf=14):
    """Canvases -> an mp4 with hard pixels."""
    import subprocess, tempfile
    d = Path(tempfile.mkdtemp(prefix='hex_'))
    for i, f in enumerate(frames): cv2.imwrite(str(d / f'f_{i:04d}.png'), f.rgb(scale)[..., ::-1])
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(fps), '-i', str(d / 'f_%04d.png'), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', str(crf), '-movflags', '+faststart', str(out)], check=True)
    return str(out)
