exec(open('paint/common.py').read())
# the snow on the peaks should take the colour of the light falling on it
for n in ('mtn_far', 'mtn_near'):
    use(n + '_relief')
    layer(n + '_light', blend='soft_light', opacity=.5, clip=True)
    gradient('linear', (0, 480), (0, 900), [(0, '#3dffa0', .9), (1, '#3dffa0', .15)])

# ---------------- frozen lake: everything above the shore, mirrored, dragged and dimmed
use('treeline')
stamp_visible('refl')
flip('v')
transform(translate=(0, 2 * 905 - (H - 1)))
motion_blur(70, 90)
gaussian_blur(3)
exposure(-1.1)
desaturate(.15)
select_poly(LAKE, feather=1.2, smooth=False)
mask('selection')
select_none()
# black ice near the eye reflects less of the sky
layer('ice_dark')
select_poly(LAKE, feather=1.2)
gradient('linear', (0, 905), (0, 1200), [(0, '#02080c', 0), (1, '#02080c', .45)])
select_none()

# wind-packed snow lying on the ice: a noise texture laid down in perspective
layer('ice_snow')
fill('#27605c')
n = noise_field(5, 5, 71)
streak = noise_field(3, 5, 72, stretch=(.35, 7))
modulate(np.clip((n - .52) * 5, 0, 1) * .6 + np.clip((streak - .6) * 4, 0, 1) * .35)
perspective(FULL, GROUND)
select_poly(LAKE, feather=1.2)
mask('selection')
select_none()
gaussian_blur(1.0)
# pressure cracks
layer('cracks', opacity=.7)
B(size=2.2, hardness=.5, flow=.3, spacing=.2, psize=True, taper=(.2, .3))
for pts in ([(120, 1010), (480, 1000), (900, 1022), (1350, 1010)], [(300, 1090), (760, 1070), (1180, 1100)],
            [(900, 960), (1300, 950), (1740, 962)], [(40, 950), (360, 946), (640, 955)], [(1180, 1100), (1420, 1140), (1600, 1128)],
            [(480, 1000), (560, 1040), (540, 1085)], [(1350, 1010), (1500, 1040), (1720, 1030)], [(760, 1070), (700, 1120)],
            [(1300, 950), (1340, 985), (1350, 1010)], [(1500, 930), (1820, 928)], [(200, 925), (700, 922), (1100, 928)]):
    stroke(pts, color='#a8f0e0')
gaussian_blur(.7)

# ---------------- the land: snow, drifted
layer('snow')
fill_poly(LAND, color='#12333a', feather=1.5)
lock(True)
B(size=520, hardness=0, flow=.10, spacing=.1, psize=False)
for pts in ([(900, 1260), (1500, 1250), (2100, 1150), (2560, 1090)], [(300, 1330), (1000, 1380), (1700, 1340)],
            [(2000, 1010), (2300, 985), (2560, 990)], [(1900, 1210), (2300, 1260), (2600, 1300)]):
    stroke(pts, color='#2f7a6c')
for pts in ([(-50, 1440), (400, 1450), (900, 1470)], [(1700, 1460), (2200, 1440), (2600, 1450)], [(1500, 1300), (1900, 1290), (2200, 1210)]):
    stroke(pts, color='#06121c')
lock(False)
layer('snow_relief', blend='overlay', clip=True, opacity=.85)
clouds('#000000', '#ffffff', scale=3.2, octaves=6, seed=81)
emboss(angle=115, depth=5)
perspective(FULL, [(2560 * .1, 905), (2560 * .9, 905), (2560 * 1.5, 1500), (-2560 * .5, 1500)])
gaussian_blur(1.5)
# frost sparkle
layer('sparkle', blend='add', opacity=.8)
m, x0, y0 = None, 0, 0
B(size=1.8, hardness=.8, flow=.8, flow_jitter=.8, size_jitter=.5, psize=False)
scatter(1400, LAND, color='#c8fff0')
# the lip where snow meets ice
layer('shore')
B(size=7, hardness=.2, flow=.5, spacing=.1, psize=False)
edge = [(0, 1140), (700, 1180), (1300, 1195), (1700, 1130), (1900, 1050), (1960, 980), (1930, 930), (1880, 905)]
stroke([(x, y - 3) for x, y in edge], color='#02090d')
B(size=5, hardness=.2, flow=.45, spacing=.1, psize=False)
stroke([(x, y + 3) for x, y in edge], color='#3f8f80')
