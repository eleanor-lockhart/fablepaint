exec(open('../atelier/prints/p2/common.py').read())
window(X0, Y0, X1, Y1)
# ---- drifts a third time: computed, so the shade dies away with no outline
use('drifts'); clear()
for a, b, yy, dp in ((-.06, .42, .668, .07), (.34, 1.0, .642, .055), (.0, .58, .805, .09), (.5, 1.08, .765, .08), (-.1, .38, .925, .085), (.36, .96, .91, .09)):
    drift(U(a, 0)[0], U(b, 0)[0], U(0, yy)[1], dp * (Y1 - Y0), S2, strength=.95)
# ---- snow plastered on the weather side of the near trunk
use('fir_snow')
marks([blob(1146 + rng.normal(0, 2), yv, 6, rng.uniform(22, 60), n=9, rough=.25) for yv in (150, 330, 520, 760, 880, 1120, 1330, 1560)], S1)
# ---- the lamp lands on something: the snow on the rail outside the windows is warm
exec(open('../atelier/subjects/lookout.py').read())
eye = (48, -36, -8)
bx, by = U(.385, .318)
P0 = camera(eye=eye, look=(0, 0, 5), fov=35.2, centre=(bx, by)); ox, oy = P0(0, 0, 0)
P = camera(eye=eye, look=(0, 0, 5), fov=35.2, centre=(bx + (bx - ox), by + (by - oy)))
block('warm', above='tower')
marks([seg(P(3, -2.6, 7.24), P(3, 2.6, 7.24), w=2.6, wob=.05), seg(P(-2.4, -3, 7.24), P(2.6, -3, 7.24), w=2.6, wob=.05)], '#ead8a8')
# ---- snow falling over everything: chips of bare paper
block('snowfall')
marks(snowfall(X0, Y0, X1, Y1, n=2600, size=(.9, 2.3)), S1)
finish(X0, Y0, X1, Y1, tooth=.3)
seal(X0 + 30, Y1 - 66, 36)
block('title')
text(X0 + 2, Y1 + 30, 'Lookout, first snow', size=30, font='Liberation Serif', color='#4b4438', anchor='la')
text(X1 - 2, Y1 + 34, 'Fable', size=24, font='Liberation Serif', color='#4b4438', anchor='ra')
