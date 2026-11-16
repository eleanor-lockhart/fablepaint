exec(open('orca/common.py').read())
# The first machine was a stack of flat shapes with an orange outline and no clear head.
# Again: heavier build, a long skull thrust forward under the horn, jaw open, and far less rim.
for n in ('mech_moon', 'mech_fire', 'mech_glow', 'foam', 'mech_refl', 'mech', 'cable'):
    delete(n)
use('ship_light')
layer('cable')
B(size=24, hardness=.8, spacing=.05, psize=False)
stroke([(2110, 440), (2260, 470), (2370, 640), (2400, 880), (2404, 1040)], color='#0b0912')
B(size=2, hardness=.6, flow=.6, psize=False, smooth=False)
for i in range(24):
    t = i / 23
    x_ = 2110 + (2404 - 2110) * t ** .55
    stroke([(x_ - 10, 440 + 600 * t ** 1.6 - 6), (x_ + 10, 440 + 600 * t ** 1.6 + 6)], color='#2a2440')
layer('mech')
A, P, J = '#141030', '#1f1846', '#090614'
def part(pts, c=A, smooth=False):
    fill_poly(pts, color=c, smooth=smooth, feather=.6)
def limb(p0, p1, w0, w1, c=A):
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L
    part([(p0[0] + nx * w0 / 2, p0[1] + ny * w0 / 2), (p1[0] + nx * w1 / 2, p1[1] + ny * w1 / 2),
          (p1[0] - nx * w1 / 2, p1[1] - ny * w1 / 2), (p0[0] - nx * w0 / 2, p0[1] - ny * w0 / 2)], c)
def joint(x, y, r, c=J):
    fill_ellipse(x, y, r, r * .85, color=c)
# far side first
part([(2168, 440), (2222, 446), (2236, 170), (2196, 160)], P)
part([(2110, 430), (2230, 446), (2244, 520), (2200, 560), (2120, 548)], A, True)
limb((2180, 500), (2290, 660), 66, 56); limb((2290, 660), (2232, 800), 54, 46, P); joint(2290, 660, 34)
part([(2212, 818), (2236, 832), (2118, 968), (2104, 958)], '#ffd9a0')
joint(2230, 806, 28)
limb((2085, 800), (2135, 935), 84, 64); limb((2135, 945), (2122, 1045), 70, 86, P); joint(2135, 938, 36)
# trunk
part([(1975, 770), (2110, 770), (2120, 830), (2045, 815), (1970, 832)], J)
part([(1990, 650), (2075, 650), (2100, 775), (1975, 775)])
part([(1850, 455), (2130, 430), (2180, 520), (2140, 600), (2080, 662), (1985, 662), (1900, 610), (1850, 540)], A, True)
part([(1862, 480), (1990, 462), (2010, 590), (1905, 580)], P, True)
part([(1975, 420), (2090, 400), (2125, 440), (1985, 462)], J)
part([(1900, 430), (1975, 425), (1985, 480), (1905, 485)], J)
# head
part([(1975, 395), (1960, 440), (1880, 452), (1800, 436), (1788, 420), (1830, 392), (1900, 372), (1955, 372)], P, True)
part([(1900, 446), (1880, 472), (1808, 480), (1796, 464), (1850, 452)], J)
part([(1880, 452), (1802, 441), (1808, 463), (1872, 461)], '#4a0c14')
for tx in range(1812, 1876, 9):
    part([(tx, 443 + (tx - 1812) * .12), (tx + 6, 444 + (tx - 1812) * .12), (tx + 3, 452 + (tx - 1812) * .12)], '#c8c0d8')
part([(1872, 380), (1700, 292), (1905, 366)], A)
# near side
limb((2000, 800), (1935, 940), 88, 66); limb((1935, 950), (1962, 1045), 72, 90, P); joint(1935, 942, 38)
part([(1800, 440), (1862, 436), (1846, 150), (1806, 160)], P)
part([(1770, 450), (1840, 425), (1915, 440), (1930, 520), (1880, 565), (1800, 560), (1765, 510)], A, True)
limb((1835, 515), (1690, 645), 74, 62); limb((1690, 645), (1565, 545), 62, 50, P); joint(1690, 645, 38)
limb((1660, 621), (1600, 573), 74, 68)
fill_ellipse(1545, 530, 30, 24, angle=-35, color=J)
B(size=15, hardness=.8, spacing=.08, taper=(0, .7))
for a_, b_ in (((1530, 514), (1478, 462)), ((1524, 522), (1462, 496)), ((1522, 534), (1464, 538)), ((1528, 546), (1484, 574)), ((1556, 550), (1540, 596))):
    stroke([a_, b_], color=A, smooth=False)

# ---------------- light: a violet sheen where the moon reaches, ember where the barrier burns, deep shadow between
lock(True)
B(size=200, hardness=0, flow=.11, spacing=.1, psize=False)
for pts in ([(1815, 170), (1826, 430)], [(1790, 470), (1880, 440)], [(1830, 395), (1930, 378)], [(1880, 490), (1960, 475)],
            [(1700, 630), (1580, 540)], [(1975, 810), (1915, 930)], [(1915, 960), (1925, 1040)], [(1790, 330), (1880, 380)]):
    stroke(pts, color='#5848aa')
for pts in ([(2220, 180), (2222, 430)], [(2230, 470), (2210, 550)], [(2300, 650), (2250, 790)], [(2140, 950), (2150, 1040)]):
    stroke(pts, color='#9a4222')
B(size=150, hardness=0, flow=.18, spacing=.1, psize=False)
for pts in ([(2030, 620), (2040, 780)], [(2040, 820), (2060, 920)], [(1990, 600), (2090, 640)], [(1760, 640), (1850, 570)], [(1960, 500), (2080, 520)]):
    stroke(pts, color='#030208')
B(size=2.4, hardness=.6, flow=.85, psize=False, smooth=False)
for pts in ([(1905, 580), (2010, 590)], [(1870, 530), (2000, 520)], [(1990, 700), (2086, 700)], [(1988, 738), (2094, 738)], [(1950, 868), (2010, 876)],
            [(2096, 866), (2152, 860)], [(1928, 990), (2000, 996)], [(2100, 992), (2168, 988)], [(1812, 300), (1850, 296)],
            [(2200, 300), (2232, 304)], [(1840, 425), (1930, 520)], [(1600, 573), (1570, 596)]):
    stroke(pts, color='#04030a')
lock(False)
edge_light('mech', 'mech_moon', '#aebcf5', -5, -3, .75)
edge_light('mech', 'mech_fire', '#ff8a40', 6, -1, .32)
layer('mech_glow', blend='add')
fill_ellipse(1840, 411, 10, 4, angle=-20, color='#b0ff70')
fill_ellipse(1868, 402, 9, 3.5, angle=-20, color='#b0ff70')
B(size=5, hardness=.5, spacing=.1, psize=False, smooth=False)
for pts in ([(1880, 500), (1975, 487)], [(1888, 530), (1984, 518)], [(1896, 560), (1992, 549)], [(1690, 640), (1580, 552)]):
    stroke(pts, color='#7dff5a')
B(size=11, hardness=.3, psize=False)
dabs([(1935, 942), (2135, 938), (1826, 170), (2216, 178)], color='#7dff5a')
B(size=9, hardness=.3, spacing=.1, psize=False, smooth=False)
stroke([(2222, 826), (2112, 962)], color='#ff9a30')
glow(16, 1.3)
# ---------------- water round its legs
layer('mech_refl', opacity=.5)
for cx_ in (1962, 2122):
    fill_poly([(cx_ - 52, 1045), (cx_ + 52, 1045), (cx_ + 44, 1320), (cx_ - 34, 1320)], color='#03040a', feather=10)
wave(5, 14, 'x')
layer('foam')
B(tip='sponge', size=46, flow=.5, spacing=.3, angle_jitter=1, scatter=.25, size_jitter=.4, psize=False)
for cx_ in (1962, 2122, 2404):
    stroke([(cx_ - 84, 1046), (cx_ - 30, 1036), (cx_ + 30, 1036), (cx_ + 86, 1048)], color='#aebcdc')
    stroke([(cx_ - 120, 1062), (cx_, 1072), (cx_ + 122, 1064)], color='#7f8fb8', flow=.3)
