exec(open('orca/common.py').read())
props('mech_fire', opacity=.4)
use('foam')
# ================= the whale: a spine with a half-girth at each station =================
ax = np.array([(430, 1210, 30), (560, 1105, 62), (700, 1000, 95), (850, 890, 118), (1000, 785, 128), (1140, 690, 122),
               (1270, 610, 108), (1380, 548, 88), (1450, 512, 60), (1492, 494, 6)], float)
T = np.gradient(ax[:, :2], axis=0)
T /= np.linalg.norm(T, axis=1)[:, None]
N = np.stack([T[:, 1], -T[:, 0]], 1)                       # points to the back (dorsal) side
def at(i, f):                                              # a point at station i, f half-girths toward the back
    return tuple(ax[i, :2] + N[i] * ax[i, 2] * f)
black, white = '#07090e', '#c9d2e6'
layer('orca')
fill_poly([(430, 1210), (380, 1150), (300, 1120), (250, 1140), (330, 1200), (380, 1260), (360, 1330), (430, 1330), (470, 1260)], color=black, smooth=True)
fill_poly([at(i, 1) for i in range(10)] + [at(i, -1) for i in range(9, -1, -1)], color=black, smooth=True)
fill_poly([(925, 683), (840, 640), (740, 585), (680, 552), (700, 610), (745, 700), (800, 782)], color=black, smooth=True)      # dorsal fin
# white: chin and throat running back along the belly; the eye patch; the grey saddle
layer('orca_white', clip=True)
fill_poly([at(i, -1.05) for i in range(9, 2, -1)] + [at(i, -.42) for i in range(3, 10)], color=white, smooth=True, feather=1.5)
fill_ellipse(1345, 512, 48, 18, angle=-30, color=white, feather=1.2)
fill_ellipse(664, 952, 72, 20, angle=-37, color='#4a525e', feather=6)
lock(True)                                                 # the white is in shadow low down, and picks up fire
B(size=150, hardness=0, flow=.16, spacing=.1, psize=False)
stroke([at(i, -.95) for i in range(3, 9)], color='#56607c')
stroke([at(i, -1.0) for i in range(4, 8)], color='#c07a50', flow=.10)
lock(False)
# the mouth
layer('mouth')
fill_poly([(1398, 586), (1492, 498), (1512, 556)], color='#4a0d18')
fill_ellipse(1456, 556, 34, 12, angle=-28, color='#b04a62', feather=2)
fill_poly([(1398, 586), (1512, 554), (1518, 582), (1474, 626), (1426, 632)], color=white, smooth=True)
for i in range(8):                                         # teeth: cones, upper row then lower
    t = .12 + i * .105
    x_, y_ = 1398 + (1492 - 1398) * t, 586 + (498 - 586) * t
    fill_poly([(x_ - 4, y_ + 4), (x_ + 4, y_ - 4), (x_ + 7, y_ + 9)], color='#f4f0e4')
    x_, y_ = 1398 + (1512 - 1398) * t, 586 + (554 - 586) * t
    fill_poly([(x_ - 5, y_ + 1), (x_ + 5, y_ - 2), (x_ - 2, y_ - 11)], color='#f4f0e4')
fill_ellipse(1404, 554, 4.5, 3.5, color='#020308')
fill_ellipse(1403, 553, 1.3, 1.1, color='#dfe8ff')
# pectoral flipper, on the near side
layer('flipper')
fill_poly([(1290, 730), (1360, 800), (1400, 890), (1380, 960), (1320, 985), (1260, 940), (1225, 860), (1212, 790)], color=black, smooth=True)
# wet skin: one long soft reflection of the sky down the flank, a hard broken glint inside it, firelight underneath
for base in ('orca', 'flipper'):
    edge_light(base, base + '_rim', '#c8d6ff', -3, -5, .8, 1.0)
use('orca_white')
layer('orca_gloss', blend='add', clip=True)
B(size=70, hardness=0, flow=.10, spacing=.08, psize=False)
stroke([at(i, .5) for i in range(1, 9)], color='#8fa4d8')
B(size=14, hardness=.2, flow=.3, spacing=.1, psize=True)
stroke([at(i, .55) for i in range(2, 9)], color='#e6eeff', pressure=[.2, 1, .3, .9, .5, 1, .4])
B(size=60, hardness=0, flow=.08, spacing=.08, psize=False)
stroke([at(i, -.7) for i in range(2, 8)], color='#ff8a40')
stroke([(705, 600), (760, 690)], color='#8fa4d8', flow=.14)
use('flipper_rim')
layer('flip_gloss', blend='add', clip=True)
B(size=50, hardness=0, flow=.12, psize=False)
stroke([(1260, 800), (1330, 880), (1350, 950)], color='#8fa4d8')

# ================= water =================
# sheets and strings of it falling back off the animal
layer('runoff')
B(size=3, hardness=.5, flow=.6, spacing=.2, taper=(0, .8), psize=True)
for i in range(1, 9):
    for k in range(7):
        x_, y_ = at(i, -1.0)
        x_ += rng.uniform(-60, 60); y_ += rng.uniform(-6, 10)
        L_ = rng.uniform(40, 170)
        stroke([(x_, y_), (x_ - L_ * .22, y_ + L_ * .6), (x_ - L_ * .5, y_ + L_)], color='#b8c8f0', size=rng.uniform(2, 5))
for x_, y_ in ((1380, 962), (1320, 986), (1262, 942), (690, 556), (330, 1200), (250, 1142)):
    for k in range(5):
        L_ = rng.uniform(40, 150)
        stroke([(x_ + rng.uniform(-14, 14), y_), (x_ - L_ * .25, y_ + L_)], color='#b8c8f0', size=rng.uniform(2, 4))
B(size=5, hardness=.6, flow=.8, flow_jitter=.6, size_jitter=.6, psize=False)
scatter(520, [(300, 1150), (1300, 720), (1420, 1000), (900, 1250), (500, 1330)], color='#cfdcff')
# the breach itself: light from the plankton underneath, then white water thrown outward
layer('biolum', blend='add')
B(size=420, hardness=0, flow=.22, psize=True)
dabs([(430, 1300, 1), (560, 1340, .7), (300, 1330, .6)], color='#18c8b0')
B(size=3, hardness=.6, flow=.9, flow_jitter=.6, size_jitter=.6, psize=False)
scatter(900, (120, 1180, 820, 1440), color='#70fff0')
layer('splash')
fill_ellipse(440, 1330, 330, 60, color='#9fb4dc', opacity=.5, feather=22)
for ang in np.linspace(200, 340, 26):
    L_ = rng.uniform(140, 360)
    c_, s_ = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    p0 = (430 + c_ * 40, 1290 + s_ * 20)
    p1 = (430 + c_ * L_ * .6, 1290 + s_ * L_ * .75)
    p2 = (430 + c_ * L_, 1290 + s_ * L_ * .8 + L_ * .18)
    B(tip='splatter', size=rng.uniform(40, 90), flow=.75, spacing=.3, follow=True, size_jitter=.4, scatter=.25, taper=(0, .6))
    stroke([p0, p1, p2], color='#dbe6ff')
    B(tip='stipple', size=rng.uniform(50, 110), flow=.6, spacing=.3, angle_jitter=1, scatter=.4, taper=(0, .5))
    stroke([p0, p1, p2], color='#eef3ff')
B(tip='cloud', size=200, flow=.10, spacing=.2, angle_jitter=1, psize=False)
stroke([(240, 1260), (430, 1180), (640, 1250)], color='#aebcdc')
