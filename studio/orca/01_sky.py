exec(open('orca/common.py').read())
mx, my, mr = MOON
use('Background')
gradient('linear', (0, 0), (0, HZ), [(0, '#050818'), (.6, '#0e1630'), (1, '#232a44')])
yy, xx = np.mgrid[:H, :W].astype(np.float32)
dmoon = np.hypot(xx - mx, yy - my)

layer('stars', blend='add')
dens = np.clip(dmoon / 800, .05, 1) * (yy < HZ)
B(size=1.8, hardness=.6, flow=.8, flow_jitter=.8, size_jitter=.5, psize=False)
scatter(1500, density=dens, color='#d6e0ff')
B(size=3, hardness=.7, flow=.9, flow_jitter=.5, psize=False)
scatter(90, density=dens, color='#ffffff')

# ---------------- the moon
layer('moon_glow', blend='add')
gradient('radial', (mx, my), (mx + 900, my), [(0, '#aebde0', .55), (.26, '#7f93c8', .26), (1, '#7f93c8', 0)])
layer('moon')
fill_ellipse(mx, my, mr, mr, color='#f2eddc')
lock(True)
B(size=150, hardness=0, flow=.32, psize=False)
dabs([(mx - 70, my - 60), (mx - 10, my - 95, .8), (mx + 60, my - 40, .9), (mx - 95, my + 30, .7), (mx + 20, my + 60, .95),
      (mx + 95, my + 85, .6), (mx - 30, my + 120, .5)], color='#b4b0a6', psize=True)
gradient('radial', (mx, my), (mx + mr, my), [(0, '#ffffff', 0), (.75, '#000000', 0), (1, '#1a1a2a', .35)])
lock(False)
layer('moon_tex', blend='overlay', clip=True, opacity=.5)
clouds('#000000', '#ffffff', scale=22, octaves=5, seed=3, ridged=True)
emboss(angle=140, depth=1.5)

# ---------------- thin cloud, lit only where it nears the moon
layer('clouds')
B(tip='cloud', size=190, flow=.13, spacing=.12, angle_jitter=1, psize=True)
for pts in ([(-100, 250, .6), (400, 230, 1), (900, 270, .8), (1300, 250, .4)], [(1500, 600, .5), (1900, 570, .9), (2300, 590, 1), (2700, 560, .7)],
            [(-100, 660, .7), (300, 640, 1), (700, 665, .6)], [(1700, 180, .4), (2100, 150, .8), (2600, 170, 1)],
            [(700, 500, .3), (1000, 470, .5), (1250, 490, .3)]):
    stroke(pts, color='#252e4c')
gaussian_blur(7)
layer('cloud_light', blend='add', clip=True)
gradient('radial', (mx, my), (mx + 850, my), [(0, '#c8d2f0', .6), (1, '#c8d2f0', 0)])

# ---------------- Rainier under the moon, and the foothills
layer('rainier')
fill_poly([(1380, 884), (1470, 824), (1540, 764), (1590, 718), (1625, 697), (1660, 690), (1700, 708), (1745, 752), (1800, 802),
           (1880, 852), (1960, 884)], color='#7f8db4')
turbulence(6, 26, seed=4)
layer('rainier_tex', blend='overlay', clip=True, opacity=.8)
clouds('#000000', '#ffffff', scale=16, octaves=6, seed=6, ridged=True)
emboss(angle=120, depth=1.6)
layer('rainier_haze', clip=True)
gradient('linear', (0, 700), (0, 884), [(0, '#232a44', 0), (1, '#232a44', .9)])
layer('foothills')
fill_poly([(0, 862), (300, 850), (700, 858), (1100, 846), (1500, 860), (2000, 850), (2560, 858), (2560, 884), (0, 884)], color='#0e1428', smooth=True)

# ---------------- Seattle
layer('city')
ink = '#080c1a'
towers = [(560, 600, 812), (606, 650, 790), (660, 700, 828), (705, 760, 770), (770, 810, 800), (815, 860, 742), (866, 905, 780),
          (910, 975, 700), (980, 1030, 760), (1035, 1080, 790), (1085, 1150, 735), (1155, 1200, 800), (1205, 1260, 770),
          (1265, 1300, 820), (1305, 1360, 790), (1365, 1400, 835)]
for x0, x1, top in towers:
    fill_rect(x0, top, x1, 884, color=ink)
fill_poly([(100, 884), (160, 858), (300, 846), (420, 852), (540, 862), (560, 884)], color=ink, smooth=True)       # Queen Anne
fill_poly([(1400, 884), (1420, 856), (1560, 852), (1700, 862), (1760, 884)], color=ink)                           # waterfront sheds
fill_poly([(410, 884), (425, 800), (435, 800), (450, 884)], color=ink)                                             # the Needle
fill_rect(426, 744, 434, 802, color=ink)
fill_ellipse(430, 737, 36, 9, color=ink)
fill_ellipse(430, 729, 23, 6, color=ink)
fill_rect(429, 690, 431, 729, color=ink)
B(size=2.5, hardness=.8, spacing=.2, psize=False)
for cx in (1450, 1520, 1600, 1680):                                                                                # port cranes
    stroke([(cx, 884), (cx + 6, 820), (cx - 34, 808)], color=ink, smooth=False)
    stroke([(cx + 6, 820), (cx + 30, 884)], color=ink, smooth=False)
lock(True)
B(size=2.2, hardness=.8, flow=.9, flow_jitter=.6, psize=False)
select_alpha('city')
scatter(2600, (100, 700, 1760, 882), color='#ffd9a0')
scatter(900, (100, 700, 1760, 882), color='#dfe8ff')
select_none()
lock(False)
B(size=3, hardness=.6, psize=False)
dabs([(430, 688), (430, 737), (396, 737), (464, 737)], color='#ff5040')
# ---------------- what is burning
layer('smoke')
B(tip='cloud', size=150, flow=.22, spacing=.12, angle_jitter=1, psize=True)
for x0 in (732, 1118, 1332, 620):
    stroke([(x0, 770, .25), (x0 + 30, 680, .45), (x0 + 90, 580, .7), (x0 + 190, 470, .9), (x0 + 330, 360, 1)], color='#0e0b10')
gaussian_blur(5)
layer('smoke_fire', blend='add', clip=True)
gradient('linear', (0, 880), (0, 560), [(0, '#ff6a20', .55), (1, '#ff6a20', 0)])
layer('fires', blend='add')
B(tip='cloud', size=46, flow=.5, angle_jitter=1, psize=True)
dabs([(732, 775, 1), (742, 760, .7), (1118, 740, 1), (1108, 728, .7), (1332, 794, .9), (620, 792, .7), (1500, 850, .6)], color='#ff7a1a')
B(size=130, hardness=0, flow=.25, psize=False)
dabs([(732, 770), (1118, 738), (1332, 792), (620, 790)], color='#ff5a10')
B(tip='cloud', size=18, flow=.8, angle_jitter=1, psize=True)
dabs([(732, 772, 1), (1118, 740, 1), (1332, 794, .8), (620, 792, .7)], color='#ffe0a0')

# ---------------- the battle overhead
layer('beams', blend='add')
for x0, x1, y1 in ((600, 1880, 300), (1010, 2050, 380), (1290, 1800, 200), (300, 1500, 120)):
    fill_poly([(x0 - 3, 880), (x0 + 3, 880), (x1 + 40, y1), (x1 - 40, y1)], color='#b8ccff', opacity=.10, feather=3)
layer('trails')
B(size=7, hardness=0, flow=.5, spacing=.1, psize=True, taper=(.5, 0))
shots = ([(2560, 60), (2480, 150), (2400, 260)], [(2560, 240), (2470, 290), (2380, 330)], [(2300, 0), (2330, 120), (2350, 250)],
         [(2040, 0), (2180, 140), (2300, 280)], [(2560, 420), (2480, 400), (2400, 370)])
for s in shots:
    stroke(s, color='#8a90aa')
gaussian_blur(1.5)
layer('fx', blend='add')
B(size=4, hardness=.5, spacing=3.2, flow=.9, psize=False)
for arc in ([(300, 905), (1000, 600), (1800, 500)], [(900, 880), (1450, 640), (1850, 560)], [(2540, 880), (2380, 700), (2180, 600)],
            [(140, 880), (700, 520), (1500, 330)]):
    stroke(arc, color='#ff8a30')
B(size=9, hardness=.2, psize=False)
dabs([s[-1] for s in shots], color='#fff0d0')
# the barrier the missiles are bursting against: nested octagons, seen at a slant
cx, cy = 2350, 310
B(size=5, hardness=.4, flow=.75, spacing=.1, psize=False)
for k in range(1, 7):
    ring = [(cx + 34 * k * .5 * math.cos(math.radians(22.5 + 45 * i)), cy + 34 * k * math.sin(math.radians(22.5 + 45 * i))) for i in range(9)]
    stroke(ring, color=mix('#ffb040', '#ff5a10', k / 6), smooth=False, flow=.8 - k * .09)
B(size=150, hardness=0, flow=.5, psize=True)
dabs([(2390, 270, 1), (2372, 335, .7), (2350, 250, .6), (2340, 300, .9)], color='#ff8a30')
B(size=50, hardness=0, flow=.9, psize=True)
dabs([(2392, 268, 1), (2374, 334, .7), (2352, 252, .6)], color='#fff4d8')
# jets
layer('jets')
for jx, jy, d in ((300, 190, 1), (520, 140, 1), (2470, 70, -1), (2240, 40, -1)):
    fill_poly([(jx - 16 * d, jy), (jx + 14 * d, jy - 3), (jx + 20 * d, jy), (jx + 2 * d, jy + 4), (jx - 12 * d, jy + 9), (jx - 8 * d, jy + 2)], color='#05070f')
use('fx')
B(size=8, hardness=.2, psize=False)
dabs([(300 - 20, 191), (520 - 20, 141), (2470 + 20, 71), (2240 + 20, 41)], color='#ffb060')
