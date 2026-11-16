exec(open('orca/common.py').read())
mx, my, mr = MOON
yy, xx = np.mgrid[:H, :W].astype(np.float32)
# ---------------- corrections to the sky
use('moon_glow'); clear()                      # the glow ended at a hard edge: ease it out
c = '#93a6d8'
gradient('radial', (mx, my), (mx + 760, my), [(0, c, .6), (.12, c, .34), (.26, c, .17), (.45, c, .075), (.65, c, .028), (.85, c, .008), (1, c, 0)])
props('moon_tex', opacity=.16)                 # it looked like dough
props('rainier_tex', opacity=.4)
use('rainier'); lock(True); fill('#99a2bc', opacity=.6); lock(False)
use('beams'); clear()                          # searchlights were planks: thin them
for x0, x1, y1 in ((600, 1880, 300), (1010, 2050, 380), (1290, 1800, 200)):
    fill_poly([(x0 - 2, 880), (x0 + 2, 880), (x1 + 13, y1), (x1 - 13, y1)], color='#b8ccff', opacity=.07, feather=2)
use('fx'); clear()                             # tracer arcs were dotted diagrams: short bursts instead
B(size=3.2, hardness=.5, flow=.9, psize=False, smooth=False)
for (x0, y0), (x1, y1) in (((300, 905), (1750, 520)), ((900, 880), (1820, 580)), ((2540, 880), (2200, 610)), ((140, 880), (1500, 340))):
    for t0 in rng.uniform(.08, .92, 9):
        t1 = t0 + .012
        stroke([(x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0 - 260 * math.sin(math.pi * t0)),
                (x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1 - 260 * math.sin(math.pi * t1))], color='#ff9a40')
shots = ((2400, 260), (2380, 330), (2350, 250), (2300, 280), (2400, 370))
B(size=9, hardness=.2, psize=False)
dabs(shots, color='#fff0d0')
cx, cy = 2350, 310                              # the barrier, quieter: thin lines that fade outward
B(size=3, hardness=.4, spacing=.1, psize=False)
for k in range(1, 8):
    ring = [(cx + 30 * k * .42 * math.cos(math.radians(22.5 + 45 * i)), cy + 30 * k * math.sin(math.radians(22.5 + 45 * i))) for i in range(9)]
    stroke(ring, color=mix('#ffc060', '#ff5a10', k / 7), smooth=False, flow=.75 * (1 - k / 8.5))
gaussian_blur(.9)
B(size=170, hardness=0, flow=.45, psize=True)
dabs([(2390, 270, 1), (2372, 335, .7), (2350, 250, .6)], color='#ff7a28')
B(tip='cloud', size=70, flow=.8, angle_jitter=1, psize=True)
dabs([(2392, 268, 1), (2374, 334, .7), (2352, 252, .6)], color='#ffe6b0')
B(size=8, hardness=.2, psize=False)
dabs([(280, 191), (500, 141), (2490, 71), (2260, 41)], color='#ffb060')

# ---------------- Puget Sound
sky_layers = ['Background', 'stars', 'moon_glow', 'moon', 'moon_tex', 'clouds', 'cloud_light', 'rainier', 'rainier_tex', 'rainier_haze',
              'foothills', 'city', 'smoke', 'smoke_fire', 'fires', 'fx']
use('jets')
layer('water')
select_rect(0, HZ, W, H)
gradient('linear', (0, HZ), (0, H), [(0, '#141d38'), (.25, '#0a1024'), (1, '#03050c')])
select_none()
stamp_visible('refl', sky_layers)
move('refl', above='water')
flip('v')
transform(translate=(0, 2 * HZ - (H - 1)))
motion_blur(150, 90)
exposure(-1.2)
mask(np.where(yy >= HZ, np.clip(1 - (yy - HZ) / 420, 0, 1) ** 1.4, 0))
# swell: fractal ridges laid flat on the water plane and lit from the moon's side
layer('waves', blend='overlay', opacity=.85)
clouds('#000000', '#ffffff', scale=5, octaves=6, seed=12, stretch=(.5, 6), ridged=True)
emboss(angle=100, depth=3)
perspective(FULL, [(W * .3, HZ), (W * .7, HZ), (W * 2.2, H + 200), (-W * 1.2, H + 200)])
mask((yy >= HZ).astype(np.float32))
# the moon's road, and firelight, broken on the chop
layer('glitter', blend='add')
def glints(n, y0, y1, size, centre, spread, colour, flow=.7):
    band = (yy >= y0) & (yy < y1)
    dens = np.exp(-((xx - centre) / np.maximum(spread[0] + (yy - HZ) * spread[1], 4)) ** 2) * band
    B(tip='flat', size=size, angle=90, roundness=.3, flow=flow, flow_jitter=.7, size_jitter=.5, psize=False)
    scatter(n, density=dens, color=colour)
glints(1000, HZ, 980, 10, mx, (34, .5), '#e8eeff')
glints(800, 980, 1150, 22, mx, (34, .5), '#e8eeff')
glints(420, 1150, H, 46, mx, (34, .5), '#dfe6ff')
glints(700, HZ, H, 14, 1280, (1400, 1.0), '#9fb0e0', .35)
for fx_ in (732, 1118, 1332, 620):
    glints(110, HZ, 1040, 9, fx_, (16, .16), '#ff8a40')

# ---------------- a ferry caught mid-crossing, and a destroyer on the horizon
layer('ships')
fill_poly([(246, 944), (644, 944), (622, 964), (268, 964)], color='#59627a')
fill_rect(300, 914, 590, 945, color='#4b546c')
fill_rect(318, 900, 356, 915, color='#4b546c'); fill_rect(534, 900, 572, 915, color='#4b546c')
fill_rect(428, 884, 462, 915, color='#3a4258'); fill_rect(428, 892, 462, 899, color='#2e6a4a')
fill_rect(246, 950, 644, 954, color='#2e6a4a')
B(size=3, hardness=.8, psize=False)
dabs([(x_, 924) for x_ in range(310, 586, 9)] + [(x_, 936) for x_ in range(310, 586, 9)], color='#ffe2a8')
dabs([(326, 907), (337, 907), (348, 907), (542, 907), (553, 907), (564, 907)], color='#cfe0ff')
fill_poly([(2390, 884), (2400, 874), (2440, 872), (2450, 858), (2470, 858), (2476, 870), (2540, 874), (2560, 884)], color='#0a0e1c')
layer('ship_light', blend='add')
B(size=60, hardness=0, flow=.5, psize=False)
dabs([(2396, 868)], color='#ffc070')
B(size=120, hardness=0, flow=.12, psize=False)
dabs([(445, 930)], color='#ffd9a0')
use('glitter')
glints(160, 962, 1010, 9, 445, (120, .2), '#ffd9a0', .5)
