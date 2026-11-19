"""Combat & Gothic Violence Concept Plates (`raid_sheet.png`, `raid_tableau.png`).

Tests the soft-R chromatic combat grammar codified in `COMBAT.md` (`The Matrix` + `The Raid: Redemption` inspirations):
  1. `raid_sheet.png`   (Fig. R0) — Reliquary Dropship, Destructible Stone, Hex-Lattice & 4-Panel Blood/Strobe Law
  2. `raid_tableau.png` (Fig. R1) — Hero Action Tableau: *The Colonnade Breach* (mutual casualties & bullet-stop)

    uv run python styles/hex/kaledathela/raid_plates.py
"""
import sys, math
from pathlib import Path
HERE = Path(__file__).resolve().parent; HEX = HERE.parent; ROOT = HERE.parents[2]
sys.path.insert(0, str(HEX / 'uptime')); sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(HEX)); sys.path.insert(0, str(HERE))
import numpy as np
import cv2
import kit, ui as U
import kit_kal as K

W, H = 640, 360


def sprite_s(c, rows, x, y, scale=2, flip=False, swap=None):
    x0, y0 = int(round(x)), int(round(y))
    for j, r in enumerate(rows):
        rr = r[::-1] if flip else r
        for i, ch in enumerate(rr):
            if ch != '.':
                col = int(ch, 16)
                if swap and col in swap:
                    col = swap[col]
                c.rect(x0 + i * scale, y0 + j * scale, x0 + (i + 1) * scale, y0 + (j + 1) * scale, col)


def strip16(c, x, y):
    c.rect(x - 2, y - 2, x + 16 * 6 + 1, y + 7, 0)
    for k in range(16):
        c.rect(x + k * 6, y, x + k * 6 + 5, y + 5, k)


# ================================================================== PLATE R0: SOFT-R COMBAT & GORE DOCTRINE SHEET
def make_raid_sheet():
    c = kit.Canvas(W, H, fill=0)
    Q, R, edge = kit.hexmap(14, w=W, h=H, ox=2, oy=2)
    c.a[:] = np.where((Q + R) % 2 == 0, 0, 1).astype(np.uint8)
    c.mask(edge, 0)

    c.rect(0, 0, W, 16, 0); c.rect(0, 16, W, 17, 0xD)
    c.text(8, 4, 'FIG. R0  GOTHIC COMBAT: BALLISTICS, BLOOD & HEX-WARD LAW', 0xA)
    strip16(c, W - 102, 5)

    # Top-Left Box: RELIQUARY DROPSHIP & BREACH SQUAD
    c.rect(10, 22, 314, 186, 0); c.bevel(10, 22, 314, 186, face=1, hi=8, lo=2)
    c.rect(12, 24, 312, 36, 0xD); c.text(16, 26, 'INQUISITION: RELIQUARY DROPSHIP', 0xA)
    c.rect(16, 40, 308, 146, 0)
    c.rect(16, 132, 308, 146, 1); c.line((16, 132), (308, 132), 8, 1)
    K.draw_dropship(c, 128, 108, scale=1.35, ramp_open=0.95, thrust=0.85)
    sprite_s(c, K.HUNTER, 232, 98, scale=2)
    sprite_s(c, K.HUNTER, 268, 98, scale=2)
    c.text(18, 151, 'VTOL THRUST = 0xE + 0xA (NO 0xF!)', 0xE)
    c.text(18, 163, 'RAMP FLOOD 0xA + STACKED 0xD VISORS', 9)
    c.text(18, 175, 'SHAPED BREACH -> AUTOMATIC VOLLEY', 9)

    # Top-Right Box: MATRIX PILLAR EROSION & BULLET-STOP LATTICE
    c.rect(326, 22, 630, 186, 0); c.bevel(326, 22, 630, 186, face=1, hi=5, lo=2)
    c.rect(328, 24, 628, 36, 5); c.text(332, 26, 'COVEN COUNTER: STONE & HEX-LATTICE', 0xA)
    c.rect(332, 40, 624, 146, 0)
    c.rect(332, 134, 624, 146, 1); c.line((332, 134), (624, 134), 8, 1)
    # Incoming ballistic lines on left chewing stone column + caught in green lattice!
    K.draw_scarred_pillar(c, 396, 44, 134, w=24, damage=0.75, burst_y=84, strobe=True, seed=7)
    for ly, lx1 in ((74, 488), (88, 491), (104, 487), (118, 490)):
        c.line((336, ly), (382 if ly == 88 else lx1, ly), 0xD, 1)
    K.draw_hex_lattice(c, 492, 94, h=70, slugs=5, pulse=0.35)
    sprite_s(c, K.WITCH_SIGNAL, 520, 74, scale=3, flip=True)
    sprite_s(c, K.WITCH_THORN,  576, 92, scale=3, flip=True)
    c.text(334, 151, 'STONE COVER CRATERS PERMANENTLY', 9)
    c.text(334, 163, '0x6/0x7 LATTICE ARRESTS 0xE SLUGS', 6)
    c.text(334, 175, 'THORN: CLOSE-QUARTERS 0x7 BLADES', 7)

    # Bottom 4-Panel Soft-R Chromatic Violence Law
    c.rect(10, 192, 630, 340, 0); c.bevel(10, 192, 630, 340, face=0, hi=3, lo=1)
    c.text(18, 198, 'SOFT-R CHROMATIC VIOLENCE LAW (CALLIGRAPHIC, PERMANENT, MUTUAL COST):', 0xA)

    panels = [
        (18,  '1. MUZZLE STROBE', '0xA CONE + BRASS'),
        (170, '2. ARTERIAL 0xD',  'SLASH -> 0x2 POOL'),
        (322, '3. WITCH WOUNDED', '0x6 -> 0x4 DIMMED'),
        (474, '4. SOLE 0xF RULE', 'NEVER IN WEAPONS'),
    ]
    for idx_p, (bx, t1, t2) in enumerate(panels):
        c.rect(bx, 212, bx + 144, 294, 0 if idx_p == 0 else 1)
        c.rect(bx, 212, bx + 144, 213, 0xD if idx_p in (1, 2) else (0xF if idx_p == 3 else 9))
        c.rect(bx, 280, bx + 144, 294, 1); c.line((bx, 280), (bx + 144, 280), 8, 1)

        if idx_p == 0:
            # Directional ballistic muzzle cone (`>`, never a `+` cross!) + tumbling 0xE brass casings
            sprite_s(c, K.HUNTER, bx + 14, 246, scale=2)
            mx, my = bx + 54, 258
            c.poly([(mx, my - 6), (mx + 18, my), (mx, my + 6)], 0xA)
            c.poly([(mx, my - 3), (mx + 10, my), (mx, my + 3)], 0xE)
            c.line((mx + 18, my), (bx + 138, my), 0xD, 1)
            for cx_b, cy_b in ((mx - 8, my - 10), (mx - 15, my - 6), (mx - 21, my + 4), (mx - 25, my + 19)):
                c.rect(cx_b, cy_b, cx_b + 3, cy_b + 2, 0xE if cy_b < my + 10 else 8)
        elif idx_p == 1:
            # Calligraphic 0xD slash + fallen Hunter over dark 0x2 pool with 0xD meniscus
            K.draw_blood_pool(c, bx + 78, 283, rx=28, ry=4)
            sprite_s(c, K.HUNTER_DOWN, bx + 50, 270, scale=2)
            K.draw_blood_arc(c, bx + 64, 262, dx=44, dy=-24, progress=0.85)
        elif idx_p == 2:
            # Wounded Witch: 0xD mortal blood + green 0x6 dimmed to 0x4 deep verdigris + 0x5 fading sparks!
            K.draw_blood_pool(c, bx + 72, 283, rx=22, ry=3)
            sprite_s(c, K.WITCH_WOUNDED, bx + 52, 262, scale=2)
            K.draw_blood_arc(c, bx + 68, 264, dx=-32, dy=-18, progress=0.75, witch_sparks=True)
        else:
            # Defended shuttered 0xF lamp untouched behind stone wall while battle rages outside
            c.rect(bx + 36, 220, bx + 48, 280, 8)
            c.line((bx + 8, 248), (bx + 36, 248), 0xA, 2)
            c.disc(bx + 36, 248, 4, 9)
            c.rect(bx + 82, 250, bx + 102, 278, 8)
            c.rect(bx + 85, 254, bx + 99, 274, 0xF)
            c.rect(bx + 76, 278, bx + 108, 280, 0xF)

        c.rect(bx, 296, bx + 144, 322, 0)
        c.text(bx + 2, 299, t1, 0xA if idx_p != 3 else 0xF)
        c.text(bx + 2, 311, t2, 0xD if idx_p == 1 else (6 if idx_p == 2 else 9))

    c.text(18, 327, 'INSPIRED BY THE MATRIX (STONE + LATTICE) & THE RAID (DARK BREACH + COST)', 9)
    c.rect(0, H - 14, W, H, 0); c.rect(0, H - 15, W, H - 14, 2)
    c.text(8, H - 11, 'COMBAT.CFG  0xD = LOCK & BLOOD  0x4 = DIMMED WITCH  0xF = LAMP', 0xA)
    strip16(c, W - 102, H - 10)
    return c.save(HERE / 'raid_sheet.png', scale=2)


# ================================================================== PLATE R1: HERO ACTION TABLEAU (*THE COLONNADE BREACH*)
def make_raid_tableau():
    c = kit.Canvas(W, H, fill=0)
    hz = 198
    K.draw_sky_canvas(c, hz, primary_x=148, primary_y=118, primary_r=106,
                      worm_p0=(30, 14), worm_vp=(218, hz - 2), transit_u=0.52, seed=91)

    # Slanted toxic violet rain across the left exterior courtyard (`x = 0..245`)
    rng = np.random.default_rng(104)
    for _ in range(110):
        rx = int(rng.integers(4, 244)); ry = int(rng.integers(18, 290))
        c.line((rx, ry), (rx - 5, ry + 12), 2 if ry > 110 else 1, 1)

    # Wet courtyard & colonnade stone floor (`y = 294..346`)
    c.grad(hz, 294, [1, 1, 0], power=1.0)
    c.rect(0, 294, W, H - 14, 1)
    c.line((0, 294), (W, 294), 8, 2)
    for fx in range(24, W, 44):
        c.line((fx, 294), (fx - 18, H - 14), 0, 1)

    # Colossal ancient Worm-Rib overarching the pillared ruin colonnade (`x = 224..628`)
    c.rect(236, 36, W, 294, 0)                                                  # dark interior colonnade hall
    for seg in range(11):
        a0 = 190 + seg * 13; a1 = a0 + 10
        cv2.ellipse(c.a, (434, 290), (206, 232), 0, a0, a1, 2, 16, cv2.LINE_8)
        cv2.ellipse(c.a, (434, 290), (206, 232), 0, a0, a1, 8, 3, cv2.LINE_8)
        if seg % 2 == 0:
            ar = math.radians(a0 + 5)
            c.disc(int(434 + 206 * math.cos(ar)), int(290 + 232 * math.sin(ar)), 2, 0xC)

    # Shattered outer stone breach wall at `x = 236`
    c.rect(228, 36, 248, 128, 8); c.rect(228, 36, 234, 128, 9)
    c.poly([(228, 128), (248, 128), (242, 152), (230, 144)], 8)                # jagged blown-out upper lintel
    c.poly([(226, 294), (252, 294), (246, 266), (232, 274)], 8)                # rubble pile at breach base

    # Left Exterior Courtyard: Landed Reliquary Dropship (`0xE` VTOL wash)
    K.draw_dropship(c, 102, 274, scale=1.42, ramp_open=1.0, thrust=0.65)

    # Three classical stone columns inside the colonnade — progressive Matrix bullet erosion!
    K.draw_scarred_pillar(c, 316, 58, 294, w=24, damage=0.90, burst_y=214, strobe=True, seed=11)
    K.draw_scarred_pillar(c, 408, 58, 294, w=24, damage=0.55, burst_y=236, strobe=True, seed=12)
    K.draw_scarred_pillar(c, 540, 58, 294, w=24, damage=0.10, burst_y=None, strobe=False, seed=13)

    # Far Right (`x = 572..636`): The defended Sanctum Doorway with horizontal shutter slats glowing warm 0xF!
    c.rect(574, 168, 636, 294, 1); c.rect(574, 168, 580, 294, 8)
    c.rect(588, 212, 624, 254, 0)
    c.rect(592, 218, 620, 225, 0xF)
    c.rect(592, 232, 620, 239, 0xF)
    c.rect(590, 225, 622, 232, 1)
    c.rect(584, 294, 628, 298, 0xF)

    # --- Mutual Casualties & Active Firefight (cleanly separated silhouettes, zero overlap!) ---
    # 1) Dead Point-Hunter #1 lying in clear space between Columns 1 & 2 over a settled 0x2/0xD blood pool!
    K.draw_blood_pool(c, 362, 302, rx=24, ry=4)
    sprite_s(c, K.HUNTER_DOWN, 336, 286, scale=2)

    # 2) Two firing Witch Hunters (#2 and #3) advancing through the breach with directional 0xA muzzle cones!
    sprite_s(c, K.HUNTER, 186, 244, scale=3)
    sprite_s(c, K.HUNTER, 244, 244, scale=3)
    for mx, my, ty_end in ((234, 264, 222), (292, 264, 240)):
        c.poly([(mx, my - 6), (mx + 18, my), (mx, my + 6)], 0xA)
        c.poly([(mx, my - 3), (mx + 9, my), (mx, my + 3)], 0xE)
        c.line((mx + 18, my), (428, ty_end), 0xD, 1)
        for bx_c, by_c in ((mx - 8, my - 10), (mx - 16, my - 5), (mx - 22, my + 8)):
            c.rect(bx_c, by_c, bx_c + 3, by_c + 2, 0xE)

    # 3) `WITCH_SIGNAL` standing resolute at `x=438` directly behind her blazing 0x6/0x7 Hex-Lattice (`x=430`)!
    K.draw_hex_lattice(c, 430, 240, h=82, slugs=5, pulse=0.25)
    sprite_s(c, K.WITCH_SIGNAL, 438, 234, scale=3, flip=True)

    # 4) Wounded Coven Sister (`WITCH_THORN`, dimmed `0x4` teal + `0xD` blood pool) clearly visible at `x=490`!
    K.draw_blood_pool(c, 508, 302, rx=20, ry=3)
    sprite_s(c, K.WITCH_WOUNDED, 488, 268, scale=3, flip=True)
    K.draw_blood_arc(c, 498, 274, dx=24, dy=-16, progress=0.72, witch_sparks=True)

    # 5) Second Coven fighter vaulting downward off Column 1 / Worm-rib rafters with a razor 0x7 green blade arc!
    sprite_s(c, K.WITCH_THORN, 344, 162, scale=3, flip=True)
    cv2.ellipse(c.a, (336, 192), (32, 22), -28, 120, 295, 6, 3, cv2.LINE_8)
    cv2.ellipse(c.a, (336, 192), (32, 22), -28, 135, 280, 7, 1, cv2.LINE_8)

    # Compact HUD telemetry top-left
    c.rect(10, 10, 238, 38, 0); c.rect(10, 10, 238, 12, 0xD)
    c.text(16, 15, 'RAID SECTOR: COLONNADE 09', 0xA)
    c.text(16, 26, 'HOSTILES: 0x6 LATTICE UP!', 0xD)

    c.rect(0, H - 14, W, H, 0); c.rect(0, H - 15, W, H - 14, 2)
    c.text(8, H - 11, 'FIG. R1  RELIQUARY RAID: SHATTERED STONE, 0xD BLOOD & 0x6 LATTICE', 0xA)
    strip16(c, W - 102, H - 10)

    # Save with 2x pixel scale + true U.glow ONLY on the 0xF sanctum slats on the far right!
    idx_big = np.repeat(np.repeat(c.a, 2, 0), 2, 1)
    img = U.C[idx_big].copy()
    sw = img[720 - 28:, 1280 - 210:].copy()
    img[720 - 28:, 1280 - 210:] = 0.0
    img = U.glow(img, strength=0.62)
    img[720 - 28:, 1280 - 210:] = sw
    bgr = (np.clip(img, 0, 1)[..., ::-1] * 255 + 0.5).astype(np.uint8)
    out_p = HERE / 'raid_tableau.png'
    cv2.imwrite(str(out_p), bgr)
    return out_p


if __name__ == '__main__':
    p0 = make_raid_sheet()
    p1 = make_raid_tableau()
    print('wrote raid plates:', p0, p1)
