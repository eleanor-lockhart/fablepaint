"""Winter quarters: the shed, the gallopers in it, and the yard outside. One model, in metres.

The ride is built as one twelfth (`sector`) and repeated twelve times, so that turned by exactly thirty degrees
it is the same ride: at the locked speed the only thing that differs from one picture to the next is which
horse is where.

    ride(theta, lights)     the turning part at angle theta (degrees): deck, poles, canopy, boards, bulbs, horses
    horses(theta)           [(name, block, number, world position)] for the twenty-four
    shed()                  the building and what stands in it (never moves)
    yard()                  outside: snow, the shed from outside, the wagon, trees
    PLACE                   where things are, for the film
    python ride.py          writes the plan and a section
"""
import sys, math
from functools import lru_cache
from pathlib import Path
HERE = Path(__file__).resolve().parent; sys.path.insert(0, str(HERE)); sys.path.insert(1, str(HERE.parent)); sys.path.insert(2, str(HERE.parents[2]))
import numpy as np
from backlot.space import Set, Solid
from backlot import depth as D
from backlot.depth import HOLE
import deep
from deep import blend
import horse as H

R_OUT, R_IN = 6.0, 4.7            # the two rings of horses
RIM, HUB = 6.9, 3.2               # the deck's outer edge; the drum in the middle
DECK, TOP, APEX = .45, 4.2, 6.5   # top of the deck; underside of the canopy; its point
SHED, EAVE = 11.0, 7.4            # half the shed's width inside; under the tie beams
RISE = .18                        # how far a horse goes up and down on its crank
N = 12
# paints: every one a fixed mixture of two registers
BOARD, BOARD2, GAP = blend(0x9, 0x3, .4), blend(0x9, 0x3, .55), blend(0x2, 0x0, .4)        # the shed's planks
CONC, CONC2 = blend(0x8, 0x1, .3), blend(0x8, 0x1, .5)                                      # its floor
DECKW, DECKW2, DECKG = blend(0xE, 0x2, .5), blend(0xE, 0x2, .62), blend(0x2, 0x0, .3)       # the ride's deck
BRASS = blend(0xE, 0xF, .35)
SNOW, SNOW2, SNOW3 = blend(0xA, 0x3, .18), blend(0xA, 0x3, .34), blend(0xA, 0x3, .5)
TARP = blend(0x8, 0x2, .5)
CANVAS = blend(0xA, 0x3, .14)

def pol(r, deg, z=0.0): a = math.radians(deg); return (r * math.cos(a), r * math.sin(a), z)

@lru_cache(maxsize=None)
def skins():
    s = {}
    s['wall'] = deep.planks(BOARD, BOARD2, GAP, width=4, length=64, along='v', seed=5)
    s['floor'] = deep.speckle(32, 32, CONC, [CONC2, 0x8], p=.16, seed=6)
    s['deck'] = deep.planks(DECKW, DECKW2, DECKG, width=4, length=24, along='u', seed=7, n=6)
    st = np.full((2, 72), 0xD, np.uint8); st[:, 36:] = 0xA; s['canopy'] = st                    # red and white, a stripe a half-sector wide
    b = np.full((14, 72), 0xB, np.uint8); b[0] = b[13] = BRASS; b[:, 0] = b[:, 71] = BRASS      # a rounding board: blue, a brass edge, a cartouche
    yy, xx = np.mgrid[:14, :72]; oval = ((xx - 35.5) / 20) ** 2 + ((yy - 6.5) / 5) ** 2
    b[oval < 1] = 0xD; b[oval < .72] = 0xA; b[(oval < .72) & ((xx + yy) % 6 == 0)] = 0x9
    for cx in (8, 63): b[4:10, cx - 2:cx + 3] = BRASS; b[5:9, cx - 1:cx + 2] = 0xD
    s['board'] = b
    m = np.full((75, 33), BRASS, np.uint8); m[2:73, 2:31] = CANVAS                              # a drum panel: pale painted canvas in a brass frame.
    m[5:70, 5] = m[5:70, 27] = 0xD; m[5, 5:28] = m[69, 5:28] = 0xD                               # (it is the screen the shadows fall on)
    for cy in (12, 62): m[cy - 2:cy + 3, 14:19] = 0xB; m[cy - 1:cy + 2, 15:18] = BRASS
    s['mirror'] = m
    for k in range(3):                                                                           # the bulbs under a board: one in three lit, chasing
        r = np.full((1, 72), HOLE, np.uint8); r[0, (np.arange(72) % 6) == 2 * k] = 0xF; s['bulbs%d' % k] = r
    r = np.full((1, 72), HOLE, np.uint8); r[0, np.arange(72) % 2 == 0] = blend(0x8, 0xF, .25); s['bulbs_off'] = r
    o = np.full((56, 52), 0xD, np.uint8); o[0:3] = BRASS; o[53:] = BRASS; o[:, 0:2] = BRASS; o[:, 50:] = BRASS   # the organ's front
    for i, x in enumerate(range(6, 46, 3)): hgt = 20 + 14 * abs(math.sin(i * .9)) ; o[int(44 - hgt):44, x:x + 2] = 0xA if i % 2 == 0 else 0x9; o[40:42, x:x + 2] = 0x1
    o[46:52, 6:46] = 0xB; o[47:51, 8:18] = 0xA; o[47:51, 34:44] = 0xA; o[48:50, 22:30] = BRASS
    s['organ'] = o
    s['door'] = deep.planks(blend(0xB, 0x1, .4), blend(0xB, 0x1, .52), 0x1, width=4, length=64, along='v', seed=14)
    import kit
    txt = 'GALLOPERS'; g = np.full((14, len(txt) * 8 + 8), 0xB, np.uint8); g[0] = g[-1] = BRASS; g[:, 0] = g[:, -1] = BRASS      # the sign over the door
    for i, ch in enumerate(txt): g[3:11, 4 + i * 8:12 + i * 8][kit.glyph(ch) > 0] = BRASS
    s['sign'] = g
    return s

def sector():
    """One twelfth of the ride, centred on the +x axis: its solids, with the ride at angle 0."""
    K = skins(); S = Set('sector'); a = 15.0
    plan = [pol(HUB, -a)[:2], pol(HUB, 0)[:2], pol(HUB, a)[:2], pol(RIM, a)[:2], pol(RIM, a / 2)[:2], pol(RIM, 0)[:2], pol(RIM, -a / 2)[:2], pol(RIM, -a)[:2]]
    D.paint(S.prism('deck', plan, DECK - .2, DECK), skin=K['deck'])
    D.paint(S.cylinder('pole.out', pol(R_OUT, 0)[:2], .045, DECK, TOP, n=4), index=BRASS)
    D.paint(S.cylinder('pole.in', pol(R_IN, a)[:2], .045, DECK, TOP, n=4), index=BRASS)
    bottom = [pol(.5, -a, TOP), pol(RIM + .1, -a, TOP), pol(RIM + .1, a, TOP), pol(.5, a, TOP)]
    top = [pol(.5, -a, APEX), pol(RIM + .1, -a, TOP + .12), pol(RIM + .1, a, TOP + .12), pol(.5, a, APEX)]
    D.paint(S.hexa('canopy', bottom, top), skin=K['canopy'])
    w = 72 * .05 / 2; r = RIM + .14
    S.add(D.panel('board', K['board'], (r, -w, TOP + .15), (0, 1, 0), (0, 0, -1)))
    S.add(D.panel('bulbs', K['bulbs0'], (r + .03, -w, TOP - .55), (0, 1, 0), (0, 0, -1), glow=1.0, cast=False))
    wm = 33 * .05 / 2; S.add(D.panel('mirror', K['mirror'], (HUB * math.cos(math.radians(a)) + .0, -wm, DECK + 3.75), (0, 1, 0), (0, 0, -1)))
    return S.solids
_SECTOR = None

def rate(theta): return math.radians(theta)

def horses(theta):
    """The twenty-four at ride angle theta: (name, block, number 1..12, world position of the saddle)."""
    out = []
    for k in range(N):
        p = (-k) % N
        for ring, (r, off, row, dp) in enumerate(((R_OUT, 0.0, 0, 0), (R_IN, 15.0, 1, 6))):
            q = (p + dp) % N; a = theta + 30.0 * k + off; z = DECK + 1.42 + RISE * math.cos(2 * math.radians(theta) - 2 * math.pi * q / N)
            x, y, _ = pol(r, a); b = H.carving(q, row).block('horse.%d.%d' % (ring, k), (x, y, z), turn=a + 90)
            out.append((b.name, b, q + 1, np.array([x, y, z])))
    return out

def ride(theta, lights='chase', frame=0, cut=False, with_horses=True):
    """Everything that turns. lights: 'chase', 'off'. cut: leave out the canopy and the boards (for the plan)."""
    global _SECTOR
    if _SECTOR is None: _SECTOR = sector()
    K = skins(); out = []
    for k in range(N):
        for s in _SECTOR:
            if cut and s.name in ('canopy', 'board', 'bulbs'): continue
            t = D.turned(s, theta + 30.0 * k)
            if s.name == 'bulbs':
                t.skin = K['bulbs%d' % ((frame // 4) % 3)] if lights == 'chase' else K['bulbs_off']; t.glow = 1.0 if lights == 'chase' else 0.0
            t.name = '%s.%d' % (s.name, k); out.append(t)
    if with_horses: out += [b for _, b, _, _ in horses(theta)]
    return out

# ------------------------------------------------------------------ the shed
PLACE = dict(door=(0.0, -SHED), switch=(3.0, -SHED + .5, 1.4), regulator=(8.5, -2.6), strobe=(9.7, -5.4, 1.95), strobe_park=(9.2, -7.4, 1.95),
             bench=(10.2, -8.5), organ=(-9.6, -5.0), wagon=(-9.5, -21.0), window=(6.2, -SHED - .29))

@lru_cache(maxsize=None)
def shed(door_open=True, inside=True):
    K = skins(); S = Set('shed'); W = SHED; t = .25
    D.paint(S.box('floor', (-W - t, W + t), (-W - t, W + t), (-.2, 0)), skin=K['floor'])
    for name, x, y in (('wall.n', (-W - t, W + t), (W, W + t)), ('wall.e', (W, W + t), (-W, W)), ('wall.w', (-W - t, -W), (-W, W))):
        D.paint(S.box(name, x, y, (0, EAVE + .4)), skin=K['wall'])
    D.paint(S.box('wall.s.w', (-W - t, -2.2), (-W - t, -W), (0, EAVE + .4)), skin=K['wall']); D.paint(S.box('wall.s.e', (2.2, W + t), (-W - t, -W), (0, EAVE + .4)), skin=K['wall'])
    D.paint(S.box('wall.s.top', (-2.2, 2.2), (-W - t, -W), (4.6, EAVE + .4)), skin=K['wall'])
    if not door_open: D.paint(S.box('door', (-2.2, 2.2), (-W - t + .05, -W - .05), (0, 4.6)), skin=K['door'])
    else: D.paint(S.box('door', (-6.4, -2.2), (-W - t - .1, -W - t), (0, 4.6)), skin=K['door'])            # slid open along the outside
    if not inside: return tuple(S.solids)
    D.paint(S.box('ceiling', (-W - t, W + t), (-W - t, W + t), (EAVE + .4, EAVE + .6)), index=GAP)
    for i, y in enumerate(np.linspace(-W + 1.4, W - 1.4, 7)):
        D.paint(S.box('beam.%d' % i, (-W, W), (y - .12, y + .12), (EAVE, EAVE + .4)), index=BOARD2)
    for i, v in enumerate(np.linspace(-W + .1, W - .1, 9)):                                  # posts along every wall
        for name, x, y in (('n', (v - .1, v + .1), (W - .16, W)), ('e', (W - .16, W), (v - .1, v + .1)), ('w', (-W, -W + .16), (v - .1, v + .1))):
            D.paint(S.box('post.%s.%d' % (name, i), x, y, (0, EAVE)), index=BOARD2)
        if abs(v) > 2.4: D.paint(S.box('post.s.%d' % i, (v - .1, v + .1), (-W, -W + .16), (0, EAVE)), index=BOARD2)
    for z in (2.4, 4.9):
        D.paint(S.box('rail.n.%d' % z, (-W, W), (W - .1, W), (z, z + .15)), index=BOARD2); D.paint(S.box('rail.e.%d' % z, (W - .1, W), (-W, W), (z, z + .15)), index=BOARD2)
        D.paint(S.box('rail.w.%d' % z, (-W, -W + .1), (-W, W), (z, z + .15)), index=BOARD2)
    # what stands in it
    bx, by = PLACE['bench']; D.paint(S.box('bench', (bx - .4, bx + .5), (by - 1.3, by + 1.3), (.82, .9)), index=DECKW);
    for i, (dx, dy) in enumerate(((-.3, -1.2), (.4, -1.2), (-.3, 1.2), (.4, 1.2))): D.paint(S.box('bench.leg%d' % i, (bx + dx - .05, bx + dx + .05), (by + dy - .05, by + dy + .05), (0, .82)), index=DECKW2)
    D.paint(S.box('bench.box', (bx - .1, bx + .35), (by + .4, by + 1.0), (.9, 1.15)), index=0xD); D.paint(S.box('bench.can', (bx, bx + .15), (by - .8, by - .65), (.9, 1.12)), index=0xB)
    crates = [((-10.4, -9.4), (7.2, 8.4), (0, 1.0)), ((-10.4, -9.5), (8.5, 9.6), (0, .8)), ((-10.3, -9.5), (7.4, 8.3), (1.0, 1.7)), ((9.2, 10.4), (8.6, 10.2), (0, 1.2)), ((9.5, 10.4), (7.3, 8.4), (0, .7)),
              ((7.6, 9.0), (9.4, 10.5), (0, .9)), ((-8.9, -7.8), (9.3, 10.4), (0, 1.1)), ((-10.5, -9.7), (-9.8, -8.6), (0, 1.3))]
    for i, (x, y, z) in enumerate(crates): D.paint(S.box('crate.%d' % i, x, y, z), skin=deep.planks(DECKW2, DECKW, DECKG, width=3, length=16, along='u', seed=20 + i, n=4))
    for i, (x, y) in enumerate(((-6.0, 10.2), (-5.1, 10.3), (9.9, 4.9), (10.1, 3.9), (-10.2, 2.0))): D.paint(S.cylinder('barrel.%d' % i, (x, y), .36, 0, .95, n=8), index=blend(0x8, 0xB, .3))
    D.paint(S.prism('tarp', [(-3.2, 9.0), (3.4, 9.0), (3.4, 10.6), (-3.2, 10.6)], 0, 2.1, top=[(-2.4, 9.3), (2.6, 9.3), (2.6, 10.4), (-2.4, 10.4)]), index=TARP)   # something else, under a sheet
    D.paint(S.prism('tarp2', [(-10.6, -3.0), (-9.4, -3.0), (-9.4, 0.4), (-10.6, 0.4)], 0, 1.6, top=[(-10.5, -2.6), (-9.7, -2.6), (-9.7, 0.0), (-10.5, 0.0)]), index=TARP)
    ox, oy = PLACE['organ']                                                                    # the organ, on its truck, facing the ride
    D.paint(S.box('organ', (ox - .6, ox + .6), (oy - 1.3, oy + 1.3), (.5, 3.3)), index=blend(0xD, 0x1, .45))
    S.add(D.panel('organ.front', K['organ'], (ox + .62, oy - 1.3, 3.3), (0, 1, 0), (0, 0, -1)))
    for i, y in enumerate((oy - .9, oy + .9)): D.paint(S.cylinder('organ.wheel%d' % i, (ox, y), .5, 0, .5, n=8), index=0x1)
    sx, sy, sz = PLACE['switch']; D.paint(S.box('switchpost', (sx - .1, sx + .1), (sy - .1, sy + .1), (0, 2.2)), index=BOARD2); D.paint(S.box('switchbox', (sx - .16, sx + .16), (sy + .1, sy + .2), (1.15, 1.6)), index=0x9)
    rx, ry = PLACE['regulator']; D.paint(S.box('regbase', (rx - .18, rx + .18), (ry - .18, ry + .18), (0, .9)), index=0x8); D.paint(S.box('regplate', (rx - .2, rx + .2), (ry - .2, ry + .2), (.9, .96)), index=BRASS)
    for i, (x, y) in enumerate(((-5.5, -5.5), (5.5, 5.5), (-5.5, 5.5))): D.paint(S.box('houselamp.%d' % i, (x - .15, x + .15), (y - .15, y + .15), (EAVE - .5, EAVE - .3)), index=0x8)
    return tuple(S.solids)

def lever(pulled):
    """The regulator's lever: 0 closed (toward the ride), 1 wide open."""
    rx, ry = PLACE['regulator']; a = math.radians(-12 + 24 * pulled); d = np.array([0, math.sin(a), math.cos(a)]); O = np.array([rx, ry, .95]); s = Set('l')
    tip = O + d * .45; D.paint(s.hexa('lever', [O + (-.03, -.03, 0), O + (.03, -.03, 0), O + (.03, .03, 0), O + (-.03, .03, 0)], [tip + (-.03, -.03, 0), tip + (.03, -.03, 0), tip + (.03, .03, 0), tip + (-.03, .03, 0)]), index=0xD)
    D.paint(s.box('knob', (tip[0] - .06, tip[0] + .06), (tip[1] - .06, tip[1] + .06), (tip[2] - .02, tip[2] + .1)), index=0xA)
    return s.solids

def switch(on):
    sx, sy, sz = PLACE['switch']; s = Set('s'); z = 1.5 if on else 1.25
    D.paint(s.box('switch.arm', (sx - .03, sx + .03), (sy + .2, sy + .34), (z - .03, z + .03)), index=0xD); return s.solids

def strobe(at, lit=True, aim=(-1.0, .5)):
    """The stroboscope on its stand: a lamp that flashes 24 times a second. `at` is where its lens is."""
    x, y, z = at; s = Set('st'); a = np.array([aim[0], aim[1]]) / math.hypot(*aim)
    D.paint(s.cylinder('strobe.stand', (x - a[0] * .1, y - a[1] * .1), .035, 0, z - .15, n=4), index=0x8)
    for i, (dx, dy) in enumerate(((.3, 0), (-.15, .26), (-.15, -.26))): D.paint(s.box('strobe.foot%d' % i, (x + dx - .2, x + dx + .2) if dy == 0 else (x + dx - .04, x + dx + .04), (y + dy - .04, y + dy + .04) if dy == 0 else (y + dy - .2, y + dy + .2), (0, .08)), index=0x8)
    D.paint(s.box('strobe.head', (x - .2, x + .2), (y - .2, y + .2), (z - .2, z + .2)), index=0x9, cast=False)
    lens = D.panel('strobe.lens', np.full((6, 6), 0xF if lit else 0x8, np.uint8), (x + a[0] * .21 - a[1] * .15, y + a[1] * .21 + a[0] * .15, z + .15), (a[1], -a[0], 0), (0, 0, -1), glow=1.0 if lit else 0.0, cast=False)
    return s.solids + [lens]

# ------------------------------------------------------------------ outside
def tree(seed, h=60):
    """A bare tree, drawn by rule: a trunk that forks. A card (it is far away and nobody walks round it)."""
    r = np.random.default_rng(seed); w = int(h * .8); a = np.full((h, w), HOLE, np.uint8)
    def limb(x, y, ang, ln, th):
        for i in range(int(ln)):
            xx, yy = int(x + math.sin(ang) * i), int(y - math.cos(ang) * i)
            if 0 <= yy < h and 0 <= xx < w: a[yy, max(xx - th // 2, 0):xx + (th + 1) // 2] = 0x1
        if ln > 5:
            ex, ey = x + math.sin(ang) * ln, y - math.cos(ang) * ln
            for d in (-1, 1): limb(ex, ey, ang + d * r.uniform(.3, .7), ln * r.uniform(.55, .75), max(th - 1, 1))
    limb(w / 2, h - 1, r.uniform(-.1, .1), h * .32, 3); return a

@lru_cache(maxsize=None)
def yard(window_lit=False):
    K = skins(); S = Set('yard'); W = SHED + .25
    D.paint(S.box('snow', (-60, 60), (-70, 40), (-.5, 0)), skin=deep.speckle(32, 32, SNOW, [SNOW2, 0xA], p=.2, seed=9))
    for i, (x, y, rx, ry, hh) in enumerate(((-3, -16, 3.0, 1.6, .25), (7, -20, 4.0, 2.0, .3), (-15, -14, 3.5, 2.2, .35), (14, -13.5, 3.0, 1.4, .3), (2, -26, 5, 2.5, .3))):   # drifts
        D.paint(S.prism('drift.%d' % i, [(x - rx, y - ry), (x + rx, y - ry), (x + rx, y + ry), (x - rx, y + ry)], 0, hh, top=[(x - rx * .6, y - ry * .5), (x + rx * .6, y - ry * .5), (x + rx * .6, y + ry * .5), (x - rx * .6, y + ry * .5)]), skin=deep.speckle(16, 16, SNOW, [0xA], p=.3, seed=30 + i))
    ext = [s for s in shed(door_open=False, inside=False) if s.name != 'floor']; S.solids += ext
    D.paint(S.gable('roof', (-W, W), (-W, W), EAVE + .4, EAVE + 3.6, along='x', over=.5), skin=deep.speckle(16, 16, SNOW, [SNOW2, 0xA], p=.3, seed=11))
    wx, wy = PLACE['window']; S.add(D.panel('window', np.full((14, 18), 0xF if window_lit else GAP, np.uint8), (wx - .45, wy - .02, 2.6), (1, 0, 0), (0, 0, -1), glow=1.0 if window_lit else 0.0, cast=False))
    for dx in (-.02, .43): S.add(D.panel('window.bar%d' % (dx > 0), np.full((14, 1), BOARD2, np.uint8), (wx + dx, wy - .04, 2.6), (1, 0, 0), (0, 0, -1), cast=False))
    S.add(D.panel('window.bar2', np.full((1, 18), BOARD2, np.uint8), (wx - .45, wy - .04, 2.25), (1, 0, 0), (0, 0, -1), cast=False))
    D.paint(S.box('doorline', (-2.3, 2.3), (-W - .3, -W - .26), (4.6, 4.72)), index=BOARD2)
    for i, x in enumerate((-2.3, 2.22)): D.paint(S.box('doorpost%d' % i, (x, x + .08), (-W - .3, -W - .26), (0, 4.6)), index=BOARD2)
    sg = K['sign']; S.add(D.panel('sign', sg, (-sg.shape[1] * .025, -W - .32, 5.75), (1, 0, 0), (0, 0, -1), cast=False))
    gx, gy = PLACE['wagon']                                                                    # the living wagon: where the one light is
    D.paint(S.box('wagon', (gx - 2.6, gx + 2.6), (gy - 1.1, gy + 1.1), (.7, 2.9)), skin=deep.planks(blend(0xB, 0x1, .35), blend(0xB, 0x1, .5), 0x1, width=3, length=32, along='v', seed=12))
    D.paint(S.prism('wagon.roof', [(gx - 2.8, gy - 1.3), (gx + 2.8, gy - 1.3), (gx + 2.8, gy + 1.3), (gx - 2.8, gy + 1.3)], 2.9, 3.3, top=[(gx - 2.7, gy - .5), (gx + 2.7, gy - .5), (gx + 2.7, gy + .5), (gx - 2.7, gy + .5)]), skin=deep.speckle(8, 8, SNOW, [0xA], p=.3, seed=13))
    for i, x in enumerate((gx - 1.7, gx + 1.7)):
        for j, y in enumerate((gy - 1.15, gy + 1.05)): D.paint(S.box('wagon.wheel%d%d' % (i, j), (x - .45, x + .45), (y, y + .1), (0, .9)), index=0x1)
    S.add(D.panel('wagon.window', np.full((12, 14), 0xF, np.uint8), (gx + 2.62, gy - .35, 2.3), (0, 1, 0), (0, 0, -1), glow=1.0, cast=False))
    S.add(D.panel('wagon.window2', np.full((12, 12), 0xF, np.uint8), (gx + .4, gy + 1.12, 2.3), (1, 0, 0), (0, 0, -1), glow=1.0, cast=False))
    D.paint(S.box('wagon.step', (gx + 2.6, gx + 3.3), (gy - .4, gy + .4), (.3, .5)), index=BOARD2); D.paint(S.box('wagon.flue', (gx - 1.4, gx - 1.2), (gy - .1, gy + .1), (3.2, 4.0)), index=0x1)
    for i, (x, y, ln, hh) in enumerate(((16, -20, 7, 2.8), (-22, -9, 8, 3.2), (24, -8, 6, 2.5))):                              # other rides, sheeted, under snow
        D.paint(S.prism('lump.%d' % i, [(x - ln / 2, y - 1.6), (x + ln / 2, y - 1.6), (x + ln / 2, y + 1.6), (x - ln / 2, y + 1.6)], 0, hh, top=[(x - ln / 2 + .6, y - .8), (x + ln / 2 - .6, y - .8), (x + ln / 2 - .6, y + .8), (x - ln / 2 + .6, y + .8)]), index=TARP)
        D.paint(S.box('lump.snow%d' % i, (x - ln / 2 + .6, x + ln / 2 - .6), (y - .8, y + .8), (hh, hh + .12)), index=SNOW)
    for i, (x, y, hh, sd) in enumerate(((-26, 6, 110, 1), (-19, 14, 90, 2), (20, 10, 120, 3), (30, 2, 100, 4), (-34, -4, 100, 5), (12, 22, 90, 6), (-8, 24, 100, 7), (36, 16, 110, 8), (-40, 14, 120, 9))):
        S.add(D.card('tree.%d' % i, tree(sd, hh), (x, y, 0), (1, 0, 0), flat=True, cast=False))
    return tuple(S.solids)

if __name__ == '__main__':
    from backlot.space import Camera
    import cv2
    out = HERE.parents[2] / 'out' / 'hex' / 'persistence'; out.mkdir(parents=True, exist_ok=True)
    import time; t0 = time.time()
    things = list(shed()) + ride(0.0) + lever(0) + switch(True) + strobe(PLACE['strobe'])
    print(len(things), 'solids')
    for name, cam in (('wide', Camera((9.5, -10.2, 2.6), look=(0, 0, 2.2), lens=20, size=(1280, 720))), ('rim', Camera((8.6, -4.0, 1.9), look=(4.5, 1.5, 2.1), lens=28, size=(1280, 720)))):
        t0 = time.time(); g = D.gbuffer(things, cam); t1 = time.time()
        lamps = [D.Light(pol(RIM - .6, 30 * k + 15, TOP - .5), power=.55, reach=3.5, shadow=False) for k in range(0, 12, 2)] + [D.Light((-7, -8, 7.0), power=1.6, reach=11, aim=(.6, .65, -.5), cone=(45, 60)).bake(things)]
        lv = D.lighting(g, lamps, ambient=.07); img = deep.glow(deep.colour(g, lv, steps=6, dither=0)); deep.save(out / ('t_%s.png' % name), img); print(name, 'gbuffer', round(t1 - t0, 2), 'light', round(time.time() - t1, 2))
