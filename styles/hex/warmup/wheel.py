"""Warmup 3: The Sixth Wheel (compound turret-clock reduction train, 10.0 s seamless loop).

In a stone clock room while snow falls outside, five compound reduction stages step a 36 RPM escapement shaft down
until the sixth wheel turns once in a thousand years. Under one tended lantern (register F), a keeper with an
oilcan oils the sixth wheel's bearing anyway.

Stage 5: built in metres on the 5 cm grid (`backlot.space`, `backlot.depth`, `backlot.carve`, `puppet.py`, `deep.py`).
Every spinning wheel is constructed as one symmetric sector and rotated with its paint (`turned_y`), so at frame 240
every shaft — whether it turned 6 times, 1 time, 1/6 of a turn, 1/36 of a turn, or 0 pixels — matches frame 0
to the texel. Zero green registers appear outside the sixteen-register signature strip.

    uv run python styles/hex/warmup/wheel.py test     render key frames + elevation to inspect first
    uv run python styles/hex/warmup/wheel.py          render all 240 frames, encode mp4, run seam/pops/motion checks
"""
import sys, copy, math, subprocess
from functools import lru_cache
from multiprocessing import Pool
from pathlib import Path
HERE = Path(__file__).resolve().parent; HEX = HERE.parent; ROOT = HERE.parents[2]
sys.path.insert(0, str(HEX)); sys.path.insert(1, str(ROOT)); sys.path.insert(2, str(HEX / 'uptime'))
import numpy as np
import cv2
from backlot import space as sp, depth as D
import deep as X, puppet as P, kit, ui as U
from deep import blend

FPS, SECONDS = 24, 10
NF = FPS * SECONDS                                                             # 240 frames
W, H = 1280, 720
OUT = ROOT / 'out' / 'hex' / 'wheel'
FRAMES = OUT / 'frames'

# Strictly zero green paints (registers 4, 5, 6, 7 untouched)
STONE1, STONE2, STONE_LO = blend(0x3, 0x8, .48), blend(0x2, 0x8, .36), blend(0x1, 0x2, .5)
FLOOR1, FLOOR2, FLOOR_G = blend(0xE, 0x2, .62), blend(0xE, 0x1, .68), blend(0x1, 0x0, .5)
IRON, IRON_DARK, STEEL_HI = blend(0x8, 0x2, .30), blend(0x1, 0x8, .35), 0x9
BRASS, BRASS_LO = blend(0xE, 0xA, .36), blend(0xE, 0x8, .42)
RED_ENAMEL = blend(0xD, 0x8, .25)

# Six shafts: (x, z, R_wheel, r_pinion, n_sym, deg_per_loop, rate_label)
# Compound mesh: pinion on shaft k (at y = +0.20) drives main wheel on shaft k+1 (at y = +0.20 or -0.08)
SHAFTS = [
    (-3.75, 1.50, 0.44, 0.16,  6, +2160.0, '01  36/MIN'),                      # 6 full turns CW
    (-2.62, 1.56, 0.72, 0.15,  6,  -360.0, '02  6/MIN'),                       # 1 full turn CCW
    (-1.26, 1.48, 0.80, 0.15,  6,   +60.0, '03  1/MIN'),                       # 1/6 turn CW  (6-spoke symmetry -> exact seam!)
    (+0.18, 1.58, 0.88, 0.16, 12,   -30.0, '04  10/HR'),                       # 1/12 turn CCW (12-bolt symmetry -> exact seam!)
    (+1.68, 1.50, 0.94, 0.16, 12,     0.0, '05  1/YR'),                        # worm-reduced: 0.0002 deg in 10 s
    (+3.55, 1.92, 1.38, 0.00,  8,     0.0, '06  1/1000 YR'),                   # the sixth wheel: 2.76 m tall, 0 pixels moved
]


def turned_y(sol, deg, about=(0.0, 1.5)):
    """Rotate a Solid about the horizontal y-axis through (about[0], y, about[1]), carrying its texel grid with it."""
    c, sn = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    ax, az = about
    def pt(P):
        q = np.asarray(P, float); dx, dz = q[..., 0] - ax, q[..., 2] - az
        return np.stack([ax + c * dx + sn * dz, q[..., 1], az - sn * dx + c * dz], -1)
    def vec(v):
        v = np.asarray(v, float)
        return np.array([c * v[0] + sn * v[2], v[1], -sn * v[0] + c * v[2]])
    new = copy.copy(sol)
    new._tri = [[pt(t) for t in face] for face in D._tris(sol)]
    new.faces = [pt(f) for f in sol.faces]
    fr = getattr(sol, 'frame', None); frs = getattr(sol, 'frames', None)
    if fr is not None:
        new.frame = (pt(fr[0]), vec(fr[1]), vec(fr[2]))
    else:
        org = np.asarray(getattr(sol, 'origin', (0, 0, 0)), float)
        if frs is None:
            frs = [(org,) + D._frame(sp._normal(f)) for f in sol.faces]
        new.frames = [(pt(O), vec(U), vec(V)) for O, U, V in frs]
    return new


def _yz_prism(S, name, xz_poly, y0, y1, **paint_kw):
    """Extrude a polygon in (x, z) from y0 to y1 as a Solid."""
    pts = [(float(x), float(z)) for x, z in xz_poly]
    n = len(pts)
    front = [(x, y0, z) for x, z in pts]
    back = [(x, y1, z) for x, z in reversed(pts)]
    faces = [front, back]
    for i in range(n):
        x0, z0 = pts[i]; x1, z1 = pts[(i + 1) % n]
        faces.append([(x0, y0, z0), (x1, y0, z1), (x1, y1, z1), (x0, y1, z0)])
    sol = sp.Solid(name, faces, kind='machine')
    D.paint(sol, **paint_kw)
    S.add(sol)
    return sol


@lru_cache(maxsize=None)
def wheel_sector(idx):
    """Build ONE symmetric sector (360 / n_sym degrees) of wheel `idx` around its own (ax, az), ready for turned_y."""
    ax, az, R, r_pin, n_sym, _, _ = SHAFTS[idx]
    S = sp.Set(f'sec.{idx}')
    span = 360.0 / n_sym
    a0, a1 = math.radians(-span / 2), math.radians(+span / 2)
    am0, am1 = math.radians(-span / 6), math.radians(+span / 6)
    y_plane = -0.10 if (idx % 2 == 0) else +0.10
    th = 0.14 if idx < 5 else 0.18
    y0, y1 = y_plane - th / 2, y_plane + th / 2

    # Rim segment
    r_in = R - (0.14 if idx < 5 else 0.20)
    rim_pts = [
        (ax + r_in * math.sin(a0), az + r_in * math.cos(a0)),
        (ax + r_in * math.sin(am0), az + r_in * math.cos(am0)),
        (ax + r_in * math.sin(am1), az + r_in * math.cos(am1)),
        (ax + r_in * math.sin(a1), az + r_in * math.cos(a1)),
        (ax + R * math.sin(a1), az + R * math.cos(a1)),
        (ax + R * math.sin(am1), az + R * math.cos(am1)),
        (ax + R * math.sin(am0), az + R * math.cos(am0)),
        (ax + R * math.sin(a0), az + R * math.cos(a0)),
    ]
    rim_col = BRASS if idx in (0, 2, 4) else (RED_ENAMEL if idx == 5 else IRON)
    _yz_prism(S, f'w{idx}.rim', rim_pts, y0, y1, index=rim_col)

    # Teeth along this sector (3 teeth per 60-deg sector = 18 teeth; 2 teeth per 30-deg = 24; 3 per 45-deg = 24)
    n_teeth_sec = 3 if n_sym <= 8 else 2
    t_h = 0.085 if idx < 5 else 0.11
    for ti in range(n_teeth_sec):
        tc = -span / 2 + (ti + 0.5) * (span / n_teeth_sec)
        ta = math.radians(tc - span / n_teeth_sec * 0.24)
        tb = math.radians(tc + span / n_teeth_sec * 0.24)
        ta_tip = math.radians(tc - span / n_teeth_sec * 0.17)
        tb_tip = math.radians(tc + span / n_teeth_sec * 0.17)
        t_pts = [
            (ax + (R - .01) * math.sin(ta), az + (R - .01) * math.cos(ta)),
            (ax + (R - .01) * math.sin(tb), az + (R - .01) * math.cos(tb)),
            (ax + (R + t_h) * math.sin(tb_tip), az + (R + t_h) * math.cos(tb_tip)),
            (ax + (R + t_h) * math.sin(ta_tip), az + (R + t_h) * math.cos(ta_tip)),
        ]
        _yz_prism(S, f'w{idx}.t{ti}', t_pts, y0 + .01, y1 - .01, index=BRASS if idx == 5 else STEEL_HI)

    # Spoke or bolted web (all 6 spokes on Wheel 01..03 in bright steel/brass so 6-fold symmetry is unmistakable!)
    r_hub = 0.16 if idx < 5 else 0.24
    if n_sym <= 8:
        sw = 0.055 if idx < 5 else 0.075
        sp_pts = [(ax - sw, az + r_hub - .02), (ax + sw, az + r_hub - .02),
                  (ax + sw * .8, az + r_in + .02), (ax - sw * .8, az + r_in + .02)]
        sp_col = STEEL_HI if idx in (1, 2) else (BRASS_LO if idx == 5 else IRON)
        _yz_prism(S, f'w{idx}.spoke', sp_pts, y0 + .02, y1 - .02, index=sp_col)
    else:
        # Solid cast-iron web sector + bright brass rivet boss so 1/12-turn motion is unmistakable!
        web_pts = [
            (ax + r_hub * math.sin(a0), az + r_hub * math.cos(a0)),
            (ax + r_hub * math.sin(a1), az + r_hub * math.cos(a1)),
            (ax + (r_in + .01) * math.sin(a1), az + (r_in + .01) * math.cos(a1)),
            (ax + (r_in + .01) * math.sin(a0), az + (r_in + .01) * math.cos(a0)),
        ]
        _yz_prism(S, f'w{idx}.web', web_pts, y0 + .03, y1 - .03, index=IRON_DARK if idx == 3 else IRON)
        rb = 0.60 * R
        _yz_prism(S, f'w{idx}.bolt', [(ax - .045, az + rb - .045), (ax + .045, az + rb - .045),
                                      (ax + .045, az + rb + .045), (ax - .045, az + rb + .045)],
                  y0 - .02, y1 + .02, index=BRASS if idx == 3 else STEEL_HI)

    # Hub wedge + pinion tooth on the companion plane so compound reduction is mechanically complete
    hub_pts = [(ax, az), (ax + r_hub * math.sin(a1), az + r_hub * math.cos(a1)),
               (ax + r_hub * math.sin(a0), az + r_hub * math.cos(a0))]
    _yz_prism(S, f'w{idx}.hub', hub_pts, -0.24, +0.24, index=STEEL_HI if idx != 5 else BRASS)
    if r_pin > 0:
        py_plane = +0.10 if (idx % 2 == 0) else -0.10
        p_pts = [
            (ax + (r_pin * .6) * math.sin(a0), az + (r_pin * .6) * math.cos(a0)),
            (ax + (r_pin * .6) * math.sin(a1), az + (r_pin * .6) * math.cos(a1)),
            (ax + (r_pin * 1.15) * math.sin(am1), az + (r_pin * 1.15) * math.cos(am1)),
            (ax + (r_pin * 1.15) * math.sin(am0), az + (r_pin * 1.15) * math.cos(am0)),
        ]
        _yz_prism(S, f'w{idx}.pin', p_pts, py_plane - .07, py_plane + .07, index=BRASS)

    return tuple(S.solids)


def gears_at(phase):
    """All six wheels rotated to `phase` in [0, 1) of the 10-second loop."""
    out = []
    for idx, (ax, az, _, _, n_sym, deg_loop, _) in enumerate(SHAFTS):
        theta = phase * deg_loop
        span = 360.0 / n_sym
        sec = wheel_sector(idx)
        for k in range(n_sym):
            ang = theta + k * span
            for s in sec:
                t = turned_y(s, ang, about=(ax, az))
                t.name = f'{s.name}.{k}'
                out.append(t)
    return out


@lru_cache(maxsize=None)
def room_statics():
    """The stone clock room, twin arched windows onto winter night, cast-iron A-frames, worm housing, and lantern."""
    S = sp.Set('clock-room')
    stone_skin = X.blocks(STONE1, STONE2, bw=10, bh=5, seed=31, chips=(0x8, STONE_LO))
    floor_skin = X.planks(FLOOR1, FLOOR2, FLOOR_G, width=4, length=42, along='u', seed=33)

    # Timber floor & stone walls
    D.paint(S.box('floor', (-6.5, 6.8), (-4.5, 2.2), (-.2, 0.0), kind='deck'), skin=floor_skin)
    D.paint(S.box('wall.l', (-6.2, -5.8), (-4.0, 2.2), (0.0, 5.2), kind='wall'), skin=stone_skin)
    D.paint(S.box('wall.r', (5.6, 6.0), (-4.0, 2.2), (0.0, 5.2), kind='wall'), skin=stone_skin)

    # Back wall at y = +1.85 m with TWO tall arched windows (x in [-3.4, -1.6] and [-0.3, +1.5], z in [1.1, 3.8])
    yb0, yb1 = 1.85, 2.20
    D.paint(S.box('back.lo', (-6.0, 5.8), (yb0, yb1), (0.0, 1.15), kind='wall'), skin=stone_skin)
    D.paint(S.box('back.hi', (-6.0, 5.8), (yb0, yb1), (3.85, 5.20), kind='wall'), skin=stone_skin)
    for seg_i, (xa, xb) in enumerate(((-6.0, -3.45), (-1.55, -0.35), (1.55, 5.8))):
        D.paint(S.box(f'back.p{seg_i}', (xa, xb), (yb0, yb1), (1.15, 3.85), kind='wall'), skin=stone_skin)
    # Window mullions & stone sills
    for wi, wx in enumerate((-2.50, +0.60)):
        D.paint(S.box(f'sill.{wi}', (wx - 1.02, wx + 1.02), (yb0 - .08, yb1 + .04), (1.07, 1.17), kind='pile'), index=0x9)
        D.paint(S.box(f'mull.v.{wi}', (wx - .04, wx + .04), (yb0 + .05, yb0 + .14), (1.15, 3.85), kind='pile'), index=IRON_DARK)
        D.paint(S.box(f'mull.h.{wi}', (wx - .95, wx + .95), (yb0 + .05, yb0 + .14), (2.48, 2.56), kind='pile'), index=IRON_DARK)

    # Roof beams overhead
    for bx in (-4.2, -1.4, 1.4, 4.2):
        D.paint(S.box(f'beam.{bx:.1f}', (bx - .14, bx + .14), (-4.0, 2.0), (4.35, 4.70), kind='roof'), index=FLOOR2)

    # Heavy cast-iron machine bed & A-frame bearing standards for all 6 shafts
    D.paint(S.box('bed.main', (-4.45, 4.35), (-0.42, +0.42), (0.0, 0.42), kind='machine'), index=IRON_DARK)
    D.paint(S.box('bed.cap', (-4.50, 4.40), (-0.46, +0.46), (0.42, 0.50), kind='machine'), index=IRON)

    for idx, (ax, az, _, _, _, _, _) in enumerate(SHAFTS):
        for side, yp in (('f', -0.32), ('b', +0.32)):
            D.paint(S.box(f'st.{idx}.{side}', (ax - .09, ax + .09), (yp - .06, yp + .06), (0.50, az + .14), kind='machine'), index=IRON)
            # Brass plummer-block bearing cap on top of each standard!
            D.paint(S.box(f'brg.{idx}.{side}', (ax - .13, ax + .13), (yp - .08, yp + .08), (az - .10, az + .13), kind='machine'), index=BRASS)
        # Steel axle through both bearings
        D.paint(S.box(f'axle.{idx}', (ax - .05, ax + .05), (-0.44, +0.44), (az - .05, az + .05), kind='machine'), index=STEEL_HI)

    # Worm-gear reduction box connecting Shaft 5 -> Shaft 6, plus fixed benchmark pointer at top of Wheel 6!
    D.paint(S.box('worm.box', (2.35, 2.85), (-0.24, +0.24), (1.32, 1.78), kind='machine'), index=BRASS_LO)
    D.paint(S.box('worm.shaft', (1.68, 3.55), (+0.14, +0.22), (1.46, 1.54), kind='machine'), index=STEEL_HI)
    # Fixed index fiducial pointer right over the crown of Wheel 06 (x = 3.55, z = 1.92 + 1.49 = 3.41)
    D.paint(S.box('idx.post', (3.50, 3.60), (+0.28, +0.38), (1.92, 3.62), kind='machine'), index=IRON)
    D.paint(S.box('idx.arm', (3.49, 3.61), (-0.18, +0.36), (3.52, 3.62), kind='machine'), index=STEEL_HI)
    D.paint(S.box('idx.tip', (3.52, 3.58), (-0.14, -0.06), (3.38, 3.52), kind='machine'), index=0xA)

    # Tall brass oil-cup funnel atop Shaft 06's front bearing so the oiling target is unmistakable
    D.paint(S.box('oil.stem', (3.52, 3.58), (-0.35, -0.29), (2.05, 2.16), kind='machine'), index=BRASS)
    D.paint(S.prism('oil.cup', [(3.50, -0.37), (3.60, -0.37), (3.60, -0.27), (3.50, -0.27)],
                    2.16, 2.26, top=[(3.46, -0.41), (3.64, -0.41), (3.64, -0.23), (3.46, -0.23)], kind='machine'), index=0xA)

    # Two-step wooden platform beside Shaft 06 so the keeper's oilcan spout sits cleanly ABOVE the bearing funnel!
    D.paint(S.box('step.lo', (3.75, 4.95), (-1.15, -0.20), (0.0, 0.42), kind='deck'), skin=floor_skin)
    D.paint(S.box('step.box', (4.05, 4.92), (-0.98, -0.22), (0.42, 0.82), kind='deck'), skin=floor_skin)

    # Tended brass wall lantern on the right stone wall above the keeper, completely clear of Wheel 06's rim!
    lx, ly, lz = 5.22, -0.35, 3.05
    D.paint(S.box('lan.bracket', (lx, 5.60), (ly - .05, ly + .05), (lz + .26, lz + .34), kind='machine'), index=IRON_DARK)
    D.paint(S.box('lan.top', (lx - .20, lx + .20), (ly - .20, ly + .20), (lz + .20, lz + .30), kind='machine'), index=BRASS)
    D.paint(S.box('lan.bot', (lx - .18, lx + .18), (ly - .18, ly + .18), (lz - .24, lz - .16), kind='machine'), index=BRASS)
    D.paint(S.box('lan.glass', (lx - .15, lx + .15), (ly - .15, ly + .15), (lz - .16, lz + .20), kind='light'),
            index=0xF, glow=1.0, cast=False)

    return tuple(S.solids), (lx - .24, ly - .12, lz + .02)


def keeper_pose_at(phase):
    """Smooth 10-second periodic cycle (phase in 0..1):
    0.00..0.18: stands inspecting Wheel 06, lifts left hand (oilcan) up to front bearing (3.55, -0.32, 1.92)
    0.18..0.52: holds oilcan at bearing and tips twice (two careful drops at phase 0.26 and 0.42)
    0.52..0.70: lowers oilcan, leans slightly back to inspect the completely motionless wheel
    0.70..1.00: settles back to start pose (periodic seam at 0/1)."""
    rest = dict(P.STAND, shL=28, elL=42, outL=6, shR=6, elR=14, lean=-2, turn=-8)
    aim = dict(P.STAND, shL=92, elL=16, outL=8, shR=12, elR=22, lean=12, hipL=8, hipR=-8, kneeL=8, turn=-14)
    tip = dict(aim, shL=98, elL=8, lean=15)
    admire = dict(P.STAND, shL=34, elL=48, outL=8, shR=-8, elR=18, lean=-7, turn=-4)

    if phase < 0.18:
        pose = P.mix(rest, aim, phase / 0.18); look = -10 * (phase / 0.18)
    elif phase < 0.26:
        pose = P.mix(aim, tip, (phase - 0.18) / 0.08); look = -10
    elif phase < 0.34:
        pose = P.mix(tip, aim, (phase - 0.26) / 0.08); look = -10
    elif phase < 0.42:
        pose = P.mix(aim, tip, (phase - 0.34) / 0.08); look = -10
    elif phase < 0.50:
        pose = P.mix(tip, aim, (phase - 0.42) / 0.08); look = -10
    elif phase < 0.68:
        pose = P.mix(aim, admire, (phase - 0.50) / 0.18); look = -10 + 25 * ((phase - 0.50) / 0.18)
    elif phase < 0.86:
        pose = admire; look = 15
    else:
        pose = P.mix(admire, rest, (phase - 0.86) / 0.14); look = 15 * (1 - (phase - 0.86) / 0.14)

    # Suit without green; standing on the upper step (z = 0.82) so his red oilcan + white spout hover right over the funnel!
    suit = (0x9, 0x8, 0x1, 0xA, 0x2, 0xB)
    foot = (4.48, -0.42, 0.82)
    heading = 174.0
    fig_c = P.person(pose, look=look, carry=None, suit=suit)
    import copy as _cp
    c = _cp.deepcopy(fig_c)
    hd = P.hand(pose, 'L')
    c.ball(hd + np.array([0.08, 0.0, 0.02]), (0.11, 0.09, 0.12), 0xD)
    c.limb(hd + np.array([0.14, 0.0, 0.08]), hd + np.array([0.52, 0.0, -0.02]), 0.045, 0.028, 0xA)
    c.limb(hd + np.array([-0.02, 0.0, -0.04]), hd + np.array([-0.02, 0.0, 0.08]), 0.03, 0.03, 0x9)
    return c.block('keeper', at=foot, turn=heading)


# Periodic vertical snow outside the two arched windows (180 flakes, gentle downward fall, exact 10 s period)
_rng_s = np.random.default_rng(44)
SNOW_P = np.c_[_rng_s.uniform(-3.5, 1.6, 180), _rng_s.uniform(2.5, 3.3, 180), _rng_s.uniform(0.0, 1.0, 180), _rng_s.uniform(-0.06, 0.06, 180)]
STARS_BG = np.c_[_rng_s.uniform(-4.0, 2.2, 70), np.full(70, 9.0), _rng_s.uniform(1.2, 4.5, 70)]

CAM = sp.Camera(eye=(0.42, -7.25, 2.08), look=(0.48, 0.40, 1.82), lens=24, size=(W, H), name='clockroom')
_LIGHTS_CACHE = None


def get_lights():
    global _LIGHTS_CACHE
    if _LIGHTS_CACHE is None:
        statics, lpos = room_statics()
        # Warm lantern on the right wall casting spoked gear shadows across the stone back wall + cool window fill
        lan = D.Light(lpos, power=5.8, reach=10.5, aim=(-0.72, -0.18, -0.22), cone=(56, 82), size=768).bake(list(statics))
        win1 = D.Light((-2.5, 1.6, 2.6), power=1.05, reach=6.8, shadow=False)
        win2 = D.Light((+0.6, 1.6, 2.6), power=0.85, reach=6.4, shadow=False)
        front_fill = D.Light((-2.2, -4.2, 2.8), power=0.75, reach=9.0, shadow=False)
        _LIGHTS_CACHE = (lan, win1, win2, front_fill)
    return _LIGHTS_CACHE


def render_frame(i):
    phase = (i % NF) / NF
    statics, lpos = room_statics()
    gears = gears_at(phase)
    k_blk = keeper_pose_at(phase)

    # Prominent golden-orange oil drops falling from spout into Shaft 06's brass oil funnel (phase 0.23..0.33, 0.39..0.49)
    extras = []
    for p0 in (0.23, 0.39):
        if p0 <= phase < p0 + 0.10:
            u = (phase - p0) / 0.10
            dz = 2.46 - 0.24 * (u * u)
            extras.append(D.paint(sp.Set('d').box('drop', (3.51, 3.60), (-0.37, -0.28), (dz, dz + .11)), index=0xE, glow=0.8, cast=False))

    moving = gears + [k_blk] + extras
    g = D.gbuffer(list(statics) + moving, CAM)
    lan, win1, win2, front_fill = get_lights()
    lv = D.lighting(g, [lan, win1, win2, front_fill], ambient=.12, moving=moving)

    img = X.colour(g, lv, steps=6, gamma=.82, dark=0, dither=1.0)

    # Night sky, stars, and periodic falling snow seen through the two arched windows (~g['hit'])
    sky_m = ~g['hit']
    if sky_m.any():
        yy = np.mgrid[:H, :W][0]
        sky_col = U.C[0][None, None, :] * 0.55 + U.C[1][None, None, :] * 0.45
        img[sky_m] = sky_col[0, 0]
        for sx_w, sy_w, sz_w in STARS_BG:
            px, py = CAM.p(sx_w, sy_w, sz_w)
            ix, iy = int(round(px)), int(round(py))
            if 0 <= ix < W - 2 and 0 <= iy < H - 2 and sky_m[iy, ix]:
                img[iy:iy + 2, ix:ix + 2] = U.C[0x9]
        for sx_w, sy_w, ph0, drift in SNOW_P:
            u = (ph0 + phase * 2.0) % 1.0                                      # integer 2 cycles per loop -> seamless!
            xw = sx_w + drift * math.sin(2 * math.pi * (phase + ph0))
            zw = 4.0 - u * 3.0
            px, py = CAM.p(xw, sy_w, zw)
            ix, iy = int(round(px)), int(round(py))
            if 0 <= ix < W - 3 and 0 <= iy < H - 3 and sky_m[iy, ix]:
                img[iy:iy + 3, ix:ix + 3] = U.C[0xA]

    # Only register F glows (the tended lantern on the right pier)
    img = X.glow(img, strength=.52, r0=6, r1=24)

    # Crisp system labels above each shaft + bottom status bar + signature strip
    for idx, (ax, az, R, _, _, _, lbl) in enumerate(SHAFTS):
        px, py = CAM.p(ax, 0.0, az + R + (0.28 if idx < 5 else 0.24))
        tw = U.tw(lbl, scale=2)
        bx = min(max(int(round(px)) - tw // 2, 8), W - tw - 12)
        by = max(int(round(py)) - 22, 10)
        U.rect(img, bx - 6, by - 4, bx + tw + 6, by + 19, U.C[0], a=.86)
        U.rect(img, bx - 6, by - 6, bx + tw + 6, by - 4, U.C[0xE if idx == 5 else 0x3])
        U.text(img, bx, by, lbl, U.C[0xA if idx in (0, 5) else 0x9], scale=2)

    # Bottom status bar: live oil-drop counter so the action is registered in system type!
    U.rect(img, 0, H - 34, W, H, U.C[0])
    U.rect(img, 0, H - 36, W, H - 34, U.C[2])
    turns1 = 6.0 * phase
    drops = 0 if phase < 0.28 else (1 if phase < 0.44 else 2)
    bar_s = f'6 SHAFTS  W01: {turns1:3.1f} TURNS  W06: 0.000000 TURNS  OIL: {drops}/2 DROPS'
    assert U.tw(bar_s, 2) < W - 224, f'Status text too wide: {U.tw(bar_s, 2)}'
    U.text(img, 14, H - 25, bar_s, U.C[0xA], scale=2)
    U.strip(img, W - 206, H - 23, s=10, gap=2)
    return img


def _worker(i):
    X.save(str(FRAMES / f'f_{i:04d}.png'), render_frame(i))
    return i


def draw_elevation(out_path):
    """Mechanical elevation of the 6-shaft reduction train in Hex registers (640 x 360 -> 1280 x 720)."""
    c = kit.Canvas(640, 360, fill=0x0)
    cx0, cy0, sc = 305, 314, 62.0
    def mp(x, z): return int(round(cx0 + x * sc)), int(round(cy0 - z * sc))
    for g_x in range(-5, 6):
        x, _ = mp(g_x, 0); c.rect(x, 20, x + 1, 336, 0x1)
    for g_z in range(0, 5):
        _, y = mp(0, g_z); c.rect(10, y, 630, y + 1, 0x1)
    bx0, by0 = mp(-4.50, 0.50); bx1, by1 = mp(4.40, 0.0)
    c.rect(bx0, by0, bx1, by1, 0x2); c.line((bx0, by0), (bx1, by0), 0x8, 2)
    for idx, (ax, az, R, r_pin, n_sym, _, lbl) in enumerate(SHAFTS):
        sx, sy = mp(ax, az)
        c.line((sx, sy), (sx, by0), 0x8, 2)
        c.ring(sx, sy, int(round(R * sc)), 0xD if idx == 5 else (0xE if idx in (0, 2, 4) else 0x9), 2)
        if r_pin > 0:
            c.ring(sx, sy, int(round(r_pin * sc)), 0xA, 1)
        for k in range(n_sym):
            a = math.radians(k * 360.0 / n_sym)
            c.line((sx, sy), (sx + R * sc * math.sin(a), sy - R * sc * math.cos(a)), 0x8, 1)
        c.text(sx - 8, sy - int(round(R * sc)) - 11, f'W{idx + 1}', 0xA)
    lx, ly = mp(4.74, 2.59); c.rect(lx - 5, ly - 6, lx + 5, ly + 6, 0xF)
    c.rect(0, 0, 640, 16, 0x0); c.text(8, 4, 'ELEVATION: COMPOUND REDUCTION TRAIN (SHAFTS 01 TO 06)', 0xA)
    c.rect(0, 344, 640, 360, 0x0); c.text(8, 348, 'W01: 36/MIN -> W04: 10/HR -> W06: 1 TURN / 1000 YEARS', 0x9)
    for k in range(16): c.rect(640 - 6 - (16 - k) * 6, 349, 640 - 6 - (16 - k) * 6 + 5, 354, k)
    c.save(out_path, scale=2)


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'all'
    OUT.mkdir(parents=True, exist_ok=True); FRAMES.mkdir(parents=True, exist_ok=True)
    draw_elevation(HERE / 'sixth_wheel_plan.png')
    if mode == 'test':
        for f in (0, 66, 150, 239):
            X.save(str(OUT / f'test_{f:04d}.png'), render_frame(f))
        print('wrote test frames to', OUT)
    else:
        with Pool(24) as pool:
            list(pool.imap_unordered(_worker, range(NF), chunksize=6))
        X.save(str(HERE / 'sixth_wheel_still.png'), render_frame(66))
        subprocess.run([
            'ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS),
            '-i', str(FRAMES / 'f_%04d.png'),
            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-preset', 'slow',
            '-movflags', '+faststart', str(HERE / 'sixth_wheel.mp4')
        ], check=True)
        from backlot import screen, sync
        seam = screen.loop_seam(str(FRAMES))
        pops = sync.pops([], str(FRAMES), fps=FPS)
        screen.filmstrip(str(FRAMES), str(OUT / 'strip.jpg'), n=12)
        screen.motion_map(str(FRAMES), str(HERE / 'sixth_wheel_motion.jpg'))
        print('wrote', HERE / 'sixth_wheel.mp4', 'seam:', seam, 'pops:', pops)
