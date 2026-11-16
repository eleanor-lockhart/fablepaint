exec(open('orca/common.py').read())
# the firelight had turned the whale's white to salmon and striped its flank orange; the flipper read as a tyre
use('orca_white'); desaturate(.8)
use('orca_gloss'); colorize('#9fb0e0', .85)
props('flipper_rim', opacity=.35); props('flip_gloss', opacity=.5)

# ---------------- the rest of the pod, working the machine like a seal on a floe
use('foam')
layer('pod')
def fin(x, y, h, lean=1):
    fill_ellipse(x, y + 4, h * .9, h * .12, color='#06080d', feather=1.5)
    fill_poly([(x - h * .34, y), (x - h * .12, y - h * .5), (x + h * .14 * lean, y - h), (x + h * .2, y - h * .45), (x + h * .36, y)], color='#06080d', smooth=True)
    B(size=2.2, hardness=.4, flow=.5, spacing=.2, taper=(.2, .3))
    stroke([(x - h * .13, y - h * .5), (x + h * .12 * lean, y - h * .97)], color='#b8c8f0')
    B(tip='stipple', size=h * .5, flow=.6, spacing=.3, angle_jitter=1, scatter=.4, roundness=.4, psize=False)
    stroke([(x - h * 1.1, y + 8), (x, y + 12), (x + h * 1.1, y + 8)], color='#c8d6f4')
for x, y, h in ((1180, 1128, 74), (1640, 1082, 58), (860, 1052, 40), (2250, 1124, 66)):
    fin(x, y, h)
# one of them has found the power cable
fill_poly([(2326, 1052), (2352, 1004), (2404, 984), (2442, 1006), (2438, 1052)], color='#06080d', smooth=True)
fill_ellipse(2392, 1008, 17, 6, angle=-20, color='#c9d2e6')
layer('sparks', blend='add')
B(tip='splatter', size=90, flow=.9, angle_jitter=1, size_jitter=.4, psize=False)
dabs([(2408, 1000), (2420, 990)], color='#ffe9a0')
B(size=150, hardness=0, flow=.35, psize=False)
dabs([(2410, 1000)], color='#ffb040')
B(size=2.2, hardness=.6, flow=.9, taper=(0, .8))
for a_ in np.linspace(180, 360, 14):
    L_ = rng.uniform(40, 120)
    stroke([(2410, 1000), (2410 + math.cos(math.radians(a_)) * L_, 1000 + math.sin(math.radians(a_)) * L_ + L_ * L_ * .002)], color='#fff0c0', smooth=False)

# ---------------- a channel buoy in the foreground, with a harbor seal that wants no part of this
use('splash')
layer('buoy')
fill_ellipse(2330, 1268, 70, 10, color='#03050a', opacity=.6, feather=5)
fill_poly([(2284, 1264), (2376, 1264), (2366, 1212), (2294, 1212)], color='#7a1418')
fill_poly([(2284, 1264), (2376, 1264), (2374, 1250), (2286, 1250)], color='#3a0a0c')
fill_rect(2294, 1212, 2366, 1220, color='#a8242a')
B(size=5, hardness=.8, psize=False, smooth=False)
for a_, b_ in (((2302, 1212), (2326, 1112)), ((2358, 1212), (2334, 1112)), ((2310, 1180), (2350, 1180)), ((2318, 1146), (2342, 1146)), ((2304, 1210), (2348, 1150)), ((2356, 1210), (2312, 1150))):
    stroke([a_, b_], color='#5a1014')
fill_rect(2322, 1098, 2338, 1114, color='#20242c')
fill_poly([(2258, 1220), (2274, 1198), (2312, 1190), (2340, 1204), (2334, 1220), (2292, 1226)], color='#262a33', smooth=True)
fill_ellipse(2264, 1200, 12, 10, color='#262a33')
B(size=5, hardness=.3, flow=.5, angle_jitter=1, psize=False)
scatter(26, [(2270, 1200), (2330, 1196), (2332, 1218), (2276, 1220)], color='#4a505c')
fill_ellipse(2259, 1198, 2.2, 2.2, color='#05060a'); fill_ellipse(2258.5, 1197.4, .8, .8, color='#dfe8ff')
edge_light('buoy', 'buoy_rim', '#b8c6ff', -3, -4, .6, .9)
layer('buoy_light', blend='add')
B(size=9, hardness=.4, psize=False); dabs([(2330, 1106)], color='#80ff90')
B(size=120, hardness=0, flow=.3, psize=False); dabs([(2330, 1106)], color='#30d060')

# ---------------- air between here and the city, then the finish
use('ship_light')
layer('haze', opacity=.6)
B(size=120, hardness=0, flow=.06, spacing=.1, psize=False)
for y_ in (868, 884, 900):
    stroke([(-50, y_), (800, y_ + 4), (1700, y_ - 4), (2600, y_)], color='#3c4870')
gaussian_blur(16)
use('buoy_light')
stamp_visible('bloom')
levels(black=.68, white=1.0)
gaussian_blur(22)
props('bloom', blend='add', opacity=.38)
layer('vignette')
c = '#000000'
gradient('radial', (1280, 660), (1280, 2200), [(0, c, 0), (.45, c, 0), (.6, c, .06), (.75, c, .2), (.9, c, .42), (1, c, .6)])
layer('grain', blend='overlay', opacity=.22)
fill('#808080')
noise(.06)
adjust('grade', 'curves', points=[(0, 0), (.25, .22), (.75, .79), (1, 1)])
adjust('tone', 'balance', shadows=(-.01, 0, .03), highs=(.02, .01, -.02))
