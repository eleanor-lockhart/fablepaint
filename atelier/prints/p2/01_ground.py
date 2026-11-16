exec(open('../atelier/prints/p2/common.py').read())
window(X0, Y0, X1, Y1)
layer('paper'); fill(PAPER)
# ---- sky: snow cloud, darkest at the top, palest where it meets the ridge
block('sky'); select_rect(X0 - 4, Y0 - 4, X1 + 4, Y0 + 900)
gradient('linear', (0, Y0), (0, Y0 + 700), ramp(SKY0, (SKY1, .5), (SKY2, 1.0)))
baren(.018, seed=3); select_none()
# ---- far ridge with its rank of small firs, one tone
block('far')
ridge = [(-.02, .40), (.08, .345), (.2, .33), (.32, .35), (.5, .36), (.7, .345), (.85, .36), (1.02, .34), (1.02, .5), (-.02, .5)]
marks([wobble(Us(ridge), .8, 30)], FAR)
tr, fo = [], []
for a in np.arange(-.01, 1.02, .022):
    if .27 < a < .47: continue
    x, y = U(a + rng.normal(0, .004), np.interp(a, [r[0] for r in ridge[:8]], [r[1] for r in ridge[:8]]) + .006)
    t_, f_ = conifer(x, y, rng.uniform(46, 110), rng.uniform(22, 36), crown=.88)
    tr += t_; fo += f_
marks(tr + fo, FAR)
# ---- the knoll the tower stands on: far snow, one shade tone
block('knoll')
knoll = [(-.02, .46), (.1, .40), (.22, .345), (.31, .318), (.385, .312), (.46, .325), (.58, .37), (.76, .42), (1.02, .47), (1.02, .6), (-.02, .6)]
marks([wobble(Us(knoll), .8, 36)], S2)
# ---- the gully between, deep shade
block('gully')
marks([wobble(Us([(-.02, .49), (.14, .455), (.3, .47), (.5, .455), (.7, .48), (1.02, .505), (1.02, .64), (-.02, .66)]), .8, 36)], S3)
# ---- the near slope: bare paper, with drifts in shade
block('slope')
slope = [(-.02, .60), (.12, .555), (.27, .535), (.43, .56), (.6, .59), (.8, .57), (1.02, .60), (1.02, 1.02), (-.02, 1.02)]
marks([wobble(Us(slope), .9, 40)], S1)
bokashi('#a9b8bc', U(.0, 1.0), U(.5, .62), .8, power=1.6)
block('drifts')
drift = [[(-.02, .70), (.10, .665), (.2, .67), (.24, .69), (.14, .70), (.06, .725), (-.02, .74)],
         [(.42, .66), (.6, .625), (.78, .64), (.9, .675), (.74, .67), (.6, .665), (.5, .685)],
         [(.1, .86), (.3, .81), (.46, .82), (.4, .845), (.26, .85), (.16, .885)],
         [(.62, .80), (.8, .765), (1.02, .78), (1.02, .82), (.84, .80), (.7, .825)]]
marks([wobble(Us(d), .8, 26) for d in drift], S2)
# ---- ski tracks: two lines closing with distance, and the pole plants beside them
block('tracks')
T = spline(Us(TRACK))
d = np.r_[0, np.cumsum(np.hypot(*np.diff(T, axis=0).T))]; u = d / d[-1]
nrm = np.gradient(T, axis=0); nrm = np.c_[-nrm[:, 1], nrm[:, 0]]; nrm /= np.hypot(nrm[:, 0], nrm[:, 1])[:, None]
sep = 13 * (1 - u) ** 1.5 + 1.2
wt = 3.4 * (1 - u) ** 1.2 + .9
lines = []
for sgn in (-1, 1):
    Pth = T + nrm * (sgn * sep)[:, None]
    for a in range(0, len(Pth) - 6, 5):
        lines.append(ribbon(Pth[a:a + 7], w=float(wt[a]), taper=(0, 0), wob=.05, smooth=False))
marks(lines, '#7d9199')
poles = [chip(*(T[i] + nrm[i] * s_ * (sep[i] * 2.3 + 3)), 1.2 + 2.4 * (1 - u[i])) for i in range(4, len(T) - 4, 6) for s_ in (1, -1)]
marks(poles, '#7d9199')
