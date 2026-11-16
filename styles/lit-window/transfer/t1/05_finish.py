exec(open('../styles/lit-window/transfer/t1/common.py').read())
exec(open('../styles/lit-window/transfer/t1/coyote.py').read())
window(X0, Y0, X1, Y1)

# ---- the red lands on wet steel and wet wood. Not a glow: dashes, longest where the reflection falls
# (worked out from the lamp, the eye and each rail: about 18 m short of the mast), breaking up toward us.
block('redlight', above='rails')
hot, cool = [], []
def dash(r, sa, sb):
    ss_ = np.linspace(sa, sb, max(3, int(abs(sb - sa) / .4) + 2))
    return strip([T(s, r - .036, 0) for s in ss_], [T(s, r + .036, 0) for s in ss_], 1.8)
for r, c, far_end, near_end in ((-GAUGE, 21.5, 29.5, 15.6), (GAUGE, 24.5, 32.5, 17.6)):
    s = far_end
    while s > near_end:
        u = abs(s - c) / (far_end - c if s > c else c - near_end)          # 0 at the centre of the streak, 1 at its ends
        ln = (3.4 - 2.8 * u) * rng.uniform(.6, 1.2)
        gap = (.15 + 1.5 * u ** 1.5 * (1.4 if s < c else .8)) * rng.uniform(.7, 1.3)
        (hot if u < .5 else cool).append(dash(r, s, max(s - ln, near_end)))
        s -= ln + gap
# wet tie tops under the lamp carry a little of it
col_x = P(3.06, 40, -5.2)[0]                      # where the lamp's mirror image falls: straight under it
for s in np.arange(18.5, 27.5, .5):
    if rng.uniform() < .55:
        offs = np.linspace(-1.25, 1.25, 26)
        xs = np.array([T(s, o, -.17)[0] for o in offs])
        o = float(offs[np.argmin(np.abs(xs - (col_x + rng.normal(0, 16))))])
        hl = rng.uniform(.12, .3)
        cool.append(np.array([T(s - .04, o - hl, -.17), T(s - .04, o + hl, -.17), T(s + .04, o + hl, -.17), T(s + .04, o - hl, -.17)]))
marks(cool, RED2); marks(hot, RED)

# ---- the witness: stopped on the ballast between the brush and the rail, ears up
block('coyote')
cs, co = 15.2, -1.85
fx, fy = T(cs, co, -.15)
k = (T(cs, co, 0)[1] - T(cs, co, .6)[1]) / 592.0
coyote(fx, fy, k, '#1f1c1a', rim=RED2)
print('coyote at', round(fx), round(fy), 'k', round(k, 4), 'height px', round(792 * k))

# ---- rain rings on the near water, growing toward us
block('rings')
sh = np.array([T(s, SHOULDER, -.3) for s in np.arange(18, 70, 1.0)])
rr = []
for _ in range(15):
    y = rng.uniform(U(0, .40)[1], U(0, .63)[1])
    xlim = float(np.interp(y, sh[::-1, 1], sh[::-1, 0])) + 46
    if xlim > X1 - 30: continue
    x = rng.uniform(xlim, X1 - 12)
    f = (y - HZ) / (U(0, .64)[1] - HZ)
    rx = 3 + 20 * f * rng.uniform(.6, 1.2)
    rr.append(ring(x, y, rx, w=.9 + .5 * f))
    if rng.uniform() < .35: rr.append(ring(x, y, rx * .5, w=.8 + .3 * f))
marks(rr, '#5d727b', opacity=.7)

# ---- rain: ruled hairlines in loose sheaves, from the south-west. Dark where the picture is light, pale where it is dark.
dk, pl = [], []
for cx in (150, 420, 640, 905, 1120):
    dk += rain(cx - 110, Y0, cx + 110, Y1, n=5, angle=101, w=1.0, length=(.22, .62), spread=1.0)
    pl += rain(cx - 150, Y0, cx + 150, Y1, n=7, angle=101, w=.9, length=(.2, .6), spread=1.0)
block('rain_dark'); marks(dk, '#0b1016', opacity=.5)
block('rain_pale'); marks(pl, '#9aa9aa', opacity=.28)

finish(X0, Y0, X1, Y1, tooth=.3)
seal(X0 + 30, Y1 - 64, 32)
block('title')
text(X0 + 2, Y1 + 30, 'Red board, rain', size=30, font='Liberation Serif', color='#4b4438', anchor='la')
text(X1 - 2, Y1 + 34, 'Fable', size=24, font='Liberation Serif', color='#4b4438', anchor='ra')
