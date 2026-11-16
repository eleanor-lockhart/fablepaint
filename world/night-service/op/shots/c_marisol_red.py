"""NIGHT SERVICE opening, unit c (bars 9-12): Marisol the Lookout (poses 0-47), Red the Signal Maintainer (48-95).
0-23 Mount Vesper, wide: the light leaves the house on pose 6 · 24-47 Marisol and what she sees ·
48-71 the shore line, wide: the mast drops to green on 66 · 72-95 Red's lantern goes up: she is the signal now."""
import math
import numpy as np
import common as C

N = 96
W, H = C.W, C.H
draw, sh = C.draw, C.sh
YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)

def A(*pts): return np.array(pts, np.float32)
def box(x0, y0, x1, y1): return A((x0, y0), (x1, y0), (x1, y1), (x0, y1))
def line(a, b, w):
    a, b = np.asarray(a, np.float32), np.asarray(b, np.float32); d = b - a; o = np.array((-d[1], d[0])) / max(float(np.hypot(*d)), 1e-6) * w / 2
    return np.array([a - o, b - o, b + o, a + o], np.float32)
def fill(img, polys, colour, op=1.0): return draw.paint(img, draw.raster(polys, W, H), colour, op)
def add(img, matte, colour, k):
    """Additive light through a matte (a flat pool of light on whatever is there)."""
    out = img.copy(); out[..., :3] += C.core.col(colour)[:3] * (k * matte[..., None]); return out
def ellipse(cx, cy, rx, ry, n=40):
    t = np.linspace(0, 2 * np.pi, n, endpoint=False); return np.c_[cx + rx * np.cos(t), cy + ry * np.sin(t)].astype(np.float32)
def soft(cx, cy, r, p=2.0): return np.clip(1 - np.hypot(XX - cx, YY - cy) / r, 0, 1) ** p

def jpx(name, pose, key, x, ground, size, flip=False):
    """Pixel position of a joint of a posed figure."""
    c = C.CAST[name]; J = c['fig'].joints(c['pose'] if pose is None else pose); s = size * c['height']
    return np.array((x + (-s if flip else s) * J[key][0], ground - s * J[key][1]), np.float32)

def figc(img, name, pose, x, ground, size, flip=False, glow=5.0, sil=None):
    """C.figure drawn inside a crop round the figure (fast). It also tells the master that the figure must stay dark
    (C.figure only does that for figures drawn on a full frame); sil = a matte limiting where (the hole of the glass)."""
    h = size * C.CAST[name]['height']
    x0, x1 = int(max(0, x - .64 * h)), int(min(W, x + .64 * h)); y0, y1 = int(max(0, ground - 1.16 * h)), int(min(H, ground + .06 * h))
    if x1 - x0 < 4 or y1 - y0 < 4: return img
    before = img[y0:y1, x0:x1, :3].copy()
    out = C.figure(img[y0:y1, x0:x1].copy(), name, pose, x=x - x0, ground=ground - y0, size=size, flip=flip, glow=glow)
    if hasattr(C, 'shadow'):
        full = np.zeros((H, W), np.float32); full[y0:y1, x0:x1] = np.abs(out[..., :3] - before).sum(-1) > 1e-5
        C.shadow(full if sil is None else full * sil)
    img[y0:y1, x0:x1] = out
    return img

def chest(pose, x, ground, size, flip=True, name='passenger'):
    h, c = jpx(name, pose, 'hip', x, ground, size, flip), jpx(name, pose, 'chest', x, ground, size, flip)
    return h + (c - h) * .79

def stars(img, seed, n, ymax):
    r = np.random.default_rng(seed); xs = r.uniform(0, W, n); ys = 4 + (ymax - 4) * r.uniform(0, 1, n) ** 1.5; ss = r.choice([1.4, 2.0, 2.0, 2.8], n)
    return C.light(img, draw.raster([box(x, y, x + s, y + s) for x, y, s in zip(xs, ys, ss)], W, H), '#dfe6f5', 1.2)

def firs(img, specs, colour):
    polys = []
    for x, base, hgt, wid in specs:
        trunk, leaf = sh.conifer(x, base, hgt, wid); polys += list(trunk) + list(leaf)
    return fill(img, polys, colour)

PLIGHT = C.CAST['passenger']['window']                                          # the light of a house, and of whoever lived in it

# =================================================================== Mount Vesper, wide (0-23)
RIDGE = A((-10, 590), (120, 548), (260, 482), (380, 428), (470, 396), (560, 388), (680, 384), (800, 392), (1000, 420), (1290, 440))
def path_y(x): return float(np.interp(x, RIDGE[:, 0], RIDGE[:, 1])) + 6
HILL, HOUSE = '#0d1522', '#0a1019'
WIN = box(566, 276, 610, 336)
WIN_M = draw.raster([WIN], W, H)
WIN_X = draw.raster([box(587, 276, 589, 336), box(566, 305, 610, 307)], W, H)
DOOR_M = draw.raster([box(462, 252, 516, 408)], W, H)
WIN_HALO = soft(588, 306, 130)
DOOR_X = 489.0
LEAVES = 12                                                                     # the pose on which the light leaves the house
BAND_M = draw.raster([box(884, 206, 1166, 354)], W, H)                          # the cab's band of windows
MX, MG, MS = 962.0, 436.0, 232                                                  # Marisol on the catwalk
PS = 165                                                                        # the figure at the door
VP_ = C.walk_speed('passenger', PS) * .95

def _vesper():
    sh.setup(W, H, 21)
    img = stars(C.sky(), 31, 190, 470)
    img = fill(img, [np.r_[RIDGE, A((1290, 730), (-10, 730))]], HILL)
    img = firs(img, [(748, 392, 96, 40), (802, 397, 70, 30), (316, 462, 66, 28), (206, 514, 70, 30), (1230, 440, 90, 38)], HILL)
    img = fill(img, [box(438, 228, 682, 412), A((414, 233), (560, 140), (706, 233)), box(626, 156, 648, 214)], HOUSE)
    # a snag at the far left, and somebody on it
    img = fill(img, [A((90, 730), (93, 372), (99, 372), (104, 730)), line((96, 470), (124, 440), 3), line((96, 540), (66, 508), 3)], '#070b11')
    img = C.heron(img, 96, 373, s=.07)
    # the tower: legs, cab, roof
    dark = '#070a10'
    legs = [A((890, 444), (906, 444), (862, 730), (844, 730)), A((1144, 444), (1160, 444), (1208, 730), (1190, 730)),
            line((898, 446), (1196, 700), 5), line((1152, 446), (856, 700), 5), box(866, 586, 1184, 592)]
    img = fill(img, legs, dark)
    img = fill(img, [box(876, 196, 1174, 436), A((842, 204), (1208, 204), (1122, 150), (928, 150)), box(1024, 108, 1026, 152), box(832, 436, 1218, 446)], dark)
    img = firs(img, [(40, 770, 330, 150), (170, 790, 270, 130), (285, 780, 210, 110), (430, 800, 190, 100), (570, 805, 195, 110), (700, 795, 225, 120),
                     (780, 775, 290, 140), (1010, 810, 215, 120), (1105, 800, 180, 100), (1246, 780, 330, 150)], '#070b11')
    return img
VESPER = _vesper()
INSIDE_M = draw.raster([box(x - 2.5, 206, x + 2.5, 354) for x in (940, 997, 1053, 1110)] + [box(1086, 306, 1098, 354), ellipse(1092, 302, 36, 6), box(1058, 286, 1061, 300), box(1123, 286, 1126, 300)], W, H)
_LAMP = np.array(C.core.col(C.LAMP)[:3], np.float32)
CAB_UP = {14: _LAMP * .92, 15: np.array((.99, .66, .18), np.float32), 16: np.array((1.42, 1.09, .30), np.float32)}
def cab_rgb(i):
    """One light at a time: the cab is low (a third) while the house is lit, and comes up over 14-17, after the light has left.
    The steps are chosen so that the master's bloom comes in warm (LAMP between k 1.1 and 1.8 blooms red only)."""
    return _LAMP * .7 if i <= 13 else CAB_UP.get(i, _LAMP * 2.1)
def emit(img, matte, rgb):
    a = np.asarray(matte, np.float32)[..., None]; out = img * (1 - a); out[..., :3] += rgb * a; out[..., 3:] += a
    return out
RAIL = draw.raster([box(832, 384, 1218, 387)] + [box(x - 1, 386, x + 1, 437) for x in range(834, 1220, 48)], W, H)
M_UP = dict(C.CAST['marisol']['pose'])
M_DOWN = dict(lean=-1, head=2, shN=4, elN=14, shF=-4, elF=12, hipN=5, hipF=-6, kneeF=3)          # binoculars hanging on her chest
M_HALF = dict(lean=-2, head=-3, shN=-35, elN=143, shF=-38, elF=146, hipN=5, hipF=-6, kneeF=3)    # her hands on them

def marisol_wide(i):
    img = VESPER.copy()
    img = emit(img, BAND_M, cab_rgb(i))                                         # the cab's band of windows
    img = draw.paint(img, INSIDE_M, '#070a10')
    if i < LEAVES:                                                              # somebody is home: the brightest thing in the picture
        img = add(img, WIN_HALO, PLIGHT, .34)
        img = C.light(img, WIN_M, PLIGHT, 6.5)
        img = draw.paint(img, WIN_X, HOUSE)
        img = draw.paint(img, DOOR_M, '#111a28')
    else:                                                                       # the light has left the house: it is in his chest
        strike = i < LEAVES + 2
        img = draw.paint(img, WIN_M, '#04060a'); img = draw.paint(img, WIN_X, HOUSE)
        img = draw.paint(img, DOOR_M, '#030508')
        t = max(0, i - LEAVES - 1); x = DOOR_X - VP_ * t; g = (t / 12.0) % 1.0
        pose = C.walk_pose('passenger', g); gy = path_y(x)
        c = chest(pose, x, gy, PS)
        img = add(img, soft(c[0], c[1], 70 if strike else 46), PLIGHT, 1.0 if strike else .45)
        img = figc(img, 'passenger', pose, x, gy, PS, flip=True, glow=14.0 if strike else 8.0)
    pose = M_DOWN if i < 16 else M_HALF if i < 20 else M_UP
    img = figc(img, 'marisol', pose, MX, MG, MS, flip=True)
    return draw.paint(img, RAIL, '#070a10')

# =================================================================== Marisol and what she sees (24-47)
SCX, SCY, SCR = 330.0, 250.0, 170.0
HOLE_M = draw.disc(W, H, SCX, SCY, SCR)
SCOPE_SKY = draw.gradient(W, H, (0, 70), (0, 430), '#1b2d47', '#3d5a78')
SS = 226                                                                        # the figure in the glass
VSC = C.walk_speed('passenger', SS) * .95
_r = np.random.default_rng(77)
POSTS = np.arange(-2400, 900, 96) + _r.uniform(-10, 10, len(np.arange(-2400, 900, 96)))
STONES = np.c_[_r.uniform(-2400, 900, 150), _r.uniform(10, 150, 150), _r.uniform(3, 8, 150)]

def _cab_close():
    img = C.core.canvas(W, H, '#070b12')
    img = C.light(img, draw.raster([box(716, 120, W, 452)], W, H), '#f4cf80', 1.9)                   # lit warm, as in the wide
    return draw.paint(img, CAB_DARK, '#06090e')
CAB_DARK = draw.raster([box(700, 100, W, 120), box(700, 452, W, 470), box(700, 100, 716, 470), box(1068, 120, 1080, 452),
                        box(1170, 334, 1196, 452), ellipse(1183, 326, 88, 13), box(1104, 290, 1110, 322), box(1256, 290, 1262, 322)], W, H)
CABC = _cab_close()

def scope(i):
    t = i - 24; sc = SCOPE_SKY.copy()
    xf = 362 - 1.6 * t; gf = 396 + .56 * t                                      # his feet: he drifts down and left in the glass
    X = lambda u: xf + u + VSC * t                                              # ground point u px from where he stood on the cut
    Y = lambda xs: gf - .35 * (xs - xf)                                         # the slope: downhill is left
    dark = '#0a111c'
    polys = [A((100, Y(100)), (560, Y(560)), (560, 720), (100, 720))]
    px = [X(u) for u in POSTS if 120 < X(u) < 540]
    polys += [box(x - 2.5, Y(x) - 34, x + 2.5, Y(x) + 4) for x in px]
    polys += [line((a, Y(a) - 26), (b, Y(b) - 26), 1.6) for a, b in zip(px[:-1], px[1:])]
    sc = fill(sc, polys, dark)
    st = [box(X(u) - s, Y(X(u)) + d, X(u) + s, Y(X(u)) + d + s * .7) for u, d, s in STONES if 130 < X(u) < 530]
    if st: sc = fill(sc, st, '#18243a')
    pose = C.walk_pose('passenger', (t / 12.0) % 1.0)
    c = chest(pose, xf, gf, SS)
    sc = add(sc, soft(c[0], c[1], 70), PLIGHT, .5)
    return figc(sc, 'passenger', pose, xf, gf, SS, flip=True, glow=10.0, sil=HOLE_M)

def marisol_close(i):
    img = CABC.copy()
    m = HOLE_M[..., None]
    img = img * (1 - m) + scope(i) * m
    img = figc(img, 'marisol', M_UP, 905, 980, 860, flip=True)
    if hasattr(C, 'shadow'): C.shadow(CAB_DARK)                                 # the window's bars and the fire finder stay dark too
    return C.name_card(img, 'marisol', C.clamp01((i - 24) / 16), 'l')

# =================================================================== the shore line, wide (48-71)
SIG_RED, SIG_GREEN = '#ff3b24', C.GREEN
VPT = (1210.0, 536.0)                                                           # where the rails meet
RL0, RR0 = (380.0, 720.0), (760.0, 720.0)
def _rail_x(y, r0): return r0[0] + (r0[1] - y) / (r0[1] - VPT[1]) * (VPT[0] - r0[0])
MASTX, MASTB = 840.0, 596.0
LAMP_UP, LAMP_LO = (MASTX, 150.0), (MASTX, 198.0)
RX, RG, RS = 404.0, 668.0, 250

def _shore():
    sh.setup(W, H, 41)
    img = C.harbour(hz=455, seed=5)
    img = fill(img, [box(88, 548, 102, 600)], '#0a0f18')                        # a pile, and somebody on it
    img = C.heron(img, 95, 549, s=.07)
    img = fill(img, [A((-10, 590), (330, 580), (700, 562), (1000, 542), (1290, 530), (1290, 730), (-10, 730))], '#0a0f18')
    ties = []
    for n in range(1, 16):                                                      # sleepers, closing up toward the meeting point
        y = VPT[1] + (720 - VPT[1]) * .80 ** n * 1.1; hgt = max(1.5, 9 * .80 ** n)
        if y < 720: ties.append(A((_rail_x(y, RL0) - 22 * .8 ** n, y), (_rail_x(y, RR0) + 22 * .8 ** n, y), (_rail_x(y + hgt, RR0) + 22 * .8 ** n, y + hgt), (_rail_x(y + hgt, RL0) - 22 * .8 ** n, y + hgt)))
    img = fill(img, ties, '#121a27')
    img = fill(img, [A((_rail_x(600, RL0) - 30, 600), (_rail_x(600, RR0) + 30, 600), (_rail_x(613, RR0) + 30, 613), (_rail_x(613, RL0) - 30, 613))], '#1a2433')   # the crossing
    img = fill(img, _rails(), '#27344a')
    dark = '#06090e'
    mast = [box(MASTX - 4, 236, MASTX + 4, MASTB + 4), box(MASTX - 16, MASTB, MASTX + 16, MASTB + 8), box(MASTX - 30, 112, MASTX + 30, 240),
            A((MASTX - 30, 112), (MASTX + 30, 112), (MASTX + 18, 98), (MASTX - 18, 98)), box(MASTX + 4, 300, MASTX + 26, 304), box(MASTX + 22, 300, MASTX + 26, MASTB)]
    mast += [box(MASTX + 4, y, MASTX + 26, y + 2.5) for y in range(330, int(MASTB), 30)]
    return fill(img, mast, dark)
def _rails():
    return [A((RL0[0], 720), (RL0[0] + 15, 720), (VPT[0] + 1, VPT[1]), (VPT[0], VPT[1])), A((RR0[0], 720), (RR0[0] + 15, 720), (VPT[0] + 2, VPT[1]), (VPT[0] + 1, VPT[1]))]
SHORE = _shore()
RAILS_M = draw.raster(_rails(), W, H) * soft(MASTX + 60, MASTB + 20, 560, 1.2)
DISC_UP, DISC_LO = draw.disc(W, H, LAMP_UP[0], LAMP_UP[1], 14), draw.disc(W, H, LAMP_LO[0], LAMP_LO[1], 14)
HALO_UP, HALO_LO = soft(LAMP_UP[0], LAMP_UP[1], 190), soft(LAMP_LO[0], LAMP_LO[1], 190)
POOL_UP, POOL_LO = draw.disc(W, H, LAMP_UP[0], LAMP_UP[1], 150), draw.disc(W, H, LAMP_LO[0], LAMP_LO[1], 150)
VPW = C.walk_speed('passenger', 170)
PASSW = ((1285, .0), (1030, .35), (760, .7), (300, .15), (58, .55))
_lh = jpx('red', None, 'handN', RX, RG, RS)
RED_LOW = soft(_lh[0], _lh[1] + .074 * RS * .99, 70)

def rain(i, n=250):
    sh.setup(W, H, 4100 + i // 2)
    return draw.raster(sh.rain(-60, -60, W + 60, H + 60, n=n, angle=106, w=.8, length=(.12, .42)), W, H)

def red_wide(i):
    img = SHORE.copy(); green = i >= 66
    for x0, ph in PASSW:
        x = x0 - VPW * (i - 48)
        if -60 < x < W + 60:
            img = figc(img, 'passenger', C.walk_pose('passenger', ((i - 48) / 12.0 + ph) % 1.0), x, 606, 170, flip=True)
    img = add(img, RED_LOW, SIG_RED, .28)
    img = figc(img, 'red', None, RX, RG, RS)
    R = rain(i)
    img = draw.paint(img, R, '#8fa3bd', .26)
    col, disc, halo, pool = (SIG_GREEN, DISC_LO, HALO_LO, POOL_LO) if green else (SIG_RED, DISC_UP, HALO_UP, POOL_UP)
    hit = 2.0 if i in (66, 67) else 1.0                                         # it drops by itself, and is struck like a note
    img = draw.paint(img, DISC_UP if green else DISC_LO, '#10151e')
    img = add(img, pool, col, .07 * hit)
    img = add(img, halo, col, .30 * hit)
    img = add(img, R * pool, col, 1.5)                                          # the rain in its light takes its colour
    img = add(img, RAILS_M, col, .9 * hit)
    return C.light(img, disc, col, 7.0 * hit)

# =================================================================== Red is the signal (72-95)
CRX = 320.0
RED = dict(C.CAST['red']['pose'])
CG = 440.0                                                                      # the line, behind her
VPC = C.walk_speed('passenger', 300)
PASSC = ((1575, .2), (1300, .0), (1010, .4))                                    # nobody pale behind her or her lantern while it goes up
RAIN_BAND = np.clip((CG + 8 - YY) / 46, 0, 1)                                  # rain shows against the water, not on the dark ground (or the card)
CMAST = 1150.0

def _shore_close():
    sh.setup(W, H, 43)
    img = C.harbour(hz=132, seed=5, water=('#40566b', '#2a3e53', '#16222f'))
    img = fill(img, [box(0, CG, W, H)], '#0a0f18')
    img = fill(img, [box(0, CG - 4, W, CG)], '#27344a')                         # the rail
    img = fill(img, [box(x, CG, x + 30, CG + 6) for x in range(-10, W, 74)], '#141c29')
    dark = '#06090e'
    mast = [box(CMAST - 3, 150, CMAST + 3, CG), box(CMAST - 22, 52, CMAST + 22, 152), A((CMAST - 22, 52), (CMAST + 22, 52), (CMAST + 13, 42), (CMAST - 13, 42))]
    img = fill(img, mast, dark)
    img = fill(img, [ellipse(CMAST, 80, 10, 10, 20)], '#10151e')
    img = add(img, soft(CMAST, 122, 90), SIG_GREEN, .28)
    return C.light(img, draw.disc(W, H, CMAST, 122, 10), SIG_GREEN, 6.0)
SHORE_C = _shore_close()
POST_M = draw.raster([box(89, 372, 103, H), box(84, 372, 108, 378)], W, H)

def red_close(i):
    img = SHORE_C.copy()
    for x0, ph in PASSC:
        x = x0 - VPC * (i - 72)
        if -110 < x < W + 110:
            img = figc(img, 'passenger', C.walk_pose('passenger', ((i - 72) / 12.0 + ph) % 1.0), x, CG - 3, 300, flip=True)
    t = C.ease(C.clamp01((i - 72) / 6), 'inout'); over = {78: 5.0, 79: 3.0, 80: 1.0}.get(i, 0.0)
    pose = dict(RED, shN=14 + 86 * t + over, elN=10 + 10 * t, lean=1 - 2 * t)
    hd = jpx('red', pose, 'handN', CRX, 980, 860); lc = (float(hd[0]), float(hd[1] + .074 * 860 * .99))
    hit = 2.0 if i in (78, 79) else 1.0
    R = rain(i, 330) * RAIN_BAND
    for r, k in ((196, .10), (118, .14)):                                       # the lantern's pool of light: flat rings
        img = add(img, draw.disc(W, H, lc[0], lc[1], r) * (YY < CG - 4), SIG_RED, k * hit * (.45 + .55 * t))
    img = draw.paint(img, POST_M, '#06090e'); img = C.heron(img, 96, 372, s=.1)                 # a post by the line, and somebody on it
    img = figc(img, 'red', pose, CRX, 980, 860, glow=5.0 * hit)
    img = draw.paint(img, R, '#8fa3bd', .28)
    img = add(img, R * draw.disc(W, H, lc[0], lc[1], 196), SIG_RED, 1.8)        # the rain inside it is red
    return C.name_card(img, 'red', C.clamp01((i - 72) / 16), 'r')

def frame(i):
    i = int(i)
    img = marisol_wide(i) if i < 24 else marisol_close(i) if i < 48 else red_wide(i) if i < 72 else red_close(i)
    img = np.asarray(img, np.float32); img[..., 3] = 1.0
    return img
