"""backlot.screen: the screening room. An agent cannot watch a film, so these turn motion and
colour into still pictures and numbers it can read.

    filmstrip   frames laid out in a grid, numbered
    onion       two frames overlaid (red = first, cyan = second): what moved, and how far
    motion_map  where the picture changes over the whole shot, as a heat map
    flicker     brightness per frame, plotted; the largest jump
    loop_seam   does the last frame run into the first as smoothly as any other cut?
    scopes      histogram, waveform and vectorscope beside the picture
    stats       value masses, chroma, warm share, detail: one line of numbers
"""
from pathlib import Path
import glob
import numpy as np
import cv2
from .core import F, load, save, lum, l2s, s2l, flat, resize

def _frames(src, every=1):
    """Accept a list of arrays, a list of paths, a glob, a printf pattern or a directory."""
    if isinstance(src, (list, tuple)) and len(src) and isinstance(src[0], np.ndarray):
        return list(src)[::every]
    if isinstance(src, (str, Path)):
        s = str(src)
        if '%' in s:
            s = s[:s.index('%')] + '*' + s[s.index('%'):].split('d', 1)[1]
        paths = sorted(glob.glob(s + '/*.png') + glob.glob(s + '/*.jpg')) if Path(s).is_dir() else sorted(glob.glob(s))
    else:
        paths = list(src)
    return [load(p) for p in paths[::every]]

def _disp(img, w=None):
    """Image -> uint8 BGR for drawing on, optionally resized to width w."""
    rgb = np.clip(l2s(flat(img, '#101010')), 0, 1)
    if w: rgb = cv2.resize(rgb, (w, int(round(rgb.shape[0] * w / rgb.shape[1]))), interpolation=cv2.INTER_AREA)
    return (rgb[..., ::-1] * 255).astype(np.uint8)

def _write(path, bgr):
    Path(path).parent.mkdir(parents=True, exist_ok=True); cv2.imwrite(str(path), bgr, [cv2.IMWRITE_JPEG_QUALITY, 88]); return str(path)

def sheet(images, out, captions=None, cols=4, cell_w=360, pad=8):
    """Any images in a labelled grid."""
    cells = [_disp(im, cell_w) for im in images]
    ch = max(c.shape[0] for c in cells) + 22
    rows = (len(cells) + cols - 1) // cols
    S = np.full((rows * (ch + pad) + pad, cols * (cell_w + pad) + pad, 3), 24, np.uint8)
    for k, c in enumerate(cells):
        y, x = pad + (k // cols) * (ch + pad), pad + (k % cols) * (cell_w + pad)
        S[y:y + c.shape[0], x:x + cell_w] = c
        if captions:
            cv2.putText(S, str(captions[k]), (x + 2, y + ch - 6), cv2.FONT_HERSHEY_SIMPLEX, .45, (210, 210, 200), 1, cv2.LINE_AA)
    return _write(out, S)

def filmstrip(src, out, n=12, cols=4, cell_w=360):
    """n frames spread evenly through the shot, numbered by position."""
    fr = _frames(src)
    idx = np.unique(np.linspace(0, len(fr) - 1, min(n, len(fr))).round().astype(int))
    return sheet([fr[i] for i in idx], out, [f'frame {i}' for i in idx], cols, cell_w)

def onion(a, b, out=None, gain=1.0):
    """First frame in red, second in cyan. Grey = unchanged; coloured fringes = movement."""
    A, B = np.clip(l2s(lum(a)) * gain, 0, 1), np.clip(l2s(lum(b)) * gain, 0, 1)
    img = np.dstack([s2l(A), s2l(B), s2l(B), np.ones_like(A)]).astype(F)
    return save(out, img) if out else img

def motion_map(src, out=None, gain=6.0, soften=2.0):
    """Per-pixel change over time (standard deviation of brightness), as heat. Returns (path or image, stats).
    Frames are softened first so film grain is not counted as motion; soften=0 to count everything."""
    fr = _frames(src)
    L = np.stack([cv2.GaussianBlur(l2s(lum(f)), (0, 0), soften) if soften else l2s(lum(f)) for f in fr])
    sd = L.std(0)
    heat = cv2.applyColorMap((np.clip(sd * gain, 0, 1) * 255).astype(np.uint8), cv2.COLORMAP_INFERNO)
    base = (np.clip(L.mean(0), 0, 1) * 90).astype(np.uint8)[..., None].repeat(3, 2)
    vis = cv2.addWeighted(base, .5, heat, .9, 0)
    st = dict(moving=float((sd > .02).mean()), strong=float((sd > .08).mean()), peak=float(sd.max()))
    return (_write(out, vis) if out else vis), st

def flicker(src, out=None):
    """Mean brightness of each frame. Returns (path or None, dict with the series, the largest frame-to-frame jump, and range)."""
    fr = _frames(src)
    m = np.array([float(l2s(lum(f)).mean()) for f in fr])
    st = dict(mean=float(m.mean()), span=float(m.max() - m.min()), max_jump=float(np.abs(np.diff(m)).max()) if len(m) > 1 else 0.0, series=m.round(4).tolist())
    if out:
        W, H = 900, 260
        P = np.full((H, W, 3), 24, np.uint8)
        lo, hi = m.min() - 1e-3, m.max() + 1e-3
        pts = np.array([[20 + (W - 40) * i / max(len(m) - 1, 1), H - 30 - (H - 60) * (v - lo) / (hi - lo)] for i, v in enumerate(m)], np.int32)
        cv2.polylines(P, [pts], False, (120, 220, 255), 2, cv2.LINE_AA)
        cv2.putText(P, f'mean brightness per frame  min {m.min():.3f}  max {m.max():.3f}  largest jump {st["max_jump"]:.4f}', (20, 20), cv2.FONT_HERSHEY_SIMPLEX, .5, (220, 220, 210), 1, cv2.LINE_AA)
        _write(out, P)
    return out, st

def loop_seam(src):
    """How the cut from the last frame back to the first compares with an ordinary step.
    ratio near 1.0 = seamless; well above 1 = a visible jump at the loop point."""
    fr = _frames(src)
    L = [l2s(lum(f)) for f in fr]
    steps = [float(np.abs(L[i + 1] - L[i]).mean()) for i in range(len(L) - 1)]
    seam = float(np.abs(L[0] - L[-1]).mean())
    med = float(np.median(steps)) if steps else 0.0
    return dict(seam=seam, typical_step=med, ratio=seam / max(med, 1e-6))

def scopes(img, out, w=520):
    """The colourist's instruments: picture, RGB histogram, luma waveform, vectorscope."""
    pic = _disp(img, w); h = pic.shape[0]
    rgb = pic[..., ::-1].astype(F) / 255
    ph = max(h, 260)
    # histogram
    hist = np.full((ph, 300, 3), 18, np.uint8)
    for k, c in enumerate(((90, 90, 255), (90, 230, 90), (255, 150, 90))):
        hh = np.histogram(rgb[..., k], bins=256, range=(0, 1))[0].astype(F); hh = np.sqrt(hh / max(hh.max(), 1))
        pts = np.array([[22 + i, ph - 14 - hh[i] * (ph - 40)] for i in range(256)], np.int32)
        cv2.polylines(hist, [pts], False, c, 1, cv2.LINE_AA)
    cv2.putText(hist, 'histogram (sqrt)', (8, 14), cv2.FONT_HERSHEY_SIMPLEX, .42, (200, 200, 190), 1, cv2.LINE_AA)
    # waveform: for each column, where its pixels sit in brightness
    Y = (rgb @ np.array([.2126, .7152, .0722], F))
    wf = np.zeros((ph, 300), F)
    cols = np.clip((np.arange(Y.shape[1]) * 300 / Y.shape[1]).astype(int), 0, 299)
    rows = np.clip(((1 - Y) * (ph - 30) + 22).astype(int), 0, ph - 1)
    np.add.at(wf, (rows, np.broadcast_to(cols, Y.shape)), 1.0)
    wf = np.clip(wf / max(np.percentile(wf[wf > 0], 97), 1), 0, 1) if (wf > 0).any() else wf
    wfi = np.clip(wf[..., None] * np.array([120, 255, 150], F) * .92 + 18, 0, 255).astype(np.uint8)
    for v in (0, .5, 1):
        yy = int((1 - v) * (ph - 30) + 22); cv2.line(wfi, (0, yy), (299, yy), (70, 70, 70), 1)
    cv2.putText(wfi, 'waveform (luma by column)', (8, 14), cv2.FONT_HERSHEY_SIMPLEX, .42, (200, 200, 190), 1, cv2.LINE_AA)
    # vectorscope: chroma scatter
    cb = -.1146 * rgb[..., 0] - .3854 * rgb[..., 1] + .5 * rgb[..., 2]; cr = .5 * rgb[..., 0] - .4542 * rgb[..., 1] - .0458 * rgb[..., 2]
    vs = np.zeros((ph, ph), F)
    np.add.at(vs, (np.clip((.5 - cr) * ph, 0, ph - 1).astype(int), np.clip((.5 + cb) * ph, 0, ph - 1).astype(int)), 1.0)
    vs = np.clip(vs / max(np.percentile(vs[vs > 0], 98), 1), 0, 1) if (vs > 0).any() else vs
    vsi = np.clip(np.sqrt(vs)[..., None] * np.array([255, 220, 160], F) * .92 + 18, 0, 255).astype(np.uint8)
    cv2.circle(vsi, (ph // 2, ph // 2), int(ph * .25), (70, 70, 70), 1, cv2.LINE_AA); cv2.circle(vsi, (ph // 2, ph // 2), int(ph * .48), (70, 70, 70), 1, cv2.LINE_AA)
    for name, (r_, g_, b_) in (('R', (1, 0, 0)), ('Y', (1, 1, 0)), ('G', (0, 1, 0)), ('C', (0, 1, 1)), ('B', (0, 0, 1)), ('M', (1, 0, 1))):
        x_ = .5 + (-.1146 * r_ - .3854 * g_ + .5 * b_) * .9; y_ = .5 - (.5 * r_ - .4542 * g_ - .0458 * b_) * .9
        cv2.putText(vsi, name, (int(x_ * ph) - 5, int(y_ * ph) + 5), cv2.FONT_HERSHEY_SIMPLEX, .42, (150, 150, 150), 1, cv2.LINE_AA)
    cv2.putText(vsi, 'vectorscope', (8, 14), cv2.FONT_HERSHEY_SIMPLEX, .42, (200, 200, 190), 1, cv2.LINE_AA)
    picp = np.full((ph, w, 3), 18, np.uint8); picp[:h] = pic
    return _write(out, np.hstack([picp, hist, wfi, vsi]))

def stats(img, crop=0.0):
    """Value masses, chroma, warm share, detail (the measurements Lit Window was tuned with)."""
    rgb = np.clip(l2s(flat(img, '#000000')), 0, 1)
    h, w = rgb.shape[:2]; c = int(min(h, w) * crop)
    rgb = rgb[c:h - c, c:w - c] if c else rgb
    lab = cv2.cvtColor(rgb.astype(F), cv2.COLOR_RGB2Lab)
    L, C = lab[..., 0], np.hypot(lab[..., 1], lab[..., 2])
    hue = np.degrees(np.arctan2(lab[..., 2], lab[..., 1])) % 360
    g = cv2.Laplacian(cv2.GaussianBlur(L, (3, 3), 0), cv2.CV_32F)
    return dict(dark=float((L < 35).mean()), mid=float(((L >= 35) & (L < 65)).mean()), light=float((L >= 65).mean()), chroma=float(C.mean()),
                warm=float(((C > 18) & ((hue < 95) | (hue > 330))).mean()), cool=float(((C > 10) & (hue > 180) & (hue < 300)).mean()),
                detail=float((np.abs(g) > 6).mean()), median_L=float(np.median(L)))

def compare(a, b, out, labels=('a', 'b'), w=640):
    """Two pictures side by side with their difference."""
    A, B = _disp(a, w), _disp(b, w); h = min(A.shape[0], B.shape[0]); A, B = A[:h], B[:h]
    D = cv2.applyColorMap(np.clip(np.abs(A.astype(int) - B.astype(int)).max(-1) * 4, 0, 255).astype(np.uint8), cv2.COLORMAP_INFERNO)
    for im, t in ((A, labels[0]), (B, labels[1]), (D, 'difference x4')):
        cv2.putText(im, t, (8, 20), cv2.FONT_HERSHEY_SIMPLEX, .55, (240, 240, 230), 1, cv2.LINE_AA)
    return _write(out, np.hstack([A, B, D]))
