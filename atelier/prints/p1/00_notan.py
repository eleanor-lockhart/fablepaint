# Print 1, step 2: three notan variants in three flat values.
exec(open('../atelier/kit.py').read())
D, M, L = '#262626', '#7f7f7f', '#e8e8e8'
layer('n'); fill('#ffffff')
def panel(i):
    ox, oy, w, h = 20 + 325 * i, 20, 305, 450
    window(ox, oy, ox + w, oy + h)
    def R(a, b, c, d, col): marks([np.array([(ox + a * w, oy + b * h), (ox + c * w, oy + b * h), (ox + c * w, oy + d * h), (ox + a * w, oy + d * h)])], col)
    def Pg(pts, col): marks([np.array([(ox + a * w, oy + b * h) for a, b in pts])], col)
    def dashes(xc, y0_, y1_, wd, col=L):
        marks(ticks(ox + xc * w, oy + y0_ * h, oy + y1_ * h, wd * w, grow=1.3, th=3.0, gap=.5), col)
    return R, Pg, dashes
def heron_sil(Pg, x, y, s):          # crude hunched silhouette, top of piling at (x, y)
    Pg([(x - .03 * s, y), (x - .02 * s, y - .16 * s), (x - .06 * s, y - .22 * s), (x - .16 * s, y - .21 * s), (x - .05 * s, y - .25 * s), (x + .0 * s, y - .25 * s),
        (x + .03 * s, y - .2 * s), (x + .06 * s, y - .08 * s), (x + .05 * s, y - .03 * s), (x + .01 * s, y)], D)
# A: pilings and heron right foreground, ferry left on the horizon, light sliver behind it
R, Pg, dashes = panel(0)
R(0, 0, 1, .2, D); R(0, .2, 1, .42, M); R(0, .345, .7, .385, L); R(.5, .40, 1, .425, D)
R(0, .42, 1, .7, M); R(0, .7, 1, 1, D)
R(.06, .385, .56, .42, M); R(.1, .395, .52, .408, L)
dashes(.31, .43, .86, .36)
for x, t in ((.66, .42), (.72, .30), (.79, .36), (.86, .47)):
    R(x - .035, t, x + .035, 1, D)
heron_sil(Pg, .72, .30, 1.0)
# B: ferry large, cut by the left edge, heron small at right
R, Pg, dashes = panel(1)
R(0, 0, 1, .22, D); R(0, .22, 1, .5, M); R(0, .5, 1, .78, M); R(0, .78, 1, 1, D)
Pg([(0, .5), (0, .30), (.5, .34), (.72, .40), (.74, .5)], M); Pg([(0, .34), (.5, .37), (.66, .42), (.66, .44), (0, .40)], L); Pg([(0, .44), (.62, .46), (.62, .475), (0, .465)], L)
R(0, .49, .76, .51, D)
dashes(.3, .52, .92, .55)
R(.8, .5, .87, 1, D); heron_sil(Pg, .835, .5, .7)
# C: high horizon, ferry small upper right, a long reflection, big pilings cut by the left edge
R, Pg, dashes = panel(2)
R(0, 0, 1, .1, D); R(0, .1, 1, .24, M); R(.3, .2, 1, .225, L); R(0, .225, .5, .245, D)
R(0, .24, 1, .62, M); R(0, .62, 1, 1, D)
R(.5, .205, .92, .24, M); R(.54, .215, .88, .228, L)
dashes(.71, .25, .8, .3)
for x, t in ((.05, 0), (.17, .08), (.29, .2)):
    R(x - .06, t, x + .06, 1, D)
R(.36, .47, .46, 1, D); heron_sil(Pg, .41, .47, 1.1)
_CLIP[0] = None
