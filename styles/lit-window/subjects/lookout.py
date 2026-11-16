# subjects/lookout.py: a 1930s Forest Service fire lookout (L-4 style cab on a timber tower), from
# refs/photos/lookout_winter.jpg (Aeneas Lookout, Okanogan NF, 1943). Units are metres, z up,
# tower centred on the origin with its feet at z = 0.
#   - 4.3 m square cab, band of windows all round, pyramid roof with a lightning rod
#   - catwalk and rail round the cab; about 6 m of open timber tower, X-braced in two tiers
#   - posts lean in slightly (4.2 m square at the ground, 3.4 m at the deck)
def lookout(P, eye, c, lit=True, snow=True):
    """Draw it on the current layer. c: dict with timber, timber2, lamp, lamp2, snow, shade."""
    ex, ey = eye[0], eye[1]
    def post(i, z):                                  # position of corner post i at height z
        sx, sy = ((1, 1), (1, -1), (-1, -1), (-1, 1))[i]
        h = 2.1 - .4 * z / 6.0
        return (sx * h, sy * h, z)
    def L(a, b, w=3.0): return seg(P(*a), P(*b), w=w, wob=.05)
    faces = [(0, 1), (1, 2), (2, 3), (3, 0)]
    def facing(i, j):
        a, b = post(i, 3), post(j, 3)
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        return mx * (ex - mx) + my * (ey - my) > 0
    back, front = [], []
    for i, j in faces:
        tgt = front if facing(i, j) else back
        for z0, z1 in ((0, 3), (3, 6)):
            tgt += [L(post(i, z0), post(j, z1), 2.2), L(post(j, z0), post(i, z1), 2.2), L(post(i, z1), post(j, z1), 2.6)]
    marks(back, c['timber2'])
    marks(front + [L(post(i, -.6), post(i, 6), 4.2) for i in range(4)], c['timber'])
    # deck: underside, edge, rail
    D = 3.0
    marks([np.array([P(D, D, 5.85), P(D, -D, 5.85), P(-D, -D, 5.85), P(-D, D, 5.85)])], c['timber'])
    marks(extrude(P, boxplan(-D, D, -D, D), 5.85, 6.12, eye), c['timber'])
    rail = []
    cs = [(D, D), (D, -D), (-D, -D), (-D, D)]
    for k in range(4):
        a, b = cs[k], cs[(k + 1) % 4]
        for t in (0, .33, .66):
            x, y = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
            rail.append(L((x, y, 6.1), (x, y, 7.15), 1.6))
        rail += [L((a[0], a[1], 7.15), (b[0], b[1], 7.15), 1.8), L((a[0], a[1], 6.65), (b[0], b[1], 6.65), 1.1)]
    # cab walls and windows
    C = 2.15
    marks(extrude(P, boxplan(-C, C, -C, C), 6.12, 8.5, eye), c['timber'])
    panes, k = [], 0
    for (a, b) in ((( C, -C), ( C,  C)), ((-C, -C), ( C, -C)), ((-C,  C), (-C, -C)), (( C,  C), (-C,  C))):
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        if mx * (ex - mx) + my * (ey - my) <= 0: continue
        q = []
        for i in range(4):
            t0, t1 = .06 + i * .225, .06 + i * .225 + .19
            p0 = (a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0); p1 = (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)
            q.append(np.array([P(p0[0], p0[1], 6.95), P(p1[0], p1[1], 6.95), P(p1[0], p1[1], 8.15), P(p0[0], p0[1], 8.15)]))
            q_m = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
            panes.append(L((q_m[0], q_m[1], 6.95), (q_m[0], q_m[1], 8.15), 1.0))
        panes.append(L((a[0], a[1], 7.6), (b[0], b[1], 7.6), 1.0))
        marks(q, (c['lamp'], c['lamp2'])[k % 2] if lit else c['timber2']); k += 1
    marks(panes, c['timber'])
    marks(rail, c['timber'])
    # roof: pyramid; the two faces we see carry snow, one in light and one in shade
    E, apex = 2.65, (0, 0, 9.95)
    marks(extrude(P, boxplan(-E, E, -E, E), 8.4, 8.56, eye), c['timber'])
    ev = [(E, E), (E, -E), (-E, -E), (-E, E)]
    tones = []
    for k in range(4):
        a, b = ev[k], ev[(k + 1) % 4]
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        if mx * (ex - mx) + my * (ey - my) > 0:
            tones.append((np.array([P(a[0], a[1], 8.56), P(b[0], b[1], 8.56), P(*apex)]), mx))
    tones.sort(key=lambda t: t[1])
    for n_, (poly, _) in enumerate(tones):
        marks([poly], (c['snow'], c['shade'])[n_ % 2] if snow else c['timber2'])
    marks([L(apex, (0, 0, 11.0), 1.3), L((1.1, -1.0, 9.2), (1.1, -1.0, 10.3), 2.2)], c['timber'])
    if snow:                                         # snow lying on the rail and the deck edge
        sn = []
        for k in range(4):
            a, b = cs[k], cs[(k + 1) % 4]
            mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
            if mx * (ex - mx) + my * (ey - my) > 0:
                sn += [L((a[0], a[1], 7.24), (b[0], b[1], 7.24), 2.6), L((a[0], a[1], 6.2), (b[0], b[1], 6.2), 2.2)]
        marks(sn, c['snow'])
    return dict(pipe=P(1.1, -1.0, 10.3), base=P(0, 0, 0), apex=P(*apex))
