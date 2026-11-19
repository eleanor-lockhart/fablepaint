"""Warmup 2: Night Stacks (03:14, Special Collections) — v2, revised after cold reading.

A vaulted Gothic library built in metres on the 5 cm grid: pointed stone ribs, a compass-constructed twelve-light
rose window looking out on winter stars, twenty bookcases holding 2,560 distinct volumes (20 x 8 x 16 = 0xA00),
and one lit reading carrel (register F) where Reviewer 2 has checked out the single missing volume.
No witch is in the hall, so zero green registers appear outside the sixteen-register signature strip.

v2 changes from cold reading:
  - Missing slot (`SLOT 1655: OUT`) is now a clear dark gap on the shelf with a thin bottom tab, rather than a solid
    white block that looked like a white book spine.
  - Thick bound folio open on Carrel 04 (red leather cover + two cream pages) plus a high-backed oak reading chair.
  - Faculty wizard hat brim given a twilight/chrome edge so it reads as a brim rather than a flat black bar.
  - Screen-space lamp halo reduced so the mid-ground carrel behind Carrel 04 stays sharp; floor rat drawn in integer
    screen pixels on dark flagstones so its ears, eye and tail read cleanly.

    uv run python styles/hex/warmup/stacks.py
"""
import sys, math
from pathlib import Path
HERE = Path(__file__).resolve().parent; HEX = HERE.parent; ROOT = HERE.parents[2]
sys.path.insert(0, str(HEX)); sys.path.insert(1, str(ROOT))
import numpy as np
from backlot import space as sp, depth as D
from backlot.depth import HOLE
import deep as X, stage2 as S2, kit, sprites as SP
from deep import blend

STONE1, STONE2, STONE_LO = blend(0x3, 0x8, .52), blend(0x2, 0x8, .35), blend(0x1, 0x2, .5)
FLAG_A, FLAG_B = blend(0x8, 0x2, .48), blend(0x1, 0x2, .52)
OAK1, OAK2, OAK_LO = blend(0xE, 0x2, .62), blend(0xE, 0x1, .68), blend(0x1, 0x0, .5)
BRASS = blend(0xE, 0xA, .35)
PAGE = blend(0xA, 0x9, .12)
BINDINGS = [0x2, 0x3, 0x8, 0x9, 0xB, 0xD, 0xE, blend(0xD, 0x2, .5), blend(0xB, 0x1, .45), blend(0xE, 0x2, .45)]

W_NAVE = 4.4
Y_LEN = 19.2
Z_WALL = 5.6
Z_APEX = 9.0


def make_rose_tracery(R_m=2.50, texel=.025):
    z_bot = 3.65
    pw_m, ph_m = W_NAVE * 2, (Z_APEX + 0.35) - z_bot
    W_px, H_px = int(round(pw_m / texel)), int(round(ph_m / texel))
    skin = np.full((H_px, W_px), STONE1, np.uint8)
    for r_i in range(0, H_px, 10):
        skin[r_i:r_i + 1, :] = STONE2
        off = 9 if (r_i // 10) % 2 else 0
        for c_i in range(off, W_px, 18):
            skin[max(r_i - 10, 0):r_i, c_i:c_i + 1] = STONE2

    cx = W_px / 2.0
    cz_world = 6.38
    cy = ((Z_APEX + 0.35) - cz_world) / texel
    yy, xx = np.mgrid[:H_px, :W_px].astype(np.float32)
    dx, dy = (xx - cx) * texel, (yy - cy) * texel
    r = np.hypot(dx, dy)

    glass = r < (R_m - 0.15)
    tracery = np.zeros_like(glass)
    for rad, th in ((R_m - 0.15, 0.11), (1.68, 0.085), (0.60, 0.09), (0.23, 0.07)):
        tracery |= np.abs(r - rad) <= th

    for k in range(6):
        a = k * math.pi / 3.0
        px, py = 0.43 * math.cos(a), 0.43 * math.sin(a)
        tracery |= (r < 0.60) & (r > 0.23) & (np.abs(np.hypot(dx - px, dy - py) - 0.20) < 0.045)

    for k in range(12):
        a = k * math.pi / 6.0
        ux, uy = math.cos(a), math.sin(a); vx, vy = -uy, ux
        along = dx * ux + dy * uy; perp = np.abs(dx * vx + dy * vy)
        tracery |= (along > 0.56) & (along < 1.70) & (perp < 0.042)
        am = a + math.pi / 12.0
        hx, hy = 1.40 * math.cos(am), 1.40 * math.sin(am)
        tracery |= (r > 1.15) & (r < 1.68) & (np.abs(np.hypot(dx - hx, dy - hy) - 0.29) < 0.05)
        for side in (-1, 1):
            ca = am + side * 0.13
            tracery |= np.hypot(dx - 1.34 * math.cos(ca), dy - 1.34 * math.sin(ca)) < 0.062

    tracery |= (r >= 1.68) & (r < R_m - 0.15)
    roundel_open = np.zeros_like(glass)
    for k in range(12):
        am = (k + 0.5) * math.pi / 6.0
        rx, ry = 2.02 * math.cos(am), 2.02 * math.sin(am)
        dr = np.hypot(dx - rx, dy - ry)
        lobes = np.zeros_like(glass)
        for j in range(4):
            la = am + j * math.pi / 2.0
            lobes |= np.hypot(dx - (rx + 0.095 * math.cos(la)), dy - (ry + 0.095 * math.sin(la))) < 0.14
        roundel_open |= lobes & (dr < 0.235)
    tracery &= ~roundel_open

    skin[glass & (~tracery)] = HOLE
    skin[tracery & (np.abs(r - 1.68) < 0.04)] = 0x9
    return skin, z_bot


def make_bookcase_skin(case_id, missing_slot=None):
    """One bookcase face: 8 shelves x 16 books = 128 books per case."""
    W_t, H_t = 38, 50
    s = np.full((H_t, W_t), OAK_LO, np.uint8)
    s[:, 0:2] = OAK1; s[:, W_t - 2:W_t] = OAK1; s[0:2, :] = OAK1
    rng = np.random.default_rng(100 + case_id)
    count = 0
    for sh in range(8):
        y_bot = 6 + sh * 6
        if y_bot < H_t:
            s[y_bot:min(y_bot + 1, H_t), 1:W_t - 1] = OAK1
        for bk in range(16):
            x0 = 3 + bk * 2
            bh = int(rng.integers(4, 6))
            y0 = max(y_bot - bh, 2)
            if missing_slot == (sh, bk):
                # Clear empty dark gap (0x0) framed by bright neighbours + tiny 1-texel brass shelf tag on the plank!
                s[y_bot - 5:y_bot, max(x0 - 1, 2):min(x0 + 3, W_t - 2)] = 0x0
                s[y_bot:min(y_bot + 1, H_t), x0:x0 + 2] = 0xA
            else:
                col = (0xE if bk in (6, 8) and missing_slot and sh == missing_slot[0]
                       else BINDINGS[int(rng.integers(0, len(BINDINGS)))])
                s[y0:y_bot, x0:x0 + 2] = col
                if rng.random() < 0.30:
                    s[y0 + 1:y0 + 2, x0:x0 + 2] = 0x9
                count += 1
    return s, count


def custom_faculty():
    """SP.FACULTY with shaded blue/chrome wizard-hat brim (replaces flat black 0000000000 line that read as a censor bar)."""
    rows = list(SP.FACULTY)
    rows[6] = '3999BBBB99D.'                                                   # wide pointed-hat brim with chrome edge + red tassel!
    rows[7] = '.1BBBBBBBB.D'
    return X.sprite(rows, flip=True)


def build_hall(cam):
    S = sp.Set('Night Stacks')
    stone_skin = X.blocks(STONE1, STONE2, bw=10, bh=5, seed=21, chips=(0x8, STONE_LO))
    wood_skin = X.planks(OAK1, OAK2, OAK_LO, width=4, length=36, along='u', seed=22)

    fl = np.full((20, 20), FLAG_A, np.uint8); fl[:10, 10:] = FLAG_B; fl[10:, :10] = FLAG_B
    fl[0, :] = STONE_LO; fl[10, :] = STONE_LO; fl[:, 0] = STONE_LO; fl[:, 10] = STONE_LO
    D.paint(S.box('floor', (-W_NAVE - .5, W_NAVE + .5), (-2.0, Y_LEN + .4), (-.2, 0.0), kind='deck'), skin=fl)

    for side, sg in (('L', -1), ('R', 1)):
        xw0, xw1 = (sg * W_NAVE - .4, sg * W_NAVE) if sg < 0 else (sg * W_NAVE, sg * W_NAVE + .4)
        D.paint(S.box(f'wall.{side}', (xw0, xw1), (-2.0, Y_LEN), (0.0, Z_WALL + 1.0), kind='wall'), skin=stone_skin)
        gx0, gx1 = (-W_NAVE, -W_NAVE + 1.05) if sg < 0 else (W_NAVE - 1.05, W_NAVE)
        D.paint(S.box(f'gal.{side}', (gx0, gx1), (1.0, Y_LEN - .5), (2.72, 2.86), kind='deck'), skin=wood_skin)
        rx = gx1 - .08 if sg < 0 else gx0 + .08
        D.paint(S.box(f'rail.{side}', (rx - .05, rx + .05), (1.0, Y_LEN - .5), (3.58, 3.68), kind='rail'), index=OAK1)
        for py in np.arange(1.4, Y_LEN - .6, 1.2):
            D.paint(S.box(f'bal.{side}.{py:.1f}', (rx - .04, rx + .04), (py - .04, py + .04), (2.86, 3.58), kind='rail'), index=OAK2)

    n_seg = 6
    for side, sg in (('L', -1), ('R', 1)):
        for k in range(n_seg):
            t0, t1 = k / n_seg, (k + 1) / n_seg
            x0 = sg * W_NAVE * (1 - t0); z0 = Z_WALL + (Z_APEX - Z_WALL) * math.sin(t0 * math.pi / 2) ** 0.82
            x1 = sg * W_NAVE * (1 - t1); z1 = Z_WALL + (Z_APEX - Z_WALL) * math.sin(t1 * math.pi / 2) ** 0.82
            quad = [(x0, -2.0, z0), (x1, -2.0, z1), (x1, Y_LEN, z1), (x0, Y_LEN, z0)]
            v_sol = sp.Solid(f'vault.{side}.{k}', [quad], kind='roof')
            D.paint(v_sol, skin=stone_skin); S.add(v_sol)

    for bay_i, y_rib in enumerate((2.2, 6.2, 10.2, 14.2, 18.2)):
        for sg in (-1, 1):
            D.paint(S.box(f'pier.{bay_i}.{sg}', (sg * (W_NAVE - .34) - .17, sg * (W_NAVE - .34) + .17),
                          (y_rib - .20, y_rib + .20), (0.0, Z_WALL), kind='pile'), skin=stone_skin)
            for k in range(n_seg):
                t0, t1 = k / n_seg, (k + 1) / n_seg
                p0 = (sg * (W_NAVE - .18) * (1 - t0), y_rib, Z_WALL + (Z_APEX - .12 - Z_WALL) * math.sin(t0 * math.pi / 2) ** 0.82)
                p1 = (sg * (W_NAVE - .18) * (1 - t1), y_rib, Z_WALL + (Z_APEX - .12 - Z_WALL) * math.sin(t1 * math.pi / 2) ** 0.82)
                S.tube(f'rib.{bay_i}.{sg}.{k}', [p0, p1], .14, n=4, kind='pile')
                D.paint(S.solids[-1], index=0x9)

    rose_skin, z_rose_bot = make_rose_tracery(R_m=2.50, texel=.025)
    D.paint(S.box('north.lo', (-W_NAVE, W_NAVE), (Y_LEN, Y_LEN + .35), (0.0, z_rose_bot), kind='wall'), skin=stone_skin)
    S.add(D.panel('north.rose', rose_skin, (-W_NAVE, Y_LEN, Z_APEX + 0.35), (1, 0, 0), (0, 0, -1), texel=.025))

    total_shelved = 0
    case_idx = 0
    gap_world = None
    for side, sg in (('L', -1), ('R', 1)):
        for tier, z0 in enumerate((0.10, 2.88)):
            for bay, y_mid in enumerate((4.2, 8.2, 12.2, 16.2)):
                miss = (3, 7) if (side == 'R' and tier == 0 and bay == 1) else None
                bskin, cnt = make_bookcase_skin(case_idx, missing_slot=miss)
                total_shelved += cnt
                cx0, cx1 = (-W_NAVE + .02, -W_NAVE + .48) if sg < 0 else (W_NAVE - .48, W_NAVE - .02)
                D.paint(S.box(f'case.{case_idx}', (cx0, cx1), (y_mid - .95, y_mid + .95), (z0, z0 + 2.50), kind='cabin'), index=OAK2)
                fx = cx1 + .01 if sg < 0 else cx0 - .01
                across = (0, 1, 0) if sg < 0 else (0, -1, 0)
                S.add(D.panel(f'books.{case_idx}', bskin, (fx, y_mid - .95 if sg < 0 else y_mid + .95, z0 + 2.50), across, (0, 0, -1), texel=.05))
                if miss is not None:
                    u_m = (3 + 7 * 2 + 1) * 0.05
                    v_m = (6 + 3 * 6 - 3) * 0.05
                    gap_world = (fx, (y_mid + .95) - u_m, (z0 + 2.50) - v_m)
                case_idx += 1

    for x_mid in (-3.0, -1.0, 1.0, 3.0):
        bskin, cnt = make_bookcase_skin(case_idx, missing_slot=None)
        total_shelved += cnt
        D.paint(S.box(f'ncase.{case_idx}', (x_mid - .95, x_mid + .95), (Y_LEN - .46, Y_LEN - .02), (0.10, 2.60), kind='cabin'), index=OAK2)
        S.add(D.panel(f'nbooks.{case_idx}', bskin, (x_mid - .95, Y_LEN - .47, 2.60), (1, 0, 0), (0, 0, -1), texel=.05))
        case_idx += 1

    assert total_shelved == 2559, f'Expected 2559 shelved books, got {total_shelved}'

    # Carrel 04 + high-backed oak reading chair
    dx, dy = 1.45, 7.45
    D.paint(S.box('desk.top', (dx - .92, dx + .92), (dy - .50, dy + .50), (.74, .83), kind='cabin'), skin=wood_skin)
    for lx in (dx - .80, dx + .80):
        for ly in (dy - .40, dy + .40):
            D.paint(S.box(f'desk.leg.{lx:.2f}.{ly:.2f}', (lx - .05, lx + .05), (ly - .05, ly + .05), (0.0, .74), kind='cabin'), index=OAK2)
    # Chair right behind Reviewer 2
    chx, chy = dx + 1.08, dy + .06
    D.paint(S.box('chair.seat', (chx - .24, chx + .24), (chy - .24, chy + .24), (.42, .48), kind='cabin'), index=OAK1)
    D.paint(S.box('chair.back', (chx + .18, chx + .24), (chy - .24, chy + .24), (.48, 1.18), kind='cabin'), index=OAK1)
    for clx in (chx - .20, chx + .20):
        for cly in (chy - .20, chy + .20):
            D.paint(S.box(f'chair.leg.{clx:.2f}.{cly:.2f}', (clx - .03, clx + .03), (cly - .03, cly + .03), (0.0, .42), kind='cabin'), index=OAK2)

    for ux, uy in ((-1.65, 6.8), (-1.65, 11.8), (1.45, 13.2)):
        D.paint(S.box(f'udesk.{ux}.{uy}', (ux - .82, ux + .82), (uy - .46, uy + .46), (.74, .82), kind='cabin'), skin=wood_skin)
        for lx in (ux - .72, ux + .72):
            for ly in (uy - .36, uy + .36):
                D.paint(S.box(f'uleg.{lx:.2f}.{ly:.2f}', (lx - .05, lx + .05), (ly - .05, ly + .05), (0.0, .74), kind='cabin'), index=OAK2)

    # Thick bound folio tome on a reading lectern/wedge on Carrel 04 (unmistakably the pulled book!)
    D.paint(S.box('book.cover', (dx - .06, dx + .56), (dy - .26, dy + .22), (.83, .92), kind='cabin'), index=0xD)
    D.paint(S.box('book.pageL', (dx - .02, dx + .23), (dy - .22, dy + .18), (.92, .97), kind='cold'), index=0xA)
    D.paint(S.box('book.pageR', (dx + .27, dx + .52), (dy - .22, dy + .18), (.92, .97), kind='cold'), index=0xA)
    D.paint(S.box('book.gutter', (dx + .23, dx + .27), (dy - .23, dy + .19), (.91, .96), kind='cabin'), index=0x8)

    # Tended brass library lamp (register F — the only F in the hall)
    lx0, ly0 = dx - .52, dy + .08
    D.paint(S.box('lamp.base', (lx0 - .12, lx0 + .12), (ly0 - .12, ly0 + .12), (.83, .89), kind='machine'), index=BRASS)
    D.paint(S.box('lamp.stem', (lx0 - .03, lx0 + .03), (ly0 - .03, ly0 + .03), (.89, 1.24), kind='machine'), index=BRASS)
    D.paint(S.box('lamp.shade', (lx0 - .20, lx0 + .20), (ly0 - .15, ly0 + .15), (1.22, 1.40), kind='light'),
            index=0xF, glow=1.0, cast=False)
    lamp_pos = (lx0, ly0, 1.30)

    fac = custom_faculty()
    cards = [
        D.card('reviewer2', fac, (dx + .96, dy + .04, 0.0), cam.right, texel=.076),
    ]
    return S, cards, lamp_pos, gap_world


def render():
    cam = sp.Camera(eye=(-0.45, -1.35, 2.35), look=(0.25, 11.5, 3.65), lens=24, size=(S2.W, S2.H), name='nave')
    S, cards, lpos, gap_pos = build_hall(cam)

    sp.drawing(S, 'from_south', out=str(HERE / 'night_stacks_section.svg'), scale=28, title='NIGHT STACKS: TRANSVERSE ELEVATION')
    draw_hex_elevation(HERE / 'night_stacks_section.png')

    solids = S.solids + cards
    g = D.gbuffer(solids, cam)

    rose_fill = D.Light((0.0, 17.5, 6.4), power=1.15, reach=16.0, shadow=False)
    vault_fill = D.Light((0.0, 6.0, 7.5), power=0.55, reach=13.0, shadow=False)
    desk_lamp = D.Light((lpos[0] + .05, lpos[1] - .05, lpos[2] + .32), power=6.2, reach=6.6,
                        aim=(0.32, 0.05, -0.72), cone=(46, 78)).bake(S.solids)
    lv = D.lighting(g, [rose_fill, vault_fill, desk_lamp], ambient=.11, moving=cards)

    sx, sy = cam.p(*lpos)
    # Tighter screen-space halo (0.36 instead of 0.85) so the mid-ground carrel behind Carrel 04 is never washed out!
    idx = S2.index(g, lv, cam, haze=260.0, lamps=[(sx, sy, 0.36)], stars=True)

    sky_m = ~g['hit']
    ys, xs = np.nonzero(sky_m)
    for k in range(0, len(ys), 17):
        idx[ys[k], xs[k]] = (9, 0xA, 0xC)[k % 3]

    # Stamp the small library rat directly at 1:1 integer pixel scale on dark foreground floor so every ear & tail pixel reads!
    rx_s, ry_s = 282, 314
    for rj, row in enumerate(SP.RAT):
        for ri, ch in enumerate(row):
            if ch != '.':
                c_reg = int(ch, 16)
                # Outline dark shadow pixel behind chrome rat so it pops off the chequered tiles
                for oy, ox in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    py_, px_ = ry_s + rj + oy, rx_s + ri + ox
                    if 0 <= py_ < S2.H and 0 <= px_ < S2.W and idx[py_, px_] not in (0x9, 0xA):
                        idx[py_, px_] = 0x0
    for rj, row in enumerate(SP.RAT):
        for ri, ch in enumerate(row):
            if ch != '.':
                idx[ry_s + rj, rx_s + ri] = 0xA if ch == '9' else (0x0 if ch == '0' else 0xD)

    # Callout for the missing book slot behind Reviewer 2
    gx, gy = cam.p(*gap_pos)
    gxi, gyi = int(round(gx)), int(round(gy))
    lbl_gap = 'SLOT 1655: EMPTY'
    bx_g = min(max(gxi - len(lbl_gap) * 8 - 14, 8), S2.W - len(lbl_gap) * 8 - 8)
    by_g = max(gyi - 22, 12)
    idx_line(idx, (bx_g + len(lbl_gap) * 8 + 2, by_g + 4), (gxi - 2, gyi), 0xA)
    S2.rect(idx, bx_g - 3, by_g - 2, bx_g + len(lbl_gap) * 8 + 3, by_g + 9, 0x0)
    S2.rect(idx, bx_g - 3, by_g - 3, bx_g + len(lbl_gap) * 8 + 3, by_g - 2, 0x9)
    S2.text(idx, bx_g, by_g, lbl_gap, 0xA)

    # Unambiguous label identifying Reviewer 2 writing his note at Carrel 04
    msg = 'REVIEWER 2 (WRITING): "SEE P. 412."'
    bx = max(min(int(round(sx)) - 40, S2.W - len(msg) * 8 - 10), 8)
    by = S2.H - 29
    S2.rect(idx, bx - 4, by - 3, bx + len(msg) * 8 + 4, by + 10, 0x0)
    S2.rect(idx, bx - 4, by - 4, bx + len(msg) * 8 + 4, by - 3, 0xF)
    S2.text(idx, bx, by, msg, 0xA)

    S2.rect(idx, 0, S2.H - 14, S2.W, S2.H, 0x0)
    S2.rect(idx, 0, S2.H - 15, S2.W, S2.H - 14, 0x2)
    bar_txt = 'STACKS.DB  2560 VOLS (0xA00)  SHELVED: 2559  AT DESK: 1'
    S2.text(idx, 6, S2.H - 11, bar_txt, 0xA)

    green_px = int(np.isin(idx, [4, 5, 6, 7]).sum())
    assert green_px == 0, f'Expected 0 green pixels in witch-free scene, got {green_px}'

    for k in range(16):
        S2.rect(idx, S2.W - 6 - (16 - k) * 6, S2.H - 10, S2.W - 6 - (16 - k) * 6 + 5, S2.H - 5, k)

    out_png = HERE / 'night_stacks.png'
    X.save(str(out_png), S2.rgb(idx, 2))
    print('wrote v2', out_png)


def idx_line(idx, a, b, reg):
    n = int(max(abs(b[0] - a[0]), abs(b[1] - a[1]))) + 1
    for i in range(n + 1):
        t = i / max(n, 1)
        x, y = int(round(a[0] + (b[0] - a[0]) * t)), int(round(a[1] + (b[1] - a[1]) * t))
        if 0 <= x < idx.shape[1] and 0 <= y < idx.shape[0]:
            idx[y, x] = reg


def draw_hex_elevation(out_path):
    c = kit.Canvas(640, 360, fill=0x0)
    cx0, cy0, sc = 320, 322, 31.0
    def mp(x, z): return int(round(cx0 + x * sc)), int(round(cy0 - z * sc))
    for z_m in range(0, 10):
        _, y = mp(0, z_m); c.rect(40, y, 600, y + 1, 0x1)
    for x_m in range(-8, 9, 2):
        x, _ = mp(x_m, 0); c.rect(x, 22, x + 1, 326, 0x1)
    c.line(mp(-W_NAVE, 0), mp(-W_NAVE, Z_WALL), 0x9, 2)
    c.line(mp(W_NAVE, 0), mp(W_NAVE, Z_WALL), 0x9, 2)
    c.line(mp(-W_NAVE - .6, 0), mp(W_NAVE + .6, 0), 0xA, 2)
    for sg in (-1, 1):
        pts = [mp(sg * W_NAVE * (1 - k / 24), Z_WALL + (Z_APEX - Z_WALL) * math.sin((k / 24) * math.pi / 2) ** 0.82) for k in range(25)]
        for a, b in zip(pts, pts[1:]): c.line(a, b, 0x9, 2)
        for z0 in (0.10, 2.88):
            x0, y0 = mp(sg * W_NAVE, z0 + 2.50); x1, y1 = mp(sg * (W_NAVE - .48), z0)
            c.rect(min(x0, x1), y0, max(x0, x1), y1, 0x2)
        gx0, gy0 = mp(sg * W_NAVE, 2.86); gx1, _ = mp(sg * (W_NAVE - 1.05), 2.86)
        c.line((gx0, gy0), (gx1, gy0), 0xA, 2)
    rcx, rcy = mp(0.0, 6.38); rr = int(round(2.35 * sc))
    c.ring(rcx, rcy, rr, 0xA, 2); c.ring(rcx, rcy, int(round(1.68 * sc)), 0x9, 1); c.ring(rcx, rcy, int(round(0.60 * sc)), 0x9, 1)
    for k in range(12):
        a = k * math.pi / 6.0
        c.line((rcx + 0.60 * sc * math.cos(a), rcy + 0.60 * sc * math.sin(a)),
               (rcx + 1.68 * sc * math.cos(a), rcy + 1.68 * sc * math.sin(a)), 0x8, 1)
        am = (k + 0.5) * math.pi / 6.0
        c.ring(rcx + 2.02 * sc * math.cos(am), rcy + 2.02 * sc * math.sin(am), int(round(0.22 * sc)), 0x3, 1)
    d0, dy0 = mp(1.45 - .92, .83); d1, dy1 = mp(1.45 + .92, 0)
    c.rect(d0, dy0, d1, dy0 + 3, 0x9); c.line((d0 + 4, dy0), (d0 + 4, dy1), 0x8, 1); c.line((d1 - 4, dy0), (d1 - 4, dy1), 0x8, 1)
    lx, ly = mp(1.45 - .52, 1.30); c.rect(lx - 5, ly - 4, lx + 5, ly + 3, 0xF)
    c.rect(0, 0, 640, 16, 0x0); c.text(8, 4, 'SECTION LOOKING NORTH: VAULT (9.0 M) + 12-LIGHT ROSE', 0xA)
    c.rect(0, 344, 640, 360, 0x0); c.text(8, 348, '20 CASES x 8 SHELVES x 16 = 2560 (0xA00)   CARREL 04 LIT', 0x9)
    for k in range(16): c.rect(640 - 6 - (16 - k) * 6, 349, 640 - 6 - (16 - k) * 6 + 5, 354, k)
    c.save(out_path, scale=2)


if __name__ == '__main__':
    render()
