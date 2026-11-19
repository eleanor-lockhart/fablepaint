"""Warmup 4: Demon.exe (v2, revised after cold reading) — Maxwell's Demon on a turn-of-the-millennium desktop.

28.0 seconds, 672 frames at 24 fps, hung on the 14-bar score built by `demon_music.py`.
v2 changes from cold reading & self-check:
  - Continuous simulation clock `sim_t(t)` pauses all molecules during 20.0..22.0 s (`PAUSED BY SECOND_LAW.SYS` is now
    literal on screen) and resumes smoothly at 22.0 s when `WITCH.EXE` overrides it.
  - Right-chamber vertical bounce floor sits just above the shelter roof so molecules never pass across the lit window.
  - `18.0..20.0 s` banner explicitly notes `(LOG FULL: 16/16)`, explaining why the gate holds before the system audit.
  - `SECOND_LAW.SYS` offers two distinct bad options (`FORGET` vs `STOP`) and keeps its disabled grey buttons at 22.0 s
    so its window height never jumps; both dialogs stay strictly left of the central hatch (`x + w <= 408`).

    uv run python styles/hex/warmup/demon.py test     render key frames to inspect first
    uv run python styles/hex/warmup/demon.py          render all 672 frames, mux audio, check sync/pops/travel
"""
import sys, math, subprocess
from multiprocessing import Pool
from pathlib import Path
HERE = Path(__file__).resolve().parent; HEX = HERE.parent; ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE)); sys.path.insert(1, str(HEX)); sys.path.insert(2, str(ROOT)); sys.path.insert(3, str(HEX / 'uptime'))
import numpy as np
import cv2
import kit, sprites as SP, ui as U
from demon_music import SORT_TIMES, EXTRA_SORTS, OUT as MOUT

FPS, SECONDS = 24, 28
NF = FPS * SECONDS
W, H = 1280, 720
OUT = MOUT
FRAMES = OUT / 'frames'

WIN_X, WIN_Y, WIN_W, WIN_H = 22, 18, 848, 648
CX, CY, CW, CH = WIN_X + 4, WIN_Y + 28, WIN_W - 8, WIN_H - 32
WALL_X = CX + CW // 2                                                          # 446
WALL_HW = 15
L_X0, L_X1 = CX + 12, WALL_X - WALL_HW                                         # [38, 431]
R_X0, R_X1 = WALL_X + WALL_HW, CX + CW - 12                                    # [461, 854]
BOX_Y0, BOX_Y1 = CY + 78, CY + CH - 14                                         # [124, 648]
GATE_Y0, GATE_Y1 = 338, 426
RAD = 7

COT_X0, COT_Y0, COT_X1, COT_Y1 = R_X1 - 168, BOX_Y1 - 118, R_X1 - 14, BOX_Y1
R_BOUNCE_Y1 = COT_Y0 - 10                                                      # molecules stay clear above the shelter!


def sim_t(t):
    """Continuous physical clock: freezes during [20.0, 22.0] while SECOND_LAW.SYS pauses CHAMBER.EXE."""
    if t <= 20.0: return t
    if t < 22.0: return 20.0
    return t - 2.0


ALL_SORTS = [(t, sim_t(t), 'H' if i % 2 == 0 else 'C', i) for i, t in enumerate(SORT_TIMES)] + [
    (EXTRA_SORTS[0], sim_t(EXTRA_SORTS[0]), 'H', 16),
    (EXTRA_SORTS[1], sim_t(EXTRA_SORTS[1]), 'C', 17),
    (EXTRA_SORTS[2], sim_t(EXTRA_SORTS[2]), 'H', 18),
]
OPEN_DUR = 0.30


def gate_open_at(t):
    for ts, _, kind, idx in ALL_SORTS:
        if 0.0 <= (t - ts) < OPEN_DUR:
            return True, kind, idx, 1.0 - (t - ts) / OPEN_DUR
    return False, None, -1, 0.0


def gate_open_sim(st):
    for _, st_s, kind, idx in ALL_SORTS:
        if -0.05 <= (st - st_s) < OPEN_DUR + 0.05:
            return True
    return False


def _fold(u, a, b):
    span = b - a
    m = (u - a) % (2.0 * span)
    return a + m if m <= span else b - (m - span)


def _build_molecules():
    rng = np.random.default_rng(1867)
    mols = []

    def valid_crossing(kind, st_cross):
        spd = 255.0 if kind == 'H' else 112.0
        yb_pre = (BOX_Y1 - RAD) if kind == 'H' else (R_BOUNCE_Y1 - RAD)
        yb_post = (R_BOUNCE_Y1 - RAD) if kind == 'H' else (BOX_Y1 - RAD)
        for _ in range(800):
            ang = float(rng.uniform(0.28, 0.76)) * (1 if rng.random() < .5 else -1)
            vx = spd * math.cos(ang); vy = spd * math.sin(ang)
            yc = float(rng.uniform(GATE_Y0 + 16, GATE_Y1 - 16))
            w_pre = (L_X1 - RAD) - (L_X0 + RAD) if kind == 'H' else (R_X1 - RAD) - (R_X0 + RAD)
            w_post = (R_X1 - RAD) - (R_X0 + RAD) if kind == 'H' else (L_X1 - RAD) - (L_X0 + RAD)
            ok = True
            for m in range(1, 30):
                tp = st_cross - m * (2.0 * w_pre / vx)
                if tp >= 0:
                    yp = _fold(yc + vy * (tp - st_cross), BOX_Y0 + RAD, yb_pre)
                    if gate_open_sim(tp) and (GATE_Y0 - 8 <= yp <= GATE_Y1 + 8):
                        ok = False; break
                ta = st_cross + m * (2.0 * w_post / vx)
                if ta <= 26.0:
                    ya = _fold(yc + vy * (ta - st_cross), BOX_Y0 + RAD, yb_post)
                    if gate_open_sim(ta) and (GATE_Y0 - 8 <= ya <= GATE_Y1 + 8):
                        ok = False; break
            if ok:
                return dict(kind=kind, cross=st_cross, vx=vx, vy=vy, yc=yc)
        raise RuntimeError('Could not place crossing trajectory')

    for _, st_s, kind, _ in ALL_SORTS:
        mols.append(valid_crossing(kind, st_s))

    def valid_resident(kind, side):
        spd = 248.0 if kind == 'H' else 104.0
        xa, xb = (L_X0 + RAD, L_X1 - RAD) if side == 'L' else (R_X0 + RAD, R_X1 - RAD)
        yb1 = (BOX_Y1 - RAD) if side == 'L' else (R_BOUNCE_Y1 - RAD)
        w_ch = xb - xa
        for _ in range(800):
            ang = float(rng.uniform(0.32, 0.92)) * (1 if rng.random() < .5 else -1)
            vx = spd * math.cos(ang); vy = spd * math.sin(ang)
            t_hit0 = float(rng.uniform(0.0, 2.0 * w_ch / vx))
            y0 = float(rng.uniform(BOX_Y0 + 18, yb1 - 18))
            ok = True
            for m in range(-2, 32):
                th = t_hit0 + m * (2.0 * w_ch / vx)
                if 0.0 <= th <= 26.0:
                    yh = _fold(y0 + vy * th, BOX_Y0 + RAD, yb1)
                    if gate_open_sim(th) and (GATE_Y0 - 8 <= yh <= GATE_Y1 + 8):
                        ok = False; break
            if ok:
                return dict(kind=kind, cross=None, side=side, vx=vx, vy=vy, t_hit0=t_hit0, y0=y0)
        raise RuntimeError('Could not place resident trajectory')

    for _ in range(9):
        mols.append(valid_resident('H', 'R'))
    for _ in range(10):
        mols.append(valid_resident('C', 'L'))
    return mols


MOLS = _build_molecules()


def mol_pos(m, st):
    yb0 = BOX_Y0 + RAD
    if m['cross'] is not None:
        tc = m['cross']; vx, vy, yc = m['vx'], m['vy'], m['yc']
        tm = tc + 0.08
        dt = st - tm
        if m['kind'] == 'H':
            if abs(dt) * vx <= WALL_HW + RAD:
                return WALL_X + dt * vx, yc + vy * dt, vx, vy, ('R' if dt >= 0 else 'L')
            elif dt < 0:
                u = (L_X1 - RAD) - vx * (-dt - (WALL_HW + RAD) / vx)
                return _fold(u, L_X0 + RAD, L_X1 - RAD), _fold(yc + vy * dt, yb0, BOX_Y1 - RAD), vx, vy, 'L'
            else:
                u = (R_X0 + RAD) + vx * (dt - (WALL_HW + RAD) / vx)
                return _fold(u, R_X0 + RAD, R_X1 - RAD), _fold(yc + vy * dt, yb0, R_BOUNCE_Y1 - RAD), vx, vy, 'R'
        else:
            if abs(dt) * vx <= WALL_HW + RAD:
                return WALL_X - dt * vx, yc + vy * dt, -vx, vy, ('L' if dt >= 0 else 'R')
            elif dt < 0:
                u = (R_X0 + RAD) + vx * (-dt - (WALL_HW + RAD) / vx)
                return _fold(u, R_X0 + RAD, R_X1 - RAD), _fold(yc + vy * dt, yb0, R_BOUNCE_Y1 - RAD), -vx, vy, 'R'
            else:
                u = (L_X1 - RAD) - vx * (dt - (WALL_HW + RAD) / vx)
                return _fold(u, L_X0 + RAD, L_X1 - RAD), _fold(yc + vy * dt, yb0, BOX_Y1 - RAD), -vx, vy, 'L'
    else:
        vx, vy = m['vx'], m['vy']
        if m['side'] == 'L':
            x = _fold((L_X1 - RAD) - vx * (st - m['t_hit0']), L_X0 + RAD, L_X1 - RAD)
            return x, _fold(m['y0'] + vy * st, yb0, BOX_Y1 - RAD), vx, vy, 'L'
        else:
            x = _fold((R_X0 + RAD) + vx * (st - m['t_hit0']), R_X0 + RAD, R_X1 - RAD)
            return x, _fold(m['y0'] + vy * st, yb0, R_BOUNCE_Y1 - RAD), vx, vy, 'R'


_BG = None
def desktop_bg():
    global _BG
    if _BG is not None:
        return _BG.copy()
    Q, R, edge = kit.hexmap(18, w=W // 2, h=H // 2, ox=4, oy=4)
    small = np.where((Q + R) % 2 == 0, 1, 2).astype(np.uint8)
    small[edge] = 0
    big = np.repeat(np.repeat(small, 2, 0), 2, 1)
    _BG = U.C[big].copy()
    return _BG.copy()


def draw_cottage(img, lit):
    x0, y0, x1, y1 = COT_X0, COT_Y0, COT_X1, COT_Y1
    U.rect(img, x0 + 8, y0 + 34, x1 - 8, y1, U.C[2])
    for ry in range(y0 + 44, y1, 12):
        U.rect(img, x0 + 8, ry, x1 - 8, ry + 2, U.C[1])
    U.rect(img, x1 - 36, y0 + 2, x1 - 20, y0 + 28, U.C[8])
    pts = np.array([(x0, y0 + 36), (x1, y0 + 36), ((x0 + x1) // 2, y0 + 4)], np.int32)
    cv2.fillPoly(img, [pts], [float(v) for v in U.C[1]])
    cv2.polylines(img, [pts], True, [float(v) for v in U.C[8]], 2)
    wx0, wy0, wx1, wy1 = (x0 + x1) // 2 - 28, y0 + 44, (x0 + x1) // 2 + 28, y0 + 100
    U.rect(img, wx0 - 4, wy0 - 4, wx1 + 4, wy1 + 4, U.C[9 if lit else 8])
    U.rect(img, wx0, wy0, wx1, wy1, U.C[0xF] if lit else U.C[0])
    mcol = U.mix(0xE, 0x8, .35) if lit else U.C[1]
    U.rect(img, (wx0 + wx1) // 2 - 2, wy0, (wx0 + wx1) // 2 + 2, wy1, mcol)
    U.rect(img, wx0, (wy0 + wy1) // 2 - 2, wx1, (wy0 + wy1) // 2 + 2, mcol)
    if lit:
        U.rect(img, x0 + 6, y1 - 8, x1 - 6, y1, U.C[0xF])
    else:
        U.text(img, x0 + 36, y0 - 16, 'NEED +20 C', U.C[9], scale=1)
    U.rect(img, x0 + 20, y0 + 36, x0 + 22, y0 + 54, U.C[8])
    U.sprite(img, SP.SPIDER, x0 + 13, y0 + 52, scale=1, swap={0: 1})
    U.sprite(img, SP.RAT, x1 - 36, y1 - 20, scale=2, flip=True)


def render_frame(i):
    t = i / FPS
    st = sim_t(t)
    paused = (20.0 <= t < 22.0)
    img = desktop_bg()

    U.window(img, WIN_X, WIN_Y, WIN_W, WIN_H, "CHAMBER.EXE - MAXWELL'S DEMON", bar='hers')
    U.rect(img, CX, CY, CX + CW, BOX_Y0 - 4, U.C[0])
    U.rect(img, CX, BOX_Y0 - 6, CX + CW, BOX_Y0 - 4, U.C[3])

    if t < 2.0:
        rule_txt = 'EQUILIBRIUM: HOT & COLD MIXED (ROOM UNLIT)'
        rule_col = U.C[9]
    elif t < 18.0:
        rule_txt = 'RULE: HOT (ORANGE) -> RIGHT, COLD (BLUE) -> LEFT.'
        rule_col = U.C[0xA]
    elif t < 20.0:
        rule_txt = 'ROOM AT +20 C: WINDOW LIT. (LOG FULL: 16/16)'
        rule_col = U.C[0xA]
    elif t < 22.0:
        rule_txt = 'PAUSED BY SECOND_LAW.SYS: LOG FULL (16 / 16)'
        rule_col = U.C[0xD]
    else:
        rule_txt = 'WITCH.EXE: LOG EXPANDED. SORTING CONTINUES.'
        rule_col = U.C[6]
    assert U.tw(rule_txt, 2) < CW - 24, f'Rule text too wide: {U.tw(rule_txt, 2)}'
    U.text(img, CX + 14, CY + 10, rule_txt, rule_col, scale=2)

    U.rect(img, L_X0, BOX_Y0, L_X1, BOX_Y1, U.mix(0, 1, .65))
    U.rect(img, R_X0, BOX_Y0, R_X1, BOX_Y1, U.mix(0, 2, .48))
    for gx in range(L_X0 + 36, L_X1, 40): U.rect(img, gx, BOX_Y0, gx + 1, BOX_Y1, U.C[1])
    for gx in range(R_X0 + 36, R_X1, 40): U.rect(img, gx, BOX_Y0, gx + 1, BOX_Y1, U.C[1])
    for gy in range(BOX_Y0 + 36, BOX_Y1, 40):
        U.rect(img, L_X0, gy, L_X1, gy + 1, U.C[1])
        U.rect(img, R_X0, gy, R_X1, gy + 1, U.C[1])

    lit = (t >= 18.0)
    draw_cottage(img, lit)

    U.rect(img, L_X1, BOX_Y0, R_X0, GATE_Y0, U.C[8])
    U.rect(img, L_X1 + 3, BOX_Y0, R_X0 - 3, GATE_Y0 - 3, U.C[9])
    U.rect(img, L_X1, GATE_Y1, R_X0, BOX_Y1, U.C[8])
    U.rect(img, L_X1 + 3, GATE_Y1 + 3, R_X0 - 3, BOX_Y1, U.C[9])

    is_open, open_kind, open_idx, open_amt = gate_open_at(t)
    bx0, by0, bx1, by1 = WALL_X - 38, BOX_Y0 + 10, WALL_X + 38, BOX_Y0 + 98
    U.rrect(img, bx0 - 4, by0 - 4, bx1 + 4, by1 + 4, 8, U.C[6 if is_open else 8])
    U.rrect(img, bx0, by0, bx1, by1, 6, U.C[3])
    U.sprite(img, SP.WITCH, WALL_X - 24, by0 + 12, scale=3)

    if is_open:
        bcol = U.C[0xE] if open_kind == 'H' else U.C[0xC]
        U.rect(img, L_X1 - 8, GATE_Y0 - 4, R_X0 + 8, GATE_Y1 + 4, bcol)
        U.rect(img, L_X1 + 2, GATE_Y0 + 6, R_X0 - 2, GATE_Y1 - 6, U.mix(0xE if open_kind == 'H' else 0xC, 1, .55))
        U.rect(img, WALL_X - 34, GATE_Y1 + 8, WALL_X + 34, GATE_Y1 + 30, bcol)
        U.text(img, WALL_X - 30, GATE_Y1 + 12, 'OPEN', U.C[0], scale=2)
    else:
        U.rect(img, L_X1 + 2, GATE_Y0, R_X0 - 2, GATE_Y1, U.C[8])
        U.rect(img, L_X1 + 5, GATE_Y0 + 4, R_X0 - 5, GATE_Y1 - 4, U.C[2])
        U.rect(img, WALL_X - 2, GATE_Y0 + 6, WALL_X + 2, GATE_Y1 - 6, U.C[9])
        U.rect(img, WALL_X - 34, GATE_Y1 + 8, WALL_X + 34, GATE_Y1 + 30, U.C[0])
        U.text(img, WALL_X - 30, GATE_Y1 + 12, 'SHUT', U.C[8], scale=2)

    l_hot = l_cold = r_hot = r_cold = 0
    for m in MOLS:
        mx, my, vx_n, vy_n, ch = mol_pos(m, st)
        if ch == 'L':
            if m['kind'] == 'H': l_hot += 1
            else: l_cold += 1
        else:
            if m['kind'] == 'H': r_hot += 1
            else: r_cold += 1
        ix, iy = int(round(mx)), int(round(my))
        if not paused:
            spd = math.hypot(vx_n, vy_n)
            tx, ty = int(round(mx - vx_n / spd * 8)), int(round(my - vy_n / spd * 8))
            cv2.line(img, (ix, iy), (tx, ty), [float(v) for v in U.C[0xD if m['kind'] == 'H' else 0xB]], 3)
        cv2.circle(img, (ix, iy), RAD if m['kind'] == 'H' else RAD - 1,
                   [float(v) for v in U.C[0xE if m['kind'] == 'H' else 0xC]], -1)

    temp_L = int(round(25.0 * (l_hot - l_cold) / max(l_hot + l_cold, 1)))
    temp_R = int(round(22.5 * (r_hot - r_cold) / max(r_hot + r_cold, 1)))

    U.rect(img, L_X0, CY + 40, L_X1, BOX_Y0 - 8, U.C[1])
    U.rect(img, R_X0, CY + 40, R_X1, BOX_Y0 - 8, U.mix(0xE, 1, .45) if lit else U.C[1])
    U.text(img, L_X0 + 10, CY + 48, f'OUTSIDE: {temp_L:+3d} C  ({l_hot:2d}H {l_cold:2d}C)', U.C[0xC], scale=2)
    U.text(img, R_X0 + 10, CY + 48, f'ROOM:    {temp_R:+3d} C  ({r_hot:2d}H {r_cold:2d}C)',
           U.C[0xA if lit else (0xE if temp_R > 0 else 0x9)], scale=2)

    expanded = (t >= 22.0)
    lx, ly, lw, lh = 884, 18, 374, 648
    rcx, rcy, rcw, rch = U.window(img, lx, ly, lw, lh,
                                  'LOG.DAT - FOREVER' if expanded else 'LOG.DAT - 16 SLOTS',
                                  bar='hers' if expanded else 'sys')
    n_logged = sum(1 for ts, _, _, _ in ALL_SORTS if t >= ts)
    U.text(img, rcx + 12, rcy + 10, 'HEX  GATE EVENT', U.C[9], scale=2)
    U.rect(img, rcx + 10, rcy + 32, rcx + rcw - 10, rcy + 34, U.C[3])

    for s_i in range(16):
        ry = rcy + 40 + s_i * 27
        done = s_i < n_logged
        ts_s, _, k_s, _ = ALL_SORTS[s_i]
        just_now = done and (0.0 <= t - ts_s < OPEN_DUR)
        bg_c = (U.C[0xE] if k_s == 'H' else U.C[0xC]) if just_now else (U.C[1] if done else U.mix(0, 1, .35))
        U.rect(img, rcx + 10, ry, rcx + rcw - 10, ry + 23, bg_c)
        U.text(img, rcx + 16, ry + 4, f'0x{s_i:X}', U.C[0 if just_now else (6 if done else 8)], scale=2)
        if done:
            ev_lbl = 'HOT  -> RIGHT' if k_s == 'H' else 'COLD -> LEFT '
            U.text(img, rcx + 96, ry + 4, ev_lbl, U.C[0 if just_now else (0xE if k_s == 'H' else 0xC)], scale=2)
        else:
            U.text(img, rcx + 96, ry + 4, '.............', U.C[8], scale=2)

    by_cap = rcy + 478
    U.rect(img, rcx + 10, by_cap, rcx + rcw - 10, by_cap + 2, U.C[3])
    if not expanded:
        cap_lbl = f'MEMORY: {min(n_logged, 16):2d} / 16' + (' (FULL)' if n_logged >= 16 else '')
        U.text(img, rcx + 12, by_cap + 12, cap_lbl, U.C[0xD if n_logged >= 16 else 0xA], scale=2)
        for s_i in range(16):
            mx0 = rcx + 12 + s_i * 21
            mc = U.C[0xD if n_logged >= 16 else 6] if s_i < n_logged else U.C[1]
            U.rect(img, mx0, by_cap + 42, mx0 + 18, by_cap + 68, mc)
    else:
        U.text(img, rcx + 12, by_cap + 10, f'MEMORY: {n_logged:2d} / INF', U.C[6], scale=2)
        for ex_i in range(3):
            idx_e = 16 + ex_i
            ry = by_cap + 38 + ex_i * 27
            done = idx_e < n_logged
            ts_s, _, k_s, _ = ALL_SORTS[idx_e]
            just_now = done and (0.0 <= t - ts_s < OPEN_DUR)
            bg_c = (U.C[0xE] if k_s == 'H' else U.C[0xC]) if just_now else (U.C[1] if done else U.mix(0, 1, .35))
            U.rect(img, rcx + 10, ry, rcx + rcw - 10, ry + 23, bg_c)
            U.text(img, rcx + 16, ry + 4, f'0x{idx_e:2X}', U.C[0 if just_now else (6 if done else 8)], scale=2)
            if done:
                U.text(img, rcx + 96, ry + 4, 'HOT  -> RIGHT' if k_s == 'H' else 'COLD -> LEFT ',
                       U.C[0 if just_now else (0xE if k_s == 'H' else 0xC)], scale=2)

    # Dialogs strictly inside Left Chamber (x + w <= 408 < 412 = gate left edge!)
    if t >= 20.0:
        overruled = (t >= 22.0)
        btns = U.dialog(
            img, 34, 212, 372, 'SECOND_LAW.SYS',
            ['ORDER IS NOT FREE.',
             'LOG FULL (16 / 16).',
             'CHOOSE ONE:'],
            buttons=('FORGET', 'STOP'),
            bar='off' if overruled else 'sys',
            body=U.C[8] if overruled else U.C[9]
        )
        if overruled:
            # Grey out both buttons in place so dialog box height never shrinks or shifts!
            for bx_, by_, bw_, bh_ in btns:
                U.button(img, bx_, by_, bw_, bh_, 'FORGET' if bx_ == btns[0][0] else 'STOP', pressed=True, tint=(8, 1))
        else:
            b0x, b0y, b0w, b0h = btns[0]
            b1x, b1y, b1w, b1h = btns[1]
            p_start = (48.0, 430.0)
            p_b0 = (b0x + b0w * .5, b0y + 16.0)
            p_b1 = (b1x + b1w * .5, b1y + 16.0)
            if t < 20.75:
                u = (t - 20.0) / 0.75; u = u * u * (3 - 2 * u)
                px = p_start[0] + (p_b0[0] - p_start[0]) * u; py = p_start[1] + (p_b0[1] - p_start[1]) * u
            elif t < 21.05:
                px, py = p_b0
            elif t < 21.50:
                u = (t - 21.05) / 0.45; u = u * u * (3 - 2 * u)
                px = p_b0[0] + (p_b1[0] - p_b0[0]) * u; py = p_b0[1] + (p_b1[1] - p_b0[1]) * u
            else:
                px, py = p_b1
            U.pointer(img, px, py, k=0xA, scale=1.6)

    if t >= 22.0:
        # Custom compact padding (8 px) so 'I DO NOT FORGET THINGS.' fits inside w = 374 (34 + 374 = 408 < 412)!
        wx, wy, ww, wh = 34, 456, 374, 86
        dcx, dcy, dcw, dch = U.window(img, wx, wy, ww, wh, 'WITCH.EXE', bar='hers')
        U.rect(img, dcx, dcy, dcx + dcw, dcy + dch, U.C[9])
        U.text(img, dcx + 6, dcy + 18, 'I DO NOT FORGET THINGS.', U.C[0], scale=2)

    # Her green pointer: sits beside her booth and never moves a pixel
    U.pointer(img, WALL_X + 46, BOX_Y0 + 74, k=6, scale=1.6)

    U.rect(img, 0, H - 38, W, H, U.vgrad(38, U.C[8], U.C[1]))
    U.rect(img, 0, H - 38, W, H - 36, U.C[9])
    U.button(img, 8, H - 33, 84, 28, 'HEX', tint=(6, 5))
    U.strip(img, 104, H - 25, s=10, gap=2)
    bar_num = int(t // 2.0) + 1
    win_str = '1 LIT' if lit else '0 LIT'
    clk_str = f'BAR {bar_num:02d}/14   WINDOW: {win_str}   00:{int(t):02d}'
    U.rect(img, W - U.tw(clk_str, 2) - 24, H - 33, W - 8, H - 5, U.C[0])
    U.text(img, W - U.tw(clk_str, 2) - 16, H - 26, clk_str, U.C[0xF if lit else 0xA], scale=2)

    img = U.glow(img, strength=.55)
    return img


def _worker(i):
    img = (np.clip(render_frame(i), 0, 1)[..., ::-1] * 255 + .5).astype(np.uint8)
    cv2.imwrite(str(FRAMES / f'f_{i:04d}.png'), img)
    return i


POINTS = (
    [(ts, f'slot 0x{idx:X}') for ts, _, _, idx in ALL_SORTS[:16]]
    + [(18.0, 'window lights (register F)'),
       (20.0, 'SECOND_LAW.SYS dialog'),
       (22.0, 'WITCH.EXE: I DO NOT FORGET THINGS.'),
       (23.0, 'slot 0x10'),
       (24.0, 'slot 0x11'),
       (25.0, 'slot 0x12')]
)


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'all'
    OUT.mkdir(parents=True, exist_ok=True); FRAMES.mkdir(parents=True, exist_ok=True)
    if mode == 'test':
        for t_s in (18.5, 21.6, 23.5):
            fi = int(round(t_s * FPS))
            img = (np.clip(render_frame(fi), 0, 1)[..., ::-1] * 255 + .5).astype(np.uint8)
            cv2.imwrite(str(OUT / f'test_{t_s:04.1f}s.png'), img)
        print('wrote v2 test stills to', OUT)
    else:
        with Pool(24) as pool:
            list(pool.imap_unordered(_worker, range(NF), chunksize=16))
        poster = (np.clip(render_frame(int(23.1 * FPS)), 0, 1)[..., ::-1] * 255 + .5).astype(np.uint8)
        cv2.imwrite(str(HERE / 'demon_poster.png'), poster)
        subprocess.run([
            'ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS),
            '-i', str(FRAMES / 'f_%04d.png'), '-i', str(OUT / 'demon.wav'),
            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'slow',
            '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', '-shortest',
            str(HERE / 'demon_exe.mp4')
        ], check=True)
        from backlot import sync, screen
        res = sync.check(POINTS, str(FRAMES), str(OUT / 'demon.wav'), fps=FPS,
                         out_jpg=str(HERE / 'demon_sync.jpg'), out_json=str(OUT / 'sync.json'))
        pops = sync.pops(POINTS, str(FRAMES), fps=FPS)
        screen.filmstrip(str(FRAMES), str(OUT / 'strip.jpg'), n=16)
        print('wrote v2', HERE / 'demon_exe.mp4', 'both:', res['both'], '/', res['total'], 'pops:', pops)
