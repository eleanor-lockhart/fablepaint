exec(open('../atelier/transfer/t1/common.py').read())
window(X0, Y0, X1, Y1)
def pxm(s, off=0.0):                      # screen pixels per metre across the track at that place
    a, b = T(s, off - .5), T(s, off + .5)
    return math.hypot(b[0] - a[0], b[1] - a[1])

# ---- ballast: angular stones, clustered in the cribs, along the shoulders and close to us; the walkway stays quiet
block('ballast')
lightc, darkc = [], []
def stone(s, off, big=1.0):
    k = float(np.clip(.045 * pxm(s, off) * big, 1.1, 4.2)) * rng.uniform(.7, 1.2)
    x, y = T(s, off, -.2)
    (lightc if rng.uniform() < .55 else darkc).append(chip(x, y, k))
for s in np.arange(7.5, 34, .5):          # cribs between the ties
    for _ in range(int(max(2, 15 - s * .42))):
        stone(s + .25 + rng.normal(0, .07), rng.uniform(-1.55, 1.55))
for _ in range(900):                      # the two edges of the bed, thinning with distance
    s = 7 + 60 * rng.uniform() ** 2.2
    stone(s, rng.choice([rng.uniform(3.1, 4.15), rng.uniform(toe_off(s) - .1, -2.3)]))
for _ in range(260):                      # a few loose ones on the walkways
    s = 7 + 30 * rng.uniform() ** 2.0
    stone(s, rng.choice([rng.uniform(1.6, 3.1), rng.uniform(-2.3, -1.6)]))
marks(lightc, '#8b928d'); marks(darkc, '#454740')

# ---- ties: no two alike, fading into the ballast with distance
block('ties')
bins = {}
for i, s in enumerate(np.arange(7.5, 62, .5)):
    s = s + rng.normal(0, .03)
    la, lb = -1.3 + rng.normal(0, .06), 1.3 + rng.normal(0, .06)
    hw = .11 * rng.uniform(.85, 1.12)
    ska, skb = rng.normal(0, .035), rng.normal(0, .035)
    r_ = rng.uniform()
    if r_ < .10: la = rng.uniform(-.5, .2)                 # one end under the ballast
    elif r_ < .18: lb = rng.uniform(-.2, .5)
    q = np.array([T(s - hw + ska, la, -.17), T(s - hw + skb, lb, -.17), T(s + hw + skb, lb, -.17), T(s + hw + ska, la, -.17)])
    if s < 24: q = wobble(q, .7, 26)
    bins.setdefault((min(int((s - 7.5) / 9), 5), int(rng.uniform() < .4)), []).append(q)
tones = [('#262320', '#35302b'), ('#2c2926', '#3a3631'), ('#373531', '#44423d'), ('#474742', '#514f4a'), ('#585953', '#5e5f59'), ('#676963', '#6b6e68')]
for (b_, alt), polys in sorted(bins.items()):
    marks(polys, tones[b_][alt])
# checks along the grain of the nearest ties
chk = []
for s in np.arange(7.5, 17, .5):
    for _ in range(int(rng.integers(1, 4))):
        a = rng.uniform(-1.2, .6); ds = rng.uniform(-.07, .07)
        chk.append(ribbon([T(s + ds, a, -.17), T(s + ds + rng.normal(0, .01), a + rng.uniform(.3, 1.1), -.17)], w=rng.uniform(.9, 1.8), taper=(.3, .5), wob=.2, smooth=False))
marks(chk, '#4a4640')

# ---- rails: the web is key block; the head is wet steel carrying the sky, paler with distance
ss = np.r_[np.arange(6.0, 40, .5), np.arange(40, 170, 2.0)]
block('railweb')
marks([strip([T(s, r - .036, 0) for s in ss], [T(s, r - .085, -.17) for s in ss], 1.0) for r in (-GAUGE, GAUGE)], KEY)
block('rails')
marks([strip([T(s, r - .036, 0) for s in ss], [T(s, r + .036, 0) for s in ss], 1.3) for r in (-GAUGE, GAUGE)], PALE)
lock(True); gradient('linear', T(58), T(9), ramp(PALE, ('#a3afad', .4), ('#8497a0', .75), '#6c8089')); lock(False)

# ---- rock at the edge of the fill, water side: dark lumps with one wet plane each
block('riprap')
rock, wet = [], []
s = 19.0
while s < 150:
    k = float(np.clip(.55 * pxm(s, SHOULDER) * rng.uniform(.5, 1.1), 2.0, 30))
    x, y = T(s, SHOULDER + rng.uniform(-.25, .5), -.3)
    n = int(rng.integers(5, 8)); a = np.sort(rng.uniform(0, 6.283, n)); r = k * rng.uniform(.55, 1.0, n)
    q = np.c_[x + r * np.cos(a), y + r * np.sin(a) * .6]
    rock.append(q)
    if k > 7 and rng.uniform() < .6:
        top = q[q[:, 1] < y + k * .05]
        if len(top) >= 2:
            wet.append(np.r_[top, [(x + k * .3, y + k * .12), (x - k * .35, y + k * .1)]])
    s += max(.25, k / pxm(s, SHOULDER) * rng.uniform(.9, 2.6))
marks(rock, EARTH); marks(wet, '#4c5553')
print('rail L at 15:', [round(v) for v in T(15, -GAUGE)], 'px/m at 15:', round(pxm(15, -2)), ' at 40:', round(pxm(40, 3.3)))
