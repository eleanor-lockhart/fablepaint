"""backlot.comp: the compositing desk. Put images over one another, cut them with one another,
move them, and use depth.

All images are linear, premultiplied RGBA (see backlot.core). Mattes are H x W floats.
"""
import numpy as np
import cv2
from .core import F, col, lum

# ---------------------------------------------------------------- putting one image over another
def over(bg, fg, opacity=1.0):
    """fg over bg."""
    fg = fg * opacity
    return fg + bg * (1 - fg[..., 3:4])

def _un(img):
    a = np.maximum(img[..., 3:4], 1e-6)
    return img[..., :3] / a, img[..., 3:4]

MODES = {
    'multiply': lambda b, s: b * s,
    'screen': lambda b, s: 1 - (1 - b) * (1 - s),
    'overlay': lambda b, s: np.where(b < .5, 2 * b * s, 1 - 2 * (1 - b) * (1 - s)),
    'soft_light': lambda b, s: (1 - 2 * s) * b * b + 2 * s * b,
    'darken': np.minimum, 'lighten': np.maximum,
    'difference': lambda b, s: np.abs(b - s),
    'color_dodge': lambda b, s: np.clip(b / np.maximum(1 - s, 1e-4), 0, 8),
}

def blend(bg, fg, mode='normal', opacity=1.0):
    """fg over bg with a blend mode: normal add multiply screen overlay soft_light darken lighten difference color_dodge."""
    if mode == 'normal':
        return over(bg, fg, opacity)
    if mode == 'add':                                   # light adds; coverage does not change
        out = bg.copy(); out[..., :3] += fg[..., :3] * opacity; return out
    b, ba = _un(bg); s, sa = _un(fg); sa = sa * opacity
    mixed = MODES[mode](b, s)
    rgb = b * ba * (1 - sa) + s * sa * (1 - ba) + mixed * sa * ba
    a = ba + sa - ba * sa
    return np.concatenate([rgb, a], 2).astype(F)

def stack(layers):
    """Composite a list bottom-to-top. Each entry: image, or (image, mode), or (image, mode, opacity)."""
    out = None
    for L in layers:
        if isinstance(L, np.ndarray):
            img, mode, op = L, 'normal', 1.0
        else:
            L = tuple(L); img = L[0]; mode = L[1] if len(L) > 1 else 'normal'; op = L[2] if len(L) > 2 else 1.0
        out = img * op if out is None else blend(out, img, mode, op)
    return out

# ---------------------------------------------------------------- mattes: cutting images with one another
def alpha(img): return img[..., 3].copy()
def union(a, b): return np.maximum(a, b)
def intersect(a, b): return np.minimum(a, b)          # where both are
def subtract(a, b): return a * (1 - b)                # a with b cut out of it
def xor(a, b): return a * (1 - b) + b * (1 - a)
def invert(a): return 1 - a
def mask(img, matte): return img * np.asarray(matte, F)[..., None]         # keep the image inside the matte
def cutout(img, matte): return img * (1 - np.asarray(matte, F))[..., None]   # remove the matte from the image

def feather(m, r):
    return cv2.GaussianBlur(np.asarray(m, F), (0, 0), max(r, .01))

def grow(m, px):
    """Dilate (px > 0) or erode (px < 0) a matte by about that many pixels."""
    k = int(abs(px)) * 2 + 1
    ker = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))
    return (cv2.dilate if px > 0 else cv2.erode)(np.asarray(m, F), ker)

def outline(m, w=2.0, where='inside'):
    """A band along the edge of a matte: 'inside', 'outside' or 'centre'."""
    if where == 'inside': return m - grow(m, -w)
    if where == 'outside': return grow(m, w) - m
    return grow(m, w / 2) - grow(m, -w / 2)

def stencil(matte, color, opacity=1.0):
    """A flat colour shaped by a matte, as an image."""
    a = (np.asarray(matte, F) * opacity)[..., None]
    return np.concatenate([col(color) * a, a], 2).astype(F)

def luma_key(img, lo, hi):
    """Matte from brightness: 0 below lo, 1 above hi."""
    return np.clip((lum(img) - lo) / max(hi - lo, 1e-6), 0, 1)

# ---------------------------------------------------------------- moving images
def shift(img, dx, dy):
    """Sub-pixel translate (bilinear), transparent beyond the edges."""
    M = np.float32([[1, 0, dx], [0, 1, dy]])
    return cv2.warpAffine(img, M, (img.shape[1], img.shape[0]), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)

def affine(img, scale=1.0, rotate=0.0, translate=(0, 0), center=None, size=None):
    h, w = img.shape[:2]; c = center or (w / 2, h / 2)
    M = cv2.getRotationMatrix2D(c, rotate, scale); M[:, 2] += translate
    return cv2.warpAffine(img, M, size or (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)

def warp_quad(img, dst, size=None):
    """Perspective-map the whole image onto the quad dst = [tl, tr, br, bl]."""
    h, w = img.shape[:2]
    M = cv2.getPerspectiveTransform(np.float32([[0, 0], [w, 0], [w, h], [0, h]]), np.float32(dst))
    return cv2.warpPerspective(img, M, size or (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)

def multiplane(plates, cam=(0, 0), zoom=1.0, focal=1.0):
    """The animation stand. plates: list of (image, depth), far to near; depth 1.0 is the plane that
    moves 1:1 with the camera, larger depths (farther) move less, smaller (nearer) move more.
    cam: camera offset in pixels at depth 1. Returns the composite."""
    out = None
    for img, z in plates:
        k = focal / max(z, 1e-3)
        s = 1 + (zoom - 1) * k
        p = affine(img, scale=s, translate=(-cam[0] * k, -cam[1] * k)) if (s != 1 or cam != (0, 0)) else img
        out = p if out is None else over(out, p)
    return out

# ---------------------------------------------------------------- light and shadow made on the desk
def blur(img, r):
    return cv2.GaussianBlur(img, (0, 0), max(r, .01))

def drop_shadow(matte, dx=6, dy=8, r=8, color='#000000', opacity=.5):
    """The shadow a cut-out throws on whatever is behind it."""
    return stencil(feather(shift(np.asarray(matte, F)[..., None].repeat(4, 2), dx, dy)[..., 0], r), color, opacity)

def glow(img, r=20, strength=.6, threshold=0.0):
    """Add a blurred copy of the bright parts (bloom on the desk rather than in the lens)."""
    b = img.copy(); b[..., :3] = np.maximum(b[..., :3] - threshold, 0)
    out = img.copy(); out[..., :3] += blur(b, r)[..., :3] * strength
    return out

def light_wrap(fg, bg, r=12, amount=.5):
    """Let the background's light spill over the edge of the foreground, so a cut-out sits in its scene."""
    a = fg[..., 3]
    edge = np.clip(a - cv2.erode(a, np.ones((3, 3), np.uint8), iterations=max(1, int(r / 3))), 0, 1)
    edge = feather(edge, r / 2) * a
    out = fg.copy(); out[..., :3] += blur(bg, r)[..., :3] * (edge * amount)[..., None]
    return out

# ---------------------------------------------------------------- depth
def zmerge(a, za, b, zb):
    """Per-pixel nearest wins (smaller depth is nearer)."""
    near_a = (za <= zb)[..., None]
    return np.where(near_a, over(b, a), over(a, b)), np.minimum(za, zb)

def fog(img, z, color='#8899aa', near=1.0, far=10.0, density=1.0, curve=1.0):
    """Mix toward a haze colour by depth: nothing at `near`, `density` at `far`."""
    t = (np.clip((z - near) / max(far - near, 1e-6), 0, 1) ** curve * density)[..., None] * img[..., 3:4]
    out = img.copy(); out[..., :3] = img[..., :3] * (1 - t) + col(color) * t
    return out

def defocus(img, z, focus, aperture=6.0, steps=7, near=None, far=None):
    """Depth of field after the fact: blur grows with distance from the focus depth. `aperture` is the
    blur radius in pixels at the far limit. Sliced into `steps` bands and recombined."""
    near = z.min() if near is None else near; far = z.max() if far is None else far
    coc = np.abs(z - focus) / max(far - near, 1e-6) * aperture
    radii = np.linspace(0, max(float(coc.max()), 1e-3), steps)
    out = np.zeros_like(img); wsum = np.zeros(img.shape[:2], F)
    for i, r in enumerate(radii):
        wgt = np.clip(1 - np.abs(coc - r) / max(radii[1] - radii[0], 1e-6), 0, 1)
        layer = img * wgt[..., None]
        if r > .3:
            layer = blur(layer, r); wgt = feather(wgt, r)
        out += layer; wsum += wgt
    return out / np.maximum(wsum, 1e-6)[..., None]
