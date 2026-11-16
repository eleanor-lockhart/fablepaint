#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["pillow"]
# ///
"""gridref.py OUT.jpg IMG [IMG...] [--crop x0 y0 x1 y1 (fractions)] [--n 10] [--h 700]
Put a numbered grid over a reference so landmarks can be read off as fractions (the artist's grid method)."""
import sys
from PIL import Image, ImageDraw
a = sys.argv[1:]
crop, n, hh = None, 10, 700
if '--crop' in a: i = a.index('--crop'); crop = [float(v) for v in a[i + 1:i + 5]]; del a[i:i + 5]
if '--n' in a: i = a.index('--n'); n = int(a[i + 1]); del a[i:i + 2]
if '--h' in a: i = a.index('--h'); hh = int(a[i + 1]); del a[i:i + 2]
out, cells = a[0], []
for p in a[1:]:
    im = Image.open(p).convert('RGB')
    if crop:
        w, h = im.size; im = im.crop((int(crop[0] * w), int(crop[1] * h), int(crop[2] * w), int(crop[3] * h)))
    im = im.resize((int(im.width * hh / im.height), hh), Image.LANCZOS)
    if n:
        d = ImageDraw.Draw(im, 'RGBA')
        for k in range(1, n):
            x, y = im.width * k / n, im.height * k / n
            d.line([(x, 0), (x, im.height)], fill=(255, 60, 60, 150), width=1); d.line([(0, y), (im.width, y)], fill=(255, 60, 60, 150), width=1)
            d.text((x + 2, 2), str(k), fill=(255, 255, 0, 255)); d.text((2, y + 2), str(k), fill=(255, 255, 0, 255))
    cells.append(im)
W = sum(c.width for c in cells) + 8 * (len(cells) - 1)
sheet = Image.new('RGB', (W, hh), '#202020')
x = 0
for c in cells: sheet.paste(c, (x, 0)); x += c.width + 8
sheet.save(out, quality=86); print(out, sheet.size)
