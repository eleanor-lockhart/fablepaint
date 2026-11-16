"""Key image 1: the lineup. Everyone is a dark paper shape with one lit window. No. 4 does not fit.
    uv run python world/night-service/lineup.py      (from the repository root)"""
import sys, subprocess, math
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from backlot import core, draw, comp, lab, shapes as sh, figure as fg
import cast as CAST

W, H, GROUND, S = 2000, 1100, 930, 610
sh.setup(W, H, 4)
def font(style, size):
    f = subprocess.run(['fc-match', '-f', '%{file}', style], capture_output=True, text=True).stdout.strip()
    return ImageFont.truetype(f, size)
def text(xy, string, f, track=0, anchor='l'):
    """Text as a matte; `track` adds letter spacing in pixels."""
    im = Image.new('L', (W, H), 0); d = ImageDraw.Draw(im)
    widths = [d.textlength(ch, font=f) + track for ch in string]
    x = xy[0] - (sum(widths) / 2 if anchor == 'm' else sum(widths) if anchor == 'r' else 0)
    for ch, wd in zip(string, widths):
        d.text((x, xy[1]), ch, fill=255, font=f); x += wd
    return np.asarray(im, np.float32) / 255

img = draw.gradient(W, H, (0, 0), (0, H), '#090f1b', ('#16263e', .34), ('#3a5673', .72), ('#2b425c', .86), '#1d2e44')
lit = np.zeros((H, W), np.float32)
# ---- No. 4: forty metres. At this scale one boot is most of the picture; the rest is out of frame.
boot = [np.array([(396, GROUND + 30), (404, 868), (440, 822), (520, 792), (700, 770), (940, 742), (1180, 700), (1330, 610), (1410, 450), (1440, 200), (1450, -20),
                  (1960, -20), (1950, 420), (1990, 700), (2040, 790), (2040, GROUND + 30)])]
img = draw.paint(img, draw.raster(boot, W, H), '#1b2439')
plane = [np.array([(1440, 200), (1450, -20), (1590, -20), (1570, 360), (1500, 560), (1380, 650), (1330, 610), (1410, 450)]),
         np.array([(404, 868), (440, 822), (520, 792), (700, 770), (940, 742), (930, 790), (700, 818), (520, 842), (430, 880)])]
img = draw.paint(img, draw.raster(plane, W, H), '#27324d')
seams = [sh.seg((1330, 610), (2040, 690), w=5, wob=0), sh.seg((1180, 700), (1200, 960), w=4, wob=0), sh.seg((1640, 640), (1650, 960), w=4, wob=0),
         sh.seg((940, 742), (2040, 820), w=3, wob=0), sh.seg((1410, 450), (1955, 420), w=4, wob=0)]
img = draw.paint(img, draw.raster(seams, W, H), '#111829')
bolts = [sh.blob(x, y, 8, 8, n=10, rough=.05) for x, y in ((1260, 664), (1420, 668), (1580, 684), (1760, 700), (1920, 716), (1040, 772), (1320, 790), (1800, 838), (1480, 470), (1700, 458), (1900, 446))]
img = draw.paint(img, draw.raster(bolts, W, H), '#33405e')
cable = sh.ribbon([(1210, -20), (1250, 240), (1228, 520), (1150, 700)], w=64, taper=(0, 0), wob=0)       # the cable comes down behind the shin
img = draw.paint(img, draw.raster([cable], W, H), '#111829')
img = draw.paint(img, draw.raster([sh.seg((1190 + i * 3, 60 + i * 150), (1252 + i * 3 - i * i * 6, 74 + i * 150), w=5, wob=0) for i in range(4)], W, H), '#27324d')
# ---- the dock
img = draw.paint(img, draw.rect(W, H, 0, GROUND, W, H), '#080b12')
img = draw.paint(img, draw.rect(W, H, 0, GROUND, W, GROUND + 3), '#2a3550')
# ---- the heron, on its pile, at the end of the line
def heron(ox, oy, s):
    T = lambda pts: np.array([(ox - (x - 300) * s, oy + (y - 700) * s) for x, y in pts])
    body = [(250, 265), (268, 258), (292, 272), (335, 330), (372, 420), (400, 520), (408, 600), (398, 640), (372, 628), (340, 560), (300, 520), (262, 480), (232, 420), (210, 360), (205, 330), (225, 290)]
    neck = [(262, 198), (267, 232), (252, 262), (240, 300), (225, 345), (207, 375), (183, 345), (165, 300), (170, 258), (190, 235), (198, 226), (225, 228), (250, 215)]
    head = [(166, 190), (190, 174), (215, 167), (243, 175), (258, 198), (248, 214), (225, 226), (199, 226), (173, 207)]
    polys = [sh.spline(T(body), closed=True), sh.spline(T(neck), closed=True), sh.spline(T(head), closed=True), T([(50, 215), (120, 196), (167, 185), (175, 209), (120, 212)])]
    polys += [sh.ribbon(T(p), w=7 * s, taper=(0, 0), wob=0) for p in ([(285, 532), (292, 612), (296, 700)], [(318, 566), (323, 640), (327, 694)])]
    polys += [sh.ribbon(T([(262, 186), (290, 236), (304, 318)]), w=3.2 * s, taper=(0, .8), wob=0)]
    return polys
img = draw.paint(img, draw.rect(W, H, 96, GROUND - 150, 176, GROUND), '#0a0e18')
img = draw.paint(img, draw.raster(heron(140, GROUND - 150, .46), W, H), '#10161f')
img = draw.paint(img, draw.raster([sh.blob(170.5, GROUND - 386, 2.4, 2.4, n=8, rough=.05)], W, H), '#f2c56b')
# ---- the cast
C = CAST.cast()
order = [('keeper', 330, False), ('red', 560, False), ('dee', 790, False), ('marisol', 1020, False), ('passenger', 1280, False), ('lang', 1600, True)]
labels = []
for name, x, flip in order:
    c = C[name]
    img = fg.draw_figure(img, c['fig'], c['pose'], S * c['height'], (x, GROUND), colours=c.get('colours', ('#243044', '#0e131c', '#0e131c')),
                         edge=c.get('edge', '#35435c'), edge_w=1.6, flip=flip, window=c['window'])
    lit = np.maximum(lit, fg.draw_figure.lit)
    labels.append((x, c['title'], c['role']))
# ---- light: the windows and the small lit things glow (this is a poster, not a paper box)
img[..., :3] += img[..., :3] * lit[..., None] * 5.0
img = lab.bloom(img, r=10, strength=.55, threshold=1.0, layers=3)
img = lab.tonemap(img, 'filmic', white=6)
# ---- lettering
ink, dim, red = '#e9e2cf', '#8b97ad', '#b23b28'
img = draw.paint(img, draw.rect(W, H, 96, 84, 152, 140), red); img = draw.paint(img, draw.rect(W, H, 127, 112, 140, 129), '#f2c56b')
img = draw.paint(img, text((180, 66), 'NIGHT SERVICE', font('Open Sans Condensed:style=ExtraBold', 86), track=10), ink)
img = draw.paint(img, text((184, 170), 'SOMEBODY HAS TO STAY UP.', font('Open Sans Condensed:style=ExtraBold', 30), track=7), dim)
fn, fr = font('Open Sans Condensed:style=ExtraBold', 30), font('DejaVu Sans Condensed', 20)
for x, t, r in labels:
    img = draw.paint(img, text((x, GROUND + 34), t, fn, track=4, anchor='m'), ink)
    img = draw.paint(img, text((x, GROUND + 76), r, fr, track=1, anchor='m'), dim)
img = draw.paint(img, text((140, GROUND + 34), 'THE NOTARY', fn, track=4, anchor='m'), ink)
img = draw.paint(img, text((140, GROUND + 76), 'saw it', fr, track=1, anchor='m'), dim)
img = draw.paint(img, text((1930, 250), 'NO. 4', fn, track=4, anchor='r'), ink)
img = draw.paint(img, text((1930, 292), '(does not fit)', fr, track=1, anchor='r'), dim)
img = lab.vignette(img, .32, radius=.72)
img = lab.grain(img, .022, size=1.3)
core.save(str(HERE / 'lineup.png'), img)
print('lineup saved')
