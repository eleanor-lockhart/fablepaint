"""NIGHT SERVICE opening, unit b (bars 5-8): Orrin the Keeper (poses 0-47), Dee the Deckhand (48-95).
0-23 Tern Point, wide · 24-47 Orrin and the lamp (it follows his head) · 48-71 the car deck, wide · 72-95 Dee and the punch."""
import math
import numpy as np
import common as C

N = 96
W, H = C.W, C.H
draw, sh = C.draw, C.sh
YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)

def A(*pts): return np.array(pts, np.float32)
def box(x0, y0, x1, y1): return A((x0, y0), (x1, y0), (x1, y1), (x0, y1))
def fill(img, polys, colour, op=1.0): return draw.paint(img, draw.raster(polys, W, H), colour, op)
def add(img, matte, colour, k):
    """Additive light through a matte (a flat pool of light on whatever is there)."""
    out = img.copy(); out[..., :3] += C.core.col(colour)[:3] * (k * matte[..., None]); return out
def ellipse(cx, cy, rx, ry, n=40):
    t = np.linspace(0, 2 * np.pi, n, endpoint=False); return np.c_[cx + rx * np.cos(t), cy + ry * np.sin(t)].astype(np.float32)
def rot(pts, c, deg):
    a = math.radians(deg); p = np.asarray(pts, np.float32) - c
    return np.c_[p[:, 0] * math.cos(a) - p[:, 1] * math.sin(a), p[:, 0] * math.sin(a) + p[:, 1] * math.cos(a)] + c

def jpx(name, pose, key, x, ground, size, flip=False):
    """Pixel position of a joint of a posed figure."""
    c = C.CAST[name]; J = c['fig'].joints(c['pose'] if pose is None else pose); s = size * c['height']
    return np.array((x + (-s if flip else s) * J[key][0], ground - s * J[key][1]), np.float32)

def _sil(x0, y0, m):
    """Tell the master this dark shape must stay dark (C.figure only does it for figures drawn on a full frame)."""
    if hasattr(C, 'shadow'):
        full = np.zeros((H, W), np.float32); full[y0:y0 + m.shape[0], x0:x0 + m.shape[1]] = m; C.shadow(full)

def figc(img, name, pose, x, ground, size, flip=False, glow=5.0, rim=None):
    """C.figure drawn inside a crop round the figure (fast). rim=(colour, strength, dx): a rim of light on the edges
    that face +x (dx > 0) or -x: the shot's lamp on the figure."""
    h = size * C.CAST[name]['height']
    x0, x1 = int(max(0, x - .64 * h)), int(min(W, x + .64 * h)); y0, y1 = int(max(0, ground - 1.16 * h)), int(min(H, ground + .06 * h))
    if x1 - x0 < 4 or y1 - y0 < 4: return img
    if rim is None:
        before = img[y0:y1, x0:x1, :3].copy()
        out = C.figure(img[y0:y1, x0:x1].copy(), name, pose, x=x - x0, ground=ground - y0, size=size, flip=flip, glow=glow)
        _sil(x0, y0, (np.abs(out[..., :3] - before).sum(-1) > 1e-5).astype(np.float32))
        img[y0:y1, x0:x1] = out
        return img
    lay = C.figure(np.zeros((y1 - y0, x1 - x0, 4), np.float32), name, pose, x=x - x0, ground=ground - y0, size=size, flip=flip, glow=glow)
    a = np.clip(lay[..., 3], 0, 1); col, k, dx = rim
    edge = a * (1 - np.roll(a, -dx, axis=1))
    lay[..., :3] += C.core.col(col)[:3] * (k * edge[..., None])
    _sil(x0, y0, a)
    img[y0:y1, x0:x1] = img[y0:y1, x0:x1] * (1 - a[..., None]) + lay
    return img

def stars(img, seed, n, ymax):
    r = np.random.default_rng(seed); xs = r.uniform(0, W, n); ys = 4 + (ymax - 4) * r.uniform(0, 1, n) ** 1.5; ss = r.choice([1.4, 2.0, 2.0, 2.8], n)
    return C.light(img, draw.raster([box(x, y, x + s, y + s) for x, y, s in zip(xs, ys, ss)], W, H), '#dfe6f5', 1.2)

# =================================================================== Tern Point, wide (0-23)
LX, LY = 905.0, 232.0                                             # the lantern of the light
HL = A((-10, 644), (220, 632), (460, 616), (660, 602), (800, 590), (900, 582), (1010, 580), (1120, 588), (1290, 606))
def ground_y(x): return float(np.interp(x, HL[:, 0], HL[:, 1]))

def _tern():
    sh.setup(W, H, 5)
    img = stars(C.sky(), 11, 170, 500)
    img = C.comp.over(img, C.comp.mask(draw.gradient(W, H, (0, 524), (0, H), '#4b6274', '#2c4155', '#101a28'), draw.rect(W, H, 0, 524, W, H)))
    img = fill(img, [A((70, 590), (86, 574), (104, 567), (132, 567), (150, 575), (168, 590))], '#0a1019')          # a rock, and somebody on it
    img = C.heron(img, 118, 568, s=.08)
    img = fill(img, [np.r_[HL, A((1290, 730), (-10, 730))]], '#0a1019')
    dark = '#0b0f18'
    tower = [A((LX - 37, 588), (LX - 23, 268), (LX + 23, 268), (LX + 37, 588)), box(LX - 37, 259, LX + 37, 268), box(LX - 37, 244, LX + 37, 246.5),
             A((LX - 22, 208), (LX + 22, 208), (LX, 180)), box(LX - 1.5, 166, LX + 1.5, 184), box(LX - 18, 256, LX + 18, 260)]
    tower += [box(LX + d - 1, 246, LX + d + 1, 260) for d in (-36, -24, -12, 0, 12, 24, 36)]
    tower += [box(952, 546, 1046, 590), A((944, 548), (999, 516), (1054, 548)), box(1022, 518, 1034, 540)]            # the keeper's house
    return fill(img, tower, dark)
TERN = _tern()
GLASS = draw.raster([box(LX - 15, 208, LX + 15, 256)], W, H)
MULL = draw.raster([box(LX - 16, 208, LX - 14, 256), box(LX - 1, 208, LX + 1, 256), box(LX + 14, 208, LX + 16, 256)], W, H)
LHALO = np.clip(1 - np.hypot(XX - LX, YY - LY) / 150, 0, 1) ** 2
VK = C.walk_speed('keeper', 230)

def orrin_wide(i):
    img = TERN.copy()
    phi = math.radians(30 + 7.5 * i); c, s = math.cos(phi), math.sin(phi)      # the beam turns: right, at us (pose 8), left (pose 20)
    L = math.copysign(max(abs(1080 * c), 70), c); hw = 22 + 95 * abs(s) ** 1.5
    wedge = draw.raster([A((LX, LY - 8), (LX + L, LY - hw), (LX + L, LY + hw), (LX, LY + 8))], W, H) * np.clip(1 - np.abs(XX - LX) / abs(L), 0, 1) ** .8
    front = max(s, 0) ** 2
    img = add(img, wedge, C.LAMP, .26 + .16 * front)
    img = add(img, LHALO, C.LAMP, .22 + .7 * front)
    img = C.light(img, GLASS, C.LAMP, 4.0 + 5.0 * front)
    img = draw.paint(img, MULL, '#0b0f18')
    x = 596 - VK * (23 - i)
    return figc(img, 'keeper', C.walk_pose('keeper', (i % 12) / 12), x, ground_y(x) + 2, 230)

# =================================================================== Orrin and the lamp (24-47)
OX = 742.0
LCX, LCY, LRX, LRY = 1100.0, 268.0, 80.0, 152.0
def _lens():
    t = np.linspace(0, 2 * np.pi, 72, endpoint=False); e = 2 / 2.7
    return np.c_[LCX + LRX * np.sign(np.cos(t)) * np.abs(np.cos(t)) ** e, LCY + LRY * np.sign(np.sin(t)) * np.abs(np.sin(t)) ** e].astype(np.float32)
LENS = draw.raster([_lens()], W, H)
BANDS = draw.raster([box(LCX - LRX, LCY + d - 1.5, LCX + LRX, LCY + d + 1.5) for d in (-126, -104, -82, -60, 60, 82, 104, 126)], W, H) * LENS
BULL = draw.disc(W, H, LCX, LCY, 34)
BULLRING = np.clip(draw.disc(W, H, LCX, LCY, 50) - draw.disc(W, H, LCX, LCY, 45), 0, 1)
FRAME = draw.raster([box(LCX - LRX - 13, LCY - LRY - 26, LCX - LRX - 6, H), box(LCX + LRX + 6, LCY - LRY - 26, LCX + LRX + 13, H),
                     A((LCX - LRX - 20, LCY - LRY - 22), (LCX + LRX + 20, LCY - LRY - 22), (LCX + 30, LCY - LRY - 58), (LCX - 30, LCY - LRY - 58)),
                     box(LCX - 4, 0, LCX + 4, LCY - LRY - 50), box(LCX - LRX - 20, LCY + LRY + 6, LCX + LRX + 20, LCY + LRY + 22),
                     box(LCX - 46, LCY + LRY + 20, LCX + 46, H), box(LCX - 96, 668, LCX + 96, H)], W, H)
LDIST = np.hypot(XX - LCX, YY - LCY)
ORRIN = dict(C.CAST['keeper']['pose'])
def lamp_rgb(k):
    """LAMP at strength k. Where only its red would be over the master's bloom threshold (k about 1.1 to 1.8) the green is
    lifted, so that a low lamp glows warm and never red."""
    c = np.array(C.core.col(C.LAMP)[:3], np.float32) * k
    if c[0] > 1.0: c[1] = max(c[1], 1.0 + .22 * (c[0] - 1.0))
    return c
def emit(img, matte, rgb):
    a = np.asarray(matte, np.float32)[..., None]; out = img * (1 - a); out[..., :3] += rgb * a; out[..., 3:] += a
    return out

def nod(i):
    """0 = awake, 1 = chin on chest. The lamp is a function of this and nothing else."""
    if i <= 32: return .58 * C.clamp01((i - 24) / 8.0) ** 1.5                   # 24-32: awake, heavier, heavier
    return {33: .48, 34: .84, 35: 1.0}.get(i, 0.0)                              # 33: he nearly catches himself; 34-35: chin on chest

def lamp_level(i):
    if i <= 35: return 1.0 - .95 * nod(i)
    return {36: 1.9, 37: 1.9, 38: 1.45, 39: 1.2, 40: 1.08}.get(i, 1.0)          # he wakes: it flares, then settles

def orrin_pose(i):
    n = nod(i); p = dict(ORRIN, head=36 * n, lean=8 + 6 * n, shN=-22 + 8 * n, elN=34 - 14 * n, shF=-16 + 8 * n, elF=30 - 12 * n)
    if i >= 36:
        j = {36: 1.0, 37: .8, 38: .4, 39: .12}.get(i, 0.0)                     # the jerk awake, overshooting
        p.update(head=-11 * j, lean=8 - 3 * j, shN=-22 - 10 * j, elN=34 + 22 * j, shF=-16 - 8 * j, elF=30 + 18 * j)
    return p

def orrin_close(i):
    lv = lamp_level(i); f = C.clamp01(lv); img = C.core.canvas(W, H, '#06090f')
    cy = LCY + (1 - f) * LRY * .8; grow = .25 + .75 * lv ** .7
    for r, k in ((540, .05), (372, .075), (222, .11)):                         # the pool of light: three flat rings of paper
        img = add(img, draw.disc(W, H, LCX, cy, min(r * grow, 560)), C.LAMP, k * lv)             # never as far as the name card
    if lv > 1.3:                                                               # the flare
        rays = [A((LCX + 120 * math.cos(a - .035), LCY + 120 * math.sin(a - .035)), (LCX + 120 * math.cos(a + .035), LCY + 120 * math.sin(a + .035)),
                  (LCX + 500 * math.cos(a), LCY + 500 * math.sin(a))) for a in np.radians(np.arange(8, 360, 30))]   # short of the name card
        img = add(img, draw.raster(rays, W, H), C.LAMP, .22 * (lv - 1))
    img = draw.paint(img, FRAME, '#04060a')
    img = draw.paint(img, LENS, '#131a26')                                      # the glass, unlit
    yw = LCY - LRY + (1 - f) * 2 * LRY                                          # the light stands in the lens like water: it sinks with his head
    lit = LENS * np.clip((YY - yw) / 2 + .5, 0, 1)
    k = .3 + 5.0 * lv ** .8
    img = emit(img, lit, lamp_rgb(k))
    img = C.light(img, np.minimum(BULL, lit), '#fff0c4', k * 1.5)
    img = draw.paint(img, np.maximum(BANDS, BULLRING * LENS), '#0a0d14', .85)
    img = figc(img, 'keeper', orrin_pose(i), OX, 980, 860, rim=(C.LAMP, 1.2 * lv, 4))
    return C.name_card(img, 'keeper', C.clamp01((i - 40) / 8), 'l') if i >= 40 else img       # the card waits until he is awake again

# =================================================================== the car deck of the M/V Kittiwake
DEE = dict(C.CAST['dee']['pose'])                                               # at rest: the punch hangs in her near hand
REACH = dict(DEE, shN=-15, elN=120, wrN=0, lean=-1)                             # the punch up at the card
SQUEEZE = dict(REACH, shN=-11, elN=114, lean=1, head=8)
PAS = dict(C.CAST['passenger']['pose'])
PAPER, HOLE, STEEL, CHAD = '#d8d2bf', '#141b26', '#7c8798', '#fff6cf'

def reach(i, punches):
    """How far Dee's arm is up (0..1), and whether the punch is closed, for punches on the given poses."""
    for P in punches:
        r = i - P
        if -3 <= r <= 3:
            return {-3: .3, -2: .72, -1: 1.0, 0: 1.0, 1: 1.0, 2: .66, 3: .28}[r], r == 0
    return 0.0, False

def dee_pose(a, shut): return SQUEEZE if shut else C.fg.blend(DEE, REACH, a)

def grip(name, pose, x, ground, size, flip=False):
    """Where the near hand holds something, and the direction the forearm points."""
    w = jpx(name, pose, 'wristN', x, ground, size, flip); h = jpx(name, pose, 'handN', x, ground, size, flip)
    return w + (h - w) * .45, (h - w) / max(float(np.hypot(*(h - w))), 1e-6)

def stage(size, X0, ground, ppose):
    """Where Dee stands, and how the passenger at X0 holds his card, so that her punch closes on it."""
    k = size / 860.0
    g, n = grip('dee', REACH, 0, ground, size); bite = g + n * 60 * k
    best = None
    for el in range(84, 150, 2):
        pp = dict(ppose, shN=-20, elN=el, wrN=0); pg, _ = grip('passenger', pp, X0, ground, size, flip=True)
        if best is None or abs(pg[1] - bite[1]) < best[0]: best = (abs(pg[1] - bite[1]), pp, pg)
    _, pp, pg = best
    dee_x = float(pg[0] - 44 * k - bite[0])
    return dee_x, {j: pp[j] for j in ('shN', 'elN', 'wrN')}, bite + np.array((dee_x, 0), np.float32)

def card(img, pg, k, holes, shift=0.0):
    """The passenger's card in his hand (he faces left); holes = places along it already punched."""
    x1, y = pg[0] + 8 * k - shift, pg[1]
    img = fill(img, [box(x1 - 64 * k, y - 19 * k, x1, y + 19 * k)], PAPER)
    if holes:
        img = fill(img, [box(x1 - 64 * k + h * k - 7 * k, y - 10 * k, x1 - 64 * k + h * k + 7 * k, y + 10 * k) for h in holes], HOLE)
    return img

def punch(img, g, n, k, shut):
    """Dee's ticket punch, in her fist at g and pointing along n."""
    o = np.array((-n[1], n[0]), np.float32); p0 = g - n * 22 * k; tip = g + n * 68 * k
    gap = (1.5 if shut else 8.0) * k
    polys = [np.array([p0 - o * (gap + 6 * k), tip - o * (gap + 6 * k), tip - o * gap, p0 - o * gap + n * 34 * k], np.float32),
             np.array([p0 + o * gap + n * 34 * k, tip + o * gap, tip + o * (gap + 6 * k), p0 + o * (gap + 6 * k)], np.float32),
             np.array([g - o * 10 * k + n * 12 * k, g - o * 10 * k + n * 28 * k, g + o * 10 * k + n * 28 * k, g + o * 10 * k + n * 12 * k], np.float32)]
    return fill(img, polys, STEEL)

def chad(img, at, k, t):
    """The piece punched out: the shape of a window, and lit. It falls."""
    if t < 0 or t > 9: return img
    c = np.array((at[0] - 2.5 * k * t, at[1] + (30 + 5.4 * t * t) * k), np.float32)
    q = rot(box(c[0] - 8 * k, c[1] - 11 * k, c[0] + 8 * k, c[1] + 11 * k), c, -13 * t)
    return C.light(img, draw.raster([q], W, H), CHAD, 10.0 if t < 2 else 6.0)

# ------------------------------------------------------------------- wide (48-71)
WS, WG = 250, 628
X0 = 560.0                                                                      # where a passenger stops
STRIDE = 12 * C.walk_speed('passenger', WS)
DEE_X, OFFER, BITE = stage(WS, X0, WG, C.walk_pose('passenger', 0.0))
LDX = float(round((DEE_X + X0) / 2))                                            # the work lamp hangs over their hands

def _deck():
    sh.setup(W, H, 6)
    img = C.core.canvas(W, H, '#0a0f18')
    sea = C.harbour(hz=392, seed=3)                                             # the open side of the deck: the Sound, and somebody on the rail
    sea = C.heron(sea, 104, 470, s=.075)
    img = C.comp.over(img, C.comp.mask(sea, draw.rect(W, H, 0, 150, 190, 566)))
    img = fill(img, [box(0, 468, 190, 472), box(0, 516, 190, 519), box(38, 470, 42, 566), box(160, 470, 164, 566)], '#070a10')
    img = fill(img, [box(x, 124, x + 2, 566) for x in (190, 430, 670, 910, 1150)], '#0e1521')
    img = C.write(img, (792, 196), 'M/V KITTIWAKE', 56, '#141d2b', track=8)
    img = C.write(img, (794, 266), 'NO SMOKING ON THE CAR DECK', 22, '#141d2b', track=5)
    img = fill(img, [box(0, 0, W, 118)], '#05070c'); img = fill(img, [box(0, 118, W, 124)], '#111927')
    img = fill(img, [box(0, 566, W, H)], '#0d1521'); img = fill(img, [box(0, 566, W, 568)], '#182233'); img = fill(img, [box(0, 664, W, 668)], '#2e2b20')
    for dx, k in ((265, .085), (150, .075)):                                    # the lamp's light on the bulkhead and the deck: flat paper cones
        img = add(img, draw.raster([A((LDX - 16, 160), (LDX + 16, 160), (LDX + dx, 566), (LDX - dx, 566))], W, H), C.LAMP, k)
        img = add(img, draw.raster([ellipse(LDX, 630, dx * 1.25, dx * .2)], W, H) * (YY >= 566), C.LAMP, k)
    img = fill(img, [box(LDX - 3, 124, LDX + 3, 142), A((LDX - 9, 140), (LDX + 9, 140), (LDX + 21, 159), (LDX - 21, 159))], '#04060a')
    return C.light(img, draw.disc(W, H, LDX, 162, 8), C.LAMP, 7.0)
DECK = _deck()
def _chain(posts, top, base, sag, w):
    polys = []
    for x in posts:
        polys += [box(x - w * 1.6, top, x + w * 1.6, base), ellipse(x, top - w, w * 2.6, w * 2.6, 14), box(x - w * 4, base - w * 2, x + w * 4, base)]
    for a, b in zip(posts[:-1], posts[1:]):
        u = np.linspace(0, 1, 16); polys.append(sh.ribbon(np.c_[a + (b - a) * u, top + 4 + sag * (1 - (2 * u - 1) ** 2)], w=w, taper=(0, 0), wob=0))
    return draw.raster(polys, W, H)
sh.setup(W, H, 6)
CHAIN_W = _chain([X0 - 50, X0 + 190, X0 + 430, X0 + 670, X0 + 910], 606, 696, 30, 2.6)       # it ends between Dee and whoever is next

VW = C.walk_speed('passenger', WS)
ARRIVE = (51, 63, 75, 87)        # the pose on which each passenger stops at the chain: punched 3 poses later, walks on 5 poses later

def dee_wide(i):
    img = DECK.copy(); k = WS / 860.0
    a, shut = reach(i, (54, 66))
    for T in reversed(ARRIVE):
        if i < T:                                                               # walking up, the card coming out
            x = X0 + VW * (T - i); g = ((i - T) / 12.0) % 1.0; w = C.clamp01(1 - (T - i) / 4.0)
        elif i <= T + 5:                                                        # standing at the chain, card held out
            x = X0; g = 0.0; w = 1.0
        else:                                                                   # punched: walks on, behind Dee, at walking speed
            x = X0 - VW * (i - T - 5); g = ((i - T - 5) / 12.0) % 1.0; w = C.clamp01(1 - (i - T - 5) / 3.0)
        if x < -70 or x > W + 70: continue
        base = C.walk_pose('passenger', g)
        pose = C.fg.blend(base, dict(base, **OFFER), w) if w > 0 else base
        img = figc(img, 'passenger', pose, x, WG, WS, flip=True)
        img = card(img, grip('passenger', pose, x, WG, WS, flip=True)[0], k, [12] if i >= T + 3 else [])
    pose = dee_pose(a, shut)                                                    # Dee last: nobody is ever drawn over her
    img = figc(img, 'dee', pose, DEE_X, WG, WS)
    img = punch(img, *grip('dee', pose, DEE_X, WG, WS), k, shut)
    for P in (54, 66):
        img = chad(img, BITE, k * 1.5, i - P)
        if 0 <= i - P < 2:                                                      # director's pass: the punch is struck, like a note
            img = C.light(img, draw.disc(W, H, BITE[0], BITE[1], 13 - 5 * (i - P)), C.LAMP, 12.0)
    return draw.paint(img, CHAIN_W, '#1d2838')

# ------------------------------------------------------------------- close (72-95)
CX0 = 636.0
CDEE_X, COFFER, CBITE = stage(860, CX0, 980, PAS)
CPAS = dict(PAS, **COFFER)
CLX = float(round((CDEE_X + CX0) / 2 + 10))

def _deck_close():
    sh.setup(W, H, 7)
    img = C.core.canvas(W, H, '#0a0f18')
    img = fill(img, [box(x, 0, x + 4, H) for x in (120, 1010)], '#0e1521')
    img = C.write(img, (742, 150), 'M/V KITTIWAKE', 104, '#131c29', track=14)
    for dx, k in ((455, .085), (270, .075)):
        img = add(img, draw.raster([A((CLX - 44, 92), (CLX + 44, 92), (CLX + dx, H), (CLX - dx, H))], W, H), C.LAMP, k)
    img = fill(img, [box(CLX - 7, 0, CLX + 7, 40), A((CLX - 26, 36), (CLX + 26, 36), (CLX + 58, 90), (CLX - 58, 90))], '#04060a')
    img = C.light(img, draw.disc(W, H, CLX, 96, 22), C.LAMP, 7.0)
    return draw.paint(img, _chain([820, 1330], 652, 730, 36, 6.0), '#1d2838')
DECK_C = _deck_close()

def dee_close(i):
    img = DECK_C.copy(); a, shut = reach(i, (78, 90))
    slide = 20 * C.ease(C.clamp01((i - 82) / 3), 'inout')                      # he offers a fresh corner for the second punch
    ppose = dict(CPAS, head=10 if i >= 79 else 2)
    img = figc(img, 'passenger', ppose, CX0, 980, 860, flip=True, glow=6.0)
    img = card(img, grip('passenger', ppose, CX0, 980, 860, flip=True)[0], 1.0, ([12] if i >= 78 else []) + ([32] if i >= 90 else []), shift=slide)
    pose = dee_pose(a, shut)
    img = figc(img, 'dee', pose, CDEE_X, 980, 860)
    img = punch(img, *grip('dee', pose, CDEE_X, 980, 860), 1.0, shut)
    for P in (78, 90):
        img = chad(img, CBITE, 1.0, i - P)
    return C.name_card(img, 'dee', C.clamp01((i - 72) / 16), 'r')

def frame(i):
    i = int(i)
    img = orrin_wide(i) if i < 24 else orrin_close(i) if i < 48 else dee_wide(i) if i < 72 else dee_close(i)
    img = np.asarray(img, np.float32); img[..., 3] = 1.0
    return img
