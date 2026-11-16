exec(open('../atelier/prints/p2/common.py').read())
window(X0, Y0, X1, Y1)
for nm in ('drifts', 'fir_near', 'fir_snow', 'sapling', 'firs_mid'):
    use(nm); clear()
# ---- drifts: crests pointed at both ends (the first ones were frosted-glass rectangles)
use('drifts')
for a, b, yy, dp in ((-.06, .40, .668, .075), (.36, 1.0, .64, .06), (.02, .56, .80, .10), (.5, 1.06, .765, .085), (-.08, .36, .925, .09), (.40, .92, .91, .10)):
    drift(U(a, 0)[0], U(b, 0)[0], U(0, yy)[1], dp * (Y1 - Y0), S2)
# ---- middle-distance firs on the flank of the knoll
use('firs_mid')
tr, fo, sn = [], [], []
for (a, b, hgt, wd) in ((.70, .43, 210, 84), (.775, .45, 300, 112), (.64, .42, 150, 62)):
    x, y = U(a, b)
    t_, f_ = conifer(x, y + 30, hgt, wd, crown=.86, lean=rng.normal(0, .01), sag=.25)
    tr += t_; fo += f_; sn += snowpillows(conifer.spines, size=.11, lo=3, hi=9)
marks(tr + fo, '#26353c'); marks(sn, S2)
# ---- the near fir: trunk close to the right edge, a dozen big loaded boughs, most of it out of frame
use('fir_near')
t_, f_ = conifer(1168, Y1 + 230, 2150, 700, crown=.97, lean=-.003, trunk_w=52, tuft=(10, 24), n=20, sag=.42, body=.2)
marks(t_ + f_, DARK)
near_sp = list(conifer.spines)
use('fir_snow')
marks(snowpillows(near_sp, size=.09, lo=8, hi=30), S1)
# ---- the small one at lower left
use('sapling')
x, y = U(.115, .905)
t_, f_ = conifer(x, y, 240, 150, crown=.96, lean=.03, tuft=(7, 16), n=11, sag=.5, body=.15)
marks(t_ + f_, DARK)
marks(snowpillows(conifer.spines, size=.16, lo=5, hi=15, start=.0, gap=.15), S1)
marks([blob(x + 4, y - 244, 9, 7, n=9, rough=.2)], S1)
marks([wobble(np.array([(x - 86, y + 8), (x - 40, y - 6), (x + 20, y - 8), (x + 80, y + 2), (x + 96, y + 16), (x - 96, y + 18)]), .6, 18)], S1)
