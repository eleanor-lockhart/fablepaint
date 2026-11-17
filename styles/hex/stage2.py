"""Hex, stage 2: the sixteen-colour print. 640 x 360, every pixel exactly one register.

A model built in metres (stages 4 and 5) is printed the way a machine of about 1993 would have shown it:

    index(g, level, cam, ...)   -> (h, w) uint8, registers 0..F. Light and distance become ordered dither between
                                   registers (a 4 x 4 pattern fixed to the screen: the camera of a still does not
                                   move, so it never crawls). Haze toward the horizon; a sky in dithered bands with
                                   a lattice of stars; nothing green unless the paint was green to begin with.
    Cycle                       colour cycling: a still holds, for some of its pixels, a slot in a short table of
                                registers, and time only turns the table. The sea is a phase map and eight slots.
    dissolve(a, b, p)           the change from one still to the next, made of pixels (never a blend)
    rgb(idx, scale)             the picture, for a file
    text(idx, x, y, s, reg)     system type, straight into the registers
"""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent)); sys.path.insert(1, str(Path(__file__).resolve().parents[2]))
import numpy as np
import kit
from kit import RGB, BAYER
import deep as X

W, H = 640, 360
T16 = RGB.astype(np.float32) / 255
CAND = np.array([0, 1, 2, 3, 8, 9, 0xA, 0xB, 0xC, 0xD, 0xE, 0xF])              # what a print may use for tone: no green
_B8 = np.array([[0, 32, 8, 40, 2, 34, 10, 42], [48, 16, 56, 24, 50, 18, 58, 26], [12, 44, 4, 36, 14, 46, 6, 38], [60, 28, 52, 20, 62, 30, 54, 22],
                [3, 35, 11, 43, 1, 33, 9, 41], [51, 19, 59, 27, 49, 17, 57, 25], [15, 47, 7, 39, 13, 45, 5, 37], [63, 31, 55, 23, 61, 29, 53, 21]], np.float32) / 64 + 1 / 128

def quantise(img, amount=.16, cand=CAND):
    """Continuous colour -> registers, by ordered dither: each pixel takes the nearest register after a nudge
    from the pattern, so a tone between two registers becomes a mixture of them."""
    h, w = img.shape[:2]; yy, xx = np.mgrid[:h, :w]; q = img + ((BAYER[yy % 4, xx % 4] - .5) * amount)[..., None]
    return cand[np.argmin(((q[:, :, None, :] - T16[cand][None, None]) ** 2).sum(-1), -1)].astype(np.uint8)

def rays(cam):
    """World direction of every pixel's ray (unit), for the sky."""
    w, h = cam.size; yy, xx = np.mgrid[:h, :w]
    d = cam.fwd[None, None, :] * cam.f + cam.right[None, None, :] * (xx + .5 - cam.cx)[..., None] - cam.up[None, None, :] * (yy + .5 - cam.cy)[..., None]
    return d / np.linalg.norm(d, axis=-1, keepdims=True)

HORIZON, ZENITH, GLOW = T16[3] * .8 + T16[2] * .2, T16[0] * .6 + T16[1] * .4, T16[0xE] * .55 + T16[3] * .45
_r = np.random.default_rng(11)
STARS = np.c_[_r.uniform(0, 360, 900), np.degrees(np.arcsin(_r.uniform(.06, 1, 900))), _r.integers(0, 6, 900)]      # az, alt, kind
def sky(cam, west=250.0):
    """The sky as continuous colour: dusk at the horizon going to night overhead, the last of the light low in
    the west. Returns (colour, elevation in degrees)."""
    d = rays(cam); alt = np.degrees(np.arcsin(np.clip(d[..., 2], -1, 1))); az = np.degrees(np.arctan2(d[..., 0], d[..., 1])) % 360
    u = np.clip(alt / 24.0, 0, 1) ** .8; col = HORIZON[None, None] * (1 - u[..., None]) + ZENITH[None, None] * u[..., None]
    da = np.abs((az - west + 180) % 360 - 180); g = np.clip(1 - da / 70, 0, 1) * np.clip(1 - alt / 9, 0, 1) ** 2
    return col * (1 - g[..., None]) + GLOW[None, None] * g[..., None], alt

def index(g, level, cam, haze=260.0, keep=None, lamps=(), stars=True):
    """The print. level: light per pixel (depth.lighting). keep: a mask of pixels that keep their own paint
    register untouched (a sprite: the witch stays green). lamps: [(screen x, screen y, strength)] of lit
    lamps, for a dithered halo in the air round each."""
    rgbc = X.colour(g, level, steps=255, dither=0, gamma=.8); hit = g['hit']; skyc, alt = sky(cam)
    dist = np.where(hit, np.linalg.norm(g['pos'] - cam.eye, axis=-1), 0.0); f = (1 - np.exp(-dist / haze))[..., None]
    img = np.where(hit[..., None], rgbc * (1 - f) + HORIZON[None, None] * f * .5, skyc)                      # far land is darker than the sky behind it
    yy, xx = np.mgrid[:img.shape[0], :img.shape[1]]
    for lx, ly, k in lamps:                                               # light in the air
        r2 = (xx - lx) ** 2 + (yy - ly) ** 2; a = (k * np.exp(-r2 / (2 * (26 * k) ** 2)))[..., None]; img = img * (1 - .6 * a) + T16[0xF][None, None] * .6 * a
    idx = quantise(np.clip(img, 0, 1))
    glow = hit & (g['glow'] > 0) & (g['index'] < 16); idx[glow] = g['index'][glow]
    if keep is not None: idx[keep] = g['index'][keep]
    if stars:
        for az, al, k in STARS:
            p = cam.sky(az, al)
            if p and 1 <= p[0] < cam.size[0] - 1 and 1 <= p[1] < cam.size[1] - 1 and not hit[int(p[1]), int(p[0])]: idx[int(p[1]), int(p[0])] = (8, 8, 9, 9, 0xA, 0xC)[int(k)]
    return idx

class Cycle:
    """Colour cycling for one still. `slot` (h, w) uint8: 0 where the picture is fixed, else 1 + group * 8 + phase.
    tables[group] is eight registers; at tick n a cycling pixel shows tables[group][(phase + n) % 8]."""
    def __init__(s, shape): s.slot = np.zeros(shape, np.uint8); s.tables = []
    def group(s, mask, phase, table):
        k = len(s.tables); s.tables.append(list(table)); s.slot[mask] = (1 + k * 8 + (phase[mask] % 8)).astype(np.uint8); return k
    def at(s, idx, tick):
        out = idx.copy()
        for k, tb in enumerate(s.tables):
            m = (s.slot > k * 8) & (s.slot <= k * 8 + 8); out[m] = np.array(tb, np.uint8)[(s.slot[m].astype(np.int64) - 1 - k * 8 + int(tick)) % 8]
        return out

SEA_NEAR, SEA_MID, SEA_FAR = [0, 1, 1, 2, 1, 1, 0, 1], [1, 2, 1, 2, 1, 1, 2, 3], [2, 2, 3, 2, 2, 2, 2, 3]
GLINT = [0xF, 2, 0xE, 1, 0xF, 1, 2, 0xE]; GLINT_FAR = [0xF, 2, 2, 0xE, 2, 0xF, 2, 2]; STATIC = [0, 8, 1, 9, 0, 2, 0xA, 1]
def sea(cyc, g, cam, mask, lamps=()):
    """The sea, as cycling: a phase from where each pixel of water is (so the waves lie on the water and close
    up toward the horizon), three tables by distance, and under each lit lamp a column of glints."""
    P = g['pos']; x, y = P[..., 0], P[..., 1]; d = np.linalg.norm(P - cam.eye, axis=-1)
    ph = .21 * x + .34 * y + .8 * np.sin(.09 * x - .06 * y) + .55 * np.sin(.05 * y + .13 * x + 2.0)
    yy, xx = np.mgrid[:mask.shape[0], :mask.shape[1]]; ph = ph + ((xx * 3 + yy * 5) % 7) * .09                      # a little grain, so bands break up
    phase = np.floor((ph % 4.0) * 2).astype(np.int64)
    cyc.group(mask & (d < 45), phase, SEA_NEAR); cyc.group(mask & (d >= 45) & (d < 160), phase, SEA_MID); cyc.group(mask & (d >= 160), phase, SEA_FAR)
    for lx, ly, k in lamps:                                               # reflections: straight down the screen from the lamp
        wdt = 1.5 + (yy - ly) * .035 * k * 3; col = mask & (yy > ly) & (np.abs(xx - lx) <= wdt) & (((xx + yy * 3) % 3) != 0)
        cyc.group(col & (d < 160), phase + (xx % 3), GLINT); cyc.group(col & (d >= 160), phase + (xx % 3), GLINT_FAR)

_D8 = None
def dissolve(a, b, p):
    """p of the way from still a to still b: a fixed pattern decides which pixels have changed so far."""
    global _D8
    if _D8 is None: h, w = a.shape; yy, xx = np.mgrid[:h, :w]; _D8 = (_B8[(yy // 2) % 8, (xx // 2) % 8] * .75 + np.random.default_rng(3).random((h // 2 + 1, w // 2 + 1))[yy // 2, xx // 2] * .25)
    return np.where(_D8 < p, b, a)

def rgb(idx, scale=2): return np.kron(T16[idx], np.ones((scale, scale, 1), np.float32))
def text(idx, x, y, s, reg, back=None):
    for i, ch in enumerate(s):
        g = kit.glyph(ch); x0 = x + i * 8
        if x0 < 0 or x0 + 8 > idx.shape[1] or y < 0 or y + 8 > idx.shape[0]: continue
        sub = idx[y:y + 8, x0:x0 + 8]
        if back is not None: sub[:] = back
        sub[g] = reg
def rect(idx, x0, y0, x1, y1, reg): idx[max(y0, 0):y1, max(x0, 0):x1] = reg
