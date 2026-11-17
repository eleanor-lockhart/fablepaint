"""Two islands and the water between them. One model, in metres; x east, y north, z up; the sea is z = 0.

    here(lamp, lever, dial)     the near island as it is in that state: ground, jetty, shelter, beacon, spyglass
    there(lit, arm)             the far island: a rock, a tower, one window, and her room behind it
    lights(lamp, lit)           the lamps that are burning
    PLACE                       where things are
    height(x, y)                the ground (it is a height field: a hill that is not steps)
"""
import sys, math
from functools import lru_cache
from pathlib import Path
HERE = Path(__file__).resolve().parent; sys.path.insert(0, str(HERE)); sys.path.insert(1, str(HERE.parent)); sys.path.insert(2, str(HERE.parents[2]))
import numpy as np
from backlot.space import Set, Solid
from backlot import depth as D
from backlot.depth import HOLE
import deep, kit, sprites as SP
from deep import blend

ROCK, ROCK2, WET = blend(0x9, 0x3, .3), blend(0x8, 0x3, .35), blend(0x2, 0x0, .2)
TURF, TURF2 = blend(0xE, 0x9, .5), blend(0xE, 0x8, .55)
WOOD, WOOD2, GAP = blend(0xE, 0x2, .5), blend(0xE, 0x2, .64), blend(0x2, 0x0, .4)
STONE, STONE2 = blend(0x9, 0x3, .3), blend(0x9, 0x3, .5)
BRASS = blend(0xE, 0xF, .35); SEAP = blend(0x1, 0x2, .5); PAGE = blend(0xA, 0xE, .12)
BX, BY = 290.0, -70.0                                             # the far island
PLACE = dict(jetty=(-38.0, 0.0), shelter=(-6.0, 3.0), beacon=(18.0, 0.0), lever=(16.2, -1.3), dial=(16.2, 1.3), lookout=(27.0, -3.0), glass=(28.2, -2.6))
FAR_ROT = -math.degrees(math.atan2(-2.6 - BY, 290.0 - 28.2))            # her tower is turned so that its window looks straight at the spyglass
def far_pt(p):
    """A point given in the far island's own square-on coordinates, as it is in the world."""
    a = math.radians(FAR_ROT); x, y = p[0] - BX, p[1] - BY; return (BX + x * math.cos(a) - y * math.sin(a), BY + x * math.sin(a) + y * math.cos(a), p[2])

def _pads(x, y, h):
    for (px, py), r, z in ((PLACE['shelter'], 3.4, 2.3), (PLACE['beacon'], 3.6, 8.0), (PLACE['lookout'], 2.4, 6.3)):
        d = np.hypot(x - px, y - py); w = np.clip((r + 1.6 - d) / 1.6, 0, 1); w = w * w * (3 - 2 * w); h = h * (1 - w) + z * w
    return h
def height(x, y):
    """The ground under (x, y). Below zero is under the sea."""
    x = np.asarray(x, float); y = np.asarray(y, float); e = 1 - (x / 34.0) ** 2 - (y / 15.5) ** 2
    h = 3.2 * np.sign(e) * np.abs(e) ** .8 - .7 + 6.4 * np.exp(-((x - 18) ** 2 + y ** 2) / 60.0) + 2.4 * np.exp(-((x - 27) ** 2 + (y + 3) ** 2) / 26.0) + 1.1 * np.exp(-((x + 6) ** 2 + (y - 3) ** 2) / 40.0)
    h = h + .28 * np.sin(.9 * x + 1.3) * np.cos(1.1 * y) + .18 * np.sin(2.3 * x + .7 * y)
    return _pads(x, y, np.where(e > -.6, h, -3.0))

@lru_cache(maxsize=None)
def skins():
    s = {}
    s['rock'] = deep.speckle(32, 32, ROCK, [ROCK2, STONE2], p=.3, seed=2); s['wet'] = deep.speckle(16, 16, WET, [ROCK2], p=.12, seed=3)
    s['turf'] = deep.speckle(32, 32, TURF, [TURF2, ROCK], p=.34, seed=4); s['boards'] = deep.planks(WOOD, WOOD2, GAP, width=4, length=40, along='u', seed=5)
    s['stone'] = deep.blocks(STONE, STONE2, bw=8, bh=5, seed=6, chips=(ROCK2,)); s['roof'] = deep.planks(WOOD2, blend(0x2, 0xE, .25), GAP, width=3, length=24, along='v', seed=7)
    for n in range(10):                                                   # the dial: a brass face, one figure in its window
        d = np.full((22, 22), BRASS, np.uint8); yy, xx = np.mgrid[:22, :22]; r = np.hypot(xx - 10.5, yy - 10.5); d[r > 10.6] = HOLE; d[(r > 8.6) & (r <= 10.6)] = WOOD2
        d[5:17, 6:16] = 0x0; g = kit.glyph(str(n)); d[7:15, 7:15][g] = 0xF if False else 0xA
        for k in range(10):
            a = 2 * math.pi * k / 10; x, y = int(round(10.5 + 9.6 * math.sin(a))), int(round(10.5 - 9.6 * math.cos(a))); d[y, x] = 0xA if k == n else 0x0
        s['dial%d' % n] = d
    b = np.full((7, 12), PAGE, np.uint8); b[:, 5:7] = WOOD2; b[1:6, 7:11] = 0x1; b[1, 1:4] = b[3, 1:5] = b[5, 1:4] = 0x6; s['book'] = b; b2 = b.copy(); b2[1:6, 7:11] = 0x2; b2[3, 9] = 0xF; s['book_up'] = b2
    wn = np.full((48, 28), HOLE, np.uint8); yy, xx = np.mgrid[:48, :28]                                               # her window's tracery: a pointed arch, a mullion, a rose
    arch = (yy >= 14) | (np.hypot(xx - 13.5, yy - 14) <= 14); wn[~arch] = STONE2; edge = arch & ((xx < 2) | (xx > 25) | (np.abs(np.hypot(xx - 13.5, yy - 14) - 13) < 1.2) & (yy < 14)); wn[edge] = STONE2
    wn[14:, 13:15] = STONE2; ring = np.abs(np.hypot(xx - 13.5, yy - 9) - 5) < .9; wn[ring & arch] = STONE2
    for a in range(6): t = a * math.pi / 3; wn[np.clip((9 + np.arange(5) * math.cos(t)).round().astype(int), 0, 47), np.clip((13.5 + np.arange(5) * math.sin(t)).round().astype(int), 0, 27)] = STONE2
    s['tracery'] = wn
    return s

@lru_cache(maxsize=None)
def ground():
    """The near island: triangles on a 1.5 m grid, sorted into turf, rock and wet rock by height and slope."""
    K = skins(); xs = np.arange(-37.5, 37.6, 1.5); ys = np.arange(-18.0, 18.1, 1.5); Hh = height(xs[:, None], ys[None, :]); faces = dict(turf=[], rock=[], wet=[])
    for i in range(len(xs) - 1):
        for j in range(len(ys) - 1):
            P = [(xs[a], ys[b], float(Hh[a, b])) for a, b in ((i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1))]
            if max(p[2] for p in P) < -.25: continue
            for tri in ((P[0], P[1], P[2]), (P[0], P[2], P[3])):
                a, b, c = (np.array(p) for p in tri); n = np.cross(b - a, c - a); n = n / (np.linalg.norm(n) + 1e-12); z = (a[2] + b[2] + c[2]) / 3
                faces['wet' if z < .45 else ('turf' if abs(n[2]) > .9 and z > 1.3 else 'rock')].append(tri)
    out = []
    for name, skin in (('turf', K['turf']), ('rock', K['rock']), ('wet', K['wet'])):
        s = Solid('ground.' + name, faces[name]); D.paint(s, skin=skin); out.append(s)
    return tuple(out)

def _box(S, name, c, size, **kw):
    x, y, z = c; a, b, h = size; return D.paint(S.box(name, (x - a / 2, x + a / 2), (y - b / 2, y + b / 2), (z, z + h)), **kw)

@lru_cache(maxsize=None)
def fixed():
    """What never changes on the near island, and the sea."""
    K = skins(); S = Set('here')
    D.paint(S.box('sea', (-900, 900), (-900, 900), (-1.0, 0.0)), index=SEAP)
    D.paint(S.box('jetty', (-44, -30.5), (-1.1, 1.1), (.75, .9)), skin=K['boards'])
    for i, x in enumerate((-43.5, -39, -34.5, -31)):
        for y in (-1.0, 1.0): _box(S, 'jetty.post%d%d' % (i, y > 0), (x, y, -1.0), (.22, .22, 2.3 if i else 2.9), index=WOOD2)
    px = np.linspace(-30.0, 14.5, 34); py = 1.6 * np.sin((px + 30) / 44.5 * math.pi) * np.where(px < -6, 1.2, .5)             # stepping stones up the island
    for i, (x, y) in enumerate(zip(px, py)):
        if np.hypot(x - PLACE['shelter'][0], y - PLACE['shelter'][1]) < 2.2: continue
        _box(S, 'step.%d' % i, (x, y, float(height(x, y)) - .04), (.8, .7, .12), index=STONE if i % 2 else STONE2)
    sx, sy = PLACE['shelter']; z = 2.3                                                                                   # the shelter: a roof on four posts, a desk, the log
    for i, (dx, dy) in enumerate(((-1.6, -1.2), (1.6, -1.2), (-1.6, 1.2), (1.6, 1.2))): _box(S, 'shelter.post%d' % i, (sx + dx, sy + dy, z), (.16, .16, 2.3), index=WOOD2)
    D.paint(S.gable('shelter.roof', (sx - 1.8, sx + 1.8), (sy - 1.4, sy + 1.4), z + 2.3, z + 3.2, along='x', over=.35), skin=K['roof'])
    _box(S, 'desk.top', (sx + .2, sy + .5, z + .74), (1.5, .75, .07), index=WOOD);
    for i, (dx, dy) in enumerate(((-.45, .2), (.85, .2), (-.45, .8), (.85, .8))): _box(S, 'desk.leg%d' % i, (sx + dx, sy + dy, z), (.08, .08, .74), index=WOOD2)
    _box(S, 'stool', (sx + .2, sy - .45, z), (.4, .4, .45), index=WOOD2)
    bx, by = PLACE['beacon']; z = 8.0                                                                                    # the beacon: a stone plinth, a cage, the lamp in it
    D.paint(S.cylinder('beacon.plinth', (bx, by), 1.0, z, z + 2.2, r1=.8, n=8), skin=K['stone'])
    for i in range(4): a = math.pi / 4 + i * math.pi / 2; _box(S, 'beacon.bar%d' % i, (bx + .55 * math.cos(a), by + .55 * math.sin(a), z + 2.2), (.07, .07, 1.0), index=0x1)
    D.paint(S.cylinder('beacon.cap', (bx, by), .85, z + 3.2, z + 3.7, r1=.1, n=8), index=0x1)
    lx, ly = PLACE['lever']; _box(S, 'lever.base', (lx, ly, float(height(lx, ly)) - .1), (.4, .4, .9), index=0x8)
    dx, dy = PLACE['dial']; _box(S, 'dial.post', (dx, dy, float(height(dx, dy)) - .1), (.22, .22, 1.2), index=0x8)
    gx, gy = PLACE['glass']; gz = float(height(gx, gy))                                                                  # the spyglass on its three legs
    for i in range(3): a = i * 2 * math.pi / 3 + .4; S.tube('glass.leg%d' % i, [(gx + .45 * math.cos(a), gy + .45 * math.sin(a), gz - .05), (gx, gy, gz + 1.25)], .035, n=4); D.paint(S.solids[-1], index=WOOD2)
    aim = np.array([BX - gx, BY - gy, 22.0 - gz - 1.4]); aim = aim / np.linalg.norm(aim); c = np.array([gx, gy, gz + 1.4])
    S.tube('glass.tube', [c - aim * .45, c + aim * .55], .07, n=6); D.paint(S.solids[-1], index=BRASS)
    return tuple(S.solids)

def here(lamp=False, lever=False, dial=0, linked=False):
    """The near island in one state."""
    K = skins(); S = Set('state'); bx, by = PLACE['beacon']; z = 8.0
    _box(S, 'lamp', (bx, by, z + 2.45), (.5, .5, .55), index=0xF if lamp else 0x8, glow=1.0 if lamp else 0.0, cast=False)
    lx, ly = PLACE['lever']; lz = float(height(lx, ly)) + .8; a = math.radians(35 if lever else -35); tip = np.array([lx, ly + .8 * math.sin(a), lz + .8 * math.cos(a)]); O = np.array([lx, ly, lz])
    D.paint(S.hexa('lever', [O + (-.04, -.04, 0), O + (.04, -.04, 0), O + (.04, .04, 0), O + (-.04, .04, 0)], [tip + (-.04, -.04, 0), tip + (.04, -.04, 0), tip + (.04, .04, 0), tip + (-.04, .04, 0)]), index=0xD)
    _box(S, 'lever.knob', (tip[0], tip[1], tip[2] - .02), (.16, .16, .16), index=0xA)
    dx, dy = PLACE['dial']; dz = float(height(dx, dy)) + 1.0; d = K['dial%d' % dial]
    S.add(D.panel('dial', d, (dx - .12, dy + .55, dz + 1.1), (0, -1, 0), (0, 0, -1), cast=False))
    sx, sy = PLACE['shelter']; b = K['book_up' if linked else 'book']
    S.add(D.panel('book', b, (sx - .1, sy + .68, 2.3 + .83), (1, 0, 0), (0, -1, 0), cast=False))
    return list(ground()) + list(fixed()) + S.solids

@lru_cache(maxsize=None)
def rock_there():
    """The far island: a stack of rock, a gothic tower with one window, and the room behind the window."""
    K = skins(); S = Set('there'); r = np.random.default_rng(5)
    for i, (dx, dy, rad, h) in enumerate(((0, 0, 15, 15), (-9, 6, 9, 8), (10, -5, 10, 10), (3, 9, 8, 6))):
        D.paint(S.cylinder('far.rock%d' % i, (BX + dx, BY + dy), rad, -1, h, r1=rad * .55, n=9), index=ROCK2, texel=.4)
    x0, x1, y0, y1 = BX - 3, BX + 3, BY - 3, BY + 3; zb, zt = 14.0, 36.0; wz0, wz1, wy = 26.0, 28.4, .7                 # the tower; the window is in its west face
    for name, x, y in (('n', (x0, x1), (y1 - .4, y1)), ('s', (x0, x1), (y0, y0 + .4)), ('e', (x1 - .4, x1), (y0, y1))): D.paint(S.box('far.wall.' + name, x, y, (zb, zt)), index=STONE2, texel=.2)
    D.paint(S.box('far.wall.w.lo', (x0, x0 + .4), (y0, y1), (zb, wz0)), index=STONE2, texel=.2); D.paint(S.box('far.wall.w.hi', (x0, x0 + .4), (y0, y1), (wz1, zt)), index=STONE2, texel=.2)
    D.paint(S.box('far.wall.w.l', (x0, x0 + .4), (y0, BY - wy), (wz0, wz1)), index=STONE2, texel=.2); D.paint(S.box('far.wall.w.r', (x0, x0 + .4), (BY + wy, y1), (wz0, wz1)), index=STONE2, texel=.2)
    D.paint(S.prism('far.spire', [(x0 - .3, y0 - .3), (x1 + .3, y0 - .3), (x1 + .3, y1 + .3), (x0 - .3, y1 + .3)], zt, zt + 9, top=[(BX - .1, BY - .1), (BX + .1, BY - .1), (BX + .1, BY + .1), (BX - .1, BY + .1)]), index=0x1, texel=.2)
    for i, (cx, cy) in enumerate(((x0, y0), (x0, y1), (x1, y0), (x1, y1))): D.paint(S.prism('far.pin%d' % i, [(cx - .5, cy - .5), (cx + .5, cy - .5), (cx + .5, cy + .5), (cx - .5, cy + .5)], zt, zt + 3.2, top=[(cx - .05, cy - .05), (cx + .05, cy - .05), (cx + .05, cy + .05), (cx - .05, cy + .05)]), index=0x1, texel=.2)
    for i, z in enumerate((20.0, 31.5)): D.paint(S.box('far.band%d' % i, (x0 - .15, x1 + .15), (y0 - .15, y1 + .15), (z, z + .35)), index=STONE, texel=.2)
    D.paint(S.box('room.floor', (x0, x1), (y0, y1), (wz0 - .2, wz0)), index=WOOD2); D.paint(S.box('room.back', (x0 + 2.6, x0 + 2.7), (y0, y1), (wz0, wz1 + .6)), skin=deep.bricks(blend(0x9, 0x3, .45), 0x2, bw=6, bh=3, seed=8))
    D.paint(S.box('room.desk', (x0 + .9, x0 + 1.5), (BY - .68, BY + .68), (wz0 + .62, wz0 + .7)), index=WOOD)
    S.add(D.panel('her.book', np.array([[PAGE, PAGE, WOOD2, PAGE, PAGE]] * 3, np.uint8), (x0 + 1.0, BY - .2, wz0 + .72), (0, 1, 0), (1, 0, 0), cast=False))
    S.add(D.panel('tracery', K['tracery'], (x0 - .02, BY - wy, wz1), (0, 1, 0), (0, 0, -1), cast=False))
    return tuple(S.solids)

def there(lit=False, arm=False, spider=0.0):
    """Her side in one state: the lamp on her desk, and her."""
    S = Set('her'); x0 = BX - 3; wz0 = 26.0
    _box(S, 'her.lamp', (x0 + 1.15, BY + .44, wz0 + .7), (.15, .15, .3), index=0xF if lit else 0x8, glow=1.0 if lit else 0.0, cast=False)
    S.add(D.panel('her.glass', np.full((48, 28), 0xF if lit else 0x1, np.uint8), (x0 + .25, BY - .7, wz0 + 2.4), (0, 1, 0), (0, 0, -1), glow=1.0 if lit else 0.0, cast=False, on='far'))
    w = deep.sprite(SP.WITCH); S.add(D.card('her', w, (x0 + 1.9, BY - .16, wz0 + .28), (0, 1, 0), flat=True, cast=False))
    sp = deep.sprite(SP.SPIDER); S.add(D.card('spider', sp, (x0 + .55, BY + .22, wz0 + 1.55 - spider), (0, 1, 0), flat=True, cast=False, texel=.025))     # her familiar, on its thread
    S.add(D.panel('thread', np.full((int((.85 + spider - .25) / .025), 1), 0x9, np.uint8), (x0 + .55, BY + .22, wz0 + 2.4), (0, 1, 0), (0, 0, -1), texel=.025, cast=False))
    return [D.turned(q, FAR_ROT, about=(BX, BY)) for q in list(rock_there()) + S.solids]

def lights(lamp=False, lit=False):
    out = [D.Light((-500, -320, 260), power=.75, reach=1e6, shadow=False)]                                               # what is left of the day, from the west
    bx, by = PLACE['beacon']
    if lamp: out.append(('beacon', (bx, by, 8.0 + 2.75)))
    if lit: out.append(D.Light(far_pt((BX - 1.75, BY + .44, 27.0)), power=2.2, reach=2.4, shadow=False))
    return out
