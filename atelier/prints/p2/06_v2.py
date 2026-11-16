exec(open('../atelier/prints/p2/common.py').read())
window(X0, Y0, X1, Y1)
# ---- three values, not two: the far knoll drops to a middle tone so the near crest is the light
use('knoll'); lock(True)
gradient('linear', U(0, .31), U(0, .60), ramp('#8a9ea5', ('#71868e', .5), '#586d76'))
lock(False)
use('heap'); lock(True); fill('#9db0b6'); lock(False)
# ---- tracks again: darker where the snow is darker
use('tracks'); clear()
T = spline(Us(TRACK))
d = np.r_[0, np.cumsum(np.hypot(*np.diff(T, axis=0).T))]; u = d / d[-1]
nrm = np.gradient(T, axis=0); nrm = np.c_[-nrm[:, 1], nrm[:, 0]]; nrm /= np.hypot(nrm[:, 0], nrm[:, 1])[:, None]
sep = 13 * (1 - u) ** 1.5 + 1.2
wt = 3.4 * (1 - u) ** 1.2 + .9
near, far = [], []
ycrest = U(0, .565)[1]
for sgn in (-1, 1):
    Pth = T + nrm * (sgn * sep)[:, None]
    for a in range(0, len(Pth) - 6, 5):
        (far if Pth[a + 3][1] < ycrest else near).append(ribbon(Pth[a:a + 7], w=float(wt[a]), taper=(0, 0), wob=.05, smooth=False))
marks(near, '#7d9199'); marks(far, '#4c616a')
idx = range(4, len(T) - 4, 6)
marks([chip(*(T[i] + nrm[i] * s_ * (sep[i] * 2.3 + 3)), 1.2 + 2.4 * (1 - u[i])) for i in idx for s_ in (1, -1) if T[i][1] >= ycrest], '#7d9199')
marks([chip(*(T[i] + nrm[i] * s_ * (sep[i] * 2.3 + 3)), 1.2 + 2.4 * (1 - u[i])) for i in idx for s_ in (1, -1) if T[i][1] < ycrest], '#4c616a')
# ---- more snow in the air where it shows: against sky and far hill
use('snowfall')
marks(snowfall(X0, Y0, X1, Y0 + 980, n=1700, size=(1.2, 3.0)), S1)
