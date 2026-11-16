exec(open('orca/common.py').read())
# Second machine was soft and blobby, with a head lost in its shoulder. Third: hard angular plates,
# kept almost as a silhouette against the moonlit sky, the light confined to edges, eyes and chest.
for n in ('mech_moon', 'mech_fire', 'mech_glow', 'foam', 'mech_refl', 'mech'):
    delete(n)
use('cable')
layer('mech')
A, P, J = '#100c28', '#191440', '#07050f'
def part(pts, c=A):
    fill_poly(pts, color=c, feather=.5)
def limb(p0, p1, w0, w1, c=A):
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L
    part([(p0[0] + nx * w0 / 2, p0[1] + ny * w0 / 2), (p1[0] + nx * w1 / 2, p1[1] + ny * w1 / 2),
          (p1[0] - nx * w1 / 2, p1[1] - ny * w1 / 2), (p0[0] - nx * w0 / 2, p0[1] - ny * w0 / 2)], c)
def guard(x, y, r, c=J):
    part([(x - r, y), (x - r * .5, y - r * .8), (x + r * .5, y - r * .8), (x + r, y), (x + r * .5, y + r * .8), (x - r * .5, y + r * .8)], c)
# far side
part([(2168, 440), (2224, 446), (2238, 165), (2198, 155)], P)
part([(2108, 436), (2200, 440), (2246, 470), (2248, 530), (2206, 562), (2122, 550)])
limb((2190, 500), (2290, 660), 56, 48); limb((2290, 660), (2232, 800), 50, 42, P); guard(2290, 660, 32)
part([(2212, 818), (2236, 832), (2118, 968), (2104, 958)], '#ffd9a0')
guard(2230, 806, 27)
limb((2085, 810), (2135, 935), 66, 54); limb((2135, 945), (2122, 1045), 62, 90, P); guard(2135, 938, 34)
part([(2166, 930), (2200, 950), (2160, 972)], P)
# trunk
part([(1968, 775), (2112, 775), (2126, 820), (2080, 850), (2040, 825), (2000, 850), (1958, 822)], J)
part([(1995, 655), (2075, 655), (2090, 720), (2098, 780), (1978, 780), (1985, 720)])
part([(1870, 470), (1960, 455), (2110, 440), (2170, 470), (2190, 540), (2150, 610), (2080, 660), (1990, 660), (1915, 620), (1865, 560)])
part([(1876, 490), (1985, 474), (2005, 585), (1915, 585)], P)
part([(1925, 450), (1975, 440), (1990, 500), (1930, 500)], J)
part([(1985, 440), (2080, 408), (2120, 440), (2000, 470)], J)
# head
part([(1958, 392), (1968, 426), (1940, 452), (1880, 460), (1820, 452), (1778, 436), (1790, 414), (1838, 396), (1890, 376), (1940, 374)], P)
part([(1905, 458), (1890, 486), (1830, 494), (1790, 476), (1800, 460), (1850, 468)], J)
part([(1880, 380), (1690, 270), (1900, 362)])
part([(1876, 461), (1800, 447), (1806, 462), (1852, 469)], '#5a0e16')
for tx in range(1808, 1872, 9):
    part([(tx, 449 + (tx - 1808) * .17), (tx + 6, 450 + (tx - 1808) * .17), (tx + 3, 458 + (tx - 1808) * .17)], '#d0c8e0')
# near side
limb((2000, 810), (1940, 940), 70, 56); limb((1940, 950), (1962, 1045), 66, 96, P); guard(1940, 942, 36)
part([(1908, 928), (1868, 950), (1914, 974)], P)
part([(1798, 446), (1866, 440), (1850, 140), (1808, 150)], P)
part([(1768, 452), (1800, 430), (1900, 438), (1934, 470), (1928, 530), (1890, 566), (1808, 560), (1766, 520)])
limb((1835, 520), (1690, 645), 58, 50); guard(1690, 645, 36); limb((1690, 645), (1565, 545), 56, 46, P)
limb((1668, 628), (1600, 574), 78, 70)
part([(1578, 520), (1560, 560), (1524, 552), (1516, 520), (1540, 502)], J)
B(size=13, hardness=.85, spacing=.08, taper=(0, .75))
for a_, b_ in (((1528, 510), (1476, 458)), ((1520, 520), (1458, 494)), ((1518, 534), (1460, 538)), ((1526, 546), (1482, 576)), ((1556, 552), (1542, 600))):
    stroke([a_, b_], color=A, smooth=False)

# ---------------- light, kept broad and quiet: one wash from the moon's side, one from the fire's
lock(True)
gradient('linear', (1650, 150), (2150, 800), [(0, '#5a4cb0', .42), (.5, '#5a4cb0', .12), (1, '#5a4cb0', 0)])
gradient('linear', (2320, 250), (2060, 520), [(0, '#a04424', .34), (1, '#a04424', 0)])
B(size=2.2, hardness=.6, flow=.9, psize=False, smooth=False)
for pts in ([(1915, 585), (2005, 585)], [(1880, 532), (1996, 520)], [(1987, 700), (2088, 700)], [(1982, 742), (2094, 742)], [(1955, 868), (2008, 878)],
            [(2100, 866), (2150, 862)], [(1930, 990), (2000, 996)], [(2104, 992), (2166, 988)], [(1812, 300), (1856, 296)],
            [(2202, 300), (2234, 304)], [(1800, 430), (1808, 560)], [(1900, 438), (1890, 566)], [(2122, 550), (2108, 436)]):
    stroke(pts, color='#030208')
lock(False)
edge_light('mech', 'mech_moon', '#b8c6ff', -4, -3, .9, .8)
edge_light('mech', 'mech_fire', '#ff8a40', 6, 0, .22, 1.5)
layer('mech_glow', blend='add')
fill_ellipse(1836, 418, 10, 3.5, angle=-18, color='#b0ff70')
fill_ellipse(1864, 409, 9, 3.2, angle=-18, color='#b0ff70')
B(size=3.6, hardness=.5, spacing=.1, psize=False, smooth=False)
for pts in ([(1890, 508), (1978, 496)], [(1896, 534), (1986, 522)], [(1904, 560), (1994, 549)], [(1686, 640), (1580, 554)]):
    stroke(pts, color='#7dff5a')
B(size=9, hardness=.3, psize=False)
dabs([(1940, 942), (2135, 938), (1829, 158), (2218, 172)], color='#7dff5a')
B(size=8, hardness=.3, spacing=.1, psize=False, smooth=False)
stroke([(2222, 826), (2112, 962)], color='#ff9a30')
glow(14, 1.2)
# ---------------- white water where it wades, flatter and wetter than before
layer('mech_refl', opacity=.5)
for cx_ in (1962, 2122):
    fill_poly([(cx_ - 52, 1045), (cx_ + 52, 1045), (cx_ + 44, 1320), (cx_ - 34, 1320)], color='#03040a', feather=10)
wave(5, 14, 'x')
layer('foam')
for cx_ in (1962, 2122, 2404):
    fill_ellipse(cx_, 1052, 120, 16, color='#8f9fc8', opacity=.45, feather=9)
    B(tip='stipple', size=34, flow=.8, spacing=.25, angle_jitter=1, scatter=.5, size_jitter=.5, roundness=.5, psize=False)
    stroke([(cx_ - 110, 1054), (cx_ - 40, 1042), (cx_ + 40, 1042), (cx_ + 112, 1056)], color='#dfe8ff')
    stroke([(cx_ - 150, 1070), (cx_, 1080), (cx_ + 150, 1072)], color='#9fb0d8', flow=.5)
