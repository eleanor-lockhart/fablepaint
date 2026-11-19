"""Kaledathela concept plates (strictly sixteen registers, 640 x 360 saved at 2x = 1280 x 720):

  1. concept_sheet.png   Cast silhouettes, four ruin/terrain motifs, and the sixteen-register chromatic law
  2. east_bayou.png      East Texas: cypress/loblolly bayou, refinery flare stacks, broadcast cross, shuttered shack
  3. west_wastes.png     West Texas: caprock mesas, Lufkin pumpjack, Worm-rib + fallen arches, Pastor's convoy, cellar

    uv run python styles/hex/kaledathela/plates.py
"""
import sys, math
from pathlib import Path
HERE = Path(__file__).resolve().parent; HEX = HERE.parent; ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE)); sys.path.insert(1, str(HEX)); sys.path.insert(2, str(ROOT))
import numpy as np
import cv2
import kit, sprites as SP
import kit_kal as K

W, H = 640, 360


def strip16(c, x, y):
    c.rect(x - 2, y - 2, x + 16 * 6 + 1, y + 7, 0)
    for k in range(16):
        c.rect(x + k * 6, y, x + k * 6 + 5, y + 5, k)


def sprite_scaled(c, rows, x, y, scale=2, flip=False, swap=None):
    wd = max(len(r) for r in rows)
    for j, r in enumerate(rows):
        r = r.ljust(wd, '.')
        r = r[::-1] if flip else r
        for i, ch in enumerate(r):
            if ch == '.':
                continue
            col = int(ch, 16)
            col = swap.get(col, col) if swap else col
            c.rect(x + i * scale, y + j * scale, x + (i + 1) * scale, y + (j + 1) * scale, col)


# ================================================================== PLATE 1: CONCEPT SHEET
def make_concept_sheet():
    c = kit.Canvas(W, H, fill=0)
    Q, R, edge = kit.hexmap(14, w=W, h=H, ox=2, oy=2)
    c.a[:] = np.where((Q + R) % 2 == 0, 0, 1).astype(np.uint8)
    c.mask(edge, 0)

    c.rect(0, 0, W, 16, 0); c.rect(0, 16, W, 17, 3)
    c.text(8, 4, 'FIG. K0  KALEDATHELA: CAST, STRATA & CHROMATIC LAW', 0xA)
    strip16(c, W - 102, 5)

    # Left Box: THE DOMINION / INQUISITION
    c.rect(10, 22, 314, 188, 0); c.bevel(10, 22, 314, 188, face=1, hi=8, lo=2)
    c.rect(12, 24, 312, 36, 0xB); c.text(16, 26, 'INQUISITION (PASTORAL SCAN)', 0xA)

    cards_l = [
        (K.PASTOR, 22, 42, 3, 'THE PASTOR', 'COLLAR 0xA',  'CROSS STAFF'),
        (K.HUNTER, 122, 58, 3, 'HUNTER',     'VISOR 0xD',   'DISH RIFLE'),
        (K.DRONE_INQ, 220, 68, 3, 'CENSER',  'CONE 0xA',    'LOCK 0xD'),
    ]
    for spr, sx, sy, sc, nm, l1, l2 in cards_l:
        bx0 = sx - 4; bx1 = bx0 + 94
        c.rect(bx0, 40, bx1, 140, 1); c.rect(bx0, 40, bx1, 41, 2)
        if nm == 'CENSER':
            cm = np.zeros((H, W), bool)
            cv2.fillPoly(cm, [np.array([(sx + 38, sy + 21), (sx + 18, 138), (sx + 58, 138)], np.int32)], 1)
            c.mix(cm, 1, 0xA, 0.42)
            c.line((sx + 38, sy + 21), (sx + 38, 138), 0xD, 1)
        sprite_scaled(c, spr, sx + 14, sy, scale=sc)
        c.text(bx0 + 4, 145, nm, 0xA)
        c.text(bx0 + 4, 158, l1, 9)
        c.text(bx0 + 4, 170, l2, 0xD if '0xD' in l2 else 9)

    # Right Box: THE COVEN (IN HIDING)
    c.rect(326, 22, 630, 188, 0); c.bevel(326, 22, 630, 188, face=1, hi=5, lo=2)
    c.rect(328, 24, 628, 36, 5); c.text(332, 26, 'THE COVEN (CONTRABAND 0x5-0x7)', 0xA)

    cards_r = [
        (K.WITCH_SIGNAL, 338, 52, 3, 'SIGNAL', 'WORM-TAP',  'GREEN 0x6'),
        (K.WITCH_BAYOU,  438, 64, 3, 'BAYOU',  'CYPRESS',   'HOLDS STILL'),
        (K.WITCH_RUNNER, 536, 70, 3, 'RUNNER', 'SHUTTERED', 'LAMP 0xF'),
    ]
    for spr, sx, sy, sc, nm, l1, l2 in cards_r:
        bx0 = sx - 4; bx1 = bx0 + 94
        c.rect(bx0, 40, bx1, 140, 1); c.rect(bx0, 40, bx1, 41, 2)
        sprite_scaled(c, spr, sx + 16, sy, scale=sc)
        if nm == 'BAYOU':
            sprite_scaled(c, SP.SPIDER, sx + 54, 48, scale=1, swap={0: 2})
            c.line((sx + 62, 41), (sx + 62, 48), 8, 1)
        c.text(bx0 + 4, 145, nm, 6)
        c.text(bx0 + 4, 158, l1, 9)
        c.text(bx0 + 4, 170, l2, 0xF if '0xF' in l2 else 6)

    # Bottom Section: FOUR STRATA + REGISTER SPECTRUM LAW (cleanly separated, zero overlap!)
    c.rect(10, 194, 630, 340, 0); c.bevel(10, 194, 630, 340, face=0, hi=3, lo=1)
    c.text(18, 200, 'FOUR STRATA IN ONE FRAME (NO LORE CAPTIONS NEEDED):', 0xA)

    strata = [
        (18,  '1. WORM BORDER', 'RIBS + 0xC RAIL'),
        (170, '2. DEAD EMPIRES', 'BROKEN ARCHES'),
        (322, '3. TEXAS GRIT',   'PUMP + BAYOU'),
        (474, '4. DOMINION',     'PYLON + FLARE'),
    ]
    for idx_s, (bx, t1, t2) in enumerate(strata):
        c.rect(bx, 212, bx + 144, 266, 1); c.rect(bx, 212, bx + 144, 213, 3)
        if idx_s == 0:
            c.line((bx + 8, 220), (bx + 136, 240), 0xC, 1); c.line((bx + 8, 226), (bx + 136, 242), 0xB, 1)
            for rr in range(3):
                cv2.ellipse(c.a, (bx + 54 + rr * 22, 258), (16, 22), -18, 190, 345, 2, 6, cv2.LINE_8)
                cv2.ellipse(c.a, (bx + 54 + rr * 22, 258), (16, 22), -18, 190, 345, 8, 2, cv2.LINE_8)
                c.disc(bx + 52 + rr * 22, 236, 2, 0xC)                          # dormant 0xC Worm conduit node on rib!
        elif idx_s == 1:
            c.rect(bx + 18, 238, bx + 28, 264, 8); c.rect(bx + 56, 234, bx + 66, 264, 8); c.rect(bx + 98, 248, bx + 110, 264, 8)
            cv2.ellipse(c.a, (bx + 42, 240), (15, 12), 0, 180, 360, 9, 3, cv2.LINE_8)
            cv2.ellipse(c.a, (bx + 82, 240), (15, 12), 0, 180, 265, 8, 3, cv2.LINE_8)
        elif idx_s == 2:
            K.draw_pumpjack_2d(c, bx + 52, 262, scale=0.76, phase=0.12, col_main=0, col_hi=9)
            K.draw_loblolly(c, bx + 118, 264, 44, seed=5, col_trunk=2, col_crown=0)
        else:
            c.poly([(bx + 26, 264), (bx + 34, 220), (bx + 54, 220), (bx + 62, 264)], 8)
            c.line((bx + 44, 224), (bx + 44, 248), 0xA, 2); c.line((bx + 36, 232), (bx + 52, 232), 0xA, 2)
            c.line((bx + 106, 264), (bx + 106, 228), 8, 2)
            c.disc(bx + 106, 223, 4, 0xE); c.disc(bx + 108, 220, 3, 0xD)
        c.rect(bx, 266, bx + 144, 286, 0)
        c.text(bx + 2, 268, t1, 0xA)
        c.text(bx + 2, 277, t2, 9)

    # Two-row Chromatic Scanner Table (all 7 register groups inside x < 622!)
    c.rect(18, 290, 622, 335, 1); c.rect(18, 290, 622, 291, 3)
    row1 = [
        (24,  [0, 1, 2, 3], '0-3 NIGHT/PINE', 9),
        (194, [4, 5, 6, 7], '4-7 HEX [HUNT]', 6),
        (366, [8, 9],       '8-9 RUIN/STEEL', 9),
        (514, [0xE],        'E FLARE',        0xE),
    ]
    row2 = [
        (24,  [0xA, 0xD],   'A+D PASTOR/LOCK', 0xA),
        (206, [0xB, 0xC],   'B+C WORM BORDER', 0xC),
        (392, [0xF],        'F SHELTER LAMP (SOLE GLOW)', 0xF),
    ]
    for rx, regs, lbl, tc in row1:
        for k_i, r_i in enumerate(regs):
            c.rect(rx + k_i * 7, 296, rx + k_i * 7 + 6, 304, r_i)
        c.text(rx + len(regs) * 7 + 5, 296, lbl, tc)
    for rx, regs, lbl, tc in row2:
        for k_i, r_i in enumerate(regs):
            c.rect(rx + k_i * 7, 316, rx + k_i * 7 + 6, 324, r_i)
        c.text(rx + len(regs) * 7 + 5, 316, lbl, tc)

    c.rect(0, H - 14, W, H, 0); c.rect(0, H - 15, W, H - 14, 2)
    c.text(8, H - 11, 'KALEDATHELA.CFG  TOXIC FLORA = VIOLET  ONLY WITCHES = GREEN', 0xA)
    strip16(c, W - 102, H - 10)
    return c.save(HERE / 'concept_sheet.png', scale=2)


# ================================================================== PLATE 2: EAST TEXAS BAYOU & REFINERY
def make_east_bayou():
    c = kit.Canvas(W, H, fill=0)
    hz = 198
    # Sky-rail descends to x=92 on far left — completely clear of drones & refinery flare!
    K.draw_sky_canvas(c, hz, primary_x=488, primary_y=118, primary_r=112,
                      worm_p0=(-10, 22), worm_vp=(92, hz - 2), transit_u=0.45, seed=51)

    # Distant refinery skyline on the horizon
    c.poly([(0, hz), (120, hz - 8), (280, hz - 4), (440, hz - 10), (W, hz - 6), (W, hz + 6), (0, hz + 6)], 1)
    towers = [(72, 42, 8), (94, 56, 10), (144, 68, 9), (164, 48, 8),
              (342, 52, 9), (382, 68, 11), (408, 44, 14), (568, 58, 9)]
    for tx, th, tw in towers:
        c.rect(tx, hz - th, tx + tw, hz, 1)
        c.rect(tx, hz - th, tx + 2, hz, 8)
        for ry in range(hz - th + 8, hz, 12):
            c.rect(tx - 1, ry, tx + tw + 1, ry + 1, 2)
    c.rect(68, hz - 24, 178, hz - 20, 1); c.rect(338, hz - 30, 426, hz - 26, 1)

    # Two roaring chemical flare stacks in clear sky (fx = 122 and fx = 366, clear of drones & cypress crowns!)
    for fx, fh in ((122, 94), (366, 92)):
        c.line((fx, hz), (fx, hz - fh), 8, 2)
        c.poly([(fx, hz - fh), (fx + 16, hz - fh - 12), (fx + 28, hz - fh - 6), (fx + 12, hz - fh + 3)], 0xD)
        c.poly([(fx, hz - fh), (fx + 11, hz - fh - 8), (fx + 18, hz - fh - 4), (fx + 7, hz - fh + 2)], 0xE)
        c.disc(fx + 3, hz - fh - 2, 3, 0xA)
        for sm in range(5):
            c.disc(fx + 22 + sm * 9, hz - fh - 10 - sm * 3, 4 + sm, 2 if sm < 2 else 1)

    # Tall broken Dead-Empires double-arch stone aqueduct standing proudly ABOVE the modern causeway!
    for px_a, ph_a in ((206, 48), (236, 52), (266, 34)):
        c.rect(px_a, hz - ph_a, px_a + 8, hz + 6, 8); c.rect(px_a, hz - ph_a, px_a + 2, hz + 6, 9)
    cv2.ellipse(c.a, (225, hz - 32), (15, 14), 0, 180, 360, 9, 4, cv2.LINE_8)
    cv2.ellipse(c.a, (255, hz - 32), (15, 14), 0, 180, 285, 8, 4, cv2.LINE_8)

    # Elevated concrete interstate overpass + Imperial Megachurch Broadcast Pylon with stark 0xA cross!
    c.rect(0, hz + 4, 345, hz + 11, 1); c.rect(0, hz + 4, 345, hz + 6, 8)
    for px in range(28, 330, 54):
        c.rect(px - 3, hz + 11, px + 3, hz + 34, 1); c.rect(px - 7, hz + 11, px + 7, hz + 14, 8)

    c.poly([(292, hz + 18), (301, hz - 78), (317, hz - 78), (326, hz + 18)], 1)
    c.line((301, hz - 78), (292, hz + 18), 8, 1)
    c.rect(307, hz - 116, 311, hz - 66, 0xA)
    c.rect(295, hz - 102, 323, hz - 98, 0xA)
    c.px(309, hz - 119, 0xD); c.px(293, hz - 100, 0xD); c.px(325, hz - 100, 0xD)

    # Stagnant toxic bayou water + broken reflections directly under the two flares and the white cross
    c.grad(hz + 16, H - 14, [2, 1, 1, 0, 0], power=0.9)
    rng = np.random.default_rng(62)
    for wy in range(hz + 20, H - 16, 3):
        for _ in range(18):
            wx = int(rng.integers(0, W - 24))
            c.rect(wx, wy, wx + int(rng.integers(6, 20)), wy + 1, 2 if wy < hz + 65 else 1)
    for rx, rcol in ((126, 0xE), (370, 0xE), (309, 0xA)):
        for wy in range(hz + 20, hz + 92, 3):
            jit = int(rng.integers(-4, 5))
            c.rect(rx + jit - 3, wy, rx + jit + 3, wy + 1, rcol if (wy % 6 == 0) else (0xD if rcol == 0xE else 9))

    # Censer-Drones in wide open sky (dx=178 and dx=262, zero overlap with sky-rail or flare pipes!)
    for dx, dy, aim_x in ((176, 104, 168), (264, 110, 256)):
        cone_mask = np.zeros((H, W), bool)
        pts = np.array([[(dx, dy + 10), (aim_x - 24, hz + 52), (aim_x + 24, hz + 52)]], np.int32)
        cv2.fillPoly(cone_mask, pts, 1)
        c.mix(cone_mask, 1, 0xA, 0.36)
        c.line((dx, dy + 10), (aim_x, hz + 52), 0xD, 1)
        sprite_scaled(c, K.DRONE_INQ, dx - 16, dy - 6, scale=2)

    # Bare-trunked East Texas loblolly pines along the bayou bank
    for px, ph, sd in ((58, 142, 2), (332, 124, 3), (434, 158, 4), (598, 168, 6)):
        K.draw_loblolly(c, px, hz + 34, ph, seed=sd, col_trunk=1, col_crown=0)

    # Foreground Bald Cypresses + Hidden Corrugated-Tin Stilt Shack
    K.draw_cypress(c, 464, hz + 92, 196, seed=11, col_trunk=1, col_moss=2)
    K.draw_cypress(c, 610, hz + 104, 214, seed=12, col_trunk=0, col_moss=1)

    sx0, sx1, deck_y = 482, 582, 282
    for pil_x in (488, 514, 546, 576):
        c.rect(pil_x - 2, deck_y, pil_x + 2, 326, 0)
        c.rect(pil_x - 2, 322, pil_x + 4, 324, 2)
    c.rect(sx0 - 6, deck_y - 3, sx1 + 6, deck_y, 2)
    c.rect(sx0 + 14, deck_y - 46, sx1 - 4, deck_y - 3, 1)
    for tx in range(sx0 + 16, sx1 - 4, 4):
        c.rect(tx, deck_y - 46, tx + 1, deck_y - 3, 2 if (tx // 4) % 2 else 0)
    c.poly([(sx0 - 8, deck_y - 45), (sx1 + 6, deck_y - 45), (sx1 - 6, deck_y - 60), (sx0 + 10, deck_y - 60)], 8)
    c.line((sx0 - 8, deck_y - 45), (sx1 + 6, deck_y - 45), 9, 1)

    # Boarded shutter window: TWO HORIZONTAL SLAT CRACKS of register F (never a cross — crosses belong to the Pastor!)
    wx0, wy0 = 536, deck_y - 34
    c.rect(wx0 - 2, wy0 - 2, wx0 + 24, wy0 + 18, 0)
    c.rect(wx0 + 1, wy0 + 3, wx0 + 21, wy0 + 6, 0xF)
    c.rect(wx0 + 1, wy0 + 10, wx0 + 21, wy0 + 13, 0xF)
    c.rect(wx0 - 1, wy0 + 6, wx0 + 23, wy0 + 10, 1)                            # heavy horizontal wooden slat between the cracks
    for wy in range(318, 336, 4):
        c.rect(wx0 + 6, wy, wx0 + 16, wy + 1, 0xF if wy == 318 else 0xE)

    # Two Coven witches on the dark porch keeping watch
    sprite_scaled(c, K.WITCH_SIGNAL, sx0 - 2, deck_y - 43, scale=2, flip=True)
    sprite_scaled(c, K.WITCH_BAYOU, sx0 + 24, deck_y - 33, scale=2, flip=True)

    # Foreground-left cypress framing edge (kept left of dx=108 drone!)
    K.draw_cypress(c, 22, hz + 122, 236, seed=15, col_trunk=0, col_moss=1)

    c.rect(10, 10, 232, 38, 0); c.rect(10, 10, 232, 12, 0xA)
    c.text(16, 15, 'SECTOR: PINEY SLOUGH 04', 0xA)
    c.text(16, 26, 'SCAN 0x5..0x7: 0 FOUND', 9)

    c.rect(0, H - 14, W, H, 0); c.rect(0, H - 15, W, H - 14, 2)
    c.text(8, H - 11, 'FIG. K1  EAST: BAYOU, REFINERY FLARES & SHUTTERED LAMP', 0xA)
    strip16(c, W - 102, H - 10)
    return c.save(HERE / 'east_bayou.png', scale=2)


# ================================================================== PLATE 3: WEST TEXAS WASTES & WORM-RIB
def make_west_wastes():
    c = kit.Canvas(W, H, fill=0)
    hz = 222
    vp_x = 304
    # Worm sky-rail descends toward x=582 in open sky right of the mesas — zero tangency with gate, HUD, or rib!
    K.draw_sky_canvas(c, hz, primary_x=130, primary_y=138, primary_r=116,
                      worm_p0=(636, 14), worm_vp=(582, hz - 2), transit_u=0.58, seed=77)

    mesas = [
        [(0, hz), (18, hz - 24), (92, hz - 24), (114, hz)],
        [(142, hz), (156, hz - 16), (228, hz - 16), (244, hz)],
        [(368, hz), (386, hz - 32), (488, hz - 32), (512, hz - 14), (548, hz - 14), (566, hz)],
    ]
    for m_pts in mesas:
        c.poly(m_pts, 1)
        c.line(m_pts[1], m_pts[2], 3, 1)

    c.grad(hz, H - 14, [2, 1, 1, 0], power=0.85)
    rng = np.random.default_rng(88)
    for dy in range(hz + 4, H - 15, 4):
        for _ in range(14):
            dx = int(rng.integers(0, W - 30))
            c.rect(dx, dy, dx + int(rng.integers(8, 28)), dy + 1, 2 if dy < hz + 36 else 1)

    # Two-lane West Texas highway converging to vp_x
    road_mask = np.zeros((H, W), bool)
    road_poly = np.array([[(vp_x - 3, hz), (vp_x + 3, hz), (242, H - 14), (114, H - 14)]], np.int32)
    cv2.fillPoly(road_mask, road_poly, 1)
    c.mask(road_mask, 0)
    c.line((vp_x - 3, hz), (114, H - 14), 8, 1)
    c.line((vp_x + 3, hz), (242, H - 14), 8, 1)

    # Dithered headlight beams on the asphalt from The Pastor's approaching convoy
    gy = hz + 34
    conv_x, conv_y = 260, gy + 10
    beam_mask = np.zeros((H, W), bool)
    cv2.fillPoly(beam_mask, [np.array([(conv_x - 5, conv_y + 2), (conv_x + 5, conv_y + 2),
                                       (228, H - 18), (138, H - 18)], np.int32)], 1)
    c.mix(beam_mask & road_mask, 0, 9, 0.42)

    for k in range(14):
        u0 = (k / 14.0) ** 1.7; u1 = ((k + 0.5) / 14.0) ** 1.7
        xa, ya = vp_x + (178 - vp_x) * u0, hz + (H - 14 - hz) * u0
        xb, yb = vp_x + (178 - vp_x) * u1, hz + (H - 14 - hz) * u1
        c.line((xa, ya), (xb, yb), 9, 1)

    for k in range(1, 10):
        u = (k / 9.5) ** 1.65
        px = int(round(vp_x - 5 - 152 * u))
        py = int(round(hz + (H - 14 - hz) * u))
        ph = max(4, int(round(68 * u)))
        c.line((px, py), (px, py - ph), 1 if u < 0.4 else 0, max(1, int(round(2 * u))))
        c.line((px - int(7 * u) - 1, py - ph + 2), (px + int(7 * u) + 1, py - ph + 2), 8, 1)

    # Checkpoint gantry + armoured Pastor truck silhouette with roof cross
    c.rect(234, gy - 30, 242, gy + 4, 8); c.rect(296, gy - 30, 304, gy + 4, 8)
    c.rect(230, gy - 34, 308, gy - 26, 1); c.rect(230, gy - 34, 308, gy - 33, 9)
    c.line((269, gy - 46), (269, gy - 28), 0xA, 2); c.line((263, gy - 40), (275, gy - 40), 0xA, 2)
    # Lead armoured Pastor vehicle + two trailing hunter trucks
    c.rect(280, gy - 9, 287, gy - 4, 1); c.px(282, gy - 5, 0xA); c.px(285, gy - 5, 0xA)
    c.rect(269, gy - 3, 279, gy + 3, 1); c.px(271, gy + 1, 0xA); c.px(277, gy + 1, 0xA)
    c.rect(conv_x - 7, conv_y - 7, conv_x + 7, conv_y + 2, 0)
    c.rect(conv_x - 5, conv_y - 11, conv_x + 5, conv_y - 7, 8)
    c.disc(conv_x - 4, conv_y, 2, 0xA); c.disc(conv_x + 4, conv_y, 2, 0xA)
    c.line((conv_x, conv_y - 17), (conv_x, conv_y - 11), 0xA, 1); c.line((conv_x - 2, conv_y - 15), (conv_x + 2, conv_y - 15), 0xA, 1)
    c.px(conv_x + 5, conv_y - 12, 0xD)

    # Colossal segmented Worm-Rib rising from an eroded caliche mound + dormant 0xC nodes linking it to the sky-rail!
    c.poly([(366, 326), (416, 286), (546, 284), (602, 328)], 1)
    for seg in range(9):
        a0 = 198 + seg * 14; a1 = a0 + 10
        cv2.ellipse(c.a, (476, 298), (94, 118), -10, a0, a1, 2, 15, cv2.LINE_8)
        cv2.ellipse(c.a, (476, 298), (94, 118), -10, a0, a1, 8, 3, cv2.LINE_8)
        ar = math.radians(a0 + 5)
        rx0 = int(476 + 86 * math.cos(ar)); ry0 = int(298 + 108 * math.sin(ar))
        rx1 = int(476 + 102 * math.cos(ar)); ry1 = int(298 + 126 * math.sin(ar))
        if ry1 < 300:
            c.line((rx0, ry0), (rx1, ry1), 9, 2)
            c.disc((rx0 + rx1) // 2, (ry0 + ry1) // 2, 2, 0xC if seg % 2 == 0 else 0xB)

    for ax, ah in ((392, 34), (422, 38), (558, 28)):
        c.rect(ax, 292 - ah, ax + 8, 292, 8); c.rect(ax, 292 - ah, ax + 2, 292, 9)
    cv2.ellipse(c.a, (411, 260), (15, 13), 0, 180, 315, 8, 4, cv2.LINE_8)

    # Foreground Left: Lufkin Pumpjack + Rusted Tank Battery + desert scrub (no ambiguous white pins)
    c.rect(14, 264, 38, 292, 1); c.rect(14, 264, 20, 292, 8); c.rect(42, 270, 62, 292, 1)
    K.draw_pumpjack_2d(c, 88, 304, scale=1.45, phase=0.08, col_main=0, col_hi=8)

    for yx, yy_b in ((18, 332), (96, 336), (346, 322), (614, 330)):
        for blade in (-5, -2, 0, 3, 6):
            c.line((yx, yy_b), (yx + blade * 2, yy_b - 12 + abs(blade)), 0, 1)
        c.line((yx, yy_b - 10), (yx, yy_b - 20), 2, 1)

    # Sunken Storm-Cellar wired directly to the grounded left foot of the Worm-Rib `(384, 286)` via a Worm-tap conduit!
    cx0, cy0 = 476, 306
    c.line((384, 286), (426, 304), 8, 2); c.line((426, 304), (cx0 - 18, cy0 + 4), 8, 2)
    c.line((384, 286), (426, 304), 0xC, 1); c.line((426, 304), (cx0 - 18, cy0 + 4), 0xB, 1)
    c.poly([(cx0 - 28, cy0 + 20), (cx0 + 42, cy0 + 20), (cx0 + 32, cy0 - 2), (cx0 - 18, cy0 - 2)], 0)
    c.line((cx0 - 28, cy0 + 20), (cx0 + 42, cy0 + 20), 8, 2)
    c.poly([(cx0 - 10, cy0 + 16), (cx0 + 26, cy0 + 16), (cx0 + 22, cy0 + 8), (cx0 - 6, cy0 + 8)], 0xF)
    c.poly([(cx0 - 14, cy0 + 7), (cx0 + 26, cy0 + 1), (cx0 + 22, cy0 - 5), (cx0 - 16, cy0 + 1)], 8)
    c.line((cx0 - 14, cy0 + 7), (cx0 + 26, cy0 + 1), 9, 1)
    sprite_scaled(c, K.WITCH_SIGNAL[:11], cx0 - 2, cy0 - 12, scale=2, flip=True)

    msg = 'CONVOY: PASTOR + 2 HUNTERS (1.8 MI)'
    c.rect(184, hz - 58, 184 + len(msg) * 8 + 8, hz - 45, 0)
    c.rect(184, hz - 59, 184 + len(msg) * 8 + 8, hz - 58, 0xD)
    c.line((conv_x, conv_y - 17), (238, hz - 45), 0xD, 1)
    c.text(188, hz - 55, msg, 0xA)

    c.rect(0, H - 14, W, H, 0); c.rect(0, H - 15, W, H - 14, 2)
    c.text(8, H - 11, 'FIG. K2  WEST: CAPROCK, PUMPJACK, WORM-RIB & CELLAR', 0xA)
    strip16(c, W - 102, H - 10)
    return c.save(HERE / 'west_wastes.png', scale=2)


if __name__ == '__main__':
    p0 = make_concept_sheet()
    p1 = make_east_bayou()
    p2 = make_west_wastes()
    print('wrote updated plates:', p0, p1, p2)
