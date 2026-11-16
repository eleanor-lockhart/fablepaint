"""Base Case: the house. One model, in metres, of the parts of it the film goes through.

x is east, y is north, z is up. The ground floor is z = 0. The ground outside is 0.6 m lower, the basement floor
2.4 m lower. The world is cut off along the house's south face, like a model on a shelf: from the south the
basement is seen in section, with the earth it is dug into.

    S = build()              the things that never move (cached)
    lid(angle)               the trap door in the pantry floor, hinged on its east edge: 0 shut, 80 open
    windows(lit)             the windows of the south face, lit or dark
    screen(skin)             the monitor's glass, showing `skin` (320 x 180) or one flat paint
    CAMS                     named cameras; SPOT, the places things stand

The basement is the one in the reference photograph (kept out of the repository): a red steel post on a concrete
pad, a brick chimney, a furnace with a sheet-metal plenum, a white water heater, a shop light, painted block
walls. The pantry and its trap door are the ones already drawn in gallery/house.
"""
import sys, math
from pathlib import Path
HERE = Path(__file__).resolve().parent; sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(HERE.parents[2]))
import numpy as np
from backlot.space import Set, Camera, Solid
from backlot import depth as D
import deep as X
from deep import blend

GRADE, FLOOR, TX = -.6, -2.4, .05
# ------------------------------------------------------------------ paints: registers, and blends of two
WD1, WD2, WD3, PINE, PINE2 = blend(0xE, 1, .5), blend(0xE, 1, .65), blend(0xE, 0, .8), blend(0xE, 0xA, .45), blend(0xE, 0xA, .25)
BR, BR2, BR3, MORT = blend(0xE, 0xD, .35), blend(0xE, 0xD, .6), blend(0xE, 1, .3), blend(9, 8, .5)
CONC, CONC2, CONC3 = 8, blend(8, 1, .4), blend(8, 9, .5)
JOINT, FURN, FURN2, BEIGE, BEIGE2 = blend(9, 8, .6), blend(8, 4, .5), blend(8, 4, .8), blend(0xA, 0xE, .16), blend(9, 0xE, .2)
EARTH, EARTH2, EARTH3, ROOT = blend(1, 0, .35), blend(2, 0, .5), blend(1, 0, .7), blend(0xE, 0, .7)
SNOW2, SIDE1, SIDE2, SIDE3, ROOF1, ROOF2 = blend(0xA, 0xB, .22), blend(0xE, 1, .62), blend(0xE, 1, .72), blend(0xE, 0, .85), blend(0xD, 1, .6), blend(0xD, 1, .75)
NIGHT, NIGHT2 = blend(1, 0, .5), blend(2, 1, .5)
PAPER, PAPER2 = blend(9, 3, .4), blend(9, 0xD, .3)

def _earth(seed=7):
    r = np.random.default_rng(seed); a = X.speckle(128, 128, EARTH, [EARTH2, EARTH3, 1], .34, seed)
    for _ in range(26):                                             # stones
        y, x, w = int(r.integers(4, 124)), int(r.integers(4, 122)), int(r.integers(2, 5)); a[y:y + max(w - 1, 1), x:x + w] = 8 if r.random() > .4 else CONC2; a[y, x:x + w] = 9 if r.random() > .6 else 8
    for _ in range(9):                                              # roots, wandering down
        x, y = int(r.integers(128)), int(r.integers(128))
        for k in range(int(r.integers(12, 40))): a[(y + k) % 128, x % 128] = ROOT; x += int(r.integers(-1, 2))
    a[40] = np.where(r.random(128) > .3, EARTH3, a[40]); a[90] = np.where(r.random(128) > .4, 2, a[90])      # two strata
    return a
def _jars(n, seed):
    """A shelf's worth of preserves, one texel = 5 cm: n texels long, 7 high."""
    r = np.random.default_rng(seed); a = np.full((7, n), X.HOLE, np.uint8); x = int(r.integers(0, 2))
    while x < n - 3:
        w, h = int(r.integers(3, 6)), int(r.integers(4, 8)); w = min(w, n - x)
        body = [0xE, 0xD, 3, 0xC, 9, BR2, 2, PINE][int(r.integers(8))]; lid = [8, 9, 0xA, 0xD, 1][int(r.integers(5))]
        a[7 - h:, x:x + w] = body; a[7 - h, x:x + w] = lid
        if h > 4 and w > 2: a[7 - h + 2:7 - h + 4, x + 1:x + w - 1] = 0xA if r.random() > .3 else 9; a[7 - h + 2, x + 1] = 0
        a[7 - h + 1:, x] = blend(body, 0xA, .35) if body < 16 else body
        x += w + int(r.integers(1, 3))
    return a
def _window(lit, w=16, h=24):
    a = np.full((h, w), 0xF if lit else NIGHT, np.uint8); a[[0, 1, h - 2, h - 1]] = 0xA; a[:, [0, 1, w - 2, w - 1]] = 0xA; a[h // 2 - 1:h // 2 + 1] = 0xA; a[:, w // 2 - 1:w // 2 + 1] = 0xA
    if not lit: a[3:6, 3:5] = NIGHT2; a[13:15, 10:13] = NIGHT2
    else: a[h - 8:h - 2, 2:w - 2][::2, ::3] = blend(0xF, 0xE, .5)     # something on the sill
    return a
def _spruce(seed, w=64, h=150):
    """A spruce at night: tiers of dark boughs with snow lying on each."""
    r = np.random.default_rng(seed); a = np.full((h, w), X.HOLE, np.uint8); cx = w // 2
    for y in range(h - 8, h): a[y, cx - 1:cx + 2] = WD3
    tier = 0
    for y in range(2, h - 8):
        half = int(2 + (y / (h - 8)) ** .9 * (w // 2 - 3)); wob = int(3 * math.sin(y * .9 + seed)); k = (y % 11)
        hw = max(1, half - (10 - k) // 2 + wob // 2)
        a[y, cx - hw:cx + hw + 1] = NIGHT if (y + seed) % 3 else 1
        if k == 0:                                                   # a bough's upper edge carries snow
            for x in range(cx - hw, cx + hw + 1):
                if r.random() > .25: a[y, x] = 0xA if r.random() > .3 else 9
        elif k == 1:
            for x in range(cx - hw, cx + hw + 1):
                if r.random() > .7: a[y, x] = 9
    return a

SK = {}
def skins():
    if SK: return SK
    SK.update(
        earth=_earth(), snow=X.speckle(64, 64, 0xA, [9, SNOW2], .22, 5), conc=X.speckle(64, 64, CONC, [CONC3, CONC2, 9], .3, 6),
        block=X.blocks(9, JOINT, chips=[CONC3]), found=X.blocks(8, CONC2, chips=[9]), brick=X.bricks(BR, MORT, odd=[BR2, BR3, 0xE]),
        wood=X.planks(WD1, WD2, WD3), boards=X.planks(WD1, WD2, WD3, width=6, length=64, along='v'), pine=X.planks(PINE, PINE2, WD1, width=5),
        white=X.planks(0xA, 9, JOINT, width=3, length=40, along='v'), siding=X.planks(SIDE1, SIDE2, SIDE3, width=3, length=80),
        duct=np.array([[0xA, 9, 9, 9, 9, 9, 9, 8]] * 4 + [[8] * 8], np.uint8), furn=np.array([[FURN] * 8] * 7 + [[FURN2] * 8], np.uint8),
        roof=X.speckle(32, 32, 0xA, [9, SNOW2, ROOF1], .16, 9), paper=np.array([[9, 9, PAPER, 9, 9, 9, PAPER2, 9]] * 7 + [[9, PAPER, PAPER, PAPER, 9, PAPER2, PAPER2, PAPER2]], np.uint8), shingle=X.bricks(ROOF1, ROOF2, bw=5, bh=2, odd=[ROOF2]))
    return SK

_S = {}
PX, FX, EAST = 3.1, 3.25, 12.25          # the pantry and stairs sit 3.1 m in from the west wall; the fixtures follow; the east wall
def build():
    """The things that never move."""
    if 'S' in _S: return _S['S']
    k = skins(); S = Set('the house'); b = lambda name, x, y, z, **kw: D.paint(S.box(name, x, y, z), **kw); E = EAST
    # --- the earth, in section, and the snow lying on it
    for nm, x, y in (('w', (-16, -.25), (-.25, 20)), ('e', (E + .25, 30), (-.25, 20)), ('n', (-.25, E + .25), (5.85, 20))):
        b('earth.' + nm, x, y, (-7, GRADE), skin=k['earth'])
    b('earth.d', (-.25, E + .25), (-.25, 5.85), (-7, FLOOR - .15), skin=k['earth'])
    for nm, x, y in (('w', (-16, -.25), (-.25, 20)), ('n', (-.25, 30), (7.25, 20)), ('e', (18.75, 30), (-.25, 7.25))):
        b('snow.' + nm, x, y, (GRADE, GRADE + .1), skin=k['snow'])
    # --- the basement: slab, three walls (the fourth, 'cut', is put in only when the camera is inside)
    b('slab', (-.25, E + .25), (-.25, 5.85), (FLOOR - .15, FLOOR), skin=k['conc'])
    b('wall.n', (-.25, E + .25), (5.6, 5.85), (FLOOR, -.05), skin=k['block']); b('wall.w', (-.25, 0), (0, 5.6), (FLOOR, -.05), skin=k['block']); b('wall.e', (E, E + .25), (0, 5.6), (FLOOR, -.05), skin=k['block'])
    # --- the ground floor over it, with the hatch left open, on joists; a beam down the middle on two red posts
    h0, h1 = PX + 1.1, PX + 2.7
    for nm, x, y in (('w', (-.25, h0), (-.25, 7.25)), ('e', (h1, 14.25), (-.25, 7.25)), ('s', (h0, h1), (-.25, 4.45)), ('n', (h0, h1), (5.25, 7.25))):
        b('floor.' + nm, x, y, (-.05, 0), skin=k['boards'])
    for i in range(31):
        x = .15 + i * .4; b(f'joist.{i}', (x, x + .05), (0, 4.45 if h0 - .05 < x < h1 else 5.6), (-.28, -.05), skin=k['wood'])
    b('header', (h0 - .05, h1 + .05), (4.4, 4.45), (-.28, -.05), skin=k['wood']); b('beam', (0, E), (2.34, 2.46), (-.46, -.28), skin=k['wood'])
    for i, x in enumerate((4.1, 8.4)):
        D.paint(S.cylinder(f'post.{i}', (x, 2.4), .06, FLOOR + .08, -.46, n=8), index=0xD); b(f'post.pad.{i}', (x - .22, x + .22), (2.18, 2.62), (FLOOR, FLOOR + .08), skin=k['conc']); b(f'post.cap.{i}', (x - .1, x + .1), (2.3, 2.5), (-.5, -.46), index=8)
    # --- the stairs: twelve risers of 20 cm, eleven treads, two stringers; steep, as stairs under a hatch are
    for i in range(1, 12):
        b(f'tread.{i}', (h0 + .2 * (i - 1), h0 + .2 * i + .06), (4.45, 5.25), (-.2 * i - .04, -.2 * i), skin=k['wood'])
    for nm, y in (('s', (4.45, 4.49)), ('n', (5.21, 5.25))):
        D.paint(S.hexa('stringer.' + nm, [(h0 - .08, y[0], -.2), (h0 + 2.32, y[0], FLOOR), (h0 + 2.32, y[1], FLOOR), (h0 - .08, y[1], -.2)], [(h0 + .12, y[0], 0.0), (h0 + 2.5, y[0], FLOOR + .18), (h0 + 2.5, y[1], FLOOR + .18), (h0 + .12, y[1], 0.0)]), skin=k['wood'])
    for i, (x, w, hgt, up) in enumerate(((.15, .5, .4, 0), (.7, .45, .3, 0), (.2, .4, .3, .4), (1.25, .5, .45, 0))):
        b(f'box.{i}', (h0 + x, h0 + x + w), (5.25, 5.55), (FLOOR + up, FLOOR + up + hgt), skin=k['pine'] if i % 2 else k['wood'])
    # --- along the north wall, east of the stairs: furnace and plenum, the chimney (up through the roof), the water heater
    f = FX
    b('furnace', (f + 4.2, f + 5.0), (4.75, 5.5), (FLOOR, -1.0), skin=k['furn']); b('furnace.door', (f + 4.3, f + 4.9), (4.72, 4.75), (FLOOR + .25, FLOOR + .7), index=FURN2); b('furnace.plate', (f + 4.5, f + 4.7), (4.71, 4.72), (-1.45, -1.3), index=0xA)
    b('plenum', (f + 4.28, f + 4.92), (4.83, 5.42), (-1.0, -.5), skin=k['duct']); b('trunk', (.6, E - .4), (3.75, 4.1), (-.6, -.3), skin=k['duct'])
    b('trunk.rise', (f + 4.4, f + 4.8), (4.1, 4.83), (-.6, -.34), skin=k['duct'])
    for i, x in enumerate((1.6, 3.4, 6.9, 9.3, 11.2)): b(f'branch.{i}', (x, x + .22), (.3, 3.75), (-.5, -.3), skin=k['duct'])
    b('chimney', (f + 5.3, f + 5.9), (5.0, 5.6), (FLOOR, 5.5), skin=k['brick']); b('chimney.cap', (f + 5.24, f + 5.96), (4.94, 5.66), (5.5, 5.6), index=8)
    hx, hy = f + 5.6, 4.7                                           # the water heater stands in front of the chimney, as it does in the photograph
    D.paint(S.cylinder('heater', (hx, hy), .27, FLOOR + .12, -1.0, n=12), index=0xA); D.paint(S.cylinder('heater.band', (hx, hy), .275, -1.75, -1.5, n=12), index=0xE)
    D.paint(S.cylinder('heater.foot', (hx, hy), .2, FLOOR, FLOOR + .12, n=8), index=8)
    D.paint(S.tube('heater.flue', [(hx, hy, -1.0), (hx, hy, -.75), (hx, 5.02, -.68)], .06, n=6), index=9); D.paint(S.tube('furnace.flue', [(f + 5.0, 5.2, -1.2), (f + 5.3, 5.3, -1.1)], .08, n=6), index=9)
    D.paint(S.tube('pipe.1', [(hx - .15, hy + .05, -1.0), (hx - .15, hy + .05, -.34), (1.0, hy + .05, -.34)], .025, n=4), index=1); D.paint(S.tube('pipe.2', [(hx + .15, hy + .05, -1.0), (hx + .15, hy + .05, -.38), (f + 6.2, 5.3, -.38), (E - .1, 5.3, -.38)], .025, n=4), index=BR2)
    D.paint(S.tube('gas', [(hx - .25, hy - .15, -2.0), (hx - .42, hy - .1, -1.7), (hx - .42, hy - .1, -.34)], .02, n=4), index=0xE)
    # --- the shop light (dark until the end), the cabinet, shelves, the dehumidifier
    b('tube.box', (f + 5.5, f + 6.9), (2.92, 3.08), (-.5, -.44), index=9); D.paint(S.tube('tube.chain1', [(f + 5.6, 3.0, -.44), (f + 5.6, 3.0, -.28)], .008, n=3), index=8); D.paint(S.tube('tube.chain2', [(f + 6.8, 3.0, -.44), (f + 6.8, 3.0, -.28)], .008, n=3), index=8)
    b('cabinet', (0, .45), (1.3, 2.1), (FLOOR, -.7), skin=k['pine'])
    for i, z in enumerate((-1.9, -1.4, -.95)): b(f'eshelf.{i}', (E - .3, E), (2.3, 3.5), (z - .03, z), index=8); S.add(D.panel(f'eshelf.jars.{i}', _jars(24, 40 + i), (E - .28, 3.8, z + .35), (0, -1, 0), (0, 0, -1)))
    b('dehum', (f + 6.9, f + 7.25), (3.35, 3.65), (FLOOR, FLOOR + .6), index=BEIGE); b('dehum.grille', (f + 6.94, f + 7.21), (3.33, 3.35), (FLOOR + .3, FLOOR + .5), index=1); b('dehum.bucket', (f + 6.94, f + 7.21), (3.33, 3.35), (FLOOR + .04, FLOOR + .22), index=BEIGE2)
    # --- the west end: the washer, jars along the wall, a workbench with a pegboard
    for i, z in enumerate((-1.8, -1.3, -.8)): b(f'wshelf.{i}', (0, .28), (2.2, 5.3), (z - .04, z), skin=k['wood']); S.add(D.panel(f'wshelf.jars.{i}', _jars(60, 50 + i), (.26, 2.25, z + .35), (0, 1, 0), (0, 0, -1)))
    b('washer', (.1, .8), (.5, 1.2), (FLOOR, FLOOR + .9), index=0xA); b('washer.lid', (.1, .8), (.5, 1.2), (FLOOR + .9, FLOOR + .93), index=9); b('basket', (.95, 1.45), (.55, .95), (FLOOR, FLOOR + .35), index=PINE)
    b('bench', (1.0, 3.0), (5.0, 5.6), (FLOOR + .8, FLOOR + .86), skin=k['wood']); b('bench.leg.0', (1.05, 1.12), (5.05, 5.55), (FLOOR, FLOOR + .8), index=WD2); b('bench.leg.1', (2.88, 2.95), (5.05, 5.55), (FLOOR, FLOOR + .8), index=WD2)
    b('pegboard', (1.1, 2.9), (5.57, 5.6), (FLOOR + 1.0, FLOOR + 1.9), index=PINE); b('vise', (2.5, 2.75), (5.05, 5.2), (FLOOR + .86, FLOOR + 1.02), index=8); b('paint.0', (1.3, 1.45), (5.3, 5.45), (FLOOR + .86, FLOOR + 1.04), index=0xD); b('paint.1', (1.55, 1.7), (5.3, 5.45), (FLOOR + .86, FLOOR + 1.04), index=0xC)
    # --- the desk under the north wall: a table, a tower beside it, the monitor with its back to the room
    b('desk.top', (f + 7.25, f + 8.75), (3.95, 4.62), (FLOOR + .7, FLOOR + .74), skin=k['wood'])
    for i, (x, y) in enumerate(((7.28, 3.98), (8.67, 3.98), (7.28, 4.54), (8.67, 4.54))): b(f'desk.leg.{i}', (f + x, f + x + .05), (y, y + .05), (FLOOR, FLOOR + .7), index=WD2)
    b('monitor', (f + 7.72, f + 8.22), (3.98, 4.4), (FLOOR + .78, FLOOR + 1.2), index=BEIGE); b('monitor.foot', (f + 7.85, f + 8.09), (4.08, 4.32), (FLOOR + .74, FLOOR + .78), index=BEIGE2)
    b('tower', (f + 8.36, f + 8.58), (4.0, 4.5), (FLOOR + .74, FLOOR + 1.2), index=BEIGE); b('keyboard', (f + 7.75, f + 8.2), (4.46, 4.6), (FLOOR + .74, FLOOR + .77), index=BEIGE2)
    b('chair.seat', (f + 7.78, f + 8.18), (4.82, 5.2), (FLOOR + .42, FLOOR + .46), index=WD1); b('chair.back', (f + 7.78, f + 8.18), (5.17, 5.2), (FLOOR + .46, FLOOR + .95), index=WD1)
    for i, (x, y) in enumerate(((7.79, 4.83), (8.14, 4.83), (7.79, 5.16), (8.14, 5.16))): b(f'chair.leg.{i}', (f + x, f + x + .03), (y, y + .03), (FLOOR, FLOOR + .42), index=WD2)
    # --- the pantry over the stairs, and the piece of kitchen it is seen from
    p = PX
    b('pantry.n', (p + .6, p + 3.2), (5.6, 5.7), (0, 2.4), skin=k['white']); b('pantry.s', (p + .6, p + 3.2), (4.0, 4.1), (0, 2.4), skin=k['white']); b('pantry.e', (p + 3.1, p + 3.2), (4.0, 5.7), (0, 2.4), skin=k['white'])
    b('ceiling', (0, p + 3.2), (2.0, 7.1), (2.4, 2.45), index=9); b('kwall.s', (p + .5, p + .6), (2.0, 4.1), (0, 2.4), skin=k['paper']); b('kwall.n', (p + .5, p + .6), (5.6, 7.1), (0, 2.4), skin=k['paper']); b('kwall.top', (p + .5, p + .6), (4.1, 5.6), (2.05, 2.4), skin=k['paper'])
    for i, (y0, y1) in enumerate(((4.02, 4.1), (5.6, 5.68))): b(f'trim.{i}', (p + .47, p + .5), (y0, y1), (0, 2.05), index=0xA)
    b('trim.top', (p + .47, p + .5), (4.02, 5.68), (2.05, 2.13), index=0xA)
    for i, z in enumerate((.85, 1.35, 1.85)):
        b(f'pshelf.n.{i}', (p + .7, p + 3.1), (5.4, 5.6), (z - .03, z), skin=k['wood']); S.add(D.panel(f'pjars.n.{i}', _jars(46, 10 + i), (p + .75, 5.42, z + .35), (1, 0, 0), (0, 0, -1)))
        b(f'pshelf.s.{i}', (p + .7, p + 3.1), (4.1, 4.3), (z - .03, z), skin=k['wood']); S.add(D.panel(f'pjars.s.{i}', _jars(46, 20 + i), (p + .75, 4.28, z + .35), (1, 0, 0), (0, 0, -1)))
        b(f'pshelf.e.{i}', (p + 2.9, p + 3.1), (4.3, 5.4), (z - .03, z), skin=k['wood']); S.add(D.panel(f'pjars.e.{i}', _jars(20, 30 + i), (p + 2.92, 5.38, z + .35), (0, -1, 0), (0, 0, -1)))
    D.paint(S.tube('bulb.cord', [(p + 1.9, 4.85, 2.4), (p + 1.9, 4.85, 2.12)], .008, n=3), index=0)
    D.paint(S.tube('broom', [(p + .78, 5.3, 0.0), (p + .72, 5.5, 1.5)], .015, n=4), index=PINE); b('broom.head', (p + .68, p + .9), (5.2, 5.4), (0, .18), index=0xE)
    # --- the house above ground, from outside: foundation, siding, a snowed-on roof, the wing with its roof deck
    b('found.s', (-.25, 14.25), (-.25, 0), (GRADE, 0), skin=k['found']); b('found.w', (-.25, 0), (0, 7.25), (GRADE, 0), skin=k['found']); b('found.e', (14, 14.25), (0, 7.25), (GRADE, 0), skin=k['found'])
    b('house.s', (-.25, 14.25), (-.25, -.1), (0, 2.6), skin=k['siding']); b('house.w', (-.25, -.1), (-.1, 7.25), (0, 2.6), skin=k['siding']); b('house.e', (14.1, 14.25), (-.1, 7.25), (0, 2.6), skin=k['siding']); b('house.n', (-.25, 14.25), (7.1, 7.25), (GRADE, 2.6), skin=k['siding'])
    D.paint(S.gable('roof', (-.25, 14.25), (-.25, 7.25), 2.6, 4.9, along='x', over=.45), skin=k['roof'])
    for nm, x in (('w', -.26), ('e', 14.26)): D.paint(S.face('gable.' + nm, [(x, -.25, 2.6), (x, 7.25, 2.6), (x, 3.5, 4.9)]), skin=k['siding'])
    b('eave', (-.7, 14.7), (-.72, -.64), (2.5, 2.62), index=0xA)
    b('wing.found', (14.25, 18.75), (.7, 6.2), (GRADE, 0), skin=k['found']); b('wing', (14.25, 18.75), (.7, 6.2), (0, 2.5), skin=k['siding']); b('wing.roof', (14.2, 18.85), (.55, 6.3), (2.5, 2.68), skin=k['roof'])
    for i in range(10): b(f'rail.{i}', (14.4 + i * .48, 14.46 + i * .48), (.62, .68), (2.68, 3.5), index=PINE)
    b('rail.top', (14.36, 18.8), (.6, .7), (3.5, 3.56), index=PINE); b('step', (15.9, 17.1), (.2, .7), (GRADE, -.15), index=8); b('door', (16.1, 16.9), (.66, .7), (0, 2.0), index=0xA)
    for i, (x, y, sd) in enumerate(((9.5, 12.5, 1), (13.2, 15.0, 2), (-6.5, 14.0, 3))):
        S.add(D.card(f'spruce.{i}', _spruce(sd, 64 if i < 2 else 48, 150 if i < 2 else 110), (x, y, GRADE), (1, 0, 0), texel=.1, cast=False))
    b('birdhouse.post', (-3.02, -2.98), (.5, .54), (GRADE, .9), index=WD2); b('birdhouse', (-3.14, -2.86), (.4, .64), (.9, 1.2), index=PINE); b('birdhouse.snow', (-3.18, -2.82), (.36, .68), (1.2, 1.28), index=0xA)
    for q in S.solids:
        if q.name.split('.')[0] in ('snow', 'spruce', 'roof', 'wing', 'birdhouse') or q.name.startswith('earth'): q.cast = False
    _S['S'] = S; return S

WINDOWS = [(1.0, 0), (3.6, 0), (6.4, 0), (9.6, 0), (12.2, 0), (14.9, 1), (17.5, 1)]                      # x of the left edge; 0 the house, 1 the wing
def windows(lit=None):
    """The south windows. lit: a list of booleans, one per window (default all dark)."""
    lit = lit or [False] * len(WINDOWS); out = []
    for i, ((x, wing), on) in enumerate(zip(WINDOWS, lit)):
        out.append(D.panel(f'window.{i}', _window(on), (x, (.69 if wing else -.26), 1.95), (1, 0, 0), (0, 0, -1), glow=1.0 if on else 0.0, cast=False))
    return out

HX = PX + 2.7                                 # the hinge line
def lid(angle=0.0):
    """The trap door: 1.6 m long, 0.8 wide, 4 cm thick, hinged along its east edge. angle in degrees from shut."""
    a = math.radians(angle); c, s = math.cos(a), math.sin(a); k = skins()
    P = lambda d, t, y: (HX - d * c - t * s, y, d * s - t * c + 0.0)          # d along the lid from the hinge, t into its thickness
    bottom = [P(0, .04, 4.46), P(1.59, .04, 4.46), P(1.59, .04, 5.24), P(0, .04, 5.24)]; top = [P(0, 0, 4.46), P(1.59, 0, 4.46), P(1.59, 0, 5.24), P(0, 0, 5.24)]
    sol = Solid('lid', [bottom[::-1], top] + [[bottom[i], bottom[(i + 1) % 4], top[(i + 1) % 4], top[i]] for i in range(4)], kind='wall')
    D.paint(sol, skin=k['boards'], origin=(HX, 4.46, 0)); ring = Solid('lid.ring', [[P(1.42, -.012, 4.78), P(1.52, -.012, 4.78), P(1.52, -.012, 4.92), P(1.42, -.012, 4.92)]], kind='wall'); D.paint(ring, index=8, cast=False)
    return [sol, ring]
def leak(k=1.0, index=0xF):
    """Light coming up round the edges of the shut trap door: three thin strips of register F. (With k=0 and
    index=0 it is only the crack, for the machines that have no register F yet.)"""
    out = []
    for i, (x0, x1, y0, y1) in enumerate(((PX + 1.1, HX, 4.445, 4.465), (PX + 1.1, HX, 5.235, 5.255), (PX + 1.095, PX + 1.115, 4.45, 5.25))):
        q = Solid(f'leak.{i}', [[(x0, y0, .004), (x1, y0, .004), (x1, y1, .004), (x0, y1, .004)]], kind='light'); D.paint(q, index=index, glow=k, cast=False); out.append(q)
    return out
def cut():
    """The basement's south wall, for when the camera is inside the room."""
    return [D.paint(Set('x').box('cut', (-.25, EAST + .25), (-.25, 0), (FLOOR, 0)), skin=skins()['block'])]

SCREEN = dict(corner=(FX + 8.17, 4.405, FLOOR + 1.165), across=(-1, 0, 0), down=(0, 0, -1), w=.40, h=.225)      # the glass faces north, toward the chair
def screen(skin=None, glow=1.0, index=0xF):
    """The monitor's glass. skin: a (180, 320) index picture (seen close), or None for one flat lit paint (seen far)."""
    if skin is None: return [D.panel('screen', np.full((5, 8), index, np.uint8), SCREEN['corner'], SCREEN['across'], SCREEN['down'], texel=.05, glow=glow, cast=False)]
    return [D.panel('screen', skin, SCREEN['corner'], SCREEN['across'], SCREEN['down'], texel=SCREEN['w'] / skin.shape[1], glow=glow, cast=False)]
def bulb(on=0.0):
    """The pantry's bare bulb."""
    return [D.paint(Set('x').box('bulb', (PX + 1.84, PX + 1.96), (4.79, 4.91), (1.98, 2.12), kind='light'), index=0xF if on else 9, glow=on, cast=False)]
def led(on=1.0):
    """The dehumidifier's pilot lamp."""
    return [D.paint(Set('x').box('led', (FX + 7.14, FX + 7.2), (3.32, 3.33), (FLOOR + .53, FLOOR + .57), kind='light'), index=0xF if on else 8, glow=on, cast=False)]
def tube(on=1.0):
    return [D.paint(Set('x').box('tube', (FX + 5.55, FX + 6.85), (2.95, 3.05), (-.53, -.5), kind='light'), index=0xF if on else 9, glow=on, cast=False)]

SPOT = dict(chair=(FX + 7.98, 4.98, FLOOR), stairs_top=(PX + 1.0, 4.85, 0.0), stairs_foot=(PX + 3.6, 4.85, FLOOR), screen=(FX + 7.97, 4.405, FLOOR + 1.05), hatch=(PX + 1.9, 4.85, 0.0), tube=(FX + 6.2, 3.0, -.56))
def stair(k):
    """The foot position on step k (0 the pantry floor, 12 the basement floor)."""
    return np.array([PX + 1.02 + .2 * k + (.05 if k else 0), 4.85, -.2 * min(k, 12)])

if __name__ == '__main__':
    from backlot import space
    S = build(); print(len(S.solids), 'solids,', sum(len(q.faces) for q in S.solids), 'faces')
    for text, at in (('stairs (12 risers)', (PX + 2.3, 4.2, -1)), ('workbench', (2.0, 4.75, -1)), ('washer', (.45, 1.6, -1)), ('furnace', (FX + 4.6, 4.5, -1)), ('chimney', (FX + 5.6, 4.75, -1)), ('water heater', (FX + 6.6, 4.5, -1)),
                     ('desk, monitor facing the wall', (FX + 8.0, 3.75, -1)), ('chair', (FX + 7.98, 5.42, -1)), ('red post', (4.1, 2.0, -1)), ('red post', (8.4, 2.0, -1)), ('shop light', (FX + 6.2, 2.75, -1)), ('dehumidifier', (FX + 7.1, 3.1, -1)),
                     ('the cut: the south wall is left off, and the world ends here', (6.0, -.6, -1)), ('trunk duct', (2.2, 3.55, -1)), ('beam', (6.3, 2.62, -1))):
        S.label(text, at, small=True)
    space.drawing(S, 'plan', out=str(HERE / 'drawing_plan.svg'), bounds=((-1, 13.5), (-1, 7), (FLOOR, -.3)), scale=60, grid=1.0, title='the basement')
    S.labels = []
    for text, at in (('pantry', (PX + 1.9, 3, 1.3)), ('kitchen', (1.8, 3, 1.3)), ('trap door', (PX + 1.9, 3, .25)), ('stairs', (PX + 2.9, 3, -1.0)), ('furnace', (FX + 4.6, 3, -.72)), ('chimney', (FX + 5.6, 3, 3.3)), ('desk', (FX + 8.0, 3, -1.45)),
                     ('earth', (-1.2, 3, -1.6)), ('earth', (15.5, 3, -1.6)), ('ground floor = 0', (17.5, 3, .2)), ('the wing, with its roof deck', (16.5, 3, 1.3)), ('basement floor = -2.4', (10.6, 3, -2.75))):
        S.label(text, at, small=True)
    space.drawing(S, 'from_south', out=str(HERE / 'drawing_from_south.svg'), bounds=((-2, 20), (-1, 8), (-3.2, 6)), scale=40, grid=1.0, title='section, looking north', cut=-.2)
