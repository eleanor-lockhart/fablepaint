"""backlot.core: the image convention every department shares, and file in/out.

An image is a float32 array H x W x 4: linear light, premultiplied alpha (the same convention as
Fable Studio). A matte is a float32 array H x W in 0..1. Colours are given as '#rrggbb' (display
values) and converted on the way in. Values above 1.0 are legal until the lab tone-maps them.
"""
import os
from pathlib import Path
import numpy as np
import cv2

F = np.float32
os.environ.setdefault('OPENCV_IO_ENABLE_OPENEXR', '1')

def s2l(x):
    x = np.asarray(x, F)
    return np.where(x <= .04045, x / 12.92, ((x + .055) / 1.055) ** 2.4).astype(F)

def l2s(x):
    x = np.clip(np.asarray(x, F), 0, None)
    return np.where(x <= .0031308, x * 12.92, 1.055 * np.power(x, 1 / 2.4) - .055).astype(F)

def col(c):
    """'#rrggbb', (r, g, b) in 0..255 or 0..1 display values -> linear rgb, float32[3]."""
    if isinstance(c, str):
        c = c.lstrip('#'); v = np.array([int(c[i:i + 2], 16) for i in (0, 2, 4)], F) / 255
    else:
        v = np.array(c[:3], F); v = v / 255 if v.max() > 1 else v
    return s2l(v)

def canvas(w, h, color=None, alpha=1.0):
    """A blank image, transparent or filled with a colour."""
    img = np.zeros((h, w, 4), F)
    if color is not None:
        img[..., :3] = col(color) * alpha; img[..., 3] = alpha
    return img

def lum(img):
    return img[..., 0] * .2126 + img[..., 1] * .7152 + img[..., 2] * .0722

def flat(img, bg='#000000'):
    """Composite onto an opaque background colour -> H x W x 3 linear."""
    return img[..., :3] + col(bg) * (1 - img[..., 3:4])

def load(path, linear=True):
    """Read PNG/JPG/TIFF (8 or 16 bit) or single-layer EXR -> image (linear, premultiplied)."""
    a = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
    if a is None:
        raise FileNotFoundError(path)
    isf = a.dtype in (np.float32, np.float64)
    a = a.astype(F) / (1 if isf else (65535 if a.dtype == np.uint16 else 255))
    if a.ndim == 2:
        a = np.repeat(a[..., None], 3, 2)
    alpha = a[..., 3:4] if a.shape[2] == 4 else np.ones(a.shape[:2] + (1,), F)
    rgb = a[..., 2::-1] if a.shape[2] >= 3 else a
    rgb = rgb if (isf or not linear) else s2l(rgb)
    return np.concatenate([rgb * (1 if isf else alpha), alpha], 2).astype(F)

def save(path, img, bits=8, bg=None, dither=True, quality=92):
    """Write an image as display-referred sRGB. PNG keeps alpha unless `bg` is given; JPG is flattened."""
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    img = np.asarray(img, F)
    if img.ndim == 2:
        img = np.dstack([img, img, img, np.ones_like(img)])
    if img.shape[2] == 3:
        img = np.dstack([img, np.ones(img.shape[:2], F)])
    jpg = path.suffix.lower() in ('.jpg', '.jpeg')
    opaque = bg is not None or jpg or float(img[..., 3].min()) > .999
    if opaque:
        rgb = l2s(flat(img, bg or '#000000')); out = rgb
    else:
        a = np.clip(img[..., 3:4], 0, 1)
        out = np.concatenate([l2s(img[..., :3] / np.maximum(a, 1e-6)), a], 2)
    mx = 65535 if bits == 16 and not jpg else 255
    out = np.clip(out, 0, 1) * mx
    if dither and mx == 255:
        out = out + np.random.default_rng(7).uniform(-.5, .5, out.shape[:2] + (1,)).astype(F)
    out = np.clip(np.round(out), 0, mx).astype(np.uint16 if mx == 65535 else np.uint8)
    out = out[..., [2, 1, 0]] if out.shape[2] == 3 else out[..., [2, 1, 0, 3]]
    cv2.imwrite(str(path), out, [cv2.IMWRITE_JPEG_QUALITY, quality] if jpg else [])
    return str(path)

def resize(img, w, h=None):
    """Resize to width w (height follows unless given). Area filter down, Lanczos up."""
    h = h or int(round(img.shape[0] * w / img.shape[1]))
    return cv2.resize(img, (w, h), interpolation=cv2.INTER_AREA if w < img.shape[1] else cv2.INTER_LANCZOS4)

def read_exr(path):
    """Read a multilayer EXR from Blender -> dict of float32 arrays keyed by pass name with the view-layer
    prefix removed: 'Combined' (H,W,4), 'Depth' (H,W), 'Normal' (H,W,3), 'Object Index' (H,W), 'Emission' (H,W,3)..."""
    import OpenEXR
    out, parts = {}, {}
    with OpenEXR.File(str(path)) as f:
        for part in f.parts:
            for name, c in part.channels.items():
                key = name.split('.', 1)[1] if '.' in name else name
                parts[key] = np.asarray(c.pixels, F)
    for key, px in parts.items():
        base, _, suffix = key.rpartition('.')
        if base and suffix in ('X', 'Y', 'Z') and px.ndim == 2:
            sib = [parts.get(f'{base}.{k}') for k in 'XYZ']
            out[base] = np.dstack(sib) if all(v is not None for v in sib) else px
        else:
            out[key] = px
    return out
