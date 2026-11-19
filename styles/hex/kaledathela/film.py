"""Kaledathela scored concept animation (v2, revised after cold reading): *Shuttered Lamp* (`kaledathela_concept.mp4`).

32.0 seconds, 768 frames at 24 fps (16 bars of 4/4 at 120 BPM), 1280 x 720, hung on `music.py`.
v2 improvements from cold reading (`COLD_READ.md`):
  - Shot 1: Highway checkpoint gantry is solid concrete from 0.0 s; larger 3-truck Pastor convoy drives under the arch at 6.0 s;
    Worm sky-rail separated cleanly from the highway cross-gate.
  - Shot 2: Pastor's cross-topped truck parked on the overpass behind Hunter & Pastor; flying Censer-Drones have animated
    rotor blurs clear of the flare stacks, and bank West at 14.0 s when retasked.
  - Shot 3: At 18.0 s ONLY the Worm-tap monitor flashes 0xD (`DRONE INBOUND`) while Runner physically walks to the central
    table (`18.05..19.95 s`) and slams the iron hood over the 0xF lamp at 20.0 s — JUST as a Censer-Drone glides across the
    ceiling grate (`20.0..23.9 s`) sweeping full-height dithered 0xA cones to the floor (`0 LIGHTS FOUND`).
  - Shot 4: Both receding Censer-Drone and red-taillight Pastor truck depart (`24..26 s`); at 26.0 s cellar doors swing open
    and witches climb smoothly up; at 28.0 s green wand beam travels up into the rib; at 30.0 s protective green ward dome blooms.

    uv run python styles/hex/kaledathela/film.py test     render v2 key frames to inspect first
    uv run python styles/hex/kaledathela/film.py          render all 768 frames, mux audio, verify 14/14 sync & 0 pops
"""
import sys, math, subprocess
from multiprocessing import Pool
from pathlib import Path
HERE = Path(__file__).resolve().parent; HEX = HERE.parent; ROOT = HERE.parents[2]
sys.path.insert(0, str(HEX / 'uptime')); sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(HEX)); sys.path.insert(0, str(HERE))
import numpy as np
import cv2
from music import POINTS, OUT as MOUT
import kit, sprites as SP, ui as U
import kit_kal as K

FPS, SECONDS = 24, 32
NF = FPS * SECONDS
CW, CH = 640, 360
W, H = 1280, 720
OUT = MOUT
FRAMES = OUT / 'frames'


def sprite_c(c, rows, x, y, scale=2, flip=False, swap=None, y_clip=None):
    """Draw a hex-string sprite onto a `kit.Canvas` at integer `scale`, optionally clipped below `y_clip` (for stairs!)."""
    x0, y0 = int(round(x)), int(round(y))
    for j, r in enumerate(rows):
        py0, py1 = y0 + j * scale, y0 + (j + 1) * scale
        if y_clip is not None and py0 >= y_clip:
            continue
        if y_clip is not None:
            py1 = min(py1, y_clip)
        rr = r[::-1] if flip else r
        for i, ch in enumerate(rr):
            if ch != '.':
                col = int(ch, 16)
                if swap and col in swap:
                    col = swap[col]
                c.rect(x0 + i * scale, py0, x0 + (i + 1) * scale, py1, col)


def draw_drone(c, x, y, t, scale=2):
    """Draw a flying `DRONE_INQ` quadcopter with animated 24-fps spinning rotor blurs so it never reads as static."""
    sprite_c(c, K.DRONE_INQ, x - 8 * scale, y, scale=scale)
    spin = int(round(t * 24)) % 2
    rw = (5 if spin == 0 else 3) * scale
    c.rect(x - 6 * scale - rw // 2, y - 1, x - 6 * scale + rw // 2, y + 1, 0xA if spin == 0 else 9)
    c.rect(x + 5 * scale - rw // 2, y - 1, x + 5 * scale + rw // 2, y + 1, 9 if spin == 0 else 0xA)


def draw_pastor_truck(c, x, y, scale=1.0, facing='front'):
    """Armoured black Inquisition truck with stark `0xA` roof cross (shared across Shots 1, 2, 4)."""
    S = scale
    if facing == 'side_left':
        # Parked or driving profile on Shot 2 overpass
        c.rect(x, y - int(18 * S), x + int(56 * S), y - int(4 * S), 0)
        c.rect(x + int(12 * S), y - int(27 * S), x + int(46 * S), y - int(18 * S), 1)
        c.rect(x + int(15 * S), y - int(25 * S), x + int(27 * S), y - int(19 * S), 8)
        c.line((x, y - int(18 * S)), (x + int(56 * S), y - int(18 * S)), 8, 1)
        c.disc(x + int(12 * S), y - int(4 * S), max(2, int(5 * S)), 0)
        c.disc(x + int(12 * S), y - int(4 * S), max(1, int(2 * S)), 8)
        c.disc(x + int(44 * S), y - int(4 * S), max(2, int(5 * S)), 0)
        c.disc(x + int(44 * S), y - int(4 * S), max(1, int(2 * S)), 8)
        # Headlight left + tail-light right + roof cross
        c.rect(x - 1, y - int(14 * S), x + 2, y - int(10 * S), 0xA)
        c.rect(x + int(54 * S), y - int(14 * S), x + int(57 * S), y - int(10 * S), 0xD)
        cx_t = x + int(28 * S); cy_t = y - int(27 * S)
        c.line((cx_t, cy_t - int(11 * S)), (cx_t, cy_t), 0xA, 2)
        c.line((cx_t - int(4 * S), cy_t - int(7 * S)), (cx_t + int(4 * S), cy_t - int(7 * S)), 0xA, 2)
    else:
        hw = max(4, int(round(13 * S)))
        hh = max(4, int(round(10 * S)))
        c.rect(x - hw, y - hh, x + hw, y + 2, 0)
        c.rect(x - hw + 2, y - hh - max(3, int(6 * S)), x + hw - 2, y - hh, 8)
        c.line((x - hw, y - hh), (x + hw, y - hh), 9, 1)
        if facing == 'front':
            r_hl = max(1, int(round(2.5 * S)))
            c.disc(x - hw + 3, y - 1, r_hl, 0xA)
            c.disc(x + hw - 3, y - 1, r_hl, 0xA)
            c.px(x + hw - 3, y - hh - 2, 0xD)
        else:
            # Rear view: unmistakable bright crimson-pink 0xD tail-lights!
            r_tl = max(1, int(round(2.2 * S)))
            c.rect(x - hw + 1, y - 2 - r_tl, x - hw + 3 + r_tl, y, 0xD)
            c.rect(x + hw - 3 - r_tl, y - 2 - r_tl, x + hw - 1, y, 0xD)
        cx_h = max(6, int(round(13 * S)))
        cw_h = max(2, int(round(4 * S)))
        c.line((x, y - hh - int(5 * S) - cx_h), (x, y - hh - int(4 * S)), 0xA, max(1, int(round(1.6 * S))))
        c.line((x - cw_h, y - hh - int(5 * S) - int(cx_h * 0.65)),
               (x + cw_h, y - hh - int(5 * S) - int(cx_h * 0.65)), 0xA, max(1, int(round(1.6 * S))))


def _bake_sky(hz, px, py, pr, wp0, wvp, seed):
    c = kit.Canvas(CW, CH, fill=0)
    K.draw_sky_canvas(c, hz, primary_x=px, primary_y=py, primary_r=pr, worm_p0=wp0, worm_vp=wvp, transit_u=None, seed=seed)
    return c.a[:hz].copy()


# Worm sky-rail separated cleanly from highway cross-gates in Shots 1 & 4!
SKY_SHOT1 = _bake_sky(212, 128, 132, 114, (632, 12), (576, 210), seed=77)
SKY_SHOT2 = _bake_sky(196, 492, 116, 110, (-10, 22), (88, 194),  seed=51)
SKY_SHOT4 = _bake_sky(206, 476, 122, 112, (36, 10),  (112, 204), seed=63)


# ================================================================== SHOT 1 (0–8 s): WEST TEXAS WASTE
def draw_shot1(c, t):
    hz = 212
    vp_x = 304
    c.a[:hz] = SKY_SHOT1

    # Sync 4.0 s (4.0..4.95 s): Bright subspace vessel streaking down the Worm-Border on the right!
    if 4.0 <= t < 4.95:
        u_tr = (t - 4.0) / 0.95
        x0, y0 = 632.0, 12.0; x1, y1 = 576.0, float(hz - 2)
        vx, vy = x1 - x0, y1 - y0
        tx, ty = int(round(x0 + vx * u_tr)), int(round(y0 + vy * u_tr))
        u_tail = max(0.0, u_tr - 0.30)
        cx0, cy0 = int(round(x0 + vx * u_tail)), int(round(y0 + vy * u_tail))
        c.line((cx0, cy0), (tx, ty), 0xC, 4)
        c.line((cx0, cy0), (tx, ty), 0xA, 2)
        if ty < hz - 4:
            c.disc(tx, ty, 7, 0xC); c.disc(tx, ty, 4, 0xA)
    elif t >= 4.95:
        c.line((602, 118), (576, hz - 2), 0xC, 2)

    for pts in ([(0, hz), (18, hz - 24), (96, hz - 24), (118, hz)],
                [(150, hz), (164, hz - 15), (236, hz - 15), (252, hz)],
                [(378, hz), (398, hz - 32), (502, hz - 32), (526, hz - 14), (552, hz - 14), (566, hz)]):
        c.poly(pts, 1); c.line(pts[1], pts[2], 3, 1)

    c.grad(hz, CH - 20, [2, 1, 1, 0], power=0.85)
    rng = np.random.default_rng(88)
    for dy in range(hz + 5, CH - 22, 5):
        for _ in range(12):
            dx = int(rng.integers(0, CW - 28))
            c.rect(dx, dy, dx + int(rng.integers(8, 24)), dy + 1, 2 if dy < hz + 34 else 1)

    # Eroded Worm-rib & broken stone arch on right desert flat (with dormant 0xC nodes linking to sky-rail!)
    for seg in range(7):
        a0 = 200 + seg * 15; a1 = a0 + 10
        cv2.ellipse(c.a, (498, 294), (68, 84), -8, a0, a1, 2, 11, cv2.LINE_8)
        cv2.ellipse(c.a, (498, 294), (68, 84), -8, a0, a1, 8, 2, cv2.LINE_8)
        ar = math.radians(a0 + 5)
        if int(294 + 84 * math.sin(ar)) < 288 and seg % 2 == 0:
            c.disc(int(498 + 68 * math.cos(ar)), int(294 + 84 * math.sin(ar)), 2, 0xC)
    c.rect(418, 262, 426, 294, 8); c.rect(448, 266, 456, 294, 8)
    cv2.ellipse(c.a, (437, 266), (15, 12), 0, 180, 320, 9, 3, cv2.LINE_8)

    # Straight two-lane West Texas blacktop
    road_mask = np.zeros((CH, CW), bool)
    cv2.fillPoly(road_mask, [np.array([(vp_x - 3, hz), (vp_x + 3, hz), (372, CH - 20), (196, CH - 20)], np.int32)], 1)
    c.mask(road_mask, 0)
    c.line((vp_x - 3, hz), (196, CH - 20), 8, 1)
    c.line((vp_x + 3, hz), (372, CH - 20), 8, 1)

    # Convoy advances boldly from distance (u=0.22) past checkpoint (u=0.46 at 5.5s) into foreground (u=0.72 at 8.0s)!
    u_lead = 0.22 + 0.062 * t
    cx_lead = int(round(vp_x + (284 - vp_x) * u_lead))
    cy_lead = int(round(hz + (CH - 20 - hz) * u_lead))
    beam_w = int(round(24 + 62 * u_lead))
    beam_mask = np.zeros((CH, CW), bool)
    cv2.fillPoly(beam_mask, [np.array([(cx_lead - 8, cy_lead + 2), (cx_lead + 8, cy_lead + 2),
                                       (284 + beam_w, CH - 20), (284 - beam_w, CH - 20)], np.int32)], 1)
    c.mix(beam_mask & road_mask, 0, 9, 0.48 if t < 6.0 else 0.62)

    for k in range(13):
        u0 = (k / 13.0) ** 1.7; u1 = ((k + 0.5) / 13.0) ** 1.7
        c.line((vp_x + (284 - vp_x) * u0, hz + (CH - 20 - hz) * u0),
               (vp_x + (284 - vp_x) * u1, hz + (CH - 20 - hz) * u1), 9, 1)
    for k in range(1, 9):
        u = (k / 8.5) ** 1.65
        px = int(round(vp_x - 6 - 122 * u)); py = int(round(hz + (CH - 20 - hz) * u))
        ph = max(4, int(round(64 * u)))
        c.line((px, py), (px, py - ph), 1 if u < 0.4 else 0, max(1, int(round(2 * u))))
        c.line((px - int(6 * u) - 1, py - ph + 2), (px + int(6 * u) + 1, py - ph + 2), 8, 1)

    # Checkpoint gantry at u_gantry = 0.42 (SOLID concrete from t = 0.0 s — zero pop-in!)
    gy = int(round(hz + (CH - 20 - hz) * 0.42))                                  # y = 266
    gantry_lit = (t >= 6.0)

    # Draw vehicles BEHIND gantry first (`u <= 0.42`), then gantry, then vehicles IN FRONT of gantry (`u > 0.42`)!
    vehicles = [
        (u_lead - 0.18, False),
        (u_lead - 0.09, False),
        (u_lead,        True),
    ]
    for uv, is_p in vehicles:
        if 0.06 < uv <= 0.43:
            vx_c = int(round(vp_x + (284 - vp_x) * uv))
            vy_c = int(round(hz + (CH - 20 - hz) * uv))
            if is_p:
                draw_pastor_truck(c, vx_c, vy_c, scale=0.45 + 0.85 * uv, facing='front')
            else:
                hw = max(3, int(round(10 * uv))); hh = max(3, int(round(8 * uv)))
                c.rect(vx_c - hw, vy_c - hh, vx_c + hw, vy_c + 1, 1)
                c.rect(vx_c - hw + 1, vy_c - hh - 3, vx_c + hw - 1, vy_c - hh, 8)
                c.disc(vx_c - hw + 2, vy_c, max(1, int(2 * uv)), 0xA)
                c.disc(vx_c + hw - 2, vy_c, max(1, int(2 * uv)), 0xA)

    # Solid concrete checkpoint arch (always visible!)
    c.rect(254, gy - 36, 263, gy + 4, 8); c.rect(333, gy - 36, 342, gy + 4, 8)
    c.rect(250, gy - 43, 346, gy - 34, 0xD if gantry_lit else 8)
    c.rect(250, gy - 44, 346, gy - 42, 0xA if gantry_lit else 9)
    c.line((298, gy - 58), (298, gy - 36), 0xA, 2); c.line((291, gy - 50), (305, gy - 50), 0xA, 2)
    if gantry_lit:
        scan_m = np.zeros((CH, CW), bool)
        cv2.fillPoly(scan_m, [np.array([(263, gy - 34), (333, gy - 34), (336, gy + 4), (260, gy + 4)], np.int32)], 1)
        c.mix(scan_m, 0, 0xA, 0.36)

    for uv, is_p in vehicles:
        if uv > 0.43:
            vx_c = int(round(vp_x + (284 - vp_x) * uv))
            vy_c = int(round(hz + (CH - 20 - hz) * uv))
            if is_p:
                draw_pastor_truck(c, vx_c, vy_c, scale=0.45 + 0.85 * uv, facing='front')
            else:
                hw = max(4, int(round(11 * uv))); hh = max(4, int(round(9 * uv)))
                c.rect(vx_c - hw, vy_c - hh, vx_c + hw, vy_c + 2, 1)
                c.rect(vx_c - hw + 2, vy_c - hh - 4, vx_c + hw - 2, vy_c - hh, 8)
                c.disc(vx_c - hw + 2, vy_c, 2, 0xA); c.disc(vx_c + hw - 2, vy_c, 2, 0xA)
                c.px(vx_c, vy_c - hh - 2, 0xD)

    # Four-bar Lufkin Pumpjack on left (bottom-strokes at 2.0 s and 6.0 s)
    phase = ((t - 1.0) / 4.0) % 1.0
    pj_x, pj_y, pj_s = 104, 304, 1.55
    K.draw_pumpjack_2d(c, pj_x, pj_y, scale=pj_s, phase=phase, col_main=0, col_hi=8)
    for t_stroke in (2.0, 6.0):
        if t_stroke <= t < t_stroke + 0.70:
            age = (t - t_stroke) / 0.70
            wx, wy = int(round(pj_x - 24.0 * pj_s)), int(round(pj_y - 12.0 * pj_s))
            rad_p = int(round(6 + 14 * age))
            puff_m = np.zeros((CH, CW), bool)
            cv2.ellipse(puff_m, (wx - int(10 * age) - 6, wy - int(6 * age)), (rad_p, max(4, rad_p // 2)), -15, 0, 360, 1, -1)
            c.mix(puff_m, 1, 0xA if age < 0.45 else 9, 0.55 * (1.0 - 0.5 * age))
            c.disc(wx, wy - 2, 3, 0xA)


# ================================================================== SHOT 2 (8–16 s): EAST BAYOU & THE PASTOR
def draw_shot2(c, t):
    lt = t - 8.0
    hz = 196
    c.a[:hz] = SKY_SHOT2

    c.poly([(0, hz), (180, hz - 8), (360, hz - 5), (520, hz - 10), (CW, hz - 6), (CW, hz + 6), (0, hz + 6)], 1)
    for tx, th, tw in ((198, 48, 9), (220, 64, 10), (382, 58, 10), (406, 44, 9)):
        c.rect(tx, hz - th, tx + tw, hz, 1); c.rect(tx + tw - 2, hz - th, tx + tw, hz, 2)

    # Refinery flare stacks placed cleanly AWAY from drone flight lanes!
    flares = [(214, hz - 92, 0.0), (398, hz - 88, 1.7)]
    for fx, fy, ph0 in flares:
        c.line((fx, fy), (fx, hz), 8, 2)
        sway = 2.5 * math.sin(2 * math.pi * 0.75 * lt + ph0)
        c.poly([(fx, fy), (fx + 15, fy - 12 + sway), (fx + 24, fy - 5 + sway), (fx + 10, fy + 3)], 0xD)
        c.poly([(fx, fy), (fx + 10, fy - 8 + sway * 0.6), (fx + 15, fy - 3 + sway * 0.6), (fx + 6, fy + 2)], 0xE)
        c.disc(fx + 2, fy - 1, 3, 0xA)

    # Dominion Broadcast Cross Pylon at x=336 (flares 0xA/0xD at t >= 14.0 s!)
    cross_lock = (t >= 14.0)
    c.poly([(324, hz + 12), (331, hz - 68), (341, hz - 68), (348, hz + 12)], 8 if cross_lock else 1)
    if cross_lock:
        glow_m = np.zeros((CH, CW), bool)
        cv2.circle(glow_m, (336, hz - 92), 32, 1, -1)
        c.mix(glow_m, 2, 0xA, 0.42)
        c.line((336, hz - 122), (336, hz - 66), 0xA, 5); c.line((318, hz - 104), (354, hz - 104), 0xA, 5)
        c.rect(332, hz - 64, 340, hz - 12, 0xD)
    else:
        c.line((336, hz - 116), (336, hz - 68), 0xA, 3); c.line((322, hz - 100), (350, hz - 100), 0xA, 3)

    # Tall broken Dead-Empires stone aqueduct clearly broken mid-span
    c.rect(254, hz - 38, 262, hz + 8, 8); c.rect(286, hz - 42, 294, hz + 8, 8)
    cv2.ellipse(c.a, (274, hz - 24), (16, 14), 0, 180, 360, 9, 4, cv2.LINE_8)

    # Stagnant bayou water + shoreline banks
    c.grad(hz, CH - 20, [2, 1, 1, 0], power=0.9)
    for wy in range(hz + 6, CH - 22, 4):
        sh = int(round(3.0 * math.sin(wy * 0.25 + lt * 2.2)))
        for fx, _, _ in flares:
            c.rect(fx + 4 + sh, wy, fx + 13 + sh, wy + 1, 0xE if (wy // 4) % 2 == 0 else 0xD)
        c.rect(332 - sh // 2, wy, 340 - sh // 2, wy + 1, 0xA if cross_lock or wy < hz + 76 else 9)

    for px, ph, sd in ((452, 142, 4), (596, 158, 6)):
        K.draw_loblolly(c, px, hz + 26, ph, seed=sd, col_trunk=1, col_crown=0)
    K.draw_cypress(c, 486, hz + 88, 184, seed=11, col_trunk=1, col_moss=2)
    K.draw_cypress(c, 616, hz + 102, 206, seed=12, col_trunk=0, col_moss=1)

    # Shuttered dark stilt shack on right
    sx0, sx1, deck_y = 516, 594, 280
    for pil_x in (522, 546, 568, 588):
        c.rect(pil_x - 2, deck_y, pil_x + 2, 322, 0)
    c.rect(sx0 - 4, deck_y - 3, sx1 + 4, deck_y, 2)
    c.rect(sx0 + 6, deck_y - 42, sx1 - 4, deck_y - 3, 1)
    for tx in range(sx0 + 8, sx1 - 4, 4):
        c.rect(tx, deck_y - 42, tx + 1, deck_y - 3, 2 if (tx // 4) % 2 else 0)
    c.poly([(sx0 - 6, deck_y - 41), (sx1 + 4, deck_y - 41), (sx1 - 6, deck_y - 54), (sx0 + 6, deck_y - 54)], 8)
    c.rect(552, deck_y - 30, 576, deck_y - 14, 0)
    c.line((552, deck_y - 22), (576, deck_y - 22), 2, 1)

    # Two FLYING Censer-Drones: glide right across open water (`8..14 s`), then bank & fly rapidly WEST (`14..16 s`)!
    if t < 14.0:
        d1_x = int(round(256 + 7.5 * lt))
        d2_x = int(round(466 + 8.5 * lt))
    else:
        dt_w = t - 14.0
        d1_x = int(round(256 + 7.5 * 6.0 - 46.0 * dt_w))
        d2_x = int(round(466 + 8.5 * 6.0 - 52.0 * dt_w))
    d1_y = int(round(104 + 3.0 * math.sin(lt * 2.4)))
    d2_y = int(round(110 + 3.0 * math.cos(lt * 2.2)))
    scan1_hi = (10.0 <= t < 11.5)
    scan2_hi = (12.0 <= t < 13.5)

    for dx, dy, is_hi in ((d1_x, d1_y, scan1_hi), (d2_x, d2_y, scan2_hi)):
        cone_hw = 56 if is_hi else 20
        cone_y1 = 304 if is_hi else 268
        tilt = -18 if t >= 14.0 else 0
        cone_m = np.zeros((CH, CW), bool)
        cv2.fillPoly(cone_m, [np.array([(dx - 2, dy + 14), (dx + 2, dy + 14),
                                        (dx + cone_hw + tilt, cone_y1), (dx - cone_hw + tilt, cone_y1)], np.int32)], 1)
        c.mix(cone_m, 2 if is_hi else 1, 0xA, 0.52 if is_hi else 0.22)
        c.line((dx, dy + 14), (dx + tilt + int(6 * math.sin(lt * 3.0)), cone_y1), 0xD, 2 if is_hi else 1)
        if is_hi:
            c.rect(dx - cone_hw, cone_y1 - 2, dx + cone_hw, cone_y1 + 2, 0xA)
        draw_drone(c, dx, dy, t, scale=2)

    # Foreground Left: Concrete Overpass with PARKED PASTOR TRUCK + HUNTER + THE PASTOR!
    c.rect(0, 248, 218, 274, 8); c.rect(0, 248, 218, 252, 9)
    c.rect(0, 274, 212, CH - 20, 0)
    c.rect(28, 274, 52, CH - 20, 1); c.rect(148, 274, 172, CH - 20, 1)

    # Parked Pastor truck (`facing='side_left'` ready to head back West at 14.0 s!)
    tx_off = -int(round(28.0 * (t - 14.4))) if t >= 14.4 else 0
    draw_pastor_truck(c, 8 + tx_off, 250, scale=1.15, facing='side_left')

    # Hunter & Pastor turn West toward their truck at 14.0 s (`RETASK WEST`)!
    going_west = (t >= 14.0)
    hx_w = 82 - (int(round(18 * (t - 14.0))) if going_west else 0)
    px_w = 136 - (int(round(16 * (t - 14.0))) if going_west else 0)
    sprite_c(c, K.HUNTER, hx_w, 198, scale=3, flip=going_west)
    sprite_c(c, K.PASTOR, px_w, 176, scale=3, flip=going_west)
    if scan1_hi or scan2_hi:
        cx_st, cy_st = px_w + 52, 201
        c.line((cx_st, cy_st - 9), (cx_st, cy_st + 9), 0xA, 3)
        c.line((cx_st - 7, cy_st - 2), (cx_st + 7, cy_st - 2), 0xA, 3)
        cv2.circle(c.a, (cx_st, cy_st - 1), 11, 0xD, 1, cv2.LINE_8)


# ================================================================== SHOT 3 (16–24 s): SUNKEN WORM-RIB SHELTER
def draw_shot3(c, t):
    lt = t - 16.0
    alert = (t >= 18.0)
    shuttered = (t >= 20.0)

    c.a[:] = 0
    # Night sky strip visible ABOVE the ceiling grate (`y = 0..42`) so we SEE the Censer-Drone fly overhead at 20..24s!
    c.rect(204, 8, 436, 44, 1)
    for sx_st in (226, 268, 314, 358, 408):
        c.px(sx_st, 16 + (sx_st % 7), 8)

    if not shuttered:
        yy, xx = np.mgrid[46:CH, :CW].astype(np.float32)
        dist = np.hypot((xx - 320.0) * 0.85, (yy - 228.0) * 1.15)
        byr = kit.bayer(CH - 46, CW)
        r_inner = 1.0 - np.clip(dist / 250.0, 0.0, 1.0)
        sub = c.a[46:]
        sub[(r_inner > 0.12) & (byr < r_inner * 0.85)] = 1
        sub[(r_inner > 0.38) & (byr < (r_inner - 0.25) * 1.1)] = 2
        sub[(r_inner > 0.68) & (byr < (r_inner - 0.58) * 1.6)] = 3
        sub[(dist < 58.0) & (byr < (1.0 - dist / 58.0) * 0.55)] = 0xE

    wall_col = 2 if not shuttered else 1
    hi_col = 8 if not shuttered else 2
    c.rect(44, 54, 88, 316, wall_col); c.rect(CW - 88, 54, CW - 44, 316, wall_col)
    for by in range(64, 310, 26):
        c.line((44, by), (88, by), 0, 1); c.line((CW - 88, by), (CW - 44, by), 0, 1)
    c.rect(36, 312, CW - 36, CH - 20, 1 if not shuttered else 0)
    c.line((36, 312), (CW - 36, 312), hi_col, 2)

    # Colossal curved ancient Worm-Rib arching overhead (with dormant 0xC conduit nodes!)
    for seg in range(13):
        a0 = 192 + seg * 12; a1 = a0 + 9
        cv2.ellipse(c.a, (320, 306), (254, 248), 0, a0, a1, hi_col, 18, cv2.LINE_8)
        cv2.ellipse(c.a, (320, 306), (254, 248), 0, a0, a1, 9 if not shuttered else 8, 3, cv2.LINE_8)
        if seg % 3 == 1:
            ar = math.radians(a0 + 4)
            c.disc(int(320 + 254 * math.cos(ar)), int(306 + 248 * math.sin(ar)), 2, 0xB if shuttered else 0xC)

    # Ceiling grate frame (`y = 38..54`) with three wide ventilation bays opening to the surface sky
    c.rect(196, 38, 444, 54, 1); c.rect(196, 52, 444, 55, hi_col)
    slat_xs = [(214, 278), (292, 354), (368, 430)]
    for sx0, sx1 in slat_xs:
        c.rect(sx0, 38, sx1, 52, 1 if not shuttered else 0)

    # CRITICAL V2 FIX:
    # - During 18.0..20.0 s (`PROXIMITY ALERT`): NO searchlight inside the lit vault! Only a distant faint horizon
    #   glint in the sky above left (`x=218`) + big 0xD alarm on Signal's Worm-tap monitor while Runner walks to the lamp!
    # - At 20.0..24.0 s (`SHUTTERED`): NOW the Censer-Drone flies directly across the open sky grate above (`y=18`),
    #   casting full-depth dithered `0xA` cones all the way down to the dark vault floor (`y=312`)!
    if shuttered:
        u_dr = (t - 20.0) / 3.95
        dr_x = int(round(220 + 204 * u_dr))
        # Draw Censer-Drone flying across the surface sky strip visible through the grate!
        draw_drone(c, dr_x, 18, t, scale=2)
        yy_b, xx_b = np.mgrid[52:312, :CW].astype(np.float32)
        byr_b = kit.bayer(312 - 52, CW)
        # Cone from drone `(dr_x, 30)` masked through the three ceiling grate openings, fading smoothly to floor!
        cone_all = np.zeros((312 - 52, CW), bool)
        for sx0, sx1 in slat_xs:
            # Project grate edges `(sx0, 48)` and `(sx1, 48)` from `(dr_x, 26)` down to `y = 312`
            x_bot_l = int(round(dr_x + (sx0 - dr_x) * (312 - 26) / (48 - 26)))
            x_bot_r = int(round(dr_x + (sx1 - dr_x) * (312 - 26) / (48 - 26)))
            m_s = np.zeros((312 - 52, CW), np.uint8)
            cv2.fillPoly(m_s, [np.array([(sx0, 0), (sx1, 0), (x_bot_r, 312 - 52), (x_bot_l, 312 - 52)], np.int32)], 1)
            cone_all |= m_s.astype(bool)
        cone_all[:, :88] = False; cone_all[:, CW - 88:] = False                  # stop light cleanly on interior masonry walls!
        fade = np.clip(1.0 - (yy_b - 52.0) / 290.0, 0.14, 1.0) * 0.62
        lit_px = cone_all & (byr_b < fade)
        c.a[52:312][lit_px] = np.where(yy_b[lit_px] < 190, 0xA, 9)
        # Central 0xD laser lock line from the drone straight down to the floor!
        c.line((dr_x, 32), (dr_x, 311), 0xD, 1)

    # Left: Salvaged Worm-Tap coil & large readable CRT terminal tended by WITCH_SIGNAL
    tap_hot = (18.0 <= t < 20.0)
    c.line((138, 134), (154, 232), 0xD if tap_hot else (8 if not shuttered else 2), 2)
    c.rect(112, 228, 192, 286, 0xD if tap_hot else (8 if not shuttered else 1))
    c.rect(118, 234, 186, 278, 0xD if tap_hot else 0)
    if tap_hot:
        # Big unmistakable 18.0 s visual spike: bright 0xD/0xA radar warning flash on the Worm-tap screen & beacon!
        c.rect(122, 238, 182, 274, 0)
        c.rect(122, 238, 182, 248, 0xD)
        for wx in range(125, 179, 2):
            wy = int(round(261 + 8 * math.sin((wx - 124) * 0.5 + lt * 9.0)))
            c.rect(wx, wy - 1, wx + 2, wy + 2, 0xA if (wx // 4) % 2 == 0 else 0xD)
        # Flashing warning beacon atop the CRT
        c.disc(152, 220, 7, 0xD); c.disc(152, 220, 3, 0xA)
    elif not shuttered:
        for wx in range(124, 180, 2):
            wy = int(round(256 + 6 * math.sin((wx - 124) * 0.35 + lt * 5.0)))
            c.px(wx, wy, 6)
    else:
        c.px(126, 270, 5)
    c.rect(108, 286, 196, 312, 2 if not shuttered else 1)

    # Center Wooden Spool Table + THE SOLE 0xF SHELTER LANTERN
    c.rect(284, 266, 356, 273, hi_col)
    c.rect(302, 273, 338, 312, wall_col)
    c.rect(280, 308, 360, 312, hi_col)

    # WITCH_RUNNER physically walks from x=384 (`t<=18.0`) right up to the lantern pedestal (`x=330` at `t=19.9`)!
    if t <= 18.0:
        rx_run = 384; walk_bob = 0
    elif t < 20.0:
        u_w = min(1.0, (t - 18.0) / 1.85)
        rx_run = int(round(384 - 54 * u_w))
        walk_bob = -2 * (int(round(t * 12)) % 2) if u_w < 1.0 else 0
    else:
        rx_run = 330; walk_bob = 0

    if not shuttered:
        c.rect(308, 236, 332, 266, 8)
        c.rect(311, 241, 329, 262, 0xF)
        # As Runner reaches the pedestal (`19.7..20.0 s`), she lifts the iron hood poised right over the flame!
        hood_y = 228 if t >= 19.6 else 232
        c.rect(305, hood_y, 335, hood_y + 5, 9)
        c.rect(292, 266, 348, 268, 0xF)
    else:
        # SHUTTERED AT 20.0 s: heavy iron hood dropped all the way over the lantern!
        c.rect(305, 238, 335, 266, 1)
        c.rect(305, 238, 335, 242, 8)
        if t < 20.5:
            c.line((296, 265), (344, 265), 9, 1)

    # Bayou's hanging spider stays visible in both lit AND dark states (dark silhouette in 20..24s so it never vanishes!)
    c.line((504, 56), (504, 198), 2 if not shuttered else 1, 1)
    sprite_c(c, SP.SPIDER, 496, 198, scale=2, swap={0: 8 if not shuttered else 1, 0xD: 0xD if not shuttered else 2})

    if not shuttered:
        sprite_c(c, K.WITCH_SIGNAL, 192, 232, scale=4, flip=tap_hot)
        sprite_c(c, K.WITCH_RUNNER, rx_run, 264 + walk_bob, scale=4, flip=True, swap={0xF: 9})
        sprite_c(c, K.WITCH_BAYOU,  446, 252, scale=4, flip=True)
    else:
        dark_swap = {6: 1, 5: 1, 7: 1, 2: 1, 3: 1, 8: 1, 0xA: 1, 0xF: 1}
        sprite_c(c, K.WITCH_SIGNAL, 192, 232, scale=4, swap=dark_swap)
        sprite_c(c, K.WITCH_RUNNER, rx_run, 264, scale=4, flip=True, swap=dark_swap)
        sprite_c(c, K.WITCH_BAYOU,  446, 252, scale=4, flip=True, swap=dark_swap)
        for ex, ey in ((214, 264), (226, 264), (rx_run + 30, 276), (rx_run + 42, 276), (474, 272), (486, 272)):
            c.rect(ex, ey, ex + 4, ey + 4, 6)


# ================================================================== SHOT 4 (24–32 s): AFTER HE PASSES — RE-LIGHTING
def draw_shot4(c, t):
    lt = t - 24.0
    reopened = (t >= 26.0)
    ward_lit = (t >= 28.0)
    final_ch = (t >= 30.0)

    hz = 206
    vp_x = 216
    c.a[:hz] = SKY_SHOT4

    # Sync 30.0 s: Protective green hex-ward canopy + animated cyan Worm-Border tether growing smoothly (30.0..30.5 s)!
    if final_ch:
        u_f = min(1.0, (t - 30.0) / 0.45)
        # Protective green hex-dome arching over the entire shelter mound!
        dome_m = np.zeros((CH, CW), bool)
        cv2.ellipse(dome_m, (458, 326), (156, int(round(182 * u_f))), 0, 180, 360, 1, 6)
        c.mix(dome_m, 1, 6, 0.65)
        cv2.ellipse(c.a, (458, 326), (156, max(4, int(round(182 * u_f)))), 0, 185, 355, 7, 1, cv2.LINE_8)
        # Animated tether shooting from Worm-rib crown `(456, 168)` to sky Worm-Border `(86, 128)`
        tx_e = int(round(456 + (86 - 456) * u_f))
        ty_e = int(round(168 + (128 - 168) * u_f))
        c.line((456, 168), (tx_e, ty_e), 6, 2)
        c.line((456, 167), (tx_e, ty_e - 1), 0xC, 1)
        if u_f >= 0.98:
            c.disc(86, 128, 4, 0xC); c.disc(86, 128, 2, 0xA)

    c.poly([(0, hz), (22, hz - 22), (118, hz - 22), (142, hz)], 1)
    c.line((22, hz - 22), (118, hz - 22), 3, 1)
    c.poly([(310, hz), (380, hz - 8), (CW, hz - 12), (CW, hz + 4), (310, hz + 4)], 1)
    c.grad(hz, CH - 20, [2, 1, 1, 0], power=0.88)

    K.draw_pumpjack_2d(c, 74, 256, scale=0.85, phase=((t - 1.0) / 4.0) % 1.0, col_main=0, col_hi=8)

    # Receding highway: Pastor's cross-topped truck with BRIGHT 0xD RED TAIL-LIGHTS + receding Censer-Drone!
    c.poly([(vp_x - 3, hz), (vp_x + 3, hz), (168, CH - 20), (62, CH - 20)], 0)
    c.line((vp_x - 3, hz), (62, CH - 20), 8, 1)
    c.line((vp_x + 3, hz), (168, CH - 20), 8, 1)
    if lt < 3.6:
        u_rec = max(0.08, 0.56 - 0.13 * lt)
        rx = int(round(vp_x + (115 - vp_x) * u_rec))
        ry = int(round(hz + (CH - 20 - hz) * u_rec))
        draw_pastor_truck(c, rx, ry, scale=0.35 + 0.75 * u_rec, facing='rear')
        # Receding Censer-Drone escorting the Pastor's truck back down the highway (links directly to Shot 3!)
        dr_rx = int(round(vp_x + 38 * u_rec))
        dr_ry = int(round(hz - 16 - 42 * u_rec))
        draw_drone(c, dr_rx, dr_ry, t, scale=1 if u_rec < 0.32 else 2)

    K.draw_cypress(c, 606, hz + 108, 212, seed=19, col_trunk=0, col_moss=1)

    # Eroded caliche mound + broken stone arch + colossal ancient Worm-Rib
    c.poly([(292, 334), (356, 280), (548, 278), (602, 336)], 1)
    c.rect(342, 246, 352, 294, 8); c.rect(386, 250, 396, 294, 8)
    cv2.ellipse(c.a, (369, 250), (22, 18), 0, 180, 360, 9, 4, cv2.LINE_8)

    u_ward = min(1.0, (t - 28.0) / 0.45) if ward_lit else 0.0
    n_lit_segs = int(round(10 * u_ward))
    for seg in range(10):
        a0 = 196 + seg * 14; a1 = a0 + 10
        cv2.ellipse(c.a, (458, 294), (104, 126), -8, a0, a1, 2, 16, cv2.LINE_8)
        # Ignite segments outward from the crown (`seg 4, 5`) as the wand beam strikes!
        seg_on = ward_lit and (abs(seg - 4.5) <= n_lit_segs * 0.55)
        cv2.ellipse(c.a, (458, 294), (104, 126), -8, a0, a1, 6 if seg_on else 8, 3, cv2.LINE_8)
        ar = math.radians(a0 + 5)
        wx, wy = int(round(458 + 104 * math.cos(ar))), int(round(294 + 126 * math.sin(ar)))
        if wy < 290:
            if seg_on:
                c.disc(wx, wy, 5, 5); c.disc(wx, wy, 3 if final_ch else 2, 7); c.px(wx, wy, 7)
            elif seg % 2 == 0:
                c.disc(wx, wy, 2, 0xC)

    # Sunken Storm-Cellar Hatch: doors swing open smoothly at 26.0..26.35 s, witches climb smoothly up stairwell!
    hx0, hy0, hx1, hy1 = 414, 286, 514, 330
    c.poly([(hx0 - 8, hy1), (hx0 + 6, hy0), (hx1 - 6, hy0), (hx1 + 8, hy1)], 0)
    c.line((hx0 - 8, hy1), (hx1 + 8, hy1), 8, 2)

    if not reopened:
        c.rect(hx0 + 8, hy0 + 6, hx1 - 8, hy1 - 4, 1)
        c.line((hx0 + 8, hy0 + 18), (hx1 - 8, hy0 + 18), 2, 1)
    else:
        u_open = min(1.0, (t - 26.0) / 0.30)
        hw_open = int(round(40 * u_open))
        cx_h = (hx0 + hx1) // 2
        if hw_open > 2:
            c.poly([(cx_h - hw_open, hy1 - 3), (cx_h - int(hw_open * 0.78), hy0 + 10),
                    (cx_h + int(hw_open * 0.78), hy0 + 10), (cx_h + hw_open, hy1 - 3)], 0xF)
            c.rect(cx_h - hw_open + 2, hy0 + 21, cx_h + hw_open - 2, hy0 + 25, 2)
        # Open hatch leaf edges folded back on left & right
        c.rect(cx_h - hw_open - 6, hy0 + 8, cx_h - hw_open, hy1 - 3, 8)
        c.rect(cx_h + hw_open, hy0 + 8, cx_h + hw_open + 6, hy1 - 3, 8)

        # Witches climb smoothly up out of the stairwell (`26.05..26.65 s`, clipped cleanly at `hy1 - 3`)!
        u_climb = min(1.0, max(0.0, (t - 26.04) / 0.55))
        y_sig = int(round(304 - 60 * u_climb))
        y_bay = int(round(308 - 48 * u_climb))
        sprite_c(c, K.WITCH_SIGNAL, 402, y_sig, scale=3, y_clip=hy1 - 2)
        sprite_c(c, K.WITCH_BAYOU,  500, y_bay, scale=3, flip=True, y_clip=hy1 - 2)

        if ward_lit:
            # Travelling green wand beam (`28.0..28.25 s`) from Signal's wand `(447, 266)` up to `(456, 168)`!
            u_b = min(1.0, (t - 28.0) / 0.25)
            bx_t = int(round(447 + (456 - 447) * u_b))
            by_t = int(round(266 + (168 - 266) * u_b))
            c.disc(447, 266, 4, 6); c.disc(447, 266, 2, 7)
            c.line((447, 266), (bx_t, by_t), 6, 2)


# ================================================================== FULL 1280 x 720 COMPOSITE + HUD + GLOW
def render_frame(fi):
    t = fi / FPS
    c = kit.Canvas(CW, CH, fill=0)

    if t < 8.0:
        draw_shot1(c, t)
        assert not np.isin(c.a, [4, 5, 6, 7, 0xF]).any(), f'Contraband colour in Shot 1 at t={t:.2f}!'
    elif t < 16.0:
        draw_shot2(c, t)
        assert not np.isin(c.a, [4, 5, 6, 7, 0xF]).any(), f'Contraband colour in Shot 2 at t={t:.2f}!'
    elif t < 24.0:
        draw_shot3(c, t)
        if t >= 20.0:
            assert not (c.a == 0xF).any(), f'0xF leaked while shuttered at t={t:.2f}!'
    else:
        draw_shot4(c, t)
        if t < 26.0:
            assert not (c.a == 0xF).any(), f'0xF leaked before shutter re-opened at t={t:.2f}!'

    img = np.zeros((H, W, 3), np.float32)
    U.blit(img, c.a, 0, 0, scale=2)

    if t < 2.0:
        hdr, sub, bcol = 'WEST SECTOR // CAPROCK HWY', 'PASTORAL CONVOY EN ROUTE', 8
    elif t < 4.0:
        hdr, sub, bcol = 'WEST SECTOR // WELLHEAD 01', 'PRESSURE RELIEF STROKE', 0xA
    elif t < 6.0:
        hdr, sub, bcol = 'WORM BORDER // TRANSIT WAKE', 'CORRIDOR 0xC IONISATION', 0xC
    elif t < 8.0:
        hdr, sub, bcol = 'CHECKPOINT LOCK // PASTOR + 2', 'PASSING GATE -> PINEY SLOUGH', 0xD
    elif t < 10.0:
        hdr, sub, bcol = 'EAST SECTOR // PINEY SLOUGH', 'PASTOR OVERPASS COMMAND', 8
    elif t < 12.0:
        hdr, sub, bcol = 'PASTORAL SCAN 01 // BAYOU', 'REGISTERS 0x5..0x7: 0 FOUND', 0xA
    elif t < 14.0:
        hdr, sub, bcol = 'PASTORAL SCAN 02 // STILT SHACK', 'REGISTER 0xF LAMP: 0 FOUND', 0xA
    elif t < 16.0:
        hdr, sub, bcol = 'SLOUGH CLEAR // RETASK WEST', 'DRONES + CONVOY RETURNING', 0xD
    elif t < 18.0:
        hdr, sub, bcol = 'SUNKEN WORM-RIB // COVEN VAULT', 'LAMP: 0xF OPEN  WORM-TAP: IDLE', 6
    elif t < 20.0:
        hdr, sub, bcol = 'WORM-TAP ALERT // DRONE 0.2 MI', 'RUNNER STEPPING TO SHUTTER!', 0xD
    elif t < 24.0:
        hdr, sub, bcol = 'LAMP SHUTTERED // DRONE ABOVE', 'PASTORAL SWEEP: 0 LIGHTS FOUND', 8
    elif t < 26.0:
        hdr, sub, bcol = 'RUIN RIDGE // PATROL PASSED', 'DRONE + TAIL-LIGHTS RECEDING', 8
    elif t < 28.0:
        hdr, sub, bcol = 'SHUTTER OPEN // 0xF KEPT', 'COVEN RISING FROM THE VAULT', 0xF
    elif t < 30.0:
        hdr, sub, bcol = 'HEX-WARD ACTIVE // 0x6 LIT', 'ANCIENT RIB KEYED BY SIGNAL', 6
    else:
        hdr, sub, bcol = 'KALEDATHELA // WARD DOME UP', 'COVEN SHELTERED   LAMP: KEPT', 0xF

    pw = max(U.tw(hdr, 2), U.tw(sub, 2)) + 28
    U.rect(img, 18, 16, 18 + pw, 72, U.C[0], a=0.86)
    U.rect(img, 18, 16, 18 + pw, 20, U.C[bcol])
    U.text(img, 30, 26, hdr, U.C[0xA if bcol != 0xF else 0xF], scale=2)
    U.text(img, 30, 48, sub, U.C[6 if bcol == 6 else 9], scale=2)

    U.rect(img, 0, H - 38, W, H, U.C[0])
    U.rect(img, 0, H - 40, W, H - 38, U.C[2])
    bar_i = int(t // 2.0) + 1
    shot_i = int(t // 8.0) + 1
    foot = f'KALEDATHELA: SHUTTERED LAMP   SHOT {shot_i}/4   BAR {bar_i:02d}/16'
    U.text(img, 20, H - 27, foot, U.C[9], scale=2)
    U.strip(img, W - 212, H - 25, s=10, gap=2)

    swatch_save = img[H - 30:, W - 220:].copy()
    img[H - 30:, W - 220:] = 0.0
    img = U.glow(img, strength=0.62)
    img[H - 30:, W - 220:] = swatch_save
    return img


def _worker(i):
    img = (np.clip(render_frame(i), 0, 1)[..., ::-1] * 255 + .5).astype(np.uint8)
    cv2.imwrite(str(FRAMES / f'f_{i:04d}.png'), img)
    return i


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'all'
    OUT.mkdir(parents=True, exist_ok=True); FRAMES.mkdir(parents=True, exist_ok=True)
    if mode == 'test':
        test_times = (1.0, 4.3, 6.8, 9.0, 14.6, 18.8, 21.2, 24.6, 26.3, 30.6)
        for ts in test_times:
            fi = int(round(ts * FPS))
            img = (np.clip(render_frame(fi), 0, 1)[..., ::-1] * 255 + .5).astype(np.uint8)
            cv2.imwrite(str(OUT / f'v2_test_{ts:04.1f}s.png'), img)
        print('wrote', len(test_times), 'v2 test stills to', OUT)
    else:
        with Pool(24) as pool:
            list(pool.imap_unordered(_worker, range(NF), chunksize=16))
        poster = (np.clip(render_frame(int(round(30.8 * FPS))), 0, 1)[..., ::-1] * 255 + .5).astype(np.uint8)
        cv2.imwrite(str(HERE / 'kaledathela_poster.png'), poster)
        subprocess.run([
            'ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS),
            '-i', str(FRAMES / 'f_%04d.png'), '-i', str(OUT / 'kaledathela.wav'),
            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'slow',
            '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', '-shortest',
            str(HERE / 'kaledathela_concept.mp4')
        ], check=True)
        from backlot import sync, screen
        res = sync.check(POINTS, str(FRAMES), str(OUT / 'kaledathela.wav'), fps=FPS,
                         out_jpg=str(HERE / 'kaledathela_sync.jpg'), out_json=str(OUT / 'sync.json'))
        pops = sync.pops(POINTS, str(FRAMES), fps=FPS)
        tr = sync.travel(str(FRAMES))
        screen.filmstrip(str(FRAMES), str(OUT / 'strip.jpg'), n=16)
        sync.events(POINTS, str(FRAMES), str(OUT / 'events_sheets'), fps=FPS)
        print('wrote v2', HERE / 'kaledathela_concept.mp4')
        print('sync both:', res['both'], '/', res['total'], '| pops:', pops, '| travel:', tr[1])
