exec(open('paint/common.py').read())
# frost sparkle belongs on the snow, not floating in front of the cabin
move('sparkle', above='snow_ridges')
props('sparkle', opacity=.25)
props('cabin_glow', opacity=.75)
use('snow'); noise(.02)
# hollows the snow leaves round each trunk
use('sparkle')
layer('wells')
for x, b, h in ((1945, 958, 120), (1990, 952, 150), (2030, 946, 190), (2290, 955, 210), (2345, 962, 170), (2400, 975, 250),
                (2460, 985, 220), (2520, 1000, 300), (2545, 1190, 520), (300, 1420, 560)):
    fill_ellipse(x, b + h * .02, h * .24, h * .04, color='#061520', opacity=.5, feather=max(4, h * .03))

# ---------------- the cabin again, with the detail it was missing
use('cabin')
fill_rect(2102, 862, 2124, 898, color='#17110d')
B(tip='chalk', size=7, flow=.6, angle_jitter=1, psize=False)
dabs([(2107, 870), (2118, 876), (2109, 884), (2119, 890), (2112, 866)], color='#2e241c')
fill_poly([(2052, 950), (2212, 950), (2236, 890), (2078, 890)], color='#3a8276')            # snow slab, top
B(size=26, hardness=0, flow=.5, spacing=.1, psize=False)
stroke([(2084, 897), (2232, 897)], color='#62b89e')
B(size=34, hardness=0, flow=.3, spacing=.1, psize=False)
stroke([(2060, 944), (2206, 944)], color='#255b58')
fill_poly([(2052, 950), (2212, 950), (2213, 961), (2053, 961)], color='#1d4a48', smooth=False)   # its front face
fill_poly([(2236, 890), (2265, 932), (2263, 944), (2233, 903)], color='#1b4544')
B(size=3, hardness=.5, flow=.9, spacing=.15, psize=False)
stroke([(2055, 962), (2211, 962)], color='#04080a')
B(size=1.8, hardness=.6, flow=.7, spacing=.2, taper=(0, .9))
for x_, l_ in ((2064, 7), (2079, 11), (2091, 6), (2118, 9), (2137, 12), (2149, 6), (2171, 10), (2188, 8), (2203, 5)):
    stroke([(x_, 961), (x_, 961 + l_)], color='#a8f0e0')                                     # icicles
fill_ellipse(2113, 862, 15, 6, color='#4a9a88')
fill_ellipse(2110, 860, 9, 3, color='#7fd0b4', feather=1.5)
B(size=3, hardness=.7, spacing=.2, psize=False)
for pts in ([(2087, 959), (2131, 959)], [(2087, 993), (2131, 993)], [(2087, 959), (2087, 993)], [(2131, 959), (2131, 993)]):
    stroke(pts, color='#2c1c0e')
fill_rect(2085, 993, 2133, 997, color='#3a8276')                                              # snow on the sill
B(size=1.5, hardness=.7, spacing=.3, psize=False)
for x_ in (2156, 2162, 2168):
    stroke([(x_, 968), (x_, 1011)], color='#1a120a')
dabs([(2170, 992)], color='#ffb040', size=2.5)
B(size=5.5, hardness=.8, psize=False)
dabs([(2068, y_ + 3) for y_ in range(948, 1010, 7)] + [(2200, y_ + 3) for y_ in range(948, 1010, 7)], color='#2e2014')
fill_rect(2146, 1011, 2178, 1016, color='#2f6f69')                                            # trodden step

# ---------------- finishing: bloom, grade, vignette, grain
use('trees_front')
stamp_visible('bloom')
levels(black=.62, white=1.0)
gaussian_blur(26)
props('bloom', blend='add', opacity=.4)
layer('vignette')
gradient('radial', (1280, 640), (1280, 2140), [(0, '#000000', 0), (.5, '#000000', 0), (1, '#000000', .6)])
layer('grain', blend='overlay', opacity=.3)
fill('#808080')
noise(.06)
adjust('grade', 'curves', points=[(0, 0), (.25, .215), (.75, .80), (1, 1)])
adjust('tone', 'balance', shadows=(-.01, 0, .03), highs=(.02, .01, -.01))
