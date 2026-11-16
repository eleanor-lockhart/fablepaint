exec(open('../atelier/prints/p2/common.py').read())
exec(open('../atelier/subjects/lookout.py').read())
window(X0, Y0, X1, Y1)
eye = (48, -36, -8)
bx, by = U(.385, .318)
P0 = camera(eye=eye, look=(0, 0, 5), fov=35.2, centre=(bx, by)); ox, oy = P0(0, 0, 0)
P = camera(eye=eye, look=(0, 0, 5), fov=35.2, centre=(bx + (bx - ox), by + (by - oy)))
# ---- snow again. The planes were stickers. A hollow is sharp at its near crest and fades away from it.
use('gully'); clear()
use('knoll'); bokashi(S3, U(0, .62), U(0, .36), .95, power=1.3)
use('drifts'); clear()
def drift(a, b, y, depth, sag=.012):
    """A wind crest from x=a to x=b at height y (normalised): sharp top edge, shade fading below it."""
    xs = np.linspace(a, b, 9)
    top = [(x, y + sag * math.sin(math.pi * (x - a) / (b - a)) * (-1) + rng.uniform(-.004, .004)) for x in xs]
    poly = wobble(Us(top + [(b, y + depth), (a, y + depth)]), .6, 30)
    shade(poly, S2, U(0, y - .01), U(0, y + depth), .95, power=1.4)
for a, b, y, dp in ((-.02, .34, .665, .07), (.40, .98, .635, .06), (.06, .50, .80, .09), (.58, 1.02, .76, .08), (-.02, .30, .93, .08), (.44, .86, .915, .09)):
    drift(a, b, y, dp)
# ---- tower again with shorter guys, thinner smoke, and the cabin where the ground actually is
use('tower'); clear()
info = lookout(P, eye, dict(timber=DARK, timber2='#2a363c', lamp=LAMP, lamp2=LAMP2, snow=S1, shade=S2))
marks([seg(P(3, -3, 6), P(8.5, -9.5, -.9), w=.9, wob=0), seg(P(3, 3, 6), P(9.5, 8, -.4), w=.9, wob=0), seg(P(-3, -3, 6), P(-9, -8, -.2), w=.9, wob=0)], '#2a363c')
px_, py_ = info['pipe']
marks([ribbon([(px_, py_ - 1), (px_ + 4, py_ - 22), (px_ + 26, py_ - 40), (px_ + 80, py_ - 50), (px_ + 170, py_ - 44), (px_ + 250, py_ - 52)], w=3.2, taper=(.05, .7), wob=.35)], '#6f8288', opacity=.75)
use('cabin'); clear()
ca = dict(x0=3.5, x1=7.5, y0=7.0, y1=10.5, z0=-.9, z1=.7, zr=2.0)
marks(extrude(P, boxplan(ca['x0'], ca['x1'], ca['y0'], ca['y1']), ca['z0'], ca['z1'], eye, only=lambda m: m[1] < ca['y0'] + .1), DARK)
ym = (ca['y0'] + ca['y1']) / 2
marks([np.array([P(ca['x1'], ca['y0'], ca['z0']), P(ca['x1'], ca['y1'], ca['z0']), P(ca['x1'], ca['y1'], ca['z1']), P(ca['x1'], ym, ca['zr']), P(ca['x1'], ca['y0'], ca['z1'])])], '#2a363c')
marks([np.array([P(ca['x0'] - .3, ca['y0'] - .4, ca['z1'] - .1), P(ca['x1'] + .3, ca['y0'] - .4, ca['z1'] - .1), P(ca['x1'] + .3, ym, ca['zr'] + .15), P(ca['x0'] - .3, ym, ca['zr'] + .15)])], S1)
cx_, cy_ = P(ca['x1'], ca['y0'] + .9, ca['z0'] + .3)
marks([np.array([P(ca['x1'], ca['y0'] + .7, -.5), P(ca['x1'], ca['y0'] + 1.5, -.5), P(ca['x1'], ca['y0'] + 1.5, .3), P(ca['x1'], ca['y0'] + .7, .3)])], LAMP2)
use('heap'); clear()
hx, hy = info['base']
marks([wobble(np.array([(hx - 130, hy + 34), (hx - 70, hy + 6), (hx - 20, hy - 5), (hx + 40, hy - 1), (hx + 120, hy + 8), (hx + 220, hy + 2), (hx + 300, hy + 16), (hx + 360, hy + 50), (hx - 130, hy + 50)]), .7, 22)], S2)
# ---- firs. Middle distance first, then the big one that runs out of the frame.
block('firs_mid')
tr, fo, sn = [], [], []
for (a, b, hgt, wd) in ((.735, .435, 250, 96), (.81, .452, 330, 120), (.655, .425, 170, 70)):
    x, y = U(a, b)
    t_, f_ = conifer(x, y + 30, hgt, wd, crown=.85, lean=rng.normal(0, .01))
    tr += t_; fo += f_; sn += snowload(conifer.spines, thick=.2, lo=4, hi=11)
marks(tr + fo, '#26353c')
marks(sn, S2)
block('fir_near')
x, y = U(.915, 1.0)
t_, f_ = conifer(x, y + 150, 1960, 760, crown=.96, lean=-.004, trunk_w=46, tuft=(9, 24))
marks(t_ + f_, DARK)
near_sp = list(conifer.spines)
block('fir_snow')
marks(snowload(near_sp, thick=.15, lo=7, hi=22), S1)
# the small one at lower left, bent under its load
block('sapling')
x, y = U(.115, .905)
t_, f_ = conifer(x, y, 250, 170, crown=.96, lean=.03, tuft=(8, 18))
marks(t_ + f_, DARK)
marks(snowload(conifer.spines, thick=.34, lo=8, hi=20, start=.05), S1)
marks([wobble(np.array([(x - 86, y + 8), (x - 40, y - 6), (x + 20, y - 8), (x + 80, y + 2), (x + 96, y + 16), (x - 96, y + 18)]), .6, 18)], S1)
