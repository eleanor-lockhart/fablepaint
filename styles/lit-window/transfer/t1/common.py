# Transfer print 1: "Red board, rain".
# Sentence: deep dusk, steady rain on the shore line; a block signal holds red over empty track,
# its light lying on the wet rails; a coyote has stopped to look.
# Notan: variant B (from the lip of the rock cut, high eye; the water is the pool of light).
exec(open('../atelier/kit.py').read())
X0, Y0, X1, Y1 = 80, 70, 1200, 1730
def U(a, b): return (X0 + a * (X1 - X0), Y0 + b * (Y1 - Y0))
def Us(pts): return np.array([U(a, b) for a, b in pts])

# ---- block list, light to dark (nine pigments and the key)
PALE, STEEL = '#c2c9bb', '#a9b4b0'        # 1 last light: low sky, far water; thinned for rail heads and wet steel
MIDB = '#5f737c'                          # 2 blue-grey: middle sky, middle water, far islands (thinned)
DEEP = '#2a3d4b'                          # 3 deep blue: upper sky, near water, cloud bands
NIGHT = '#131b24'                         # 4 top of the sky
STONE, STONE_FAR, STONE_NEAR = '#6a6e69', '#87918e', '#565853'   # 5 wet ballast, paler with distance
EARTH, EARTH2 = '#1d1a18', '#37322d'      # 6 brown-black: ties, bank, rock, the coyote; its lit plane
FIR, FIR2, FAR = '#141a1d', '#27353c', '#4d626b'   # 7 blue-black: near boughs; trees down the line; far headland
MOSS = '#3c4f4c'                          # 8 wet fronds and grass catching the sky
RED, RED2 = '#de5a3a', '#a9462f'          # 9 the signal, and its light thinned out on wet things
# KEY ('#1a1d24', from the kit) is the line block: mast, ladder, rail webs.

# ---- construction. World in metres: x toward the water (west), y along the line (south), z up, rail top at z = 0.
# Eye on the lip of a rock cut, 5.5 m east of the track centre and 6 m above the rail.
EYE = (-5.5, 0.0, 6.0)
P = camera(EYE, (3.6, 40.0, 3.0), fov=36, centre=(797, 734))
HZ = P(0, 1e7, 6.0)[1]                    # the horizon
YC, RAD = 70.0, 350.0                     # tangent for 70 m, then a 350 m curve to the left round the bluff
def track(s, off=0.0, z=0.0):
    """World point s metres along the centre line, `off` metres to the right of it (toward the water)."""
    if s <= YC: return (off, s, z)
    th = (s - YC) / RAD
    return (-RAD + (RAD + off) * math.cos(th), YC + (RAD + off) * math.sin(th), z)
def T(s, off=0.0, z=0.0): return P(*track(s, off, z))
GAUGE = 0.7175                            # half of 1435 mm
SIG_S, SIG_OFF = 40.0, 3.3                # the signal mast: 40 m down the line, 3.3 m right of centre
SHOULDER, TOE = 4.2, -3.2                 # edge of the ballast on the water side; foot of the cut on ours
def toe_off(s): return TOE + .22 * math.sin(s * .55) + .14 * math.sin(s * 1.3 + 1.0)
def strip(pts_a, pts_b, minw=1.2):
    """Polygon between two projected edges; where they come closer than minw px they are pushed apart."""
    A, Bq = np.asarray(pts_a, float), np.asarray(pts_b, float)
    mid, d = (A + Bq) / 2, Bq - A
    n = np.maximum(np.hypot(d[:, 0], d[:, 1]), 1e-6)
    d = d / n[:, None] * np.maximum(n, minw)[:, None] / 2
    return np.r_[mid - d, (mid + d)[::-1]]
