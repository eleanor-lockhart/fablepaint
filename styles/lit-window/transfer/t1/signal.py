# signal.py: a single-head searchlight block signal with its relay case, from grid-measured proportions on
# transfer/refs/signal_bridge_sub.jpg (CN Bridge Subdivision, mile 10.9: a three-head mast; one head used here).
# Units are metres, z up, rail top at z = 0. Measured with the 0.9 m target disc as the unit:
#   - mast pipe 0.145 m thick; head centre 5.2 m above the footing on a one-head mast
#   - the target is NOT centred on the mast: its centre sits 0.24 m to the track side of the mast axis
#   - the lens is small, a quarter of the target's width, low in a 0.22 x 0.40 m housing under a hood
#   - number plate 0.60 x 0.19 m just under the head; a wire platform frame 0.7 m wide below that
#   - ladder up the back of the mast, 0.38 m wide, rungs 0.3 m apart
#   - relay case about 0.6 x 1.2 x 1.9 m standing beside it, aluminium paint
# What memory had wrong: disc centred on the pole, a lens half the width of the disc, no ladder.
def signal(P, eye, x, y, c, track_side=-1):
    """Mast footing at (x, y); it faces -y (toward a train coming from behind the viewer).
    c: dict with key, dark2, plate, steel, red, case, case2."""
    def L(a, b, w): return seg(P(*a), P(*b), w=max(w, .9), wob=.04)
    k = math.hypot(*np.subtract(P(x + .5, y, 2.5), P(x - .5, y, 2.5)))        # pixels per metre at the mast
    # relay case first (it stands nearer the eye is handled by the caller's choice of position)
    xa, xb, ya, yb = x + .35, x + .95, y - 3.0, y - 1.8
    walls = extrude(P, boxplan(xa, xb, ya, yb), -.3, 1.6, eye)
    for q, tone in zip(walls, (c['case'], c['case2'])):
        marks([q], tone)
    marks([np.array([P(xa - .05, ya - .05, 1.6), P(xb + .05, ya - .05, 1.6), P(xb + .05, yb + .05, 1.6), P(xa - .05, yb + .05, 1.6)])], c['steel'])
    # footing
    marks(extrude(P, boxplan(x - .3, x + .3, y - .3, y + .3), -.3, .12, eye), c['dark2'])
    marks([np.array([P(x - .3, y - .3, .12), P(x + .3, y - .3, .12), P(x + .3, y + .3, .12), P(x - .3, y + .3, .12)])], c['case'])
    # ladder behind the mast, platform frame under the head
    yl = y + .3
    lad = [L((x - .19, yl, .1), (x - .19, yl, 4.4), .03 * k), L((x + .19, yl, .1), (x + .19, yl, 4.4), .03 * k)]
    z = .45
    while z < 4.35:
        lad.append(L((x - .19, yl, z), (x + .19, yl, z), .022 * k)); z += .3
    lad += [L((x - .36, y, 3.75), (x + .36, y, 3.75), .028 * k), L((x - .36, y, 3.75), (x - .2, y, 4.5), .022 * k), L((x + .36, y, 3.75), (x + .2, y, 4.5), .022 * k),
            L((x - .36, y, 3.75), (x - .36, yl, 3.75), .022 * k), L((x + .36, y, 3.75), (x + .36, yl, 3.75), .022 * k)]
    marks(lad, c['key'])
    marks([L((x, y, .1), (x, y, 5.1), .145 * k)], c['key'])
    marks([np.array([P(x - .30, y - .08, 4.05), P(x + .30, y - .08, 4.05), P(x + .30, y - .08, 4.24), P(x - .30, y - .08, 4.24)])], c['plate'])
    # the head: target disc, and the lens under its hood
    cx, cz, r = x + track_side * .24, 5.2, .45
    a = np.linspace(0, 6.283, 30)[:-1]
    marks([np.array([P(cx + r * math.cos(t), y - .1, cz + r * math.sin(t)) for t in a])], c['key'])
    rl, lz = .125, cz - .03
    lens_pts = []
    for t in np.linspace(0, 6.283, 26)[:-1]:
        dz = rl * math.sin(t)
        if dz > rl * .35: dz = rl * .35 + .22 * (dz - rl * .35)          # the hood cuts the top of the lens nearly flat
        lens_pts.append(P(cx + rl * math.cos(t), y - .14, lz + dz))
    marks([np.array(lens_pts)], c['red'])
    return dict(lens=P(cx, y - .14, lz), foot=P(x, y, 0), k=k, top=P(cx, y - .1, cz + r))
