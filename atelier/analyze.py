#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "pillow", "opencv-python-headless"]
# ///
"""Measure a picture the way I'd squint at it: value masses, palette, where the warm is.

  analyze.py stats  IMG...            one line of numbers per image
  analyze.py sheet  OUT.jpg IMG...    contact sheet: picture | 3-value notan | palette, per image
  analyze.py notan  OUT.png IMG       just the 3-value reduction, large

`--crop f` trims that fraction off every side first (to drop paper margins); default .06.
"""
import sys, os
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

def load(p, crop):
    im = Image.open(p).convert('RGB')
    w, h = im.size
    im = im.crop((int(w * crop), int(h * crop), int(w * (1 - crop)), int(h * (1 - crop))))
    return im

def lab(im):
    a = np.asarray(im, dtype=np.float32) / 255
    return cv2.cvtColor(a, cv2.COLOR_RGB2Lab)          # L 0..100

def notan3(im, blur=.012):
    """Three flat values, split at the picture's own tertiles of a blurred L."""
    L = lab(im)[..., 0]
    k = max(3, int(max(L.shape) * blur) | 1)
    Lb = cv2.GaussianBlur(L, (k, k), 0)
    lo, hi = np.percentile(Lb, [38, 76])
    lo, hi = min(lo, 45), max(hi, 62)                  # don't call a mid-grey 'light' just because it's the lightest
    out = np.where(Lb < lo, 30, np.where(Lb < hi, 125, 232)).astype(np.uint8)
    return Image.fromarray(out).convert('RGB')

def palette(im, k=8):
    small = im.copy(); small.thumbnail((220, 220))
    X = lab(small).reshape(-1, 3)
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 40, .5)
    _, lbl, cen = cv2.kmeans(X, k, None, crit, 4, cv2.KMEANS_PP_CENTERS)
    n = np.bincount(lbl.ravel(), minlength=k) / len(X)
    rgb = (cv2.cvtColor(cen.reshape(1, -1, 3).astype(np.float32), cv2.COLOR_Lab2RGB)[0] * 255).clip(0, 255).astype(int)
    order = np.argsort(cen[:, 0])
    return [(tuple(rgb[i]), float(n[i]), cen[i]) for i in order]

def stats(im):
    a = lab(im)
    L, A, Bc = a[..., 0], a[..., 1], a[..., 2]
    C = np.hypot(A, Bc)
    hue = np.degrees(np.arctan2(Bc, A)) % 360
    warm = (C > 18) & ((hue < 95) | (hue > 330))
    cool = (C > 10) & (hue > 180) & (hue < 300)
    g = cv2.Laplacian(cv2.GaussianBlur(L, (3, 3), 0), cv2.CV_32F)
    return dict(dark=float((L < 35).mean()), mid=float(((L >= 35) & (L < 65)).mean()), light=float((L >= 65).mean()),
                Lmed=float(np.median(L)), Lspan=float(np.percentile(L, 98) - np.percentile(L, 2)),
                chroma=float(C.mean()), warm=float(warm.mean()), cool=float(cool.mean()),
                detail=float((np.abs(g) > 6).mean()))

def fmt(s):
    return (f"dark {s['dark']*100:3.0f}%  mid {s['mid']*100:3.0f}%  light {s['light']*100:3.0f}%  | L~{s['Lmed']:3.0f} span {s['Lspan']:3.0f}"
            f" | chroma {s['chroma']:4.1f}  warm {s['warm']*100:4.1f}%  cool {s['cool']*100:3.0f}%  | detail {s['detail']*100:4.1f}%")

def hexs(c):
    return '#%02x%02x%02x' % tuple(c)

def main():
    a = sys.argv[1:]
    crop = .06
    if '--crop' in a:
        i = a.index('--crop'); crop = float(a[i + 1]); del a[i:i + 2]
    cmd = a[0]
    if cmd == 'stats':
        for p in a[1:]:
            im = load(p, crop)
            print(f'{os.path.basename(p)[:26]:26s} {fmt(stats(im))}')
            print(' ' * 27 + ' '.join(f'{hexs(c)}:{n*100:.0f}' for c, n, _ in palette(im)))
    elif cmd == 'notan':
        im = load(a[2], crop); notan3(im).save(a[1])
    elif cmd == 'sheet':
        out, paths = a[1], a[2:]
        ch = 330
        cells = []
        for p in paths:
            im = load(p, crop)
            w = int(im.width * ch / im.height)
            t = im.resize((w, ch), Image.LANCZOS)
            n = notan3(im).resize((w, ch), Image.NEAREST)
            pal = Image.new('RGB', (46, ch), 'white'); d = ImageDraw.Draw(pal)
            y = 0
            for c, frac, _ in palette(im):
                hh = max(2, int(round(frac * ch))); d.rectangle([0, y, 46, y + hh], fill=c); y += hh
            cell = Image.new('RGB', (2 * w + 46 + 16, ch + 30), '#202020')
            cell.paste(t, (0, 0)); cell.paste(n, (w + 4, 0)); cell.paste(pal, (2 * w + 8, 0))
            s = stats(im)
            ImageDraw.Draw(cell).text((2, ch + 2), f"{os.path.basename(p)[:22]}  D{s['dark']*100:.0f} M{s['mid']*100:.0f} L{s['light']*100:.0f}  warm {s['warm']*100:.1f}%", fill='#e0e0e0')
            cells.append(cell)
        rows, row, x = [], [], 0
        for c in cells:
            if x + c.width > 1560 and row:
                rows.append(row); row, x = [], 0
            row.append(c); x += c.width + 10
        rows.append(row)
        Wd = max(sum(c.width + 10 for c in r) for r in rows)
        sheet = Image.new('RGB', (Wd, len(rows) * (ch + 40)), '#202020')
        for j, r in enumerate(rows):
            x = 0
            for c in r:
                sheet.paste(c, (x, j * (ch + 40))); x += c.width + 10
        sheet.save(out, quality=88)
        print(out, sheet.size)

main()
