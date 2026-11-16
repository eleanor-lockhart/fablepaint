exec(open('orca/common.py').read())
mx, my, mr = MOON
yy, xx = np.mgrid[:H, :W].astype(np.float32)
# the moon's road came out as confetti squares: thin horizontal flecks instead
use('glitter'); clear()
def glints(n, y0, y1, size, centre, spread, colour, flow=.7):
    dens = np.exp(-((xx - centre) / np.maximum(spread[0] + (yy - HZ) * spread[1], 4)) ** 2) * ((yy >= y0) & (yy < y1))
    B(size=size, hardness=.5, roundness=.14, flow=flow, flow_jitter=.7, size_jitter=.6, psize=False)
    scatter(n, density=dens, color=colour)
glints(1300, HZ, 980, 14, mx, (30, .42), '#e8eeff')
glints(1000, 980, 1150, 30, mx, (30, .42), '#e8eeff')
glints(520, 1150, H, 64, mx, (30, .42), '#dfe6ff')
glints(900, HZ, H, 22, 1280, (1400, 1.0), '#9fb0e0', .3)
for fx_ in (732, 1118, 1332, 620):
    glints(140, HZ, 1050, 12, fx_, (16, .16), '#ff8a40')
glints(180, 962, 1010, 12, 445, (120, .2), '#ffd9a0', .5)

# ================= the machine =================
use('ship_light')
layer('cable')
B(size=22, hardness=.8, spacing=.05, psize=False)
stroke([(2095, 575), (2200, 600), (2290, 720), (2330, 900), (2336, 1030)], color='#0d0a14')
layer('mech')
A, P, J = '#1a1338', '#281e56', '#0b0818'          # armour, lighter plate, joints
def part(pts, c=A, smooth=False):
    fill_poly(pts, color=c, smooth=smooth, feather=.6)
# far arm, with the knife
part([(2140, 505), (2100, 535), (2195, 665), (2235, 635)])
part([(2235, 658), (2195, 642), (2148, 768), (2182, 782)], P)
fill_ellipse(2215, 650, 30, 26, color=J)
fill_ellipse(2162, 786, 25, 23, color=J)
part([(2150, 800), (2170, 812), (2086, 938), (2074, 930)], '#ffd9a0')
# far shoulder and its pylon
part([(2100, 445), (2160, 452), (2176, 228), (2140, 220)], P)
part([(2060, 440), (2172, 455), (2162, 552), (2074, 542)])
# far leg
part([(2020, 775), (2088, 770), (2112, 922), (2050, 930)])
part([(2044, 936), (2118, 930), (2138, 1040), (2038, 1040)], P)
fill_ellipse(2080, 927, 38, 30, color=J)
# trunk
part([(1935, 738), (2097, 738), (2087, 802), (2015, 790), (1945, 802)], J)
part([(1975, 638), (2052, 638), (2072, 746), (1955, 746)])
part([(1880, 470), (2092, 455), (2112, 562), (2060, 652), (1965, 652), (1890, 582)], A)
part([(1884, 492), (1962, 482), (1978, 602), (1902, 572)], P)
part([(1905, 428), (1962, 428), (1967, 482), (1900, 482)], J)
# head: long skull, one blade of a horn, a jaw
part([(1955, 400), (1940, 436), (1870, 443), (1826, 418), (1838, 378), (1890, 352), (1945, 362)], P)
part([(1838, 420), (1882, 441), (1872, 454), (1830, 434)], J)
part([(1880, 358), (1768, 266), (1906, 345)], A)
# near leg
part([(1945, 770), (2012, 776), (1977, 932), (1915, 926)])
part([(1910, 936), (1984, 941), (2002, 1040), (1903, 1040)], P)
fill_ellipse(1946, 931, 40, 32, color=J)
# near shoulder and pylon
part([(1800, 455), (1862, 448), (1842, 213), (1808, 224)], P)
part([(1790, 455), (1902, 440), (1917, 532), (1822, 547)])
# near arm reaching for the whale
part([(1830, 500), (1887, 540), (1742, 652), (1700, 606)])
part([(1731, 607), (1699, 653), (1572, 558), (1598, 522)], P)
fill_ellipse(1715, 630, 38, 32, color=J)
fill_ellipse(1562, 527, 27, 21, angle=-35, color=J)
B(size=13, hardness=.8, spacing=.08, taper=(0, .75))
for a_, b_ in (((1548, 512), (1500, 468)), ((1542, 520), (1484, 498)), ((1540, 531), (1486, 537)), ((1546, 541), (1505, 567)), ((1572, 545), (1554, 586))):
    stroke([a_, b_], color=A, smooth=False)

# ---------------- form: moonlight from behind-left, firelight from the barrier on the right
lock(True)
B(size=170, hardness=0, flow=.13, spacing=.1, psize=False)
for pts in ([(1815, 230), (1830, 440)], [(1800, 470), (1900, 450)], [(1850, 370), (1930, 360)], [(1890, 490), (1960, 480)],
            [(1720, 600), (1600, 530)], [(1930, 790), (1920, 920)], [(1915, 950), (1915, 1030)]):
    stroke(pts, color='#5a4ab0')
for pts in ([(2160, 240), (2165, 440)], [(2160, 470), (2150, 550)], [(2230, 640), (2190, 770)], [(2100, 560), (2060, 650)], [(2110, 800), (2120, 1030)]):
    stroke(pts, color='#b04a24')
B(size=120, hardness=0, flow=.16, spacing=.1, psize=False)
for pts in ([(1990, 600), (2000, 740)], [(1990, 800), (2020, 900)], [(1960, 580), (2040, 640)], [(1760, 640), (1850, 560)]):
    stroke(pts, color='#04020a')
B(size=2.2, hardness=.6, flow=.8, psize=False, smooth=False)
for pts in ([(1902, 572), (1978, 602)], [(1890, 530), (1970, 520)], [(1975, 690), (2060, 690)], [(1925, 860), (1985, 866)],
            [(2046, 860), (2104, 856)], [(1906, 980), (1996, 986)], [(2040, 984), (2130, 980)], [(1660, 598), (1632, 622)],
            [(1820, 330), (1852, 326)], [(2150, 330), (2172, 334)]):
    stroke(pts, color='#06040e')
lock(False)
edge_light('mech', 'mech_moon', '#aebcf5', -6, -3, .9)
edge_light('mech', 'mech_fire', '#ff8a40', 7, -2, .8)
# ---------------- its own lights
layer('mech_glow', blend='add')
fill_ellipse(1856, 393, 9, 4, angle=-25, color='#b0ff70')
fill_ellipse(1878, 385, 8, 3.5, angle=-25, color='#b0ff70')
B(size=5, hardness=.5, spacing=.1, psize=False, smooth=False)
for pts in ([(1905, 500), (1955, 492)], [(1910, 530), (1962, 522)], [(1916, 560), (1968, 553)], [(1830, 440), (1826, 250)],
            [(2150, 440), (2158, 250)], [(1705, 625), (1590, 545)], [(1945, 960), (1950, 1030)], [(2082, 956), (2090, 1030)]):
    stroke(pts, color='#7dff5a')
B(size=12, hardness=.3, psize=False)
dabs([(1946, 931), (2080, 927), (1715, 630)], color='#7dff5a')
B(size=9, hardness=.3, spacing=.1, psize=False, smooth=False)
stroke([(2160, 806), (2080, 934)], color='#ff9a30')
glow(16, 1.3)
# ---------------- where it stands in the water
layer('foam')
B(tip='sponge', size=44, flow=.5, spacing=.3, angle_jitter=1, scatter=.25, size_jitter=.4, psize=False)
for cx_ in (1952, 2088, 2336):
    stroke([(cx_ - 78, 1040), (cx_ - 30, 1030), (cx_ + 30, 1030), (cx_ + 80, 1042)], color='#aebcdc')
    stroke([(cx_ - 110, 1056), (cx_, 1066), (cx_ + 112, 1058)], color='#7f8fb8', flow=.3)
layer('mech_refl', below='foam', opacity=.5)
for cx_, w_ in ((1952, 50), (2088, 50)):
    fill_poly([(cx_ - w_, 1040), (cx_ + w_, 1040), (cx_ + w_ * .8, 1300), (cx_ - w_ * .6, 1300)], color='#03040a', feather=10)
wave(5, 14, 'x')
