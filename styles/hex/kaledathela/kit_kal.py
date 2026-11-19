"""Kaledathela visual kit: cast sprites, megamoon sky (Primary + Worm subspace border), Texas flora & pumpjack.

Shared across concept plates (`plates.py`) and animation (`film.py`) so every silhouette, ruin motif and light code
is built once (`Rule 12: One thing, one model`).
"""
import sys, math
from pathlib import Path
HERE = Path(__file__).resolve().parent; HEX = HERE.parent; ROOT = HERE.parents[2]
sys.path.insert(0, str(HEX)); sys.path.insert(1, str(ROOT)); sys.path.insert(2, str(HEX / 'uptime'))
import numpy as np
import cv2
import kit, ui as U

# ------------------------------------------------------------------ Cast sprites (1 hex digit per pixel; '.' empty)
# Every dark hat gets a register-8/3 rim highlight so it never vanishes against night sky (Fault 1).

PASTOR = """
......888888........
.....00000000.......
.....00000000.......
.....DDDDDDDD.......
.8888888888888888...
.0000000000000000...
.....08899880.....A.
.....08088080....ADA
.....08899880.....A.
.....00AAAA00.....9.
....0011AA1100....9.
...001111111100...9.
...011118811110...9.
..00111188111199999.
..00111188111100..9.
...011111111110...9.
...011111111110...9.
...011110011110...9.
...011110011110...9.
..00111100111100..9.
..00111000011100..9.
..001110..011100..9.
..000000..000000..9.
.0000000..0000000.8.""".strip('\n').split('\n')

HUNTER = """
....88888888........
...0000000000.......
.88888888888888.....
.00000000000000.....
....08DDDD80........
....08899880.....A..
...0888888880...AD..
..088188881889999A..
..088188881880..8...
..099188881880......
...0888888880.......
...0111001110.......
...0111001110.......
...0110..0110.......
...0110..0110.......
...0000..0000.......
..00000..00000......""".strip('\n').split('\n')

DRONE_INQ = """
.99999....99999.
...8...AA...8...
..88888AA88888..
.899999DD999998.
..88899AA99888..
.....88AA88.....
......AAAA......""".strip('\n').split('\n')

# Three distinct Coven witches (individuals, never a uniform hive; only witches are green 5, 6, 7)
WITCH_SIGNAL = """
.......80.........
......800.........
.....80000........
....8000000.......
...333333336......
.88000000000088...
..000000000000....
....0666665.......
....06A60666......
....06666655......
.....05665........
....00222200...6..
...0022332200..5..
..00222332220667..
..002222222200.5..
..00222222220..5..
..00222002220..8..
.000220..02200.8..
.000220..02200....
.000000..00000....""".strip('\n').split('\n')

WITCH_BAYOU = """
.....88888........
....8222228.......
..88222222288.....
.0000000000000....
....0566665.......
....05A6066.......
....0556655.......
...0011221100.....
..001122221100....
..011122221166....
..01122222210.....
...0122002210.....
...0110..0110.....
...0000..0000.....
..00000..00000....""".strip('\n').split('\n')

WITCH_RUNNER = """
....833338........
...33222233.......
...00666650.......
...006A6066.......
....056665........
...003322300..88..
..003322233668FF8.
..0033222330.8FF8.
...033202330..88..
...0110.0110......
...0110.0110......
...0000.0000......""".strip('\n').split('\n')


# ------------------------------------------------------------------ Megamoon Sky (Primary + Worm Subspace Border)
def draw_sky_canvas(c, horizon_y, primary_x=470, primary_y=124, primary_r=108,
                    worm_p0=(-20, 26), worm_vp=(268, None), transit_u=None, seed=41):
    """Draw the Kaledathela night sky onto an indexed `kit.Canvas` (e.g. 640 x 360):
      1. Bruised toxic twilight-to-void dithered gradient (0, 1, 2, 3) + star lattice
      2. Giant banded Primary (`Kaledathela`) half-lit in slate/violet/chrome
      3. Ruled Worm Subspace Border (perspective ring-corridor + cold aqua 0xC containment rails)."""
    W, H = c.w, c.h
    worm_vp = (worm_vp[0], horizon_y - 2) if worm_vp[1] is None else worm_vp
    c.grad(0, horizon_y, [0, 0, 1, 1, 2, 2, 3], power=1.25)
    kit.stars(c, horizon_y - 6, seed=seed, step=12, cols=(8, 8, 9, 9, 0xA))

    # Giant banded Primary (`Kaledathela`) clipped above horizon_y
    yy, xx = np.mgrid[:horizon_y, :W].astype(np.float32)
    dx, dy = xx - primary_x, yy - primary_y
    r2 = dx * dx + dy * dy
    in_disc = r2 <= primary_r * primary_r
    # Spherical normal for crescent/gibbous lighting from upper-left + tilted storm bands
    nz = np.sqrt(np.maximum(primary_r * primary_r - r2, 0.0)) / primary_r
    nx, ny = dx / primary_r, dy / primary_r
    illum = np.clip(-0.62 * nx - 0.34 * ny + 0.52 * nz, 0.0, 1.0)
    lat = (dy * 0.94 + dx * 0.34) / primary_r
    band = 0.5 + 0.5 * np.sin(lat * 15.0 + 0.35 * np.sin(lat * 5.0 + nx * 2.5))
    tone = illum * (0.68 + 0.32 * band)
    byr = kit.bayer(horizon_y, W)
    # Map tone into strictly non-green registers [0, 1, 2, 3, 8, 9]
    pal_p = np.array([1, 1, 2, 3, 8, 9], np.uint8)
    u = np.clip(tone * (len(pal_p) - 1), 0.0, len(pal_p) - 1.001)
    k = u.astype(int)
    p_reg = np.where(byr < (u - k), pal_p[k + 1], pal_p[k])
    # Dark side of the Primary blends subtly into midnight sky (register 1) so its huge dark limb is felt!
    dark_limb = in_disc & (illum <= 0.08)
    lit_limb = in_disc & (illum > 0.08)
    c.a[:horizon_y][dark_limb] = 1
    c.a[:horizon_y][lit_limb] = p_reg[lit_limb]

    # Worm Subspace Border: straight ruled perspective corridor from worm_p0 to worm_vp on the horizon
    x0, y0 = worm_p0; x1, y1 = worm_vp
    vx, vy = x1 - x0, y1 - y0
    L = math.hypot(vx, vy); ux, uy = vx / L, vy / L
    nx_p, ny_p = -uy, ux

    # Twin containment filaments converging to vanishing point
    for sign in (-1, 1):
        for s_i in range(120):
            u0, u1 = s_i / 120.0, (s_i + 1) / 120.0
            hw0 = 15.0 * (1.0 - u0) + 1.0
            hw1 = 15.0 * (1.0 - u1) + 1.0
            pa = (x0 + vx * u0 + nx_p * sign * hw0, y0 + vy * u0 + ny_p * sign * hw0)
            pb = (x0 + vx * u1 + nx_p * sign * hw1, y0 + vy * u1 + ny_p * sign * hw1)
            if pa[1] < horizon_y and pb[1] < horizon_y:
                c.line(pa, pb, 0xC if u0 < 0.55 else 0xB, 1)
    # Central faint spine
    c.line((x0, y0), (x1, y1), 0x2, 1)

    # Segmented ancient Worm-rings spaced in perspective (1 / depth spacing)
    for k_r in range(1, 18):
        u_r = 1.0 - 1.0 / (1.0 + k_r * 0.28)
        cx_r = x0 + vx * u_r; cy_r = y0 + vy * u_r
        if cy_r >= horizon_y - 2:
            continue
        rw = max(int(round(17.0 * (1.0 - u_r) + 1.2)), 2)
        rh = max(int(round(6.5 * (1.0 - u_r) + 0.8)), 1)
        ang = math.degrees(math.atan2(vy, vx)) + 90.0
        cv2.ellipse(c.a, (int(round(cx_r)), int(round(cy_r))), (rw, rh), ang, 0, 360, 0x8 if u_r < 0.65 else 0x3, 1, cv2.LINE_8)
        if rw >= 7:
            cv2.ellipse(c.a, (int(round(cx_r - ux)), int(round(cy_r - uy))), (rw, rh), ang, -70, 70, 0x9, 1, cv2.LINE_8)

    # Optional ship transit spark slipping along the corridor
    if transit_u is not None and 0.0 <= transit_u <= 1.0:
        tx = int(round(x0 + vx * transit_u)); ty = int(round(y0 + vy * transit_u))
        if 0 <= ty < horizon_y:
            c.line((tx - int(ux * 10), ty - int(uy * 10)), (tx, ty), 0xC, 1)
            c.disc(tx, ty, 2, 0xA)
    return c


# ------------------------------------------------------------------ Measured East & West Texas Motifs
def draw_loblolly(c, x, y_base, h, seed=1, col_trunk=1, col_crown=0):
    """East Texas loblolly pine (`Pinus taeda`): tall bare pole trunk for the bottom ~62%, topped by flat-ish
    irregular needle clumps (strictly non-green: 0, 1, 2)."""
    r = np.random.default_rng(seed)
    lean = float(r.uniform(-0.04, 0.04)) * h
    tw = max(1, int(round(h * 0.028)))
    # Straight bare trunk
    for k in range(int(h * 0.92)):
        yk = int(round(y_base - k))
        xk = int(round(x + lean * (k / h)))
        w_here = max(1, int(round(tw * (1.0 - 0.45 * k / h))))
        c.rect(xk - w_here, yk, xk + w_here + 1, yk + 1, col_trunk)
    # High irregular tufted crown pads (upper 38% only)
    for frac, side, wf, hf in ((0.64, -1, 0.20, 0.06), (0.69, +1, 0.22, 0.06),
                               (0.77, -0.7, 0.24, 0.07), (0.84, +0.6, 0.21, 0.07),
                               (0.93, 0.0, 0.18, 0.07)):
        cy = int(round(y_base - h * frac))
        cx = int(round(x + lean * frac + side * h * 0.11 + r.uniform(-2, 2)))
        rx, ry = max(4, int(round(h * wf))), max(2, int(round(h * hf)))
        # Branch connecting trunk to pad
        tx_b = int(round(x + lean * frac))
        c.line((tx_b, cy + 2), (cx, cy), col_trunk, 1)
        cv2.ellipse(c.a, (cx, cy), (rx, ry), 0, 0, 360, col_crown, -1, cv2.LINE_8)
        cv2.ellipse(c.a, (cx - 2, cy - 1), (max(2, rx - 3), max(1, ry - 1)), 0, 180, 360, 1 if col_crown == 0 else 2, 1, cv2.LINE_8)


def draw_cypress(c, x, y_water, h, seed=2, col_trunk=1, col_moss=2):
    """Bald cypress (`Taxodium distichum`): wide fluted buttress in stagnant water, conical knees, flat spreading
    branches, and vertical curtains of hanging moss."""
    r = np.random.default_rng(seed)
    bw = max(4, int(round(h * 0.09)))
    tw = max(2, int(round(h * 0.032)))
    # Flared buttress + tapering trunk
    pts = [
        (x - bw, y_water), (x - tw - 1, y_water - h * 0.18), (x - tw + 1, y_water - h * 0.88),
        (x + tw - 1, y_water - h * 0.88), (x + tw + 1, y_water - h * 0.18), (x + bw, y_water)
    ]
    c.poly(pts, col_trunk)
    # Conical cypress knees rising out of the bayou round the base
    for dx in (-bw * 2.1, -bw * 1.4, bw * 1.3, bw * 2.0, bw * 2.7):
        kx = int(round(x + dx + r.uniform(-2, 2)))
        kh = int(round(r.uniform(5, 12)))
        c.poly([(kx - 2, y_water), (kx + 2, y_water), (kx, y_water - kh)], col_trunk)
    # Flat-topped spreading branches + hanging moss drapes
    for frac, span in ((0.70, -0.28), (0.76, +0.30), (0.85, -0.24), (0.91, +0.22), (0.96, 0.0)):
        by = int(round(y_water - h * frac))
        bx1 = int(round(x + span * h))
        c.line((x, by + 3), (bx1, by), col_trunk, 2)
        rx = max(6, int(round(abs(span) * h * 0.65 + 8)))
        cv2.ellipse(c.a, ((x + bx1) // 2, by - 2), (rx, 4), 0, 0, 360, 0, -1, cv2.LINE_8)
        # Hanging moss threads
        x_lo, x_hi = min(x, bx1) - 4, max(x, bx1) + 4
        for mx in range(x_lo, x_hi, 4):
            ml = int(r.integers(5, 15))
            c.line((mx, by), (mx, by + ml), col_moss, 1)


def draw_pumpjack_2d(c, x, y_base, scale=1.0, phase=0.0, col_main=0, col_hi=8):
    """Four-bar Lufkin pumpjack on a `kit.Canvas` (or scaled coordinates).
    `x, y_base`: ground centre under Sampson post; horsehead to the left, crank & counterweight to the right."""
    S = scale
    # Concrete pad
    c.rect(x - 38 * S, y_base - 3 * S, x + 36 * S, y_base + 1, col_hi)
    # Sampson post A-frame to saddle pivot
    piv = (x, y_base - 34 * S)
    c.line((x - 12 * S, y_base - 3 * S), piv, col_main, max(1, int(round(2 * S))))
    c.line((x + 10 * S, y_base - 3 * S), piv, col_main, max(1, int(round(2 * S))))
    c.line((x - 7 * S, y_base - 17 * S), (x + 6 * S, y_base - 17 * S), col_main, 1)

    # Gearbox & rotary crank shaft on right
    gbx, gby = x + 22 * S, y_base - 13 * S
    c.rect(gbx - 6 * S, gby - 5 * S, gbx + 6 * S, y_base - 3 * S, col_main)
    theta = 2.0 * math.pi * phase
    r_crank = 8.5 * S
    # Heavy rotary counterweight lobe (opposite crank pin or leading)
    cw_ang = theta + math.pi * 0.15
    cwx = gbx + 11.5 * S * math.cos(cw_ang); cwy = gby + 11.5 * S * math.sin(cw_ang)
    c.line((gbx, gby), (cwx, cwy), col_hi, max(2, int(round(3 * S))))
    c.disc(cwx, cwy, max(2, int(round(4.5 * S))), col_main)

    # Four-bar beam angle driven by crank pin
    pin_x = gbx + r_crank * math.cos(theta); pin_y = gby + r_crank * math.sin(theta)
    alpha = math.asin(max(-0.45, min(0.45, 0.24 * math.sin(theta))))            # +-14 deg walking-beam rock
    L_front, L_back = 24.0 * S, 22.0 * S
    front = (piv[0] - L_front * math.cos(alpha), piv[1] - L_front * math.sin(alpha))
    back = (piv[0] + L_back * math.cos(alpha), piv[1] + L_back * math.sin(alpha))

    # Pitman arm from crank pin to rear of walking beam
    c.line((pin_x, pin_y), back, col_hi, max(1, int(round(1.6 * S))))
    # Walking beam
    c.line(front, back, col_main, max(2, int(round(3.2 * S))))
    c.line((front[0], front[1] - 1), (back[0], back[1] - 1), col_hi, 1)

    # Curved arc horsehead at `front`: circular arc of radius L_front centred on `piv` so wireline stays vertical!
    well_x = piv[0] - L_front
    hh_pts = []
    for da in np.linspace(-0.26, +0.28, 7):
        ang = alpha + da
        hh_pts.append((piv[0] - (L_front + 1.5 * S) * math.cos(ang), piv[1] - (L_front + 1.5 * S) * math.sin(ang)))
    hh_pts.append((front[0] + 3 * S, front[1]))
    c.poly(hh_pts, col_main)

    # Strictly vertical wireline bridle + polished rod + wellhead stuffing box!
    top_wire_y = hh_pts[-2][1]
    c.line((well_x, top_wire_y), (well_x, y_base - 3 * S), col_hi, 1)
    c.rect(well_x - 3 * S, y_base - 10 * S, well_x + 3 * S, y_base - 3 * S, col_main)
    return c


# ================================================================== Combat & Raid Kit (`COMBAT.md`)
# Perimeter close-quarters Coven witch (`THORN`: long dark duster, twin green-etched 0x7 blades)
WITCH_THORN = """
....8888888.......
...003333000......
.8800000000088....
..006666650.......
..006A60660.......
...0566655........
..0011221100...7..
.001122221100.76..
.01112222116676...
.011220022110.....
.01220..02210.....
.0120....0210.....
00110....01100....
00000....00000....""".strip('\n').split('\n')

# Fallen / collapsed silhouettes: knocked-off wide-brim hat + slumped coat + 0xD wound + boots (never a grey pancake!)
HUNTER_DOWN = """
.888888...888888......
80000008.08899880.....
........088DD8881100..
.......0088D8881111000
.......000088800110000""".strip('\n').split('\n')

WITCH_WOUNDED = """
....8888888.......
..88003300088.....
....0444440.......
....0494040.......
...001121100......
..00112D21100.....
..01122DD2140.....
.001120022100.....
000000..000000....""".strip('\n').split('\n')


def draw_dropship(c, x, y, scale=1.0, ramp_open=0.0, thrust=1.0, tilt_deg=0.0, damaged=False):
    """Brutalist Inquisition Reliquary Dropship (`0, 1, 8, 9` angular hull, `0xA` cross, `0xE` VTOL thrusters).
    `x, y`: hull belly centre; `ramp_open` in [0, 1] lowers the assault ramp on the right; `thrust` scales VTOL fire."""
    S = scale
    # Hull polygon (angular armored transport, nose/cockpit left, troop bay + ramp right)
    hull = np.array([
        (-58, -8), (-42, -24), (-10, -28), (38, -26), (54, -14), (50, 2), (-44, 2)
    ], np.float32) * S
    if abs(tilt_deg) > 0.1:
        rad = math.radians(tilt_deg)
        co, si = math.cos(rad), math.sin(rad)
        hull = np.c_[hull[:, 0] * co - hull[:, 1] * si, hull[:, 0] * si + hull[:, 1] * co]
    hull[:, 0] += x; hull[:, 1] += y
    c.poly(hull, 8)
    # Recessed dark armored flank slab + bright steel upper chine so the hull pops against any night sky!
    inner = np.array([
        (-48, -7), (-36, -20), (-8, -23), (34, -21), (46, -12), (44, 0), (-38, 0)
    ], np.float32) * S
    if abs(tilt_deg) > 0.1:
        inner = np.c_[inner[:, 0] * co - inner[:, 1] * si, inner[:, 0] * si + inner[:, 1] * co]
    inner[:, 0] += x; inner[:, 1] += y
    c.poly(inner, 1)
    c.line(tuple(hull[1]), tuple(hull[2]), 9, max(1, int(round(2 * S))))
    c.line(tuple(hull[2]), tuple(hull[3]), 9, max(1, int(round(2 * S))))
    c.rect(x - 42 * S, y - 2 * S, x + 46 * S, y + 3 * S, 0)

    # Crimson 0xD armored cockpit slit on left nose
    c.line((x - 49 * S, y - 12 * S), (x - 36 * S, y - 15 * S), 0xD, max(1, int(round(2 * S))))

    # Stark 0xA Liturgical Cross painted on the armored flank
    cx_p, cy_p = int(round(x - 6 * S)), int(round(y - 15 * S))
    c.line((cx_p, cy_p - int(9 * S)), (cx_p, cy_p + int(9 * S)), 0xA, max(1, int(round(2.2 * S))))
    c.line((cx_p - int(6 * S), cy_p - int(3 * S)), (cx_p + int(6 * S), cy_p - int(3 * S)), 0xA, max(1, int(round(2.2 * S))))

    # Open troop-bay interior (`0xA` harsh floodlight when ramp_open > 0.15)
    if ramp_open > 0.05:
        bx0, by0, bx1, by1 = int(round(x + 22 * S)), int(round(y - 18 * S)), int(round(x + 46 * S)), int(round(y + 1 * S))
        bay_m = np.zeros((c.h, c.w), bool)
        bay_m[max(0, by0):min(c.h, by1), max(0, bx0):min(c.w, bx1)] = True
        c.mix(bay_m, 1, 0xA, 0.58 * ramp_open)
        c.line((bx0, by0), (bx1, by0), 0xA, 1)
        # Articulated steel ramp swinging down-right to touch stone at `y + 14*S`
        rx_end = int(round(x + (48 + 20 * ramp_open) * S))
        ry_end = int(round(y + (-10 + 24 * ramp_open) * S))
        c.line((int(round(x + 44 * S)), int(round(y + 1 * S))), (rx_end, ry_end), 9, max(2, int(round(3 * S))))

    # Heavy landing struts
    for lx in (-28 * S, 18 * S):
        c.line((x + lx, y + 2 * S), (x + lx - 4 * S, y + 13 * S), 8, max(1, int(round(2 * S))))
        c.rect(x + lx - 8 * S, y + 12 * S, x + lx + 2 * S, y + 14 * S, 9)

    # Twin VTOL thruster nacelles + `0xE`/`0xA` downward propellant wash (NEVER 0xF!)
    for nx in (-24 * S, 14 * S):
        px_n, py_n = int(round(x + nx)), int(round(y - 4 * S))
        c.rect(px_n - int(7 * S), py_n - int(6 * S), px_n + int(7 * S), py_n + int(5 * S), 0)
        c.rect(px_n - int(7 * S), py_n - int(6 * S), px_n + int(7 * S), py_n - int(4 * S), 8)
        if thrust > 0.05:
            plen = int(round(22 * S * thrust))
            c.poly([(px_n - int(4 * S), py_n + int(5 * S)),
                    (px_n + int(4 * S), py_n + int(5 * S)),
                    (px_n + int(7 * S * thrust), py_n + int(5 * S) + plen),
                    (px_n - int(7 * S * thrust), py_n + int(5 * S) + plen)], 0xE)
            c.poly([(px_n - int(2 * S), py_n + int(5 * S)),
                    (px_n + int(2 * S), py_n + int(5 * S)),
                    (px_n, py_n + int(5 * S) + int(plen * 0.55))], 0xA)

    if damaged:
        # Smoke plume + blinking 0xD hull damage scar on retreat
        c.disc(int(round(x + 10 * S)), int(round(y - 16 * S)), max(2, int(4 * S)), 0xD)
        for ks in range(4):
            c.disc(int(round(x + (10 - ks * 8) * S)), int(round(y - (22 + ks * 6) * S)), max(3, int((4 + ks * 2) * S)), 2 if ks < 2 else 1)
    return c


def draw_scarred_pillar(c, x, y_top, y_bot, w=24, damage=0.0, burst_y=None, strobe=False, seed=1):
    """Carved middle-empire stone column (`8/9/1`) with persistent ballistic craters (`damage` in [0, 1])
    and optional active bullet-impact stone burst (`burst_y`) inspired by *The Matrix* lobby shootout."""
    x0, x1 = int(round(x - w // 2)), int(round(x + w // 2))
    body_col = 9 if strobe else 8
    shd_col = 8 if strobe else 1
    hi_col = 0xA if strobe else 9
    c.rect(x0, y_top, x1, y_bot, body_col)
    c.rect(x1 - max(3, w // 4), y_top, x1, y_bot, shd_col)
    c.rect(x0, y_top, x0 + 3, y_bot, hi_col)
    # Classical fluted grooves + carved capital & plinth
    for gx in range(x0 + 6, x1 - 5, 5):
        c.line((gx, y_top + 8), (gx, y_bot - 8), shd_col, 1)
    c.rect(x0 - 4, y_top, x1 + 4, y_top + 7, hi_col)
    c.rect(x0 - 4, y_bot - 7, x1 + 4, y_bot, body_col)

    # Persistent ballistic bite-marks / craters chewed out of the column (`0` void + `2`/`9` fractured stone rim so
    # craters stay 100% legible against BOTH lit `1` walls and pitch-dark `0` halls!)
    if damage > 0.02:
        r = np.random.default_rng(seed)
        n_scars = int(round(damage * 11))
        for _ in range(n_scars):
            sy = int(r.integers(y_top + 22, y_bot - 22))
            side = -1 if r.random() < 0.68 else 1
            cx_s = x0 + 2 if side < 0 else x1 - 2
            rad_s = int(r.integers(3, 8))
            c.disc(cx_s - side * 2, sy, rad_s, 9 if strobe else 2)
            c.disc(cx_s, sy, max(2, rad_s - 1), 0)

    # Active bullet impact: flying angular masonry chips (`9`/`0xA`) + Bayer-dithered stone dust cloud!
    if burst_y is not None:
        by = int(round(burst_y))
        dust_m = np.zeros((c.h, c.w), bool)
        cv2.circle(dust_m, (x0 - 6, by), 16, 1, -1)
        c.mix(dust_m, 1, 9, 0.45)
        c.disc(x0, by, 4, 0xA)
        for ang, dist in ((-2.6, 15), (-2.9, 21), (2.7, 18), (2.3, 13), (-2.2, 10)):
            px_c = int(round(x0 + dist * math.cos(ang)))
            py_c = int(round(by + dist * math.sin(ang)))
            c.rect(px_c - 1, py_c - 1, px_c + 2, py_c + 1, 0xA if dist < 15 else 9)
    return c


def draw_blood_arc(c, x, y, dx, dy, progress=0.5, witch_sparks=False):
    """Artistic/soft-R gravity-curved crimson `0xD` arterial splash & droplet fan (`progress` in [0, 1]).
    NEVER a straight ruler-line (which looks like a laser): arcs upward then curves sharply down under gravity!"""
    u = max(0.0, min(1.0, progress))
    grav = 34.0
    # Curved parabolic ribbon + discrete droplets along 3 diverging trajectories
    for spread_k, w_d, col_d in ((0.0, 3, 0xD), (0.22, 2, 0xD), (-0.18, 2, 2)):
        ddx = dx * (1.0 + spread_k * 0.4)
        ddy = dy + spread_k * 18.0
        for s in np.linspace(max(0.05, u - 0.55), u, 7):
            px_d = int(round(x + ddx * s))
            py_d = int(round(y + ddy * s + grav * s * s))
            r_d = w_d if s < u * 0.75 else max(1, w_d - 1)
            c.rect(px_d - r_d // 2, py_d - r_d // 2, px_d + (r_d + 1) // 2, py_d + (r_d + 1) // 2, col_d)
    for frac, ox, oy in ((0.65, 3, -4), (0.88, -2, 3), (1.08, 4, 6), (1.20, 2, 11)):
        s = min(1.15, u * frac)
        px_d = int(round(x + dx * s + ox))
        py_d = int(round(y + dy * s + grav * s * s + oy))
        c.rect(px_d, py_d, px_d + 2, py_d + 2, 0xD)
    if witch_sparks:
        for frac, oy in ((0.55, -8), (0.88, -5), (1.05, 2)):
            px_s = int(round(x + dx * u * frac))
            py_s = int(round(y + dy * u * frac + oy))
            c.rect(px_s, py_s, px_s + 2, py_s + 2, 5 if u < 0.5 else 4)
    return c


def draw_blood_pool(c, x, y, rx, ry=3):
    """Persistent settled blood pool on stone/water: deep wine-indigo `0x2`/`0x0` core with `1px 0xD` wet meniscus."""
    if rx <= 1:
        return c
    ix, iy, irx, iry = int(round(x)), int(round(y)), int(round(rx)), max(1, int(round(ry)))
    cv2.ellipse(c.a, (ix, iy), (irx, iry), 0, 0, 360, 0xD, 1, cv2.LINE_8)
    if irx > 2:
        cv2.ellipse(c.a, (ix, iy), (irx - 1, max(1, iry - 1)), 0, 0, 360, 2, -1, cv2.LINE_8)
    return c


def draw_hex_lattice(c, x, y, h=64, slugs=5, pulse=0.0):
    """*The Matrix* bullet-stopping hex-ward plane (`0x6`/`0x7` vertical/tilted emerald grid + ripple rings
    arresting `0xE`/`0xA` ballistic slugs in mid-air)."""
    ix, iy, hh = int(round(x)), int(round(y)), int(round(h // 2))
    # Translucent dithered emerald ward plane
    lat_m = np.zeros((c.h, c.w), bool)
    cv2.ellipse(lat_m, (ix, iy), (9, hh), 0, 0, 360, 1, -1)
    c.mix(lat_m, 4, 6, 0.55)
    cv2.ellipse(c.a, (ix, iy), (9, hh), 0, 0, 360, 6, 1, cv2.LINE_8)
    c.line((ix, iy - hh + 2), (ix, iy + hh - 2), 7, 1)

    # Suspended slugs + concentric emerald shock-ripples (`7` -> `6` -> `5`)
    offs = [(-3, -20), (2, -9), (-2, 2), (3, 13), (-1, 23)][:slugs]
    for k_s, (ox, oy) in enumerate(offs):
        sx, sy = ix + ox, iy + oy
        r_rip = int(round(4 + 5 * ((pulse + k_s * 0.23) % 1.0)))
        cv2.ellipse(c.a, (sx, sy), (max(2, r_rip // 2), r_rip), 0, 0, 360, 7 if r_rip < 6 else 5, 1, cv2.LINE_8)
        c.rect(sx - 3, sy - 1, sx + 1, sy + 1, 0xE)
        c.px(sx + 1, sy, 0xA)
    return c
