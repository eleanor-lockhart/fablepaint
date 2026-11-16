"""backlot.lab: finishing. Colour, the lens, the film, the print, the screen.

Everything takes and returns a linear premultiplied image and leaves alpha alone. Order that
usually works: comp -> exposure/grade -> lens (bloom, halation, aberration, vignette) ->
tonemap -> grain -> output. Print and screen finishes come last and expect display-range values.
"""
import numpy as np
import cv2
from .core import F, col, lum, s2l, l2s

def _rgb(img, rgb):
    out = img.copy(); out[..., :3] = rgb; return out

# ---------------------------------------------------------------- colour
def exposure(img, stops):
    return _rgb(img, img[..., :3] * (2.0 ** stops))

def white_balance(img, warm=0.0, tint=0.0):
    """warm > 0 pushes toward amber, < 0 toward blue; tint > 0 toward magenta."""
    g = np.array([1 + .25 * warm + .08 * tint, 1 - .08 * tint, 1 - .25 * warm + .08 * tint], F)
    return _rgb(img, img[..., :3] * g)

def saturation(img, s):
    L = lum(img)[..., None]
    return _rgb(img, L + (img[..., :3] - L) * s)

def cdl(img, slope=(1, 1, 1), offset=(0, 0, 0), power=(1, 1, 1), sat=1.0):
    """ASC colour decision list: out = (in * slope + offset) ** power, then saturation."""
    x = np.clip(img[..., :3] * np.array(slope, F) + np.array(offset, F), 0, None) ** np.array(power, F)
    return saturation(_rgb(img, x), sat)

def lift_gamma_gain(img, lift=(0, 0, 0), gamma=(1, 1, 1), gain=(1, 1, 1)):
    """The colourist's three wheels, applied to display-encoded values."""
    x = l2s(img[..., :3])
    x = x * np.array(gain, F) + np.array(lift, F) * (1 - x)
    x = np.clip(x, 0, None) ** (1 / np.array(gamma, F))
    return _rgb(img, s2l(x))

def curves(img, pts, channel=None):
    """Tone curve through (in, out) points on display-encoded values; channel 0/1/2 or None for all."""
    xs, ys = zip(*sorted(pts)); x = l2s(img[..., :3])
    if channel is None:
        x = np.interp(x, xs, ys)
    else:
        x[..., channel] = np.interp(x[..., channel], xs, ys)
    return _rgb(img, s2l(x.astype(F)))

def split_tone(img, shadows='#203a5a', highlights='#ffd9a0', balance=.5, amount=.25):
    """Tint the darks one colour and the lights another."""
    L = np.clip(l2s(lum(img)), 0, 1)[..., None]
    w = np.clip((L - balance) * 2 + .5, 0, 1)
    tint = col(shadows) * (1 - w) + col(highlights) * w
    tint = tint / np.maximum(tint.mean(-1, keepdims=True), 1e-4)        # keep brightness; change colour only
    return _rgb(img, img[..., :3] * (1 - amount) + img[..., :3] * tint * amount)

def tonemap(img, kind='filmic', white=4.0, contrast=1.0):
    """Bring scene light (any range) into 0..1. 'filmic' has a toe and a shoulder; 'reinhard' is gentler; 'clip' does nothing."""
    x = np.clip(img[..., :3], 0, None)
    if kind == 'reinhard':
        x = x * (1 + x / white ** 2) / (1 + x)
    elif kind == 'filmic':                               # Hable / Uncharted 2 curve
        def h(v): return ((v * (.15 * v + .05) + .004) / (v * (.15 * v + .5) + .06)) - .0667
        x = h(x * 2.0) / h(np.float32(white * 2.0))
    if contrast != 1:
        x = np.clip(.18 * (x / .18) ** contrast, 0, None)
    return _rgb(img, np.clip(x, 0, 1) if kind != 'clip' else x)

# ---------------------------------------------------------------- the lens
def _blur(a, r): return cv2.GaussianBlur(a, (0, 0), max(r, .01))

def bloom(img, r=24, strength=.35, threshold=.8, layers=3, protect=None):
    """Light spreading in the lens from the bright parts: several widths summed, so it has a core and a veil.

    `protect` is a matte of shapes that must stay dark (silhouettes). Light from elsewhere in the frame is kept
    off them, and lights inside them (a lit window in a figure's chest) still glow. Without it a large bright
    area behind a thin dark figure turns the figure grey: a moon did that to a whole shot."""
    def spread(rgb):
        hi = np.maximum(rgb - threshold, 0)
        return sum(_blur(hi, r * (2 ** i)) / (i + 1) for i in range(layers)) * strength
    rgb = img[..., :3]; acc = spread(rgb)
    if protect is not None and np.max(protect) > 0:
        s = np.asarray(protect, F)[..., None]
        acc = acc * (1 - s) + spread(rgb * s) * s
    return _rgb(img, rgb + acc)

def halation(img, r=14, strength=.5, threshold=.9, tint='#ff5a2a'):
    """Film halation: bright light bouncing off the film base and exposing the red layer around highlights."""
    hi = np.maximum(lum(img) - threshold, 0)
    return _rgb(img, img[..., :3] + _blur(hi, r)[..., None] * col(tint) * strength)

def mist(img, r=30, amount=.25):
    """Diffusion filter: a fraction of the whole image, blurred, laid back over it. Softens contrast, lifts shadows near lights."""
    return _rgb(img, img[..., :3] * (1 - amount) + _blur(img[..., :3], r) * amount)

def vignette(img, strength=.35, radius=.75, softness=.5, squeeze=1.0):
    h, w = img.shape[:2]
    y, x = np.mgrid[:h, :w].astype(F)
    d = np.hypot((x - w / 2) / (w / 2) * squeeze, (y - h / 2) / (h / 2))
    v = 1 - strength * np.clip((d - radius) / max(softness, 1e-4), 0, 1) ** 2
    return img * v[..., None] if img[..., 3].min() > .999 else _rgb(img, img[..., :3] * v[..., None])

def _radial(a, scale):
    h, w = a.shape[:2]
    M = np.float32([[scale, 0, (1 - scale) * w / 2], [0, scale, (1 - scale) * h / 2]])
    return cv2.warpAffine(a, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

def aberration(img, amount=.002):
    """Lateral chromatic aberration: red and blue magnified by slightly different amounts."""
    out = img.copy()
    out[..., 0] = _radial(img[..., 0], 1 + amount); out[..., 2] = _radial(img[..., 2], 1 - amount)
    return out

def distort(img, k=-.05):
    """Barrel (k < 0) or pincushion (k > 0) lens distortion."""
    h, w = img.shape[:2]
    y, x = np.mgrid[:h, :w].astype(F)
    u, v = (x - w / 2) / (w / 2), (y - h / 2) / (w / 2)
    f = 1 + k * (u * u + v * v)
    return cv2.remap(img, (u * f * w / 2 + w / 2).astype(F), (v * f * w / 2 + h / 2).astype(F), cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

def sharpen(img, amount=.5, r=1.2):
    return _rgb(img, np.clip(img[..., :3] + (img[..., :3] - _blur(img[..., :3], r)) * amount, 0, None))

# ---------------------------------------------------------------- the film (per-frame: pass the frame number)
def grain(img, amount=.035, size=1.3, frame=0, seed=0, colour=.25):
    """Film grain: strongest in the middle tones, a new pattern every frame, slightly coloured."""
    h, w = img.shape[:2]
    r = np.random.default_rng(seed * 100003 + frame)
    sh, sw = int(h / size) + 1, int(w / size) + 1
    n = r.normal(0, 1, (sh, sw, 3)).astype(F)
    n = n[..., :1] * (1 - colour) + n * colour
    n = cv2.resize(n, (w, h), interpolation=cv2.INTER_LINEAR)
    x = l2s(img[..., :3]); L = x.mean(-1, keepdims=True)
    weight = .35 + 2.6 * L * (1 - L)
    return _rgb(img, s2l(np.clip(x + n * amount * weight, 0, 1)))

def weave(img, frame, amount=.6, seed=0):
    """Gate weave: the whole picture shifting a fraction of a pixel from frame to frame."""
    r = np.random.default_rng(seed * 7919 + frame); dx, dy = r.normal(0, amount, 2)
    M = np.float32([[1, 0, dx], [0, 1, dy]])
    return cv2.warpAffine(img, M, (img.shape[1], img.shape[0]), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

def flicker(img, frame, amount=.02, seed=0):
    g = 1 + np.random.default_rng(seed * 104729 + frame).normal(0, amount)
    return _rgb(img, img[..., :3] * g)

# ---------------------------------------------------------------- the print
def paper(img, tone='#e9dfc9', strength=.3, seed=5):
    """Print onto paper: multiply by a paper tone with fibre in it."""
    from .draw import fbm
    h, w = img.shape[:2]
    fib = fbm(w, h, scale=w / 4, octaves=2, seed=seed, stretch=(3.0, .45))
    p = col(tone) * (1 - strength * .12 * fib[..., None])
    return _rgb(img, img[..., :3] * p)

def misregister(img, offsets=((1.2, 0), (0, 0), (-.8, .9))):
    """Shift the three channels against each other, as plates printed out of register."""
    out = img.copy()
    for k, (dx, dy) in enumerate(offsets):
        M = np.float32([[1, 0, dx], [0, 1, dy]])
        out[..., k] = cv2.warpAffine(img[..., k], M, (img.shape[1], img.shape[0]), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return out

def halftone(img, cell=7.0, angles=(15, 75, 0, 45), paper_tone='#f1ead8', inks=('#00a0d8', '#d8127a', '#f5d800', '#151515')):
    """Four-colour process printing: each ink as a screen of dots at its own angle."""
    h, w = img.shape[:2]
    rgb = np.clip(l2s(img[..., :3]), 0, 1)
    k = 1 - rgb.max(-1)
    cmy = (1 - rgb - k[..., None]) / np.maximum(1 - k[..., None], 1e-4)
    chans = [cmy[..., 0], cmy[..., 1], cmy[..., 2], k]
    y, x = np.mgrid[:h, :w].astype(F)
    out = np.broadcast_to(l2s(col(paper_tone)), (h, w, 3)).copy()
    for c, ang, ink in zip(chans, angles, inks):
        a = np.radians(ang); u = (x * np.cos(a) + y * np.sin(a)) / cell; v = (-x * np.sin(a) + y * np.cos(a)) / cell
        d = np.hypot(u - np.round(u), v - np.round(v))
        rad = np.sqrt(np.clip(_blur(c.astype(F), cell * .5), 0, 1) / np.pi) * 1.25
        cov = np.clip((rad - d) * cell * .9 + .5, 0, 1)[..., None]
        out = out * (1 - cov * (1 - l2s(col(ink))))
    return _rgb(img, s2l(out.astype(F)))

PALETTES = {
    'cga': ['#000000', '#55ffff', '#ff55ff', '#ffffff'],
    'ega': ['#000000', '#0000aa', '#00aa00', '#00aaaa', '#aa0000', '#aa00aa', '#aa5500', '#aaaaaa', '#555555', '#5555ff', '#55ff55', '#55ffff', '#ff5555', '#ff55ff', '#ffff55', '#ffffff'],
    'gameboy': ['#0f380f', '#306230', '#8bac0f', '#9bbc0f'],
    'mac': ['#000000', '#ffffff'],
    'lit-window': ['#0f1722', '#22364a', '#4f6676', '#8fa3aa', '#c5cfce', '#e9e2cf', '#d8823a', '#b23b28'],
}
_BAYER = np.array([[0, 32, 8, 40, 2, 34, 10, 42], [48, 16, 56, 24, 50, 18, 58, 26], [12, 44, 4, 36, 14, 46, 6, 38], [60, 28, 52, 20, 62, 30, 54, 22],
                   [3, 35, 11, 43, 1, 33, 9, 41], [51, 19, 59, 27, 49, 17, 57, 25], [15, 47, 7, 39, 13, 45, 5, 37], [63, 31, 55, 23, 61, 29, 53, 21]], F) / 64 - .5

def quantize(img, palette='ega', dither='bayer', spread=.22, pixel=1):
    """Reduce to a fixed palette (a name from PALETTES or a list of '#rrggbb'), with ordered or noise dither.
    pixel > 1 also drops the resolution and scales back up with hard pixels."""
    pal = PALETTES[palette] if isinstance(palette, str) else palette
    P = np.array([l2s(col(c)) for c in pal], F)
    h, w = img.shape[:2]
    x = np.clip(l2s(img[..., :3]), 0, 1)
    if pixel > 1:
        x = cv2.resize(x, (w // pixel, h // pixel), interpolation=cv2.INTER_AREA)
    hh, ww = x.shape[:2]
    if dither == 'bayer':
        x = x + np.tile(_BAYER, (hh // 8 + 1, ww // 8 + 1))[:hh, :ww, None] * spread
    elif dither == 'noise':
        x = x + np.random.default_rng(3).uniform(-.5, .5, (hh, ww, 1)).astype(F) * spread
    d = ((x[:, :, None, :] - P[None, None]) ** 2 * np.array([.3, .59, .11], F)).sum(-1)
    out = P[d.argmin(-1)]
    if pixel > 1:
        out = cv2.resize(out, (w, h), interpolation=cv2.INTER_NEAREST)
    return _rgb(img, s2l(out))

def crt(img, lines=240, mask=.25, glow=.25, curve=.04, frame=0):
    """Show it on a tube: scanlines, an aperture grille, phosphor glow, a curved face."""
    h, w = img.shape[:2]
    x = img[..., :3]
    y = np.arange(h, dtype=F)[:, None, None]
    scan = .62 + .38 * np.cos(2 * np.pi * (y * lines / h + .5 * (frame % 2))) ** 2
    grille = np.ones((1, w, 3), F)
    for k in range(3):
        grille[0, k::3, k] = 1 + mask * 1.6
    grille *= (1 - mask * .55)
    out = x * scan * grille
    out = out + _blur(out, h / 160) * glow
    res = _rgb(img, out)
    return distort(res, -curve) if curve else res
