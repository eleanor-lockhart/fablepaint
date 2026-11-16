exec(open('../styles/lit-window/prints/p1/common.py').read())
window(X0, Y0, X1, Y1)
eye = (160, 420, 3.5)        # her near end is on our left; she is heading left, so we see her port side
P = camera(eye=eye, look=(0, 0, 3.5), fov=34, centre=(X0 + 800, HZ))
block('ferry')
info = ferry(P, eye, night=True, pal=dict(white='#7b8b8e', white2='#62737a', lamp=PAL['lamp'], lamp2='#dcbf7c', lamp3='#a8935f'))
block('ferrylights')
for (lx, ly) in info['mast_lights']:
    marks([blob(lx, ly, 2.4, 2.4, n=8, rough=.05)], '#f1ead2')
gx, gy = P(51, 8.4, 17.6)
marks([blob(gx, gy, 2.6, 2.6, n=8, rough=.05)], '#d0563f')      # port sidelight: red
# ---- her light on the water: one column under the window band
block('reflection')
xa, xb = sorted((P(-44, 13.7, 0)[0], P(44, 13.7, 0)[0]))
wy = max(P(-44, 13.7, 0)[1], P(44, 13.7, 0)[1])
marks(sheen(xa + 10, xb - 10, wy + 9, wy + 520, th0=1.8, th1=3.8, breakup=5, keep=.35), PAL['lamp'])
marks(sheen(xa - 10, xb + 10, wy + 60, wy + 760, th0=2.0, th1=4.2, breakup=6, keep=.18), PAL['lamp2'], opacity=.9)
use('water')
cut([lens(rng.uniform(xa - 60, xb), wy + 3 + i * 2.2, rng.uniform(80, 300), 1.6) for i in range(3)], depth=-.0)
block('hullshadow', above='water')
marks([lens(xa - 20 + rng.uniform(0, 60), wy + 2.5 + i * 3.4, (xb - xa) * rng.uniform(.5, 1.0), 2.4) for i in range(3)], '#18222b')
print('ferry spans', round(xa), round(xb), 'waterline y', round(wy))
