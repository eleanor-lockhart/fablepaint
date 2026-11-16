exec(open('paint/common.py').read())
props('aurora2', opacity=.55)
props('fringe', opacity=.35)
use('fringe')

far = [(0, 760), (90, 735), (180, 750), (260, 700), (340, 720), (430, 660), (500, 690), (590, 640), (680, 675), (770, 700),
       (860, 730), (950, 745), (1040, 770), (1130, 790), (1220, 800), (1320, 785), (1420, 760), (1500, 720), (1580, 740),
       (1660, 690), (1750, 650), (1830, 675), (1910, 630), (2000, 660), (2080, 640), (2170, 690), (2260, 670), (2350, 710),
       (2440, 700), (2560, 740)]
near = [(0, 820), (60, 780), (140, 790), (220, 720), (300, 650), (360, 590), (410, 545), (450, 560), (500, 520), (560, 575),
        (620, 610), (700, 640), (780, 700), (860, 760), (950, 820), (1050, 850), (1150, 865), (1280, 870), (1400, 860),
        (1500, 840), (1600, 800), (1700, 770), (1790, 720), (1870, 740), (1950, 690), (2030, 640), (2100, 600), (2150, 615),
        (2220, 570), (2290, 610), (2370, 650), (2450, 700), (2560, 720)]

# ---------------- far range: pale with distance, snow catching the green
layer('mtn_far')
fill_poly(far + [(W, 915), (0, 915)], color='#102c35')
turbulence(7, 30, seed=5)
lock(True)
B(tip='chalk', size=70, flow=.35, spacing=.2, angle_jitter=1, psize=False)
for i in range(1, len(far) - 1):
    x, y = far[i]
    if y < far[i - 1][1] and y < far[i + 1][1]:                      # a summit: light one flank, shade the other
        stroke([(x - 8, y + 8), (x - 60, y + 90), (x - 90, y + 190)], color='#2a6362')
        stroke([(x + 14, y + 12), (x + 60, y + 100), (x + 70, y + 200)], color='#091a22')
lock(False)
gaussian_blur(2.2)

# ---------------- near range: darker rock, snowfields, a rim of aurora along the crests
layer('mtn_near')
fill_poly(near + [(W, 915), (0, 915)], color='#08151d')
turbulence(9, 36, seed=9)
lock(True)
B(size=380, hardness=0, flow=.09, spacing=.1, psize=False)
stroke([(120, 700), (420, 600), (700, 680)], color='#1c4c4c')
stroke([(1800, 760), (2100, 660), (2500, 720)], color='#1c4c4c')
spines = [((360, 590), (300, 720), (250, 880)), ((410, 545), (400, 700), (430, 880)), ((500, 520), (540, 680), (600, 880)),
          ((500, 520), (640, 700), (760, 880)), ((300, 650), (180, 780), (120, 890)), ((620, 610), (800, 780), (900, 890)),
          ((2100, 600), (2040, 740), (1960, 890)), ((2220, 570), (2200, 720), (2230, 890)), ((2220, 570), (2340, 720), (2420, 890)),
          ((2030, 640), (1900, 780), (1800, 890)), ((1790, 720), (1700, 820), (1640, 890)), ((2370, 650), (2480, 780), (2540, 890))]
B(tip='chalk', size=58, flow=.42, spacing=.18, angle_jitter=1, psize=False, val_jitter=.15)
for a, b, c in spines:
    lit = -1 if a[0] > 1280 else 1                                   # the flank turned toward the middle of the sky
    stroke([(a[0] + lit * 10, a[1] + 14), (b[0] + lit * 26, b[1]), (c[0] + lit * 40, c[1])], color='#2f6f69')
    stroke([(a[0] - lit * 14, a[1] + 18), (b[0] - lit * 30, b[1]), (c[0] - lit * 44, c[1])], color='#03080d')
B(tip='chalk', size=26, flow=.3, angle_jitter=1, size_jitter=.6, psize=False)
scatter(700, near + [(W, 900), (0, 900)], color='#3a7a72')
scatter(900, near + [(W, 900), (0, 900)], color='#02060a')
B(size=4, hardness=.4, flow=.4, spacing=.2, psize=False, pflow=True)
stroke([(x, y + 4) for x, y in near], color='#7fe0c0', pressure=[.2, .5, .3, .6, .8, .9, 1, .6, 1, .8, .6, .5, .4, .3, .2, .1, .1, .1, .1, .2,
                                                               .3, .4, .6, .4, .7, .9, 1, .7, 1, .8, .6, .4, .3])
lock(False)
gaussian_blur(1.1)

# ---------------- cold air pooled over the lake softens the feet of the mountains
layer('haze')
gradient('linear', (0, 640), (0, 905), [(0, '#15404a', 0), (1, '#15404a', .55)])

# ---------------- far shore: two ranks of spruce
layer('treeline')
fill_rect(0, 896, W, 908, color='#050d11')
def rank(base, lo, hi, step, colour):
    xs = np.arange(-20, W + 20, step) + rng.uniform(-step * .5, step * .5, len(np.arange(-20, W + 20, step)))
    sc = rng.uniform(lo, hi, len(xs))
    dabs([(x, base - s * 20, s) for x, s in zip(xs, sc)], color=colour, tip='spruce', size=40, psize=True, flow=1, hardness=1)
B()
rank(894, .35, .75, 6, '#0a1d24')
rank(904, .55, 1.25, 9, '#040b0f')
