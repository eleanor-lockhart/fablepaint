exec(open('../atelier/transfer/t1/common.py').read())
window(X0, Y0, X1, Y1)
layer('paper'); fill(PAPER)
# ---- sky: rain cloud, darkest at the top, the last light lying low in the west
block('sky'); select_rect(X0 - 4, Y0 - 4, X1 + 4, HZ + 6)
gradient('linear', (0, Y0), (0, HZ), ramp(NIGHT, (DEEP, .16), (MIDB, .40), ('#98a5a2', .60), (PALE, .84), PALE))
woodgrain(.02, 'v', seed=2); select_none()
# stepped cloud bands across the pale part
block('clouds')
marks([cloudband(X0 + 300, U(0, .192)[1], 800, 34), cloudband(X0 + 560, U(0, .238)[1], 560, 20), cloudband(X0 + 250, U(0, .262)[1], 330, 11)], '#465a64')
marks([cloudband(X0 + 690, U(0, .277)[1], 420, 9, ragged=.3)], '#7b8d92')
# ---- far islands across the Sound: two tone steps
block('isles')
far = [(.30, .313), (.34, .300), (.40, .296), (.47, .301), (.52, .293), (.60, .288), (.66, .294), (.74, .299), (.80, .291), (.88, .287), (.95, .292), (1.02, .289), (1.02, .316), (.30, .316)]
marks([wobble(Us(far), .6, 26)], '#8a9a9c')
near = [(.70, .314), (.73, .303), (.78, .298), (.83, .300), (.87, .296), (.92, .303), (.955, .309), (.97, .315)]
marks([wobble(Us(near), .6, 18)], '#5d7079')
def spire(x, base, h, w):
    """A far conifer: at this size a tree is a ragged notch in the skyline, not a drawing."""
    n = max(2, int(h / 4)); right, left = [], []
    for i in range(1, n + 1):
        f = i / n
        right.append((x + w / 2 * f * rng.uniform(.5, 1.15), base - h * (1 - f)))
        left.append((x - w / 2 * f * rng.uniform(.5, 1.15), base - h * (1 - f)))
    return np.array([(x, base - h)] + right + left[::-1])
sp = []
for a in np.arange(.725, .95, .0075):
    if rng.uniform() < .62:
        x, y = U(a + rng.normal(0, .002), np.interp(a, [p[0] for p in near], [p[1] for p in near]) + .003)
        sp.append(spire(x, y, rng.uniform(8, 19), rng.uniform(5, 8)))
marks(sp, '#5d7079')
# ---- water: light at the far edge, dark toward us
block('water'); select_rect(X0 - 4, HZ, X1 + 4, U(0, .70)[1])
gradient('linear', (0, HZ), (0, U(0, .66)[1]), ramp('#bfc6b9', ('#abb6b1', .22), ('#97a5a3', .42), ('#6f838b', .64), ('#465b68', .84), '#2c3f4d'))
woodgrain(.018, 'h', seed=4); select_none()
# ---- the headland the line goes round, with its firs: one tone
block('headland')
head = [(.16, .37), (.16, .222), (.215, .236), (.26, .252), (.30, .266), (.345, .281), (.385, .294), (.42, .304), (.445, .317), (.43, .326), (.37, .331), (.31, .343), (.25, .36)]
marks([wobble(Us(head), .7, 22)], FAR)
tr, fo = [], []
for a in np.arange(.17, .43, .0125):
    x, y = U(a + rng.normal(0, .003), np.interp(a, [p[0] for p in head[1:9]], [p[1] for p in head[1:9]]) + .004)
    t_, f_ = conifer(x, y, rng.uniform(34, 70) * (1.25 - a * 1.6), rng.uniform(16, 26) * (1.2 - a), crown=.88)
    tr += t_; fo += f_
marks(tr + fo, FAR)
# ---- the roadbed: wet ballast, paler with distance
block('bed')
ss = np.r_[np.arange(7.0, 40, 1.0), np.arange(40, 172, 3.0)]
far_edge = [T(s, SHOULDER, -.3) for s in ss]
near_edge = [T(s, toe_off(s) - .6, -.5) for s in ss]
bed = np.array(far_edge[::-1] + near_edge)
select_array(raster([bed]))
gradient('linear', T(110), T(11), ramp(STONE_FAR, (STONE, .45), STONE_NEAR))
select_none()
print('HZ', round(HZ, 1), 'signal foot', [round(v) for v in T(SIG_S, SIG_OFF)], 'vanish', [round(v) for v in T(165)])
