exec(open('paint/common.py').read())
# ---------------- corrections first
use('refl'); exposure(.6)                      # the ice was swallowing the sky
props('cracks', opacity=.28)
props('ice_snow', opacity=.6)
use('shore'); gaussian_blur(2.5); props('shore', opacity=.45)
props('sparkle', opacity=.3)
# the snow read as fog: smoother dunes, plus fine wind ridges, both laid in perspective
use('snow_relief'); clear()
clouds('#000000', '#ffffff', scale=2.2, octaves=3, seed=83)
emboss(angle=115, depth=9)
perspective(FULL, [(2560 * .1, 905), (2560 * .9, 905), (2560 * 1.5, 1500), (-2560 * .5, 1500)])
gaussian_blur(4)
props('snow_relief', opacity=.7)
layer('snow_ridges', blend='overlay', clip=True, opacity=.4)
clouds('#3a3a3a', '#c0c0c0', scale=2, octaves=6, seed=84, stretch=(.25, 10))
perspective(FULL, [(2560 * .1, 905), (2560 * .9, 905), (2560 * 1.5, 1500), (-2560 * .5, 1500)])

# ---------------- spruce, built bough by bough with snow lying on each
def spruce(x, base, h, seed, snow=True):
    r = np.random.default_rng(seed)
    dark = mix('#03090c', '#07141a', r.random())
    n = int(10 + h / 16)
    B(size=max(2.5, h * .022), hardness=.7, spacing=.15, taper=(0, .9))
    stroke([(x, base), (x + r.uniform(-.01, .01) * h, base - h)], color='#040605')
    for i in range(n):
        t = (i + .5) / n
        y = base - h * (1 - t) * .97 - h * .03
        reach = h * (.035 + .25 * t ** .9) * r.uniform(.8, 1.12)
        thick = max(2.0, h * (.012 + .028 * t))
        for side in (-1, 1):
            L = reach * r.uniform(.8, 1.05)
            droop = L * r.uniform(.25, .5)
            p0, p1, p2 = (x, y - thick * .3), (x + side * L * .55, y + droop * .3), (x + side * L, y + droop)
            B(tip='chalk', size=thick * 2.2, flow=.95, spacing=.12, angle_jitter=1, taper=(0, .7))
            stroke([p0, p1, p2], color=dark)
            if snow:
                B(size=thick * 1.25, hardness=.4, flow=.75, spacing=.12, taper=(.05, .6))
                lit = '#3c7f76' if side * (x - 1280) < 0 else '#27595a'
                stroke([(p0[0] + side * thick * .5, p0[1] - thick * .45), (p1[0], p1[1] - thick * .5),
                        (p2[0] - side * L * .12, p2[1] - thick * .45)], color=lit)

layer('trees_back')
for x, b, h, sd in ((1945, 958, 120, 1), (1990, 952, 150, 2), (2030, 946, 190, 3), (2290, 955, 210, 4), (2345, 962, 170, 5),
                    (2400, 975, 250, 6), (2460, 985, 220, 7), (2520, 1000, 300, 8)):
    spruce(x, b, h, sd)

# ---------------- the cabin
layer('cabin')
fill_poly([(2200, 946), (2252, 932), (2252, 1000), (2200, 1012)], color='#0d0906')
fill_poly([(2200, 946), (2226, 896), (2252, 932)], color='#0f0b07')
fill_poly([(2068, 946), (2200, 946), (2200, 1012), (2068, 1012)], color='#1a120b')
B(size=2, hardness=.6, flow=.5, spacing=.3, psize=False)
for y in range(951, 1012, 7):
    stroke([(2068, y), (2200, y)], color='#2c1f13')
    stroke([(2200, y), (2252, y - 13)], color='#1c140c')
fill_rect(2150, 966, 2174, 1012, color='#080504')
fill_rect(2087, 959, 2131, 993, color='#2a1c10')
fill_rect(2104, 866, 2122, 898, color='#120d0a')
# snow on the roof: a thick slab, lit on top, shadowed under the eave
fill_poly([(2054, 954), (2210, 954), (2234, 892), (2080, 892)], color='#2f6f69')
fill_poly([(2234, 892), (2262, 932), (2258, 940), (2228, 904)], color='#1f4d4c')
B(size=30, hardness=0, flow=.3, spacing=.1, psize=False)
stroke([(2085, 900), (2230, 900)], color='#4a9a88')
B(size=5, hardness=.3, flow=.8, spacing=.1, psize=False)
stroke([(2054, 955), (2210, 955)], color='#060b0d')
fill_ellipse(2113, 866, 13, 5, color='#3a7f76')
# lit windows
fill_rect(2090, 962, 2128, 990, color='#ff9d2e')
fill_rect(2095, 966, 2123, 986, color='#ffe6a8', feather=3)
B(size=2.4, hardness=.7, spacing=.3, psize=False)
stroke([(2109, 962), (2109, 990)], color='#2a1808')
stroke([(2090, 976), (2128, 976)], color='#2a1808')
fill_poly([(2216, 956), (2238, 950), (2238, 972), (2216, 978)], color='#ffab3c')
layer('cabin_glow', blend='add')
B(size=150, hardness=0, flow=.22, psize=False)
dabs([(2109, 976)], color='#ff8a2a')
B(size=70, hardness=0, flow=.2, psize=False)
dabs([(2227, 964)], color='#ff8a2a')
fill_ellipse(2112, 1032, 80, 15, color='#ff8a2a', opacity=.34, feather=12)
fill_ellipse(2266, 1004, 40, 8, color='#ff8a2a', opacity=.22, feather=8)
# chimney smoke, lit from above, leaning with the air
layer('smoke', opacity=.55)
B(tip='cloud', size=90, flow=.10, spacing=.1, angle_jitter=1, psize=True)
stroke([(2113, 858, .25), (2106, 822, .4), (2086, 782, .6), (2050, 744, .85), (2000, 708, 1.0)], color='#5a8f88')
gaussian_blur(5)

# ---------------- tracks from the door to the shore
layer('tracks')
path_ = path([(2162, 1018), (2120, 1052), (2040, 1087), (1940, 1132), (1820, 1178), (1700, 1212), (1585, 1236)])
d = np.concatenate([[0], np.cumsum(np.hypot(np.diff(path_[:, 0]), np.diff(path_[:, 1])))])
s, k = 0.0, 0
while s < d[-1]:
    x, y = np.interp(s, d, path_[:, 0]), np.interp(s, d, path_[:, 1])
    dz = y - 905
    off = (1 if k % 2 else -1) * dz * .022
    fill_ellipse(x + off, y, dz * .034, dz * .014, color='#050d13', opacity=.75, feather=.8)
    fill_ellipse(x + off, y + dz * .012, dz * .034, dz * .008, color='#4a9a8a', opacity=.3, feather=.8)
    s += dz * .15
    k += 1

# ---------------- someone has come down to the ice to look up, and brought the dog
layer('figure')
x, y = 1560, 1236
ink = '#04070a'
fill_ellipse(x - 30, y + 2, 60, 6, color='#040b10', opacity=.5, feather=4)
fill_poly([(x - 14, y - 60), (x - 2, y - 60), (x - 4, y), (x - 15, y)], color=ink)
fill_poly([(x + 2, y - 60), (x + 14, y - 60), (x + 15, y), (x + 4, y)], color=ink)
fill_ellipse(x - 10, y, 9, 4, color=ink); fill_ellipse(x + 10, y, 9, 4, color=ink)
fill_poly([(x - 22, y - 58), (x - 25, y - 96), (x - 15, y - 109), (x + 15, y - 109), (x + 25, y - 96), (x + 22, y - 58)], color=ink, smooth=True)
fill_poly([(x - 21, y - 102), (x - 32, y - 72), (x - 28, y - 56), (x - 20, y - 62)], color=ink, smooth=True)
fill_poly([(x + 21, y - 102), (x + 32, y - 72), (x + 28, y - 56), (x + 20, y - 62)], color=ink, smooth=True)
fill_ellipse(x, y - 116, 12, 13, color=ink)
dx = x - 62
fill_poly([(dx - 12, y), (dx - 13, y - 22), (dx - 6, y - 35), (dx + 5, y - 39), (dx + 11, y - 30), (dx + 12, y - 12), (dx + 15, y)], color=ink, smooth=True)
fill_ellipse(dx + 5, y - 44, 8, 7, color=ink)
fill_poly([(dx + 8, y - 48), (dx + 20, y - 54), (dx + 12, y - 40)], color=ink)
fill_poly([(dx - 2, y - 48), (dx + 1, y - 58), (dx + 5, y - 49)], color=ink)
B(size=4, hardness=.6, spacing=.15, taper=(0, .6))
stroke([(dx - 12, y - 4), (dx - 24, y - 2), (dx - 30, y - 10)], color=ink)
# the sky on their edges
B(size=2.6, hardness=.4, flow=.6, spacing=.15, taper=(.2, .3))
for pts in ([(x - 10, y - 125), (x, y - 129), (x + 10, y - 125)], [(x - 16, y - 108), (x - 25, y - 96), (x - 31, y - 74)],
            [(x + 16, y - 108), (x + 25, y - 96), (x + 31, y - 74)], [(dx - 4, y - 36), (dx + 4, y - 51), (dx + 18, y - 54)],
            [(dx - 13, y - 22), (dx - 7, y - 35)]):
    stroke(pts, color='#5fd0a8')

# ---------------- foreground trees frame the left and right edges
layer('trees_front')
spruce(2545, 1190, 520, 21)
spruce(300, 1420, 560, 22)
spruce(70, 1500, 940, 23)
