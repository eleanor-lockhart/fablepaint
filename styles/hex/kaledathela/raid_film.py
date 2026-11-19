"""Scored Soft-R Gothic Combat Film (v2, revised after cold reading): *Reliquary Drop* (`raid_concept.mp4`).

32.0 seconds, 768 frames at 24 fps (16 bars of 4/4 at 120 BPM), 1280 x 720, hung on `raid_music.py`.
v2 improvements from cold reading (`COLD_READ_RAID.md`):
  - Gravity-curved `0xD` blood droplet arcs (never straight lines that read like lasers); clear fallen Hunter silhouettes
    with knocked-off hats and boots; aiming lasers (`dashed 0xD`) distinct from active ballistic tracers (`0xE`/`0xA`).
  - Shot 1: Solid stone entablature encloses the ruin roof; VTOL flames shut down once parked; Hunters step back to cover
    before the 6.0 s blast with zero missing frames (`6.00..6.15 s` fixed).
  - Shot 2: Visible ceiling floodlight fixture keeps hall lighting constant across `8..14 s` (stone craters never reset at
    12.0 s); Signal arrives before 12.0 s; reversed slugs cross in 0.15 s (`frames 336..339`) while a 5th upward ricochet
    visibly shatters the ceiling floodlight.
  - Shot 3: Bayou drops behind Hunter #2's back and slashes from his left; Hunter #3 turns to engage; Runner's graze sits
    on her shoulder; at 22.0 s Bayou's thrown `0x7` knife visibly wounds Hunter #4 (`1 WIA` earned on screen).
  - Shot 4: Wounded Hunter #4 boards the ramp (`24.0..24.5 s`) as a `0x6` hex-bolt scorches the Reliquary hull (trailing
    world-space smoke); Bayou and Signal stand cleanly separated; Bayou kneels to plant the `0x7` memorial blade at 30.0 s.
"""
import sys, math, subprocess
from multiprocessing import Pool
from pathlib import Path
HERE = Path(__file__).resolve().parent; HEX = HERE.parent; ROOT = HERE.parents[2]
sys.path.insert(0, str(HEX / 'uptime')); sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(HEX)); sys.path.insert(0, str(HERE))
import numpy as np
import cv2
from raid_music import RAID_POINTS, OUT as MOUT
import kit, ui as U
import kit_kal as K

FPS, SECONDS = 24, 32
NF = FPS * SECONDS
CW, CH = 640, 360
W, H = 1280, 720
OUT = MOUT
FRAMES = OUT / 'frames'


def sprite_c(c, rows, x, y, scale=2, flip=False, swap=None):
    x0, y0 = int(round(x)), int(round(y))
    for j, r in enumerate(rows):
        rr = r[::-1] if flip else r
        for i, ch in enumerate(rr):
            if ch != '.':
                col = int(ch, 16)
                if swap and col in swap:
                    col = swap[col]
                    if col is None:
                        continue
                c.rect(x0 + i * scale, y0 + j * scale, x0 + (i + 1) * scale, y0 + (j + 1) * scale, col)


def muzzle_cone(c, x, y, dir_x=1, big=True):
    L = (18 if big else 11) * dir_x
    hw = 6 if big else 4
    c.poly([(x, y - hw), (x + L, y), (x, y + hw)], 0xA)
    c.poly([(x, y - hw // 2), (x + L // 2, y), (x, y + hw // 2)], 0xE)


def dashed_laser(c, x0, y0, x1, y1, col=0xD):
    """Thin dashed targeting laser (`0xD`), visually distinct from solid `0xE/0xA` tracer streaks and curved blood!"""
    L = max(1.0, math.hypot(x1 - x0, y1 - y0))
    steps = max(2, int(L // 10))
    for k in range(steps):
        u0, u1 = k / steps, min(1.0, (k + 0.45) / steps)
        c.line((x0 + (x1 - x0) * u0, y0 + (y1 - y0) * u0),
               (x0 + (x1 - x0) * u1, y0 + (y1 - y0) * u1), col, 1)


def draw_rain(c, t, x0=0, x1=CW, y0=16, y1=296, n=70):
    r = np.random.default_rng(303)
    span_x = max(1, x1 - x0); span_y = max(1, y1 - y0)
    for _ in range(n):
        bx = float(r.uniform(0, span_x)); by = float(r.uniform(0, span_y))
        rx = x0 + int((bx - 38.0 * t) % span_x)
        ry = y0 + int((by + 92.0 * t) % span_y)
        if y0 <= ry < y1 - 8 and x0 + 4 <= rx < x1:
            c.line((rx, ry), (rx - 4, ry + 9), 2 if ry > 130 else 1, 1)


def _bake_sky(hz, px, py, pr, wp0, wvp, seed):
    c = kit.Canvas(CW, CH, fill=0)
    K.draw_sky_canvas(c, hz, primary_x=px, primary_y=py, primary_r=pr, worm_p0=wp0, worm_vp=wvp, transit_u=None, seed=seed)
    return c.a[:hz].copy()


SKY_COURTYARD = _bake_sky(198, 138, 118, 108, (24, 12), (242, 196), seed=91)


def draw_colonnade_shell(c, breached=False, memorial_on=False):
    """Enclosed stone colonnade structure on right (`x = 384..640`) so no starry sky peeks inside the hall!"""
    # Solid carved stone roof entablature + dark interior hall (`x = 388..640, y = 42..294`)
    c.rect(388, 38, CW, 56, 8); c.rect(388, 38, CW, 42, 9)
    c.rect(392, 56, CW, 294, 0)
    for seg in range(9):
        a0 = 190 + seg * 14; a1 = a0 + 10
        cv2.ellipse(c.a, (518, 290), (148, 224), 0, a0, a1, 2, 15, cv2.LINE_8)
        cv2.ellipse(c.a, (518, 290), (148, 224), 0, a0, a1, 6 if memorial_on else 8, 3, cv2.LINE_8)
        if seg % 2 == 0 and not memorial_on:
            ar = math.radians(a0 + 5)
            c.disc(int(518 + 148 * math.cos(ar)), int(290 + 224 * math.sin(ar)), 2, 0xC)

    c.rect(382, 38, 412, 150, 8); c.rect(382, 38, 388, 150, 9)
    if not breached:
        c.rect(386, 150, 408, 294, 8)
        c.rect(392, 162, 404, 294, 1)
        for by in range(166, 290, 22):
            c.line((386, by), (408, by), 0, 1)
    else:
        c.poly([(382, 150), (412, 150), (406, 174), (386, 166)], 8)
        c.poly([(380, 294), (424, 294), (416, 272), (388, 278)], 8)


# ================================================================== SHOT 1 (0–8 s): DROPSHIP & HARD BREACH
def draw_shot1(c, t):
    hz = 198
    c.a[:hz] = SKY_COURTYARD
    c.grad(hz, 294, [1, 1, 0], power=1.0)
    c.rect(0, 294, CW, CH - 20, 1)
    c.line((0, 294), (CW, 294), 8, 2)
    for fx in range(28, CW, 46):
        c.line((fx, 294), (fx - 16, CH - 20), 0, 1)

    draw_rain(c, t, x0=0, x1=384, y0=18, y1=294, n=65)
    breached = (t >= 6.0)
    draw_colonnade_shell(c, breached=breached, memorial_on=False)
    K.draw_scarred_pillar(c, 488, 60, 294, w=22, damage=0.0, strobe=(6.0 <= t < 6.6), seed=11)

    # Reliquary Dropship: descends (`0..2.0 s`), lands at `2.0 s`, shuts down VTOL flames (`thrust -> 0` by `2.7 s`)!
    if t < 2.0:
        u_d = t / 2.0
        ease = 1.0 - (1.0 - u_d) ** 2
        ds_x = int(round(88 + 56 * ease))
        ds_y = int(round(96 + 178 * ease))
        K.draw_dropship(c, ds_x, ds_y, scale=1.38, ramp_open=0.0, thrust=1.15, tilt_deg=8.0 * (1.0 - ease))
    else:
        ramp_u = min(1.0, (t - 2.0) / 0.35)
        thrust_u = max(0.0, 0.90 * (1.0 - (t - 2.0) / 0.65)) if t < 2.65 else 0.0
        K.draw_dropship(c, 144, 274, scale=1.38, ramp_open=ramp_u, thrust=thrust_u)
        if t < 2.65:
            age = (t - 2.0) / 0.65
            sp_m = np.zeros((CH, CW), bool)
            cv2.ellipse(sp_m, (104, 292), (int(18 + 26 * age), 7), 0, 180, 360, 1, -1)
            cv2.ellipse(sp_m, (176, 292), (int(18 + 26 * age), 7), 0, 180, 360, 1, -1)
            c.mix(sp_m, 1, 0xA if age < 0.4 else 9, 0.55 * (1.0 - 0.6 * age))

    # 4-man Witch Hunter Squad — CONTINUOUSLY DRAWN from 2.15 s to 8.0 s (zero frame gap at 6.0 s!):
    #   2.15..3.95 s: run down ramp to doorway (`Lead reaches x=338 to plant charge at 3.8..4.0 s`)
    #   4.15..5.40 s: back up `46 px` to blast cover (`x = 292, 260, 228, 196`) & crouch!
    #   6.08..8.00 s: surge forward through the breached stone archway!
    if t >= 2.15:
        slots = [(0.0, 338, 292), (0.28, 306, 260), (0.56, 274, 228), (0.84, 242, 196)]
        for idx_h, (delay, x_stack, x_cover) in enumerate(slots):
            if t < 2.15 + delay:
                continue
            if t < 4.15:
                u_m = min(1.0, (t - (2.15 + delay)) / 1.05)
                hx = int(round(218 + (x_stack - 218) * u_m))
                crouch = 0
                moving = (u_m < 1.0)
            elif t < 6.08:
                u_back = min(1.0, (t - 4.15) / 0.95)
                hx = int(round(x_stack + (x_cover - x_stack) * u_back))
                crouch = 5 if u_back >= 0.8 else 0
                moving = (u_back < 1.0)
            else:
                dt_ch = t - 6.08
                hx = int(round(x_cover + 128.0 * dt_ch))
                crouch = 0
                moving = True
            bob = (-2 * ((int(round(t * 15)) + idx_h) % 2)) if moving else 0
            if hx < 536:
                sprite_c(c, K.HUNTER, hx, 244 + crouch + bob, scale=3)
                # Lead breacher extends arm to plant charge at 3.75..4.05 s!
                if idx_h == 0 and 3.75 <= t < 4.15:
                    c.line((hx + 44, 258), (386, 236), 9, 2)
                else:
                    dashed_laser(c, hx + 48, 264 + crouch + bob, min(CW - 6, hx + 148), 258)

    # Sync 4.0 s (`4.0..6.0 s`): Armed shaped thermite charge pulsing on the stone doorway!
    if 4.0 <= t < 6.0:
        pulse_r = 6 + int(3 * abs(math.sin((t - 4.0) * 10.0)))
        c.disc(388, 236, pulse_r + 3, 0xD)
        c.disc(388, 236, pulse_r, 0xE)
        c.disc(388, 236, 3, 0xA)
        cv2.rectangle(c.a, (374, 222), (402, 250), 0xD, 1)

    # Sync 6.0 s (`6.0..6.75 s`): BREACH DETONATION!
    if 6.0 <= t < 6.75:
        age_b = (t - 6.0) / 0.75
        bl_m = np.zeros((CH, CW), bool)
        cv2.circle(bl_m, (404, 228), int(round(28 + 64 * age_b)), 1, -1)
        c.mix(bl_m, 1, 0xA if age_b < 0.45 else 9, 0.68 * (1.0 - 0.55 * age_b))
        if age_b < 0.55:
            c.disc(398, 228, int(round(24 * (1.0 - age_b * 0.6))), 0xE)
            c.disc(396, 228, int(round(12 * (1.0 - age_b))), 0xA)
        for ang, spd in ((-0.45, 115), (-0.18, 140), (0.12, 128), (0.38, 98), (-0.7, 88)):
            bx_d = int(round(402 + spd * age_b * math.cos(ang)))
            by_d = int(round(226 + spd * age_b * math.sin(ang) + 36 * age_b * age_b))
            c.rect(bx_d - 3, by_d - 2, bx_d + 3, by_d + 2, 9 if age_b < 0.4 else 8)


# ================================================================== SHOT 2 (8–16 s): COLONNADE VOLLEY & HEX-LATTICE
def draw_shot2(c, t):
    lt = t - 8.0
    thorn_hit = (t >= 10.0)
    lattice_on = (t >= 12.0)
    reversed_hit = (t >= 14.0)
    lamp_shattered = (t >= 14.10)

    # Hall stays lit (`1`) by the visible ceiling floodlight `(290, 50)` ALL THE WAY until `14.10 s` —
    # so the eroded stone craters NEVER jump or reset at `12.0 s`!
    c.a[:] = 0
    if not lamp_shattered:
        c.rect(0, 36, CW, 296, 1)
    c.rect(0, 296, CW, CH - 20, 1)
    c.line((0, 296), (CW, 296), 8, 2)

    for seg in range(12):
        a0 = 188 + seg * 13; a1 = a0 + 10
        cv2.ellipse(c.a, (320, 292), (296, 242), 0, a0, a1, 2 if not lamp_shattered else 1, 16, cv2.LINE_8)
        cv2.ellipse(c.a, (320, 292), (296, 242), 0, a0, a1, 8, 3, cv2.LINE_8)
        if seg % 2 == 0:
            ar = math.radians(a0 + 5)
            c.disc(int(320 + 296 * math.cos(ar)), int(292 + 242 * math.sin(ar)), 2, 0xC)

    # Physical Inquisition Floodlight Fixture mounted under the Worm-rib crown at `(306, 52)`!
    c.line((306, 36), (306, 48), 8, 2)
    if not lamp_shattered:
        c.rect(296, 48, 316, 56, 9)
        c.rect(299, 52, 313, 57, 0xA)
    else:
        c.rect(298, 48, 314, 53, 8)
        if t < 14.55:
            age_l = (t - 14.10) / 0.45
            c.disc(306, 54, int(round(14 * (1.0 - 0.6 * age_l))), 0xA if age_l < 0.35 else 9)

    c.rect(582, 162, 638, 296, 1); c.rect(582, 162, 588, 296, 8)
    c.rect(596, 208, 628, 250, 0)
    c.line((596, 229), (628, 229), 2, 2)

    # Monotonically increasing stone damage on Columns 1 & 2; dust bursts sit AT BULLET HEIGHT (`y=252..266`)!
    dmg1 = min(0.95, max(0.0, (t - 8.0) / 3.2))
    dmg2 = min(0.65, max(0.0, (t - 8.6) / 3.4))
    burst1 = (256 + int(8 * math.sin(lt * 9.0))) if (8.0 <= t < 9.8) else None
    burst2 = (258 + int(8 * math.cos(lt * 8.0))) if (9.0 <= t < 11.8) else None

    K.draw_scarred_pillar(c, 252, 48, 296, w=24, damage=dmg1, burst_y=burst1, strobe=(not lamp_shattered), seed=11)
    K.draw_scarred_pillar(c, 366, 48, 296, w=24, damage=dmg2, burst_y=burst2, strobe=(not lamp_shattered), seed=12)
    K.draw_scarred_pillar(c, 504, 48, 296, w=24, damage=0.18 if thorn_hit else 0.0, burst_y=None, strobe=False, seed=13)

    n_brass = min(18, int(max(0.0, min(t, 12.0) - 8.0) * 4.5))
    r_b = np.random.default_rng(71)
    for _ in range(n_brass):
        bx_f = int(r_b.integers(42, 198))
        c.rect(bx_f, 298, bx_f + 3, 300, 8)

    # --- 4-man Witch Hunter Squad on left (`x = 52..188`) ---
    # Notice: Point-Hunter #1 (`x=188`) falls ONLY AFTER the fast reversed slugs hit him at `t >= 14.12 s`!
    h_positions = [52, 96, 142, 188]
    for idx_h, hx in enumerate(h_positions):
        if idx_h == 3 and t >= 14.12:
            u_fall = min(1.0, (t - 14.12) / 0.45)
            K.draw_blood_pool(c, hx + 18, 302, rx=int(round(26 * u_fall)), ry=4)
            if u_fall < 0.40:
                # Intermediate crumple frame before hitting the stone!
                sprite_c(c, K.HUNTER, hx - 6, 258, scale=3)
            else:
                sprite_c(c, K.HUNTER_DOWN, hx - 8, 282, scale=3)
            if t < 14.75:
                K.draw_blood_arc(c, hx + 16, 260, dx=-42, dy=-22, progress=(t - 14.12) / 0.63)
            continue

        sprite_c(c, K.HUNTER, hx, 246, scale=3)
        mx, my = hx + 48, 264
        if 8.0 <= t < 12.0:
            firing_now = ((int(round(lt * 6)) + idx_h) % 2 == 0) or (t < 8.6)
            end_x = 466 if t >= 9.9 else (354 if idx_h % 2 else 242)
            dashed_laser(c, mx + 12, my, end_x, 254 + (idx_h - 1) * 5)
            if firing_now:
                muzzle_cone(c, mx, my, dir_x=1, big=(idx_h >= 2))
                c.rect(mx - 12, my - 8, mx - 9, my - 6, 0xE)
                # Fast bright `0xE/0xA` ballistic tracer segment racing along the fire lane!
                u_trc = ((t * 9.0 + idx_h * 0.27) % 1.0)
                tx_tr = int(round(mx + 16 + (end_x - mx - 24) * u_trc))
                c.line((tx_tr, my - 1), (min(end_x, tx_tr + 26), my - 1), 0xE, 2)
                c.px(min(end_x, tx_tr + 26), my - 1, 0xA)
        elif 12.0 <= t < 14.0:
            # Shots streaming into the green Hex-Lattice at x=392!
            dashed_laser(c, mx + 4, my, 390, 236 + idx_h * 9)
            u_trc = ((t * 7.0 + idx_h * 0.25) % 1.0)
            tx_tr = int(round(mx + 10 + (386 - mx - 10) * u_trc))
            c.line((tx_tr, 248 + idx_h * 5), (min(388, tx_tr + 20), 248 + idx_h * 5), 0xE, 2)

    # --- WITCH_THORN: sprints (`8.2..10.0 s`), struck down at 10.0 s! ---
    if t < 10.0:
        u_th = min(1.0, max(0.0, (t - 8.2) / 1.75))
        tx_th = int(round(376 + 78 * u_th))
        bob_th = -3 * (int(round(t * 14)) % 2)
        sprite_c(c, K.WITCH_THORN, tx_th, 254 + bob_th, scale=3, flip=True)
    else:
        u_hit = min(1.0, (t - 10.0) / 0.65)
        K.draw_blood_pool(c, 474, 302, rx=int(round(22 * min(1.0, (t - 10.1) / 0.8))), ry=3)
        if t < 10.22:
            sprite_c(c, K.WITCH_THORN, 454, 254, scale=3, flip=True, swap={6: 4, 7: 5})
        else:
            sprite_c(c, K.WITCH_WOUNDED, 456, 269, scale=3, flip=True)
        if t < 10.75:
            K.draw_blood_arc(c, 464, 266, dx=38, dy=-22, progress=u_hit, witch_sparks=True)

    # --- WITCH_SIGNAL: walks smoothly to x=410 (`10.7..11.9 s` — arrives BEFORE 12.0 s, zero jump!) ---
    if t >= 10.7:
        u_sg = min(1.0, (t - 10.7) / 1.15)
        sx_sg = int(round(548 - 138 * u_sg))
        bob_sg = -2 * (int(round(t * 14)) % 2) if u_sg < 1.0 else 0
        sprite_c(c, K.WITCH_SIGNAL, sx_sg, 236 + bob_sg, scale=3, flip=True)

    if 12.0 <= t < 14.0:
        K.draw_hex_lattice(c, 392, 248, h=92, slugs=5, pulse=(t - 12.0) * 1.4)
    elif 14.0 <= t < 14.32:
        # Sync 14.0 s: Ballistic-speed reversal! 4 slugs cross `392 -> 196` in `0.14 s` (striking Hunter #1 at 14.12 s),
        # while the 5th slug streaks straight UP into the ceiling floodlight `(306, 54)` to shatter it at `14.10 s`!
        u_fast = min(1.0, (t - 14.0) / 0.14)
        for oy in (-12, -4, 4, 12):
            rx_head = int(round(392 - 196 * u_fast))
            rx_tail = min(392, rx_head + 68)
            c.line((rx_head, 258 + oy), (rx_tail, 258 + oy), 7, 2)
            c.line((rx_head, 259 + oy), (rx_tail, 259 + oy), 0xE, 1)
        # 5th slug shooting diagonally UP into the ceiling floodlight `(306, 54)`!
        ux_l = int(round(392 + (306 - 392) * min(1.0, (t - 14.0) / 0.10)))
        uy_l = int(round(232 + (54 - 232) * min(1.0, (t - 14.0) / 0.10)))
        c.line((392, 232), (ux_l, uy_l), 7, 2)


# ================================================================== SHOT 3 (16–24 s): CORRIDOR OF KNIVES (*THE RAID*)
def draw_shot3(c, t):
    lt = t - 16.0
    slash_2 = (t >= 18.0)
    snare_3 = (t >= 20.0)
    retreat_4 = (t >= 22.0)

    strobe_on = (17.80 <= t < 18.22) or (19.95 <= t < 20.20)
    c.a[:] = 1 if strobe_on else 0
    c.rect(0, 298, CW, CH - 20, 2 if strobe_on else 1)
    c.line((0, 298), (CW, 298), 9 if strobe_on else 8, 2)

    for seg in range(11):
        a0 = 195 + seg * 14; a1 = a0 + 10
        cv2.ellipse(c.a, (320, 286), (340, 254), 0, a0, a1, 8 if strobe_on else 2, 18, cv2.LINE_8)
        cv2.ellipse(c.a, (320, 286), (340, 254), 0, a0, a1, 9 if strobe_on else 8, 3, cv2.LINE_8)

    K.draw_scarred_pillar(c, 156, 36, 298, w=26, damage=0.80, burst_y=None, strobe=strobe_on, seed=21)
    K.draw_scarred_pillar(c, 488, 36, 298, w=26, damage=0.65, burst_y=None, strobe=strobe_on, seed=22)

    # --- HUNTER #2 (`x = 248`, facing right): Bayou drops BEHIND his back (`x = 186`), kicks off left column `x=156`,
    # and lands on his LEFT (`x = 188`) matching the left-side `0x7` crescent slash at `18.0 s`! ---
    if not slash_2:
        h2_flip = (t >= 17.75)                                                  # spins around too late at 17.75 s!
        sprite_c(c, K.HUNTER, 248, 232, scale=4, flip=h2_flip)
        if 17.80 <= t < 18.0:
            muzzle_cone(c, 244, 256, dir_x=-1, big=True)
        else:
            dashed_laser(c, 312, 256, 412, 256)
    else:
        u_h2 = min(1.0, (t - 18.0) / 0.55)
        K.draw_blood_pool(c, 274, 304, rx=int(round(30 * u_h2)), ry=4)
        if t < 18.22:
            sprite_c(c, K.HUNTER, 252, 244, scale=4, flip=True)
        else:
            sprite_c(c, K.HUNTER_DOWN, 242, 278, scale=3)
        if t < 18.65:
            K.draw_blood_arc(c, 268, 248, dx=44, dy=-24, progress=u_h2)

    # --- WITCH_BAYOU: drops behind Hunter #2's back (`x=186`, `16.0..16.5 s`), vaults off left column (`17.2..18.0 s`),
    # lands at `x=188` slashing right at `18.0 s`, and hurls a `0x7` throwing-knife into Hunter #4 at `22.0 s`! ---
    if t < 17.15:
        u_dr = min(1.0, lt / 0.45)
        by_y = int(round(48 + 194 * (1.0 - (1.0 - u_dr) ** 2)))
        if u_dr < 1.0:
            c.line((208, 36), (208, by_y + 12), 2, 1)
        sprite_c(c, K.WITCH_THORN, 184, by_y, scale=4, flip=False)
    elif t < 18.0:
        u_v = (t - 17.15) / 0.85
        bx_v = int(round(184 - 34 * math.sin(u_v * math.pi)))                   # plants foot right on Column 1 (`x=156`)!
        by_v = int(round(242 - 72 * math.sin(u_v * math.pi)))
        sprite_c(c, K.WITCH_THORN, bx_v, by_v, scale=4, flip=False)
    else:
        sprite_c(c, K.WITCH_THORN, 186, 242, scale=4, flip=(t >= 21.8))
        if t < 18.60:
            cv2.ellipse(c.a, (242, 246), (44, 32), 24, -115, 75, 6, 4, cv2.LINE_8)
            cv2.ellipse(c.a, (242, 246), (44, 32), 24, -100, 60, 7, 2, cv2.LINE_8)

    # --- HUNTER #3 (`x = 362`) turns left at `18.25 s` on hearing Hunter #2 die, then spins right at `19.7 s` as Runner slides in! ---
    if not snare_3:
        h3_flip = (18.25 <= t < 19.70)
        sprite_c(c, K.HUNTER, 362, 232, scale=4, flip=h3_flip)
        if h3_flip:
            dashed_laser(c, 358, 256, 260, 256)
        if t >= 19.3:
            u_sl = min(1.0, (t - 19.3) / 0.70)
            rx_sl = int(round(538 - 98 * u_sl))
            sprite_c(c, K.WITCH_RUNNER, rx_sl, 250, scale=4, flip=True, swap={0xF: None, 8: 0})
    else:
        u_h3 = min(1.0, (t - 20.0) / 0.55)
        # Hunter #3's final gunshot flashes ONLY while he is still upright (`20.00..20.16 s`)!
        if t < 20.16:
            muzzle_cone(c, 426, 256, dir_x=1, big=True)
            c.line((442, 256), (464, 264), 0xE, 2)
        K.draw_blood_pool(c, 392, 304, rx=int(round(28 * u_h3)), ry=4)
        if t < 20.22:
            sprite_c(c, K.HUNTER, 362, 244, scale=4)
        else:
            sprite_c(c, K.HUNTER_DOWN, 354, 278, scale=3)
        if t < 20.70:
            K.draw_blood_arc(c, 388, 252, dx=-42, dy=-24, progress=u_h3)
            # Runner's grazed shoulder droplet arc!
            K.draw_blood_arc(c, 456, 264, dx=22, dy=-12, progress=u_h3, witch_sparks=True)

        # Taut floor snare-wire (`y=295` right on the stone!) + Runner with `0xD` shoulder wound (no held lantern!)
        c.line((356, 295), (448, 295), 6, 2)
        sprite_c(c, K.WITCH_RUNNER, 440, 252, scale=4, flip=True, swap={0xF: None, 8: 0})
        c.rect(456, 272, 464, 282, 0xD)                                         # crisp 0xD shoulder graze on Runner's coat!
        sprite_c(c, K.WITCH_SIGNAL, 514, 218, scale=4, flip=True)
        if t < 20.55:
            c.line((518, 264), (382, 254), 7, 3)
            c.line((518, 266), (382, 256), 6, 1)

    # --- HUNTER #4 (`x = 68`): at 22.0 s Bayou flings a `0x7` green throwing-knife that VISIBLY WOUNDS his arm (`1 WIA`)! ---
    if t < 21.88:
        sprite_c(c, K.HUNTER, 68, 232, scale=4)
        dashed_laser(c, 132, 256, 184, 256)
    elif t < 22.0:
        # Spinning `0x7` green blade flying from Bayou `(186, 258)` straight into Hunter #4 `(104, 258)`!
        u_kn = (t - 21.88) / 0.12
        kx = int(round(186 - 82 * u_kn))
        c.line((kx - 8, 258), (kx + 8, 258), 7, 3)
        sprite_c(c, K.HUNTER, 68, 232, scale=4)
    else:
        # Sync 22.0 s: Knife strikes Hunter #4's shoulder! Curved `0xD` blood splash + `0xD` coat stain + limping retreat!
        u_ret = min(1.0, (t - 22.0) / 1.75)
        hx4 = int(round(68 - 148 * u_ret))
        limp = 4 if (int(round(t * 10)) % 2 == 0) else 0
        if t < 22.60:
            K.draw_blood_arc(c, max(8, hx4 + 28), 252, dx=-34, dy=-18, progress=(t - 22.0) / 0.60)
        K.draw_blood_pool(c, 84, 303, rx=12, ry=2)
        K.draw_blood_pool(c, 44, 303, rx=9, ry=2)
        if hx4 > -68:
            sprite_c(c, K.HUNTER, hx4, 232 + limp, scale=4, flip=True, swap={9: 0xD})


# ================================================================== SHOT 4 (24–32 s): RAIN, RETREAT & PIETÀ
def draw_shot4(c, t):
    lt = t - 24.0
    sanctum_open = (t >= 26.0)
    memorial_on = (t >= 30.0)

    hz = 198
    c.a[:hz] = SKY_COURTYARD
    c.grad(hz, 294, [1, 1, 0], power=1.0)
    c.rect(0, 294, CW, CH - 20, 1)
    c.line((0, 294), (CW, 294), 8, 2)
    for fx in range(28, CW, 46):
        c.line((fx, 294), (fx - 16, CH - 20), 0, 1)

    draw_rain(c, t, x0=0, x1=384, y0=18, y1=294, n=70)
    draw_colonnade_shell(c, breached=True, memorial_on=memorial_on)
    K.draw_scarred_pillar(c, 468, 60, 294, w=22, damage=0.85, burst_y=None, strobe=False, seed=11)

    # Persistent blood pools & fallen Hunter #1 inside the breach
    K.draw_blood_pool(c, 434, 302, rx=22, ry=3)
    sprite_c(c, K.HUNTER_DOWN, 412, 282, scale=2)
    K.draw_blood_pool(c, 342, 301, rx=10, ry=2)

    # Sync 24.0 s:
    # 1) Wounded Hunter #4 scrambles up the ramp (`24.0..24.55 s`)!
    # 2) Signal fires a green `0x6/0x7` hex-lance bolt out the breach (`24.0..24.30 s`) that SCORCHES the Reliquary's
    #    hull on screen — explaining why it lifts off trailing drifting smoke!
    if lt < 0.55:
        u_bd = lt / 0.55
        bx_h4 = int(round(238 - 44 * u_bd))
        by_h4 = int(round(252 - 18 * u_bd))
        sprite_c(c, K.HUNTER, bx_h4, by_h4, scale=2, flip=True, swap={9: 0xD})
    if lt < 0.32:
        u_hb = lt / 0.32
        bx_end = int(round(468 + (164 - 468) * u_hb))
        by_end = int(round(256 + (254 - 256) * u_hb))
        c.line((468, 256), (bx_end, by_end), 6, 3)
        c.line((468, 255), (bx_end, by_end - 1), 7, 1)

    if lt < 5.2:
        u_lift = max(0.0, (lt - 0.35) / 4.85)
        ease_l = u_lift * u_lift
        ds_x = int(round(144 - 138 * ease_l))
        ds_y = int(round(274 - 204 * ease_l))
        ramp_cl = max(0.0, 1.0 - max(0.0, lt - 0.45) / 0.55)
        K.draw_dropship(c, ds_x, ds_y, scale=max(0.75, 1.38 - 0.52 * ease_l),
                        ramp_open=ramp_cl, thrust=1.15 if lt >= 0.25 else 0.4,
                        tilt_deg=-9.0 * min(1.0, max(0.0, lt - 0.35) / 1.4), damaged=False)
        if lt >= 0.28:
            # Scorched `0x6`/`0xD` impact scar + drifting world-space smoke puffs left behind in the air!
            c.disc(ds_x + 12, ds_y - 16, 3, 6 if lt < 0.8 else 0xD)
            for ks in range(5):
                age_s = (lt - 0.28 + ks * 0.22) % 1.1
                sx_sm = int(round(ds_x + 16 + 18 * age_s))
                sy_sm = int(round(ds_y - 20 - 28 * age_s))
                c.disc(sx_sm, sy_sm, int(3 + 5 * age_s), 2 if age_s < 0.5 else 1)

    # Inner Sanctum Threshold on right (`x = 584..638`):
    c.rect(584, 156, 638, 294, 1); c.rect(584, 156, 590, 294, 8)
    if not sanctum_open:
        c.rect(596, 204, 630, 288, 0)
    else:
        u_op = min(1.0, (t - 26.0) / 0.45)
        h_op = max(4, int(round(78 * u_op)))
        c.rect(596, 288 - h_op, 630, 288, 0xF)
        c.rect(594, 244, 632, 250, 1)
        c.poly([(596, 294), (630, 294), (626, 316), (498, 310), (528, 294)], 0xF)

    # Pietà group (`x = 480..580`) — cleanly separated from Bayou (`x = 424 -> 342`)!
    K.draw_blood_pool(c, 532, 302, rx=20, ry=3)
    sprite_c(c, K.WITCH_WOUNDED, 514, 268, scale=3, flip=True)
    sprite_c(c, K.WITCH_SIGNAL, 476, 236, scale=3, flip=(lt < 0.6))
    sprite_c(c, K.WITCH_RUNNER, 552, 258, scale=3, flip=True, swap={0xF: None, 8: 0})
    c.rect(564, 273, 570, 281, 0xD)

    # Sync 30.0 s: WITCH_BAYOU walks from `x=426` (`50px` clear of Signal!) to `x=342`, kneels (`29.75..30.15 s`),
    # and plants Thorn's `0x7` green-etched blade into the threshold rubble!
    bx_bay = 342 if t >= 29.4 else int(round(426 - 84 * min(1.0, max(0.0, (t - 28.0) / 1.4))))
    kneel_y = 8 if (29.75 <= t < 30.20) else 0
    sprite_c(c, K.WITCH_BAYOU, bx_bay, 248 + kneel_y, scale=3, flip=(28.0 <= t < 29.4))
    if 29.75 <= t < 30.10:
        # Visible arm + blade descending into the rubble at `x=396`!
        u_pl = (t - 29.75) / 0.35
        by_b = int(round(230 + 16 * u_pl))
        c.line((396, by_b), (396, by_b + 26), 7, 2)
    elif memorial_on:
        c.line((396, 246), (396, 274), 7, 2)
        c.line((391, 254), (401, 254), 6, 2)
        u_m = min(1.0, (t - 30.0) / 0.45)
        cv2.ellipse(c.a, (396, 274), (int(round(28 * u_m)), 6), 0, 0, 360, 6, 2, cv2.LINE_8)
        c.disc(396, 246, 3, 7)


# ================================================================== FULL 1280 x 720 COMPOSITE + HUD + GLOW
def render_frame(fi):
    t = fi / FPS
    c = kit.Canvas(CW, CH, fill=0)

    if t < 8.0:
        draw_shot1(c, t)
        assert not (c.a == 0xF).any(), f'0xF leaked into Dropship/Breach at t={t:.2f}!'
    elif t < 16.0:
        draw_shot2(c, t)
        assert not (c.a == 0xF).any(), f'0xF leaked into Colonnade firefight at t={t:.2f}!'
    elif t < 24.0:
        draw_shot3(c, t)
        assert not (c.a == 0xF).any(), f'0xF leaked into Dark Corridor CQB at t={t:.2f}!'
    else:
        draw_shot4(c, t)
        if t < 26.0:
            assert not (c.a == 0xF).any(), f'0xF leaked before sanctum opened at t={t:.2f}!'

    img = np.zeros((H, W, 3), np.float32)
    U.blit(img, c.a, 0, 0, scale=2)

    if t < 2.0:
        hdr, sub, bcol = 'RELIQUARY DROP // INBOUND', 'INQUISITION STRIKE TEAM (4X)', 8
    elif t < 4.0:
        hdr, sub, bcol = 'COURTYARD TOUCHDOWN // RAMP DOWN', 'BREACH STACK DEPLOYING', 0xA
    elif t < 6.0:
        hdr, sub, bcol = 'SHAPED CHARGE ARMED // TAKING COVER', 'THERMITE COUNTDOWN ACTIVE', 0xE
    elif t < 8.0:
        hdr, sub, bcol = 'HARD BREACH! // ENTERING HALL', 'WEAPONS FREE ON WITCH COVEN', 0xD
    elif t < 10.0:
        hdr, sub, bcol = 'COLONNADE VOLLEY // STONE ERODING', 'AUTOMATIC DISH-RIFLE SUPPRESSION', 0xA
    elif t < 12.0:
        hdr, sub, bcol = 'SISTER THORN HIT! // DOWN IN HALL', 'DRAWS FIRE AWAY FROM SANCTUM DOOR', 0xD
    elif t < 14.0:
        hdr, sub, bcol = 'HEX-LATTICE UP! // SLUGS CAUGHT', 'SIGNAL ARRESTS VOLLEY MID-AIR', 6
    elif t < 16.0:
        hdr, sub, bcol = 'VOLLEY REVERSED // 1 HUNTER KIA', 'LAMP SHATTERED -> HALL IN SHADOW', 6
    elif t < 18.0:
        hdr, sub, bcol = 'DARK CORRIDOR // AMBUSH ABOVE', 'BAYOU DROPS BEHIND LEAD HUNTER', 5
    elif t < 20.0:
        hdr, sub, bcol = 'PILLAR VAULT // BLADE STRIKE', '2ND HUNTER KIA   STROBE DARKNESS', 0xD
    elif t < 22.0:
        hdr, sub, bcol = 'FLOOR WIRE-SNARE // MUTUAL BLOOD', 'RUNNER GRAZED   3RD HUNTER DOWN', 0xD
    elif t < 24.0:
        hdr, sub, bcol = 'THROWN BLADE // 4TH HUNTER WOUNDED', '3 KIA, 1 WIA -> FLEEING HALL!', 8
    elif t < 26.0:
        hdr, sub, bcol = 'COURTYARD RAIN // RAID ABORTED', 'HEX-BOLT SCORCHES RETREATING SHIP', 8
    elif t < 30.0:
        hdr, sub, bcol = 'SANCTUM UNSHUTTERED // LAMP KEPT', 'WARMTH OVER FALLEN SISTER THORN', 0xF
    else:
        hdr, sub, bcol = 'MEMORIAL BLADE // COVEN ENDURES', 'COST PAID IN BLOOD   LAMP UNBROKEN', 6

    pw = max(U.tw(hdr, 2), U.tw(sub, 2)) + 28
    U.rect(img, 18, 16, 18 + pw, 72, U.C[0], a=0.86)
    U.rect(img, 18, 16, 18 + pw, 20, U.C[bcol])
    U.text(img, 30, 26, hdr, U.C[0xA if bcol != 0xF else 0xF], scale=2)
    U.text(img, 30, 48, sub, U.C[6 if bcol in (5, 6) else 9], scale=2)

    U.rect(img, 0, H - 38, W, H, U.C[0])
    U.rect(img, 0, H - 40, W, H - 38, U.C[2])
    bar_i = int(t // 2.0) + 1
    shot_i = int(t // 8.0) + 1
    foot = f'KALEDATHELA: RELIQUARY DROP   SHOT {shot_i}/4   BAR {bar_i:02d}/16'
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
        test_times = (5.0, 6.0, 12.6, 14.2, 18.2, 22.1, 24.2, 30.6)
        for ts in test_times:
            fi = int(round(ts * FPS))
            img = (np.clip(render_frame(fi), 0, 1)[..., ::-1] * 255 + .5).astype(np.uint8)
            cv2.imwrite(str(OUT / f'v2_test_{ts:04.1f}s.png'), img)
        print('wrote', len(test_times), 'v2 raid test stills to', OUT)
    else:
        with Pool(24) as pool:
            list(pool.imap_unordered(_worker, range(NF), chunksize=16))
        poster = (np.clip(render_frame(int(round(12.6 * FPS))), 0, 1)[..., ::-1] * 255 + .5).astype(np.uint8)
        cv2.imwrite(str(HERE / 'raid_poster.png'), poster)
        subprocess.run([
            'ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS),
            '-i', str(FRAMES / 'f_%04d.png'), '-i', str(OUT / 'raid.wav'),
            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'slow',
            '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', '-shortest',
            str(HERE / 'raid_concept.mp4')
        ], check=True)
        from backlot import sync, screen
        res = sync.check(RAID_POINTS, str(FRAMES), str(OUT / 'raid.wav'), fps=FPS,
                         out_jpg=str(HERE / 'raid_sync.jpg'), out_json=str(OUT / 'sync.json'))
        pops = sync.pops(RAID_POINTS, str(FRAMES), fps=FPS)
        tr = sync.travel(str(FRAMES))
        screen.filmstrip(str(FRAMES), str(OUT / 'strip.jpg'), n=16)
        sync.events(RAID_POINTS, str(FRAMES), str(OUT / 'events_sheets'), fps=FPS)
        print('wrote v2', HERE / 'raid_concept.mp4')
        print('sync both:', res['both'], '/', res['total'], '| pops:', pops, '| travel:', tr[1])
