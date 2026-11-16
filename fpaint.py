#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "pillow"]
# ///
"""
FPAINT.EXE -- FablePaint 2.0
A make-believe DOS-era paint program with no mouse and no monitor: every tool
action is one line of a script, and the "screen" is a PNG you look at between
batches. It keeps the constraints of the hardware it pretends to run on:

  vga    320x200, 256 colours out of 262,144 (6-bit DAC), mode 13h
  ega    320x200, 16 hard-wired colours, mode 0Dh
  cga    320x200, 4 colours, mode 04h
  vga16  640x480, 16 colours out of 262,144, mode 12h
  mac    512x342, black and white, square pixels (compact Macintosh)

Indexed colour only. No anti-aliasing, no alpha, no layers. Tall pixels (5:6)
in the 320x200 modes, so the picture is shown stretched to 4:3 like a CRT did.

SHELL
  fpaint.py new <session> --mode vga        start a picture
  fpaint.py do <session> <script|->         run a batch of tool actions
  fpaint.py undo <session> [n]              take back the last n batches
  fpaint.py view <session> [--zoom x0 y0 x1 y1] [--grid] [-o png]
  fpaint.py export <session> -o png [--ui]  final picture (--ui: with toolbox)
  fpaint.py replay <session> -o gif [--ui]  time-lapse of every stroke
  fpaint.py cycle <session> -o gif          colour-cycling animation
  fpaint.py info <session>                  names, ranges, colours in use
  fpaint.py palette <session> -o png        swatch sheet

SCRIPT COMMANDS   (';' starts a comment; colours are indices, names, or range.k)
 palette  pal i r g b [name] | pal i #rrggbb [name]     (DAC values 0..63)
          ramp i j [range-name]      spread colours between two entries
          range name c c a..b ...    name a list of colours
          name n i                   name one colour
          cycle range ticks          colour-cycle a range (0 = stop)
          cgapal 0|1|2 lo|hi [bg]    pick the CGA palette
 state    color fg [bg]
          brush pixel | round n | square n | hline n | vline n | slash n | bslash n
          ink solid
          ink dither 0..16 [opaque]          ordered-dither mix of fg (and bg)
          ink pattern name [opaque]          8x8 fill pattern
          ink gradient range x0 y0 x1 y1 [radial] [bayer|bayer8|noise|none]
          shade range up|down [n] | shade off    nudge pixels along a range
          stencil protect c.. | stencil only c.. | stencil off
          seed n | title "NAME.LBM" | defpattern name ... end
 tools    dot x y [x y ..]           draw x y x y ..        (freehand polyline)
          spline x y x y x y ..      line x0 y0 x1 y1
          curve x0 y0 xm ym x1 y1    bezier x0 y0 c1 c1 c2 c2 x1 y1
          rect / frect x0 y0 x1 y1   poly / fpoly x y x y ..
          ellipse / fellipse cx cy rx ry
          circle / fcircle cx cy r   (aspect-corrected: round on the CRT)
          fill x y                   spray x y r n     sprayrect x0 y0 x1 y1 n
          text x y "string" [scale|tiny]
          pickup x0 y0 x1 y1 [transparent]    stamp x y [flipx] [flipy]
          fatbits x y a=colour b=colour ..    (rows of characters, '.' = skip)
          ...rows...
          end
          clear [colour]
"""
import sys, os, math, random, shlex, pickle, argparse, shutil, glob, json
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
SESSIONS = os.path.join(HERE, 'sessions')


class PaintError(Exception):
    pass


# ------------------------------------------------------------------ hardware
EGA16 = [(0, 0, 0), (0, 0, 42), (0, 42, 0), (0, 42, 42), (42, 0, 0), (42, 0, 42), (42, 21, 0), (42, 42, 42),
         (21, 21, 21), (21, 21, 63), (21, 63, 21), (21, 63, 63), (63, 21, 21), (63, 21, 63), (63, 63, 21), (63, 63, 63)]
EGA_NAMES = ['black', 'blue', 'green', 'cyan', 'red', 'magenta', 'brown', 'lgray',
             'dgray', 'lblue', 'lgreen', 'lcyan', 'lred', 'lmagenta', 'yellow', 'white']
CGA_PALETTES = {('0', 'lo'): (2, 4, 6), ('0', 'hi'): (10, 12, 14),
                ('1', 'lo'): (3, 5, 7), ('1', 'hi'): (11, 13, 15),
                ('2', 'lo'): (3, 4, 7), ('2', 'hi'): (11, 12, 15)}
MODES = {
    'vga':   dict(w=320, h=200, colors=256, sx=5, sy=6, dac=True,  desc='VGA mode 13h, 320x200, 256 colours'),
    'ega':   dict(w=320, h=200, colors=16,  sx=5, sy=6, dac=False, desc='EGA mode 0Dh, 320x200, 16 fixed colours'),
    'cga':   dict(w=320, h=200, colors=4,   sx=5, sy=6, dac=False, desc='CGA mode 04h, 320x200, 4 colours'),
    'vga16': dict(w=640, h=480, colors=16,  sx=2, sy=2, dac=True,  desc='VGA mode 12h, 640x480, 16 colours'),
    'mac':   dict(w=512, h=342, colors=2,   sx=3, sy=3, dac=False, desc='Macintosh 512x342, 1-bit (0 = white paper, 1 = black)'),
}


def vga_default_palette():
    """The power-on mode 13h palette: 16 EGA colours, 16 greys, three hue wheels."""
    pal = list(EGA16) + [(v, v, v) for v in (0, 5, 8, 11, 14, 17, 20, 24, 28, 32, 36, 40, 45, 50, 56, 63)]
    for hi, lows in ((63, (0, 31, 45)), (28, (0, 14, 20)), (16, (0, 8, 11))):
        for lo in lows:
            q = [int(lo + (hi - lo) * k / 4) for k in range(5)]
            up, dn = q[1:4], q[3:0:-1]
            pal += [(lo, lo, hi)] + [(v, lo, hi) for v in up] + [(hi, lo, hi)] + [(hi, lo, v) for v in dn]
            pal += [(hi, lo, lo)] + [(hi, v, lo) for v in up] + [(hi, hi, lo)] + [(v, hi, lo) for v in dn]
            pal += [(lo, hi, lo)] + [(lo, hi, v) for v in up] + [(lo, hi, hi)] + [(lo, v, hi) for v in dn]
    return pal + [(0, 0, 0)] * 8


BAYER4 = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]])
_b = np.array([[0, 2], [3, 1]])
for _ in range(2):
    _b = np.block([[4 * _b, 4 * _b + 2], [4 * _b + 3, 4 * _b + 1]])
BAYER8 = _b


def _bits(rows):
    return np.array([[bool(b & (0x80 >> i)) for i in range(8)] for b in rows])


PATTERNS = {k: _bits(v) for k, v in {
    'hlines': [0xFF, 0x00] * 4, 'hlines4': [0xFF, 0, 0, 0] * 2,
    'vlines': [0xAA] * 8, 'vlines4': [0x88] * 8,
    'diag': [0x11, 0x22, 0x44, 0x88] * 2, 'bdiag': [0x88, 0x44, 0x22, 0x11] * 2,
    'grid': [0xFF, 0x88, 0x88, 0x88] * 2, 'cross': [0x88, 0x55, 0x22, 0x55] * 2,
    'brick': [0xFF, 0x80, 0x80, 0x80, 0xFF, 0x08, 0x08, 0x08],
    'dots': [0x88, 0x00, 0x22, 0x00] * 2,
    'weave': [0xF8, 0x74, 0x22, 0x47, 0x8F, 0x17, 0x22, 0x71],
    'scales': [0x80, 0x80, 0x41, 0x3E, 0x08, 0x08, 0x14, 0xE3],
    'shingle': [0x03, 0x84, 0x48, 0x30, 0x0C, 0x02, 0x01, 0x01],
    'waves': [0x00, 0x00, 0x30, 0x48, 0x84, 0x03, 0x00, 0x00],
}.items()}

# ---------------------------------------------------------------------- fonts
with open(os.path.join(HERE, 'font8x8.hex')) as _f:
    _FONT = bytes.fromhex(_f.read().strip())          # the ROM 8x8 font, chars 32..127

_TINY = {  # a 3x5 font for labels too small for the ROM font
    'A': '.#.#.#####.##.#', 'B': '##.#.###.#.###.', 'C': '.###..#..#...##', 'D': '##.#.##.##.###.',
    'E': '####..##.#..###', 'F': '####..##.#..#..', 'G': '.###..#.##.#.##', 'H': '#.##.#####.##.#',
    'I': '###.#..#..#.###', 'J': '..#..#..##.#.#.', 'K': '#.##.###.#.##.#', 'L': '#..#..#..#..###',
    'M': '#.#######.##.##', 'N': '####.##.##.##.#', 'O': '.#.#.##.##.#.#.', 'P': '##.#.###.#..#..',
    'Q': '.#.#.##.####.##', 'R': '##.#.###.#.##.#', 'S': '.###...#...###.', 'T': '###.#..#..#..#.',
    'U': '#.##.##.##.####', 'V': '#.##.##.##.#.#.', 'W': '#.##.#######.##', 'X': '#.##.#.#.#.##.#',
    'Y': '#.##.#.#..#..#.', 'Z': '###..#.#.#..###', '0': '####.##.##.####', '1': '.#.##..#..#.###',
    '2': '##...#.#.#..###', '3': '##...#.#...###.', '4': '#.##.####..#..#', '5': '####..##...###.',
    '6': '.###..####.####', '7': '###..#.#..#..#.', '8': '####.#####.####', '9': '####.####..###.',
    ' ': '...............', '.': '.............#.', ',': '..........#.#..', ':': '....#.....#....',
    '-': '......###......', '+': '....#.###.#....', '!': '.#..#..#.....#.', '?': '##...#.#.....#.',
    '/': '..#..#.#.#..#..', '*': '...#.#.#.#.#...', "'": '.#..#..........', '=': '...###...###...',
    '>': '#...#...#.#.#..', '<': '..#.#.#...#...#', '_': '............###', '#': '#.####.#.####.#',
}


def text_mask(s, scale=1):
    m = np.zeros((8, 8 * max(1, len(s))), bool)
    for i, ch in enumerate(s):
        k = ord(ch) - 32
        if not 0 <= k < 96:
            k = ord('?') - 32
        for r in range(8):
            row = _FONT[k * 8 + r]
            for b in range(8):
                if row & (0x80 >> b):
                    m[r, i * 8 + b] = True
    return m.repeat(scale, 0).repeat(scale, 1) if scale > 1 else m


def tiny_mask(s):
    m = np.zeros((5, 4 * max(1, len(s))), bool)
    for i, ch in enumerate(s.upper()):
        g = _TINY.get(ch, _TINY['?'])
        for k, c in enumerate(g):
            if c == '#':
                m[k // 3, i * 4 + k % 3] = True
    return m[:, :-1]


# ------------------------------------------------------------------- geometry
def bres(x0, y0, x1, y1):
    pts = []
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
    err = dx + dy
    while True:
        pts.append((x0, y0))
        if x0 == x1 and y0 == y1:
            return pts
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def path_pts(fpts, closed=False):
    """Join points with Bresenham runs into one ordered pixel path."""
    ip = [(int(round(x)), int(round(y))) for x, y in fpts]
    if closed:
        ip.append(ip[0])
    out = [ip[0]]
    for (x0, y0), (x1, y1) in zip(ip, ip[1:]):
        if (x0, y0) != (x1, y1):
            out.extend(bres(x0, y0, x1, y1)[1:])
    return out


def catmull(pts):
    P = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        n = max(4, int(math.hypot(p2[0] - p1[0], p2[1] - p1[1])))
        for k in range(n):
            t = k / n
            out.append(tuple(
                0.5 * (2 * b + (c - a) * t + (2 * a - 5 * b + 4 * c - d) * t * t + (3 * b - a - 3 * c + d) * t ** 3)
                for a, b, c, d in zip(p0, p1, p2, p3)))
    out.append(pts[-1])
    return out


def bezier(ctrl):
    n = max(8, int(sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(ctrl, ctrl[1:]))))
    out = []
    for k in range(n + 1):
        t = k / n
        pts = list(ctrl)
        while len(pts) > 1:
            pts = [((1 - t) * a[0] + t * b[0], (1 - t) * a[1] + t * b[1]) for a, b in zip(pts, pts[1:])]
        out.append(pts[0])
    return out


def outline_of(m):
    p = np.pad(m, 1, mode='edge')
    return m & ~(p[:-2, 1:-1] & p[2:, 1:-1] & p[1:-1, :-2] & p[1:-1, 2:])


TOOL_OF = {'dot': 'dots', 'draw': 'draw', 'spline': 'draw', 'line': 'line', 'curve': 'curve', 'bezier': 'curve',
           'fill': 'fill', 'spray': 'spray', 'sprayrect': 'spray', 'rect': 'rect', 'frect': 'rect',
           'circle': 'circle', 'fcircle': 'circle', 'ellipse': 'ellipse', 'fellipse': 'ellipse',
           'poly': 'poly', 'fpoly': 'poly', 'pickup': 'brush', 'stamp': 'brush', 'text': 'text',
           'fatbits': 'magnify'}


# --------------------------------------------------------------------- canvas
class Canvas:
    CHUNK = 32          # a stroke lands on screen this many pixels of travel at a time

    def __init__(self, mode='vga', seed=1987):
        if mode not in MODES:
            raise PaintError(f'no such video mode {mode!r}')
        m = MODES[mode]
        self.mode, self.w, self.h, self.ncol = mode, m['w'], m['h'], m['colors']
        self.sx, self.sy = m['sx'], m['sy']
        self.asp = m['sy'] / m['sx']
        self.pix = np.zeros((self.h, self.w), np.uint8)
        if mode == 'vga':
            self.pal = [list(c) for c in vga_default_palette()]
        elif mode == 'cga':
            self.pal = [list(EGA16[i]) for i in (0, 11, 13, 15)]
        elif mode == 'mac':
            self.pal = [[63, 63, 63], [0, 0, 0]]
        else:
            self.pal = [list(c) for c in EGA16]
        self.names = ({'black': 0, 'cyan': 1, 'magenta': 2, 'white': 3} if mode == 'cga'
                      else {'white': 0, 'black': 1} if mode == 'mac'
                      else {n: i for i, n in enumerate(EGA_NAMES)})
        self.ranges, self.cycles, self.userpats = {}, {}, {}
        self.fg, self.bg = {'cga': 3, 'mac': 1}.get(mode, 15), 0
        self.ink = ('solid',)
        self.brush, self.brush_desc = np.ones((1, 1), bool), 'pixel'
        self.custom = None
        self.shade = None
        self.stencil = None
        self.rng = random.Random(seed)
        self.title = 'UNTITLED'
        self.tool, self.cursor = 'draw', (self.w // 2, self.h // 2)
        self.hook = None

    def __getstate__(self):
        d = dict(self.__dict__)
        d['hook'] = None
        return d

    def tick(self):
        if self.hook:
            self.hook(self)

    # ---- colours
    def col(self, tok):
        t = str(tok)
        try:
            if t.lstrip('-').isdigit():
                i = int(t)
            elif t in self.names:
                i = self.names[t]
            elif '.' in t:
                r, k = t.rsplit('.', 1)
                i = self.ranges[r][int(k)]
            else:
                raise KeyError(t)
        except (KeyError, IndexError, ValueError):
            raise PaintError(f'unknown colour {t!r}')
        if not 0 <= i < self.ncol:
            raise PaintError(f'colour {i} does not exist in {self.mode} mode ({self.ncol} colours)')
        return i

    def cols(self, toks):
        out = []
        for t in toks:
            if t in self.ranges:
                out += self.ranges[t]
            elif '..' in t:
                a, b = (self.col(v) for v in t.split('..'))
                out += list(range(a, b + (1 if b >= a else -1), 1 if b >= a else -1))
            else:
                out.append(self.col(t))
        return out

    # ---- laying ink through a mask
    def apply(self, mask):
        if self.stencil is not None:
            mask = mask & ~self.stencil[self.pix]
        ys, xs = np.nonzero(mask)
        if len(ys) == 0:
            return
        kind = self.ink[0]
        if kind == 'solid':
            c = self.fg
        elif kind in ('dither', 'pattern'):
            on = (BAYER4[ys % 4, xs % 4] < self.ink[1]) if kind == 'dither' else self.ink[1][ys % 8, xs % 8]
            if self.ink[2]:
                c = np.where(on, self.fg, self.bg).astype(np.uint8)
            else:
                ys, xs = ys[on], xs[on]
                c = self.fg
        else:   # gradient
            _, rng_, x0, y0, x1, y1, radial, dith = self.ink
            n = len(rng_)
            if radial:
                t = np.hypot(xs - x0, (ys - y0) * self.asp) / (math.hypot(x1 - x0, (y1 - y0) * self.asp) or 1)
            else:
                dx, dy = x1 - x0, y1 - y0
                t = ((xs - x0) * dx + (ys - y0) * dy) / (dx * dx + dy * dy or 1)
            p = np.clip(t, 0, 1) * (n - 1)
            i0 = np.floor(p)
            if dith == 'bayer':
                thr = (BAYER4[ys % 4, xs % 4] + 0.5) / 16
            elif dith == 'bayer8':
                thr = (BAYER8[ys % 8, xs % 8] + 0.5) / 64
            elif dith == 'noise':
                thr = np.random.RandomState(self.rng.getrandbits(32)).random_sample(len(ys))
            else:
                thr = 0.5
            c = np.asarray(rng_, np.uint8)[np.clip(i0 + (p - i0 > thr), 0, n - 1).astype(int)]
        if self.shade is not None:
            pos_lut, arr, step = self.shade
            pos = pos_lut[self.pix[ys, xs]]
            ok = pos >= 0
            self.pix[ys[ok], xs[ok]] = arr[np.clip(pos[ok] + step, 0, len(arr) - 1)]
        else:
            self.pix[ys, xs] = c

    def spread(self, pts):
        """Stamp the brush at every point; return what it covers."""
        b = self.brush
        bh, bw = b.shape
        pad = max(bh, bw)
        P = np.zeros((self.h + 2 * pad, self.w + 2 * pad), bool)
        for x, y in pts:
            if -pad <= x < self.w + pad and -pad <= y < self.h + pad:
                P[y + pad, x + pad] = True
        if b.size > 1:
            out = np.zeros_like(P)
            for by, bx in zip(*np.nonzero(b)):
                out |= np.roll(P, (int(by) - bh // 2, int(bx) - bw // 2), (0, 1))
            P = out
        return P[pad:pad + self.h, pad:pad + self.w]

    def stroke(self, pts):
        touched = np.zeros((self.h, self.w), bool)
        for i in range(0, len(pts), self.CHUNK):
            m = self.spread(pts[i:i + self.CHUNK])
            self.apply(m & ~touched)
            touched |= m
            self.cursor = pts[min(i + self.CHUNK, len(pts)) - 1]
            self.tick()

    # ---- shape masks
    def ellipse_mask(self, cx, cy, rx, ry):
        yy, xx = np.ogrid[:self.h, :self.w]
        return ((xx - cx) / (max(rx, 0) + 0.4)) ** 2 + ((yy - cy) / (max(ry, 0) + 0.4)) ** 2 <= 1.0

    def poly_mask(self, pts):
        im = Image.new('1', (self.w, self.h), 0)
        ImageDraw.Draw(im).polygon([tuple(p) for p in pts], fill=1, outline=1)
        m = np.array(im, bool)
        for x, y in path_pts(pts, closed=True):
            if 0 <= x < self.w and 0 <= y < self.h:
                m[y, x] = True
        return m

    def flood_mask(self, x, y):
        if not (0 <= x < self.w and 0 <= y < self.h):
            raise PaintError(f'fill point {x},{y} is off the page')
        same = self.pix == self.pix[y, x]
        mask = np.zeros_like(same)
        stack = [(x, y)]
        while stack:
            x, y = stack.pop()
            if mask[y, x] or not same[y, x]:
                continue
            xl = xr = x
            while xl > 0 and same[y, xl - 1]:
                xl -= 1
            while xr < self.w - 1 and same[y, xr + 1]:
                xr += 1
            mask[y, xl:xr + 1] = True
            for ny in (y - 1, y + 1):
                if 0 <= ny < self.h:
                    run = np.nonzero(same[ny, xl:xr + 1] & ~mask[ny, xl:xr + 1])[0]
                    if len(run):
                        for s in run[np.insert(np.diff(run) > 1, 0, True)]:
                            stack.append((xl + int(s), ny))
        return mask

    def place(self, small, x, y):
        m = np.zeros((self.h, self.w), bool)
        h, w = small.shape
        x0, y0, x1, y1 = max(x, 0), max(y, 0), min(x + w, self.w), min(y + h, self.h)
        if x1 > x0 and y1 > y0:
            m[y0:y1, x0:x1] = small[y0 - y:y1 - y, x0 - x:x1 - x]
        return m

    # ---- one tool action
    def command(self, cmd, a, block=None):
        n = lambda t: int(round(float(t)))

        def P(args, need=None, least=1):
            v = [n(t) for t in args]
            if len(v) % 2 or len(v) < 2 * least or (need and len(v) != 2 * need):
                raise PaintError(f'{cmd} wants {need or "at least %d" % least} x y pair(s)')
            return list(zip(v[0::2], v[1::2]))

        drew = True
        if cmd in ('color', 'colour'):
            self.fg = self.col(a[0])
            if len(a) > 1:
                self.bg = self.col(a[1])
            drew = False
        elif cmd == 'ink':
            k = a[0]
            if k == 'solid':
                self.ink = ('solid',)
            elif k == 'dither':
                lvl = n(a[1])
                if not 0 <= lvl <= 16:
                    raise PaintError('dither level is 0..16')
                self.ink = ('dither', lvl, 'opaque' in a[2:])
            elif k == 'pattern':
                pat = self.userpats.get(a[1], PATTERNS.get(a[1]))
                if pat is None:
                    raise PaintError(f'no pattern {a[1]!r}; have {", ".join(sorted({**PATTERNS, **self.userpats}))}')
                self.ink = ('pattern', pat, 'opaque' in a[2:])
            elif k == 'gradient':
                rng_ = self.cols([a[1]])
                opts = a[6:]
                dith = next((o for o in opts if o in ('bayer', 'bayer8', 'noise', 'none')), 'bayer')
                self.ink = ('gradient', rng_, n(a[2]), n(a[3]), n(a[4]), n(a[5]), 'radial' in opts, dith)
            else:
                raise PaintError(f'no ink {k!r}')
            drew = False
        elif cmd == 'brush':
            k, s = a[0], (n(a[1]) if len(a) > 1 else 1)
            if not 1 <= s <= 40:
                raise PaintError('brush size is 1..40')
            if k == 'pixel':
                b = np.ones((1, 1), bool)
            elif k == 'round':
                c = (s - 1) / 2
                yy, xx = np.ogrid[:s, :s]
                b = (xx - c) ** 2 + (yy - c) ** 2 <= max((s / 2) ** 2 - 0.5, 0.3)
            elif k == 'square':
                b = np.ones((s, s), bool)
            elif k == 'hline':
                b = np.ones((1, s), bool)
            elif k == 'vline':
                b = np.ones((s, 1), bool)
            elif k == 'slash':
                b = np.eye(s, dtype=bool)[::-1]
            elif k == 'bslash':
                b = np.eye(s, dtype=bool)
            else:
                raise PaintError(f'no brush {k!r}')
            self.brush, self.brush_desc = b, ' '.join(a)
            drew = False
        elif cmd == 'shade':
            if a[0] == 'off':
                self.shade = None
            else:
                rng_ = self.cols([a[0]])
                step = (n(a[2]) if len(a) > 2 else 1) * {'up': 1, 'down': -1}[a[1]]
                lut = np.full(256, -1, int)
                for k, c in enumerate(rng_):
                    lut[c] = k
                self.shade = (lut, np.asarray(rng_, np.uint8), step)
            drew = False
        elif cmd == 'stencil':
            if a[0] == 'off':
                self.stencil = None
            else:
                lut = np.zeros(256, bool)
                lut[self.cols(a[1:])] = True
                self.stencil = {'protect': lut, 'only': ~lut}[a[0]]
            drew = False
        elif cmd == 'pal':
            if not MODES[self.mode]['dac']:
                raise PaintError(f'the palette is hard-wired in {self.mode} mode')
            i = self.col(a[0])
            if a[1].startswith('#'):
                rgb, rest = [int(a[1][k:k + 2], 16) >> 2 for k in (1, 3, 5)], a[2:]
            else:
                rgb, rest = [n(v) for v in a[1:4]], a[4:]
            if not all(0 <= v <= 63 for v in rgb):
                raise PaintError('DAC values are 0..63')
            self.pal[i] = rgb
            if rest:
                self.names[rest[0]] = i
        elif cmd == 'ramp':
            if not MODES[self.mode]['dac']:
                raise PaintError(f'the palette is hard-wired in {self.mode} mode')
            i, j = self.col(a[0]), self.col(a[1])
            if i == j:
                raise PaintError('ramp needs two different entries')
            step = 1 if j > i else -1
            for k in range(i, j + step, step):
                t = (k - i) / (j - i)
                self.pal[k] = [int(round(self.pal[i][c] + (self.pal[j][c] - self.pal[i][c]) * t)) for c in range(3)]
            if len(a) > 2:
                self.ranges[a[2]] = list(range(i, j + step, step))
        elif cmd == 'range':
            self.ranges[a[0]] = self.cols(a[1:])
            drew = False
        elif cmd == 'name':
            self.names[a[0]] = self.col(a[1])
            drew = False
        elif cmd == 'cycle':
            if a[0] not in self.ranges:
                raise PaintError(f'no range {a[0]!r}')
            if n(a[1]) == 0:
                self.cycles.pop(a[0], None)
            else:
                self.cycles[a[0]] = n(a[1])
            drew = False
        elif cmd == 'cgapal':
            if self.mode != 'cga':
                raise PaintError('cgapal is for cga mode')
            trio = CGA_PALETTES[(a[0], a[1])]
            bg = n(a[2]) if len(a) > 2 else 0
            self.pal = [list(EGA16[i]) for i in (bg,) + trio]
            self.names = {EGA_NAMES[c]: i for i, c in enumerate((bg,) + trio)}
        elif cmd == 'seed':
            self.rng = random.Random(n(a[0]))
            drew = False
        elif cmd == 'title':
            self.title = a[0]
            drew = False
        elif cmd == 'defpattern':
            rows = [r.strip() for r in block if r.strip()]
            if len(rows) != 8 or any(len(r) != 8 for r in rows):
                raise PaintError('a pattern is 8 rows of 8 characters')
            self.userpats[a[0]] = np.array([[c == '#' for c in r] for r in rows])
            drew = False
        elif cmd == 'clear':
            self.pix[:] = self.col(a[0]) if a else self.bg
        elif cmd == 'dot':
            for p in P(a):
                self.stroke([p])
            drew = False
        elif cmd in ('draw', 'line'):
            self.stroke(path_pts(P(a, need=2 if cmd == 'line' else None)))
            drew = False
        elif cmd == 'spline':
            self.stroke(path_pts(catmull(P(a, least=2))))
            drew = False
        elif cmd == 'curve':
            p0, pm, p1 = P(a, need=3)
            c = (2 * pm[0] - (p0[0] + p1[0]) / 2, 2 * pm[1] - (p0[1] + p1[1]) / 2)
            self.stroke(path_pts(bezier([p0, c, p1])))
            drew = False
        elif cmd == 'bezier':
            self.stroke(path_pts(bezier(P(a, need=4))))
            drew = False
        elif cmd in ('rect', 'frect'):
            (x0, y0), (x1, y1) = P(a, need=2)
            x0, x1, y0, y1 = min(x0, x1), max(x0, x1), min(y0, y1), max(y0, y1)
            if cmd == 'rect':
                self.stroke(path_pts([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], closed=True))
                drew = False
            else:
                self.apply(self.place(np.ones((y1 - y0 + 1, x1 - x0 + 1), bool), x0, y0))
                self.cursor = (x1, y1)
        elif cmd in ('poly', 'fpoly'):
            pts = P(a, least=3)
            if cmd == 'poly':
                self.stroke(path_pts(pts, closed=True))
                drew = False
            else:
                self.apply(self.poly_mask(pts))
                self.cursor = pts[-1]
        elif cmd in ('ellipse', 'fellipse', 'circle', 'fcircle'):
            cx, cy, rx = float(a[0]), float(a[1]), float(a[2])
            ry = float(a[3]) if 'ellipse' in cmd else rx / self.asp
            m = self.ellipse_mask(cx, cy, rx, ry)
            if cmd[0] != 'f':
                ys, xs = np.nonzero(outline_of(m))
                m = self.spread(list(zip(xs.tolist(), ys.tolist())))
            self.apply(m)
            self.cursor = (n(cx + rx), n(cy))
        elif cmd == 'fill':
            (x, y), = P(a, need=1)
            self.apply(self.flood_mask(x, y))
            self.cursor = (x, y)
        elif cmd in ('spray', 'sprayrect'):
            pts = []
            if cmd == 'spray':
                x, y, r, cnt = n(a[0]), n(a[1]), float(a[2]), n(a[3])
                for _ in range(cnt):
                    ang, d = self.rng.random() * 2 * math.pi, r * self.rng.random()
                    pts.append((n(x + math.cos(ang) * d), n(y + math.sin(ang) * d / self.asp)))
                self.cursor = (x, y)
            else:
                x0, y0, x1, y1, cnt = (n(v) for v in a[:5])
                for _ in range(cnt):
                    pts.append((self.rng.randint(min(x0, x1), max(x0, x1)), self.rng.randint(min(y0, y1), max(y0, y1))))
                self.cursor = (x1, y1)
            self.apply(self.spread(pts))
        elif cmd == 'text':
            x, y, s = n(a[0]), n(a[1]), a[2]
            opt = a[3] if len(a) > 3 else '1'
            self.apply(self.place(tiny_mask(s) if opt == 'tiny' else text_mask(s, n(opt)), x, y))
            self.cursor = (x, y)
        elif cmd == 'pickup':
            (x0, y0), (x1, y1) = P(a[:4], need=2)
            x0, x1, y0, y1 = max(min(x0, x1), 0), min(max(x0, x1), self.w - 1), max(min(y0, y1), 0), min(max(y0, y1), self.h - 1)
            self.custom = self.pix[y0:y1 + 1, x0:x1 + 1].astype(np.int16)
            if len(a) > 4:
                self.custom[self.custom == self.col(a[4])] = -1
            self.cursor = (x1, y1)
        elif cmd == 'stamp':
            if self.custom is None:
                raise PaintError('pick up a brush first')
            x, y = n(a[0]), n(a[1])
            b = self.custom
            if 'flipx' in a[2:]:
                b = b[:, ::-1]
            if 'flipy' in a[2:]:
                b = b[::-1]
            m = self.place(b >= 0, x, y)
            if self.stencil is not None:
                m &= ~self.stencil[self.pix]
            src = np.zeros((self.h, self.w), np.int16)
            h, w = b.shape
            x0, y0, x1, y1 = max(x, 0), max(y, 0), min(x + w, self.w), min(y + h, self.h)
            if x1 > x0 and y1 > y0:
                src[y0:y1, x0:x1] = b[y0 - y:y1 - y, x0 - x:x1 - x]
            self.pix[m] = src[m]
            self.cursor = (x, y)
        elif cmd == 'fatbits':
            x, y = n(a[0]), n(a[1])
            key = {}
            for kv in a[2:]:
                ch, _, v = kv.partition('=')
                if len(ch) != 1 or not v:
                    raise PaintError(f'fatbits key {kv!r} should look like a=colour')
                key[ch] = None if v == '-' else self.col(v)
            for r, row in enumerate(block):
                for c, ch in enumerate(row.strip()):
                    if ch == '.' and '.' not in key:
                        continue
                    if ch not in key:
                        raise PaintError(f'fatbits row {r + 1}: no colour for {ch!r}')
                    px, py = x + c, y + r
                    if key[ch] is not None and 0 <= px < self.w and 0 <= py < self.h:
                        self.pix[py, px] = key[ch]
            self.cursor = (x, y)
        else:
            raise PaintError(f'unknown command {cmd!r}')
        if cmd in TOOL_OF:
            self.tool = TOOL_OF[cmd]
        if drew:
            self.tick()


def run_script(cv, text, name='script'):
    lines = text.splitlines()
    i = count = 0
    while i < len(lines):
        lineno, raw = i + 1, lines[i]
        i += 1
        lx = shlex.shlex(raw, posix=True)
        lx.whitespace_split, lx.commenters = True, ';'
        try:
            toks = list(lx)
        except ValueError as e:
            raise PaintError(f'{name}:{lineno}: {e}')
        if not toks:
            continue
        cmd, block = toks[0].lower(), None
        if cmd in ('fatbits', 'defpattern'):
            block = []
            while i < len(lines) and lines[i].strip().lower() != 'end':
                block.append(lines[i])
                i += 1
            if i >= len(lines):
                raise PaintError(f'{name}:{lineno}: {cmd} has no end')
            i += 1
        try:
            cv.command(cmd, toks[1:], block)
        except PaintError as e:
            raise PaintError(f'{name}:{lineno}: {e}')
        except (ValueError, IndexError, KeyError) as e:
            raise PaintError(f'{name}:{lineno}: bad arguments for {cmd} ({e})')
        count += 1
    return count


# ------------------------------------------------------------------ rendering
def rgb_palette(pal):
    return np.array([[(v << 2) | (v >> 4) for v in c] for c in pal], np.uint8)


def render_view(cv, zoom=None, grid=False, rulers=True):
    x0, y0, x1, y1 = zoom if zoom else (0, 0, cv.w - 1, cv.h - 1)
    x0, x1 = sorted(max(0, min(cv.w - 1, v)) for v in (x0, x1))
    y0, y1 = sorted(max(0, min(cv.h - 1, v)) for v in (y0, y1))
    w, h = x1 - x0 + 1, y1 - y0 + 1
    k = max(1, min(1500 // (w * cv.sx), 1140 // (h * cv.sy)))
    sx, sy = cv.sx * k, cv.sy * k
    big = rgb_palette(cv.pal)[cv.pix[y0:y1 + 1, x0:x1 + 1]].repeat(sy, 0).repeat(sx, 1)
    fine = sx >= 15
    if grid or fine:
        g = big.astype(np.int16)
        step, major = (1, 10) if fine else (10, 50)
        for c in range(x0 + 1, x1 + 1):
            if c % step == 0:
                X = (c - x0) * sx
                g[:, X] = (g[:, X] + 255) // 2 if c % major == 0 else (g[:, X] * 3 + 140) // 4
        for c in range(y0 + 1, y1 + 1):
            if c % step == 0:
                Y = (c - y0) * sy
                g[Y, :] = (g[Y, :] + 255) // 2 if c % major == 0 else (g[Y, :] * 3 + 140) // 4
        big = g.astype(np.uint8)
    if not rulers:
        return big
    L, T = 54, 24
    out = np.full((big.shape[0] + T, big.shape[1] + L, 3), 28, np.uint8)
    out[T:, L:] = big
    tick, lab = (1, 5) if fine else ((5, 10) if k >= 2 else (10, 20))

    def put(mask, X, Y):
        hh, ww = mask.shape
        X, Y = max(0, min(out.shape[1] - ww, X)), max(0, min(out.shape[0] - hh, Y))
        out[Y:Y + hh, X:X + ww][mask] = (235, 235, 235)

    for c in range(x0, x1 + 1):
        if c % tick == 0:
            X = L + (c - x0) * sx + sx // 2
            out[T - (8 if c % lab == 0 else 4):T, X] = (200, 200, 200)
            if c % lab == 0:
                m = text_mask(str(c), 2)
                put(m, X - m.shape[1] // 2, 0)
    for c in range(y0, y1 + 1):
        if c % tick == 0:
            Y = T + (c - y0) * sy + sy // 2
            out[Y, L - (8 if c % lab == 0 else 4):L] = (200, 200, 200)
            if c % lab == 0:
                m = text_mask(str(c), 2)
                put(m, L - 9 - m.shape[1], Y - 8)
    return out


_ICONS = {name: np.array([[c == '#' for c in row] for row in rows.split()]) for name, rows in {
    'dots':     '.......... ......#.#. ....#..... ..#....... .#........ ..#....... ....#.#... ........#. ..........',
    'draw':     '.......... .....###.. ....#...#. ...#...... ..#....... ..#...##.. ...###..#. ........#. ..........',
    'line':     '.......... ........#. .......#.. ......#... .....#.... ....#..... ...#...... ..#....... .#........',
    'curve':    '.......... .#........ .#........ .#........ ..#....... ...#...... ....##.... ......###. ..........',
    'fill':     '....#..... ...#.#.... ..#...#... .#.....#.. .##...###. .#.#.#.##. ..#.#..##. ...#....#. ..........',
    'spray':    '#.#....... .#..##.... #.#.##.... ...####... ...####... ...####... ...####... ...####... ..........',
    'rect':     '.......... .########. .#.....##. .#....###. .#...####. .#..#####. .#.######. .########. ..........',
    'circle':   '.......... ...####... ..#...##.. .#...####. .#..#####. .#.######. ..######.. ...####... ..........',
    'ellipse':  '.......... .......... ..######.. .#....###. .#..#####. .#.######. ..######.. .......... ..........',
    'poly':     '.......... ....#..... ...#.#.... ..#...##.. .#....###. .#...###.. ..#.###... ...##..... ..........',
    'brush':    '.......... .##.##.##. .#......#. .......... .#......#. .#......#. .......... .#......#. .##.##.##.',
    'text':     '.......... ....##.... ...####... ..##..##.. ..##..##.. ..######.. ..##..##.. ..##..##.. ..........',
    'grid':     '.......... ..#..#..#. .########. ..#..#..#. ..#..#..#. .########. ..#..#..#. ..#..#..#. .########.',
    'symmetry': '.......... .#..#..#.. ..#.#.#... ...###.... .#######.. ...###.... ..#.#.#... .#..#..#.. ..........',
    'magnify':  '.......... ..###..... .#...#.... .#...#.... .#...#.... ..###..... .....##... ......##.. .......##.',
    'zoom':     '.......... .#######.. .....##... ....##.... ...##..... ..##...... .#######.. .......... ..........',
}.items()}
_ICON_ORDER = ['dots', 'draw', 'line', 'curve', 'fill', 'spray', 'rect', 'circle',
               'ellipse', 'poly', 'brush', 'text', 'grid', 'symmetry', 'magnify', 'zoom']


def render_chrome(cv):
    """The picture as it would sit on screen with the title bar and toolbox up."""
    if (cv.w, cv.h) != (320, 200):
        raise PaintError('the toolbox is only drawn for the 320x200 modes')
    pal = rgb_palette(cv.pal)
    img = pal[cv.pix].copy()
    if cv.mode == 'cga':
        face, dark, ink, lite = (tuple(int(v) for v in pal[i]) for i in (3, 1, 0, 3))
    else:
        face, dark, ink, lite = (170, 170, 170), (85, 85, 85), (0, 0, 0), (255, 255, 255)

    def box(x0, y0, x1, y1, c):
        img[y0:y1 + 1, x0:x1 + 1] = c

    def blit(mask, x, y, c):
        sub = img[y:y + mask.shape[0], x:x + mask.shape[1]]
        sub[mask[:sub.shape[0], :sub.shape[1]]] = c

    cx, cy = cv.cursor
    cx, cy = max(0, min(319, cx)), max(0, min(199, cy))
    if cx < 294 and cy > 11:            # crosshair where the "mouse" last was
        for d in (-5, -4, -3, 3, 4, 5):
            for X, Y in ((cx + d, cy), (cx, cy + d)):
                if 0 <= X < 295 and 11 <= Y < 200:
                    img[Y, X] = 255 - img[Y, X]
    box(0, 0, 319, 9, lite)
    box(0, 10, 319, 10, ink)
    blit(text_mask('FablePaint 2.0  ' + cv.title[:12]), 3, 1, ink)
    blit(text_mask(f'{cx:3d} {cy:3d}'), 320 - 7 * 8 - 3, 1, ink)
    TX = 295
    box(TX, 11, 319, 199, face)
    box(TX, 11, TX, 199, ink)
    for i, s in enumerate((1, 2, 3, 5)):          # built-in brushes
        c = (s - 1) / 2
        yy, xx = np.ogrid[:s, :s]
        blit((xx - c) ** 2 + (yy - c) ** 2 <= max((s / 2) ** 2 - 0.5, 0.3), TX + 3 + i * 6 - s // 2, 16 - s // 2, ink)
    box(TX + 1, 22, 319, 22, dark)
    for i, name in enumerate(_ICON_ORDER):
        X, Y = TX + 1 + (i % 2) * 12, 23 + (i // 2) * 11
        sel = name == cv.tool
        if sel:
            box(X, Y, X + 11, Y + 10, ink)
        blit(_ICONS[name], X + 1, Y + 1, lite if sel else ink)
    Y = 23 + 8 * 11
    box(TX + 1, Y, 319, Y, dark)
    blit(tiny_mask('UNDO'), TX + 5, Y + 3, ink)
    box(TX + 1, Y + 10, 319, Y + 10, dark)
    blit(tiny_mask('CLR'), TX + 7, Y + 13, ink)
    box(TX + 1, Y + 20, 319, Y + 20, dark)
    Y += 23
    box(TX + 3, Y, 317, Y + 13, ink)               # background / foreground indicator
    box(TX + 4, Y + 1, 316, Y + 12, pal[cv.bg])
    box(TX + 8, Y + 4, 312, Y + 9, ink)
    box(TX + 9, Y + 5, 311, Y + 8, pal[cv.fg])
    Y += 16
    used = np.bincount(cv.pix.ravel(), minlength=256)
    if cv.ncol <= 16:
        cols_, cw, ch_ = list(range(cv.ncol)), 12, 5
    else:
        cols_, cw, ch_ = sorted(np.argsort(-used)[:40].tolist()), 6, 5
    for i, c in enumerate(cols_):
        X, Yc = TX + 1 + (i % (24 // cw)) * cw, Y + (i // (24 // cw)) * ch_
        if Yc + ch_ - 1 <= 199:
            box(X, Yc, X + cw - 1, Yc + ch_ - 1, pal[c])
    return img


def upscale(a, sx, sy):
    return a.repeat(sy, 0).repeat(sx, 1)


def save_gif(frames, path, durations, sx, sy):
    """frames: native-size RGB arrays. One shared palette when the colours fit."""
    packed = [(f[..., 0].astype(np.uint32) << 16) | (f[..., 1].astype(np.uint32) << 8) | f[..., 2] for f in frames]
    uniq = np.unique(np.concatenate([np.unique(p) for p in packed]))
    if len(uniq) <= 256:
        flat = []
        for v in uniq.tolist():
            flat += [(v >> 16) & 255, (v >> 8) & 255, v & 255]
        flat += [0] * (768 - len(flat))
        ims = []
        for p in packed:
            im = Image.fromarray(upscale(np.searchsorted(uniq, p).astype(np.uint8), sx, sy), 'P')
            im.putpalette(flat)
            ims.append(im)
    else:
        ims = [Image.fromarray(upscale(f, sx, sy), 'RGB') for f in frames]
    ims[0].save(path, save_all=True, append_images=ims[1:], duration=durations, loop=0, optimize=False)


# ------------------------------------------------------------------- sessions
def sdir(name, *more):
    return os.path.join(SESSIONS, name, *more)


def load(name):
    if not os.path.exists(sdir(name, 'state.pkl')):
        sys.exit(f'no session {name!r} (fpaint.py new {name} --mode vga)')
    with open(sdir(name, 'state.pkl'), 'rb') as f:
        return pickle.load(f)


def save(name, cv, n):
    for p in (sdir(name, 'state.pkl'), sdir(name, 'hist', f'{n:03d}.pkl')):
        with open(p, 'wb') as f:
            pickle.dump(cv, f)


def batch_files(name):
    return sorted(glob.glob(sdir(name, 'batches', '*.fp')))


def write_view(name, cv, **kw):
    path = kw.pop('out', None) or sdir(name, 'view.png')
    Image.fromarray(render_view(cv, **kw)).save(path)
    return path


def cmd_new(a):
    if os.path.exists(sdir(a.session)):
        if not a.force:
            sys.exit(f'session {a.session!r} exists (use --force to start over)')
        shutil.rmtree(sdir(a.session))
    os.makedirs(sdir(a.session, 'batches'))
    os.makedirs(sdir(a.session, 'hist'))
    with open(sdir(a.session, 'meta.json'), 'w') as f:
        json.dump({'mode': a.mode, 'seed': a.seed}, f)
    save(a.session, Canvas(a.mode, a.seed), 0)
    print(f'{a.session}: {MODES[a.mode]["desc"]}')


def cmd_do(a):
    cv = load(a.session)
    text = sys.stdin.read() if a.script == '-' else open(a.script).read()
    try:
        count = run_script(cv, text, 'stdin' if a.script == '-' else os.path.basename(a.script))
    except PaintError as e:
        sys.exit(f'ERROR {e}\n(nothing was changed)')
    n = len(batch_files(a.session)) + 1
    with open(sdir(a.session, 'batches', f'{n:03d}.fp'), 'w') as f:
        f.write(text)
    save(a.session, cv, n)
    print(f'batch {n:03d}: {count} commands. view -> {write_view(a.session, cv)}')


def cmd_undo(a):
    files = batch_files(a.session)
    k = min(a.n, len(files))
    for f in files[len(files) - k:]:
        os.remove(f)
        os.remove(sdir(a.session, 'hist', os.path.basename(f)[:3] + '.pkl'))
    n = len(files) - k
    shutil.copy(sdir(a.session, 'hist', f'{n:03d}.pkl'), sdir(a.session, 'state.pkl'))
    print(f'took back {k} batch(es); now at batch {n:03d}. view -> {write_view(a.session, load(a.session))}')


def cmd_view(a):
    cv = load(a.session)
    print(write_view(a.session, cv, zoom=a.zoom, grid=a.grid, rulers=not a.plain, out=a.out))


def cmd_export(a):
    cv = load(a.session)
    if a.ui:
        Image.fromarray(upscale(render_chrome(cv), cv.sx, cv.sy)).save(a.out)
    else:
        s = (1, 1) if a.native else (cv.sx, cv.sy)
        im = Image.fromarray(upscale(cv.pix, *s), 'P')
        flat = [int(v) for c in rgb_palette(cv.pal) for v in c]
        im.putpalette(flat + [0] * (768 - len(flat)))
        im.save(a.out)
    print(a.out)


def replay_frames(name, ui=False, want=200):
    with open(sdir(name, 'meta.json')) as f:
        meta = json.load(f)
    scripts = [open(p).read() for p in batch_files(name)]

    def run(hook):
        cv = Canvas(meta['mode'], meta['seed'])
        cv.hook = hook
        for s in scripts:
            run_script(cv, s)
        return cv

    total = [0]
    run(lambda cv: total.__setitem__(0, total[0] + 1))
    stride = max(1, math.ceil(total[0] / want))
    frames, k = [], [0]

    def grab(cv):
        k[0] += 1
        if k[0] % stride == 0 or k[0] == total[0]:
            frames.append(render_chrome(cv) if ui else rgb_palette(cv.pal)[cv.pix])

    cv = run(grab)
    return cv, frames, total[0]


def cmd_replay(a):
    cv, frames, total = replay_frames(a.session, a.ui, a.frames)
    frames.append(rgb_palette(cv.pal)[cv.pix])        # toolbox away for the last look
    save_gif(frames, a.out, [a.ms] * (len(frames) - 1) + [a.hold], cv.sx, cv.sy)
    print(f'{a.out}: {len(frames)} frames from {total} screen updates')


def cycle_frames(cv, limit=240):
    period = 1
    for r, t in cv.cycles.items():
        period = math.lcm(period, len(cv.ranges[r]) * abs(t))
    period = min(period, limit)
    base = rgb_palette(cv.pal)
    frames = []
    for f in range(period):
        pal = base.copy()
        for r, t in cv.cycles.items():
            idx = cv.ranges[r]
            s = (f // abs(t)) * (1 if t > 0 else -1)
            for i, c in enumerate(idx):
                pal[c] = base[idx[(i - s) % len(idx)]]
        frames.append(pal[cv.pix])
    return frames


def cmd_cycle(a):
    cv = load(a.session)
    if not cv.cycles:
        sys.exit('this picture has no cycling ranges')
    frames = cycle_frames(cv)
    save_gif(frames, a.out, [a.ms] * len(frames), cv.sx, cv.sy)
    print(f'{a.out}: {len(frames)} frames')


def cmd_info(a):
    cv = load(a.session)
    used = np.bincount(cv.pix.ravel(), minlength=256)
    print(f'{a.session}: {MODES[cv.mode]["desc"]}; {len(batch_files(a.session))} batches; '
          f'{int((used > 0).sum())} colours on screen; title {cv.title}')
    print('names: ' + ', '.join(f'{k}={v}' for k, v in sorted(cv.names.items(), key=lambda kv: kv[1])))
    for k, v in cv.ranges.items():
        cyc = f'  (cycles every {cv.cycles[k]} ticks)' if k in cv.cycles else ''
        print(f'range {k}: {v[0]}..{v[-1]} ({len(v)}){cyc}' if v == list(range(v[0], v[-1] + 1)) else f'range {k}: {v}{cyc}')
    print(f'fg {cv.fg} bg {cv.bg} brush {cv.brush_desc} ink {cv.ink[0]} '
          f'shade {"on" if cv.shade else "off"} stencil {"on" if cv.stencil is not None else "off"}')


def cmd_palette(a):
    cv = load(a.session)
    pal = rgb_palette(cv.pal)
    per = 16 if cv.ncol > 16 else 8
    rows = (cv.ncol + per - 1) // per
    cw, ch = 64, 44
    out = np.zeros((rows * ch, per * cw, 3), np.uint8)
    for i in range(cv.ncol):
        X, Y = (i % per) * cw, (i // per) * ch
        out[Y:Y + ch - 2, X:X + cw - 2] = pal[i]
        m = text_mask(str(i), 2)
        sub = out[Y + 2:Y + 2 + m.shape[0], X + 2:X + 2 + m.shape[1]]
        sub[m[:, :sub.shape[1]]] = (0, 0, 0) if int(pal[i].sum()) > 380 else (255, 255, 255)
    Image.fromarray(out).save(a.out)
    print(a.out)


def main():
    ap = argparse.ArgumentParser(prog='fpaint.py', description='FablePaint 2.0', epilog='fpaint.py help  for the manual')
    sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('new'); p.add_argument('session'); p.add_argument('--mode', default='vga', choices=MODES)
    p.add_argument('--seed', type=int, default=1987); p.add_argument('--force', action='store_true'); p.set_defaults(fn=cmd_new)
    p = sub.add_parser('do'); p.add_argument('session'); p.add_argument('script'); p.set_defaults(fn=cmd_do)
    p = sub.add_parser('undo'); p.add_argument('session'); p.add_argument('n', type=int, nargs='?', default=1); p.set_defaults(fn=cmd_undo)
    p = sub.add_parser('view'); p.add_argument('session'); p.add_argument('--zoom', type=int, nargs=4, metavar=('X0', 'Y0', 'X1', 'Y1'))
    p.add_argument('--grid', action='store_true'); p.add_argument('--plain', action='store_true'); p.add_argument('-o', '--out'); p.set_defaults(fn=cmd_view)
    p = sub.add_parser('export'); p.add_argument('session'); p.add_argument('-o', '--out', required=True)
    p.add_argument('--ui', action='store_true'); p.add_argument('--native', action='store_true'); p.set_defaults(fn=cmd_export)
    p = sub.add_parser('replay'); p.add_argument('session'); p.add_argument('-o', '--out', required=True); p.add_argument('--ui', action='store_true')
    p.add_argument('--frames', type=int, default=200); p.add_argument('--ms', type=int, default=60); p.add_argument('--hold', type=int, default=4000); p.set_defaults(fn=cmd_replay)
    p = sub.add_parser('cycle'); p.add_argument('session'); p.add_argument('-o', '--out', required=True); p.add_argument('--ms', type=int, default=70); p.set_defaults(fn=cmd_cycle)
    p = sub.add_parser('info'); p.add_argument('session'); p.set_defaults(fn=cmd_info)
    p = sub.add_parser('palette'); p.add_argument('session'); p.add_argument('-o', '--out', required=True); p.set_defaults(fn=cmd_palette)
    sub.add_parser('help').set_defaults(fn=lambda a: print(__doc__))
    a = ap.parse_args()
    a.fn(a)


if __name__ == '__main__':
    main()
