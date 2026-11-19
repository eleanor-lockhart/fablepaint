"""Warmup 1: Token Ring (ca. 3200 BCE) — v2, revised after cold reading.

Eight sarsen trilithons wired into a chalk octagon on a dark moor. Only the stone holding the one lit lantern
(register F) may speak; the lantern passes clockwise round the ring, so in five thousand years there has not been
a collision. Stage 2 print: 640 x 360 in strictly sixteen registers (no green anywhere outside the signature strip),
saved at 2x (1280 x 720), plus a plan derived from the same model in metres.

v2 changes from cold reading:
  - Monolith stonework: vertical weathered sarsen grain instead of mortared brick courses.
  - Clockwise chalk chevrons inlaid on the ring bus so passing direction is visible on the ground.
  - Handled iron lantern with pitched cap and lighter air-dither halo so the lantern shape reads cleanly.
  - `06 QUEUED: SNACKS?` lifted above Stone 06 with a leader line to the purple acolyte (off Stone 05's pillar).
  - Figure 02 shifted clear of Stone 03 so all eight participants can be counted.

    uv run python styles/hex/warmup/ring.py
"""
import sys, math
from pathlib import Path
HERE = Path(__file__).resolve().parent; HEX = HERE.parent; ROOT = HERE.parents[2]
sys.path.insert(0, str(HEX)); sys.path.insert(1, str(ROOT))
import numpy as np
from backlot import space as sp, depth as D
import deep as X, stage2 as S2, kit, sprites as SP
from deep import blend

RING_R = 9.6
N_NODES = 8
TOKEN_NODE = 3
NODE_AZ = [18.0 + 45.0 * k for k in range(N_NODES)]

MOOR1, MOOR2 = blend(0x1, 0x2, .55), blend(0x2, 0x8, .28)
ROCK_DARK = blend(0x1, 0x8, .22)
SARSEN1, SARSEN2, SARSEN_HI = blend(0x9, 0x3, .24), blend(0x8, 0x2, .34), blend(0xA, 0x9, .45)
CHALK1, CHALK2 = blend(0xA, 0x9, .28), blend(0x9, 0x8, .35)
IRON = 0x1


def node_xy(k, r=RING_R):
    a = math.radians(NODE_AZ[k])
    return (r * math.sin(a), r * math.cos(a))


def ground_z(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    r2 = x * x + y * y
    crown = 2.1 * np.exp(-r2 / 340.0)
    undul = 0.20 * np.sin(0.14 * x + 0.4) * np.cos(0.12 * y - 0.3) + 0.12 * np.cos(0.27 * x - 0.19 * y)
    ridge = 3.8 * np.exp(-((y - 74.0) / 20.0) ** 2) * (0.72 + 0.28 * np.sin(0.07 * x + 1.1))
    ring_w = np.exp(-((np.sqrt(r2) - RING_R) / 2.8) ** 2)
    return (crown + undul) * (1.0 - 0.70 * ring_w) + 1.70 * (0.70 * ring_w) + ridge


def make_sarsen_skin(seed=17):
    """Weathered monolithic sandstone/sarsen with vertical fissures and lichen patches (not mortared bricks)."""
    r = np.random.default_rng(seed)
    H_t, W_t = 64, 48
    a = X.speckle(H_t, W_t, SARSEN1, [SARSEN2, SARSEN_HI, 0x8], p=.42, seed=seed)
    for _ in range(14):
        col = int(r.integers(0, W_t))
        y0 = int(r.integers(0, H_t - 12))
        ln = int(r.integers(10, 34))
        a[y0:min(y0 + ln, H_t), col] = SARSEN2 if r.random() < .7 else 0x2
    for _ in range(9):
        cx, cy = int(r.integers(2, W_t - 2)), int(r.integers(2, H_t - 2))
        a[cy - 1:cy + 2, cx - 1:cx + 2] = SARSEN_HI
    return a


def idx_line(idx, a, b, reg):
    n = int(max(abs(b[0] - a[0]), abs(b[1] - a[1]))) + 1
    for i in range(n + 1):
        t = i / max(n, 1)
        x, y = int(round(a[0] + (b[0] - a[0]) * t)), int(round(a[1] + (b[1] - a[1]) * t))
        if 0 <= x < idx.shape[1] and 0 <= y < idx.shape[0]:
            idx[y, x] = reg


def build_set(cam):
    S = sp.Set('Token Ring')
    moor_skin = X.speckle(32, 32, MOOR1, [MOOR2, ROCK_DARK], p=.36, seed=11)
    ridge_skin = X.speckle(32, 32, 0x1, [ROCK_DARK, 0x0], p=.28, seed=12)
    sarsen_skin = make_sarsen_skin(17)
    chalk_skin = X.speckle(16, 16, CHALK1, [CHALK2, 0xA], p=.25, seed=19)

    xs = np.concatenate([np.arange(-58.0, -18.0, 3.0), np.arange(-18.0, 18.1, 1.5), np.arange(21.0, 58.1, 3.0)])
    ys = np.concatenate([np.arange(-28.0, -16.0, 2.5), np.arange(-16.0, 18.1, 1.5), np.arange(21.0, 96.1, 3.5)])
    Z = ground_z(xs[:, None], ys[None, :])
    near_faces, far_faces = [], []
    for i in range(len(xs) - 1):
        for j in range(len(ys) - 1):
            P = [(float(xs[a]), float(ys[b]), float(Z[a, b])) for a, b in ((i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1))]
            ym = 0.25 * sum(p[1] for p in P)
            (far_faces if ym > 36.0 else near_faces).extend([[P[0], P[1], P[2]], [P[0], P[2], P[3]]])
    s_moor = sp.Solid('moor', near_faces, kind='land'); D.paint(s_moor, skin=moor_skin, texel=.10); S.add(s_moor)
    s_ridge = sp.Solid('far_ridge', far_faces, kind='far'); D.paint(s_ridge, skin=ridge_skin, texel=.25); S.add(s_ridge)

    # Inlaid chalk octagon trench ("the ring bus") + clockwise white stone chevrons on every segment
    bus_r = RING_R - 1.75
    for k in range(N_NODES):
        a0, a1 = math.radians(NODE_AZ[k]), math.radians(NODE_AZ[(k + 1) % N_NODES])
        p0 = np.array([bus_r * math.sin(a0), bus_r * math.cos(a0)])
        p1 = np.array([bus_r * math.sin(a1), bus_r * math.cos(a1)])
        seg = p1 - p0; L = float(np.linalg.norm(seg)); u = seg / L; nrm = np.array([-u[1], u[0]])
        steps = 8
        for s_i in range(steps):
            t0, t1 = s_i / steps, (s_i + 1) / steps
            qa, qb = p0 + seg * t0, p0 + seg * t1
            zm = max(float(ground_z(0.5 * (qa[0] + qb[0]), 0.5 * (qa[1] + qb[1]))), 1.65)
            hw = 0.17
            quad = [(qa[0] - nrm[0] * hw, qa[1] - nrm[1] * hw), (qb[0] - nrm[0] * hw, qb[1] - nrm[1] * hw),
                    (qb[0] + nrm[0] * hw, qb[1] + nrm[1] * hw), (qa[0] + nrm[0] * hw, qa[1] + nrm[1] * hw)]
            D.paint(S.prism(f'chalk.{k}.{s_i}', quad, zm - .05, zm + .06, kind='track'), skin=chalk_skin)
        # Clockwise chevron arrow at midpoint of segment k -> k+1
        pm = 0.5 * (p0 + p1); zm = max(float(ground_z(pm[0], pm[1])), 1.66)
        tip = pm + u * 0.42
        for sg in (-1, 1):
            wing = pm - u * 0.25 + nrm * (sg * 0.48)
            S.tube(f'arrow.{k}.{sg}', [(wing[0], wing[1], zm + .08), (tip[0], tip[1], zm + .08)], .09, n=4, kind='cold')
            D.paint(S.solids[-1], index=0xA)

    z_hub = float(ground_z(0.0, 0.0))
    D.paint(S.cylinder('hub_stone', (0.0, 0.0), .42, z_hub - .1, z_hub + .24, n=8, kind='pile'), skin=sarsen_skin)

    druid_r = X.sprite(SP.DRUID, swap={5: 8, 6: 0xA})
    druid_l = X.sprite(SP.DRUID, swap={5: 8, 6: 0xA}, flip=True)
    acolyte_wait = X.sprite(SP.ACOLYTE, swap={0xE: 8, 0xA: 9})

    cards = []
    token_pos = None
    rng = np.random.default_rng(32)
    for k in range(N_NODES):
        cx, cy = node_xy(k)
        zb = float(ground_z(cx, cy)) - 0.14
        tang_deg = -NODE_AZ[k]
        h_up = 3.45 + float(rng.uniform(-.10, .14))
        tmp = sp.Set('tri')
        # Tapered megalithic uprights (hexahedra slightly narrower at top than base)
        for side, off in (('L', -0.84), ('R', 0.84)):
            b_lo = [(cx + off - .40, cy - .33, zb), (cx + off + .40, cy - .33, zb),
                    (cx + off + .40, cy + .33, zb), (cx + off - .40, cy + .33, zb)]
            b_hi = [(cx + off - .33, cy - .28, zb + h_up), (cx + off + .33, cy - .28, zb + h_up),
                    (cx + off + .33, cy + .28, zb + h_up), (cx + off - .33, cy + .28, zb + h_up)]
            D.paint(tmp.hexa(f'stone.{k}.{side}', b_lo, b_hi, kind='wall'), skin=sarsen_skin)
        D.paint(tmp.box(f'stone.{k}.top', (cx - 1.42, cx + 1.42), (cy - .40, cy + .40), (zb + h_up, zb + h_up + .66), kind='roof'), skin=sarsen_skin)
        for sol in tmp.solids:
            S.add(D.turned(sol, tang_deg, about=(cx, cy)))

        px, py = node_xy(k, r=bus_r)
        pz = float(ground_z(px, py))
        D.paint(S.box(f'plinth.{k}', (px - .26, px + .26), (py - .26, py + .26), (pz - .1, pz + .54), kind='pile'), skin=sarsen_skin)

        if k == TOKEN_NODE:
            a_fig = math.radians(NODE_AZ[k] + 9.0); r_fig = RING_R - 2.38
        elif k == 2:
            a_fig = math.radians(NODE_AZ[k] - 7.5); r_fig = RING_R - 1.15        # clear of Stone 03's right upright!
        elif k == 7:
            a_fig = math.radians(NODE_AZ[k] - 6.0); r_fig = RING_R - 0.95        # clear of Stone 04's left upright!
        else:
            a_fig = math.radians(NODE_AZ[k]); r_fig = RING_R - 0.85
        fx, fy = r_fig * math.sin(a_fig), r_fig * math.cos(a_fig)
        fz = float(ground_z(fx, fy))
        spr = acolyte_wait if k == 6 else (druid_r if k == TOKEN_NODE else (druid_l if fx > 0 else druid_r))
        cards.append(D.card(f'fig.{k}', spr, (fx, fy, fz), cam.right, texel=.075))

        if k == TOKEN_NODE:
            # Distinct handled lantern on plinth 03: dark iron base, 4 corner bars, pitched roof cap, bail handle, F glass
            D.paint(S.box('lan.base', (px - .23, px + .23), (py - .23, py + .23), (pz + .54, pz + .64), kind='machine'), index=IRON)
            for sx_i in (-1, 1):
                for sy_i in (-1, 1):
                    D.paint(S.box(f'lan.bar.{sx_i}.{sy_i}', (px + sx_i * .18 - .03, px + sx_i * .18 + .03),
                                  (py + sy_i * .18 - .03, py + sy_i * .18 + .03), (pz + .64, pz + 1.12), kind='machine'), index=IRON)
            D.paint(S.prism('lan.cap', [(px - .26, py - .26), (px + .26, py - .26), (px + .26, py + .26), (px - .26, py + .26)],
                            pz + 1.12, pz + 1.32, top=[(px - .06, py - .06), (px + .06, py - .06), (px + .06, py + .06), (px - .06, py + .06)], kind='machine'), index=IRON)
            D.paint(S.box('lan.bail', (px - .14, px + .14), (py - .02, py + .02), (pz + 1.32, pz + 1.48), kind='machine'), index=0x9)
            D.paint(S.box('token.lamp', (px - .15, px + .15), (py - .15, py + .15), (pz + .64, pz + 1.12), kind='light'),
                    index=0xF, glow=1.0, cast=False)
            token_pos = (px, py, pz + .88)

    return S, cards, token_pos


def render():
    cam = sp.Camera(eye=(-2.4, -22.8, 6.8), look=(0.2, 0.8, 2.2), lens=30, size=(S2.W, S2.H), name='cam1')
    S, cards, tpos = build_set(cam)

    sp.drawing(S, 'plan', out=str(HERE / 'token_ring_plan.svg'), scale=12, cameras=[cam], title='TOKEN RING (8 NODES, R = 9.6 M)')
    draw_hex_plan(cam, HERE / 'token_ring_plan.png')

    solids = S.solids + cards
    g = D.gbuffer(solids, cam)

    moon_dir = sp.direction(295, 26)
    moon_light = D.Light(tuple(moon_dir * 400.0), power=.62, reach=1e6, shadow=False)
    token_light = D.Light((tpos[0], tpos[1], tpos[2] + .42), power=5.2, reach=14.5).bake(S.solids)
    lv = D.lighting(g, [moon_light, token_light], ambient=.15, moving=cards)

    sx, sy = cam.p(*tpos)
    # Tighter air-halo (0.42 instead of 0.85) so the iron lantern frame & plinth stonework stay sharp!
    idx = S2.index(g, lv, cam, haze=155.0, lamps=[(sx, sy, 0.42)], stars=True)

    rng = np.random.default_rng(7)
    sky_mask = ~g['hit']
    for gy in range(2, 160, 14):
        for gx in range(2, S2.W - 2, 14):
            x = gx + int(rng.integers(0, 13)); y = gy + int(rng.integers(0, 13))
            if y < S2.H and x < S2.W and sky_mask[y, x]:
                idx[y, x] = (8, 8, 9, 9, 0xA, 0xC)[int(rng.integers(0, 6))]

    mx, my, mr = 82, 42, 14
    yy, xx = np.mgrid[:S2.H, :S2.W]
    disc = ((xx - mx) ** 2 + (yy - my) ** 2 <= mr ** 2) & sky_mask
    bite = (xx - (mx + 5)) ** 2 + (yy - (my - 3)) ** 2 <= (mr - 1) ** 2
    cres = disc & ~bite
    craters = cres & (((xx - (mx - 5)) ** 2 + (yy - (my + 2)) ** 2 <= 9) | ((xx - (mx - 3)) ** 2 + (yy - (my - 6)) ** 2 <= 4))
    idx[cres] = 0xA; idx[craters] = 0x9

    # Crisp node tags on each lintel; 06 QUEUED placed in clear sky above Stone 06 with a leader line to Acolyte 06!
    for k in range(N_NODES):
        cx, cy = node_xy(k)
        zb = float(ground_z(cx, cy)) + 3.80
        px, py = cam.p(cx, cy, zb)
        ix, iy = int(round(px)), int(round(py)) - 4
        S2.rect(idx, ix - 11, iy - 2, ix + 11, iy + 9, 0x0)
        if k == TOKEN_NODE:
            S2.rect(idx, ix - 11, iy - 3, ix + 11, iy - 2, 0xF)
            S2.text(idx, ix - 8, iy, '03', 0xF)
            msg = '03 TX: "STILL WINTER."'
            bx = min(max(int(round(sx)) - 58, 8), S2.W - len(msg) * 8 - 10)
            by = min(int(round(sy)) + 36, S2.H - 32)
            idx_line(idx, (int(round(sx)), int(round(sy)) + 12), (bx + 12, by - 4), 0xF)
            S2.rect(idx, bx - 4, by - 4, bx + len(msg) * 8 + 4, by + 11, 0x0)
            S2.rect(idx, bx - 4, by - 4, bx + len(msg) * 8 + 4, by - 3, 0xF)
            S2.text(idx, bx, by, msg, 0xA)
            S2.rect(idx, bx, by, bx + 16, by + 8, 0x0); S2.text(idx, bx, by, '03', 0xF)
        else:
            S2.rect(idx, ix - 11, iy - 3, ix + 11, iy - 2, 0x8)
            S2.text(idx, ix - 8, iy, f'{k:02d}', 0xA)
            if k == 6:
                ac_xy = node_xy(6, RING_R - 0.85)
                ax, ay = cam.p(ac_xy[0], ac_xy[1], float(ground_z(*ac_xy)) + 1.35)
                msg = '06 QUEUED: "SNACKS?"'
                bx, by = 112, 68                                               # clear dark sky above Stone 06!
                idx_line(idx, (bx + 54, by + 10), (int(round(ax)), int(round(ay))), 0x9)
                S2.rect(idx, bx - 4, by - 3, bx + len(msg) * 8 + 4, by + 10, 0x0)
                S2.rect(idx, bx - 4, by - 4, bx + len(msg) * 8 + 4, by - 3, 0x3)
                S2.text(idx, bx, by, msg, 0x9)

    S2.rect(idx, 0, S2.H - 14, S2.W, S2.H, 0x0)
    S2.rect(idx, 0, S2.H - 15, S2.W, S2.H - 14, 0x2)
    bar_txt = 'RING.SYS  8 STONES (00-07)  TOKEN: 03  COLLISIONS (5200 YR): 0'
    S2.text(idx, 6, S2.H - 11, bar_txt, 0xA)

    green_px = int(np.isin(idx, [4, 5, 6, 7]).sum())
    assert green_px == 0, f'Expected 0 green pixels in witch-free scene, got {green_px}'

    for k in range(16):
        S2.rect(idx, S2.W - 6 - (16 - k) * 6, S2.H - 10, S2.W - 6 - (16 - k) * 6 + 5, S2.H - 5, k)

    out_png = HERE / 'token_ring.png'
    X.save(str(out_png), S2.rgb(idx, 2))
    print('wrote v2', out_png)


def draw_hex_plan(cam, out_path):
    c = kit.Canvas(640, 360, fill=0x0)
    cx0, cy0, sc = 320, 184, 11.2
    def mp(x, y): return int(round(cx0 + x * sc)), int(round(cy0 - y * sc))
    for g in range(-25, 26, 5):
        x, _ = mp(g, 0); _, y = mp(0, g)
        if 0 <= x < 640: c.rect(x, 18, x + 1, 342, 0x1)
        if 18 <= y < 342: c.rect(0, y, 640, y + 1, 0x1)
    pts = [mp(*node_xy(k, RING_R - 1.75)) for k in range(N_NODES)]
    for k in range(N_NODES):
        a, b = pts[k], pts[(k + 1) % N_NODES]
        c.line(a, b, 0x9, 2)
        mx, my = (a[0] + b[0]) // 2, (a[1] + b[1]) // 2
        dx, dy = b[0] - a[0], b[1] - a[1]; L = max(math.hypot(dx, dy), 1.0); ux, uy = dx / L, dy / L
        c.line((mx, my), (mx - 6 * ux - 4 * uy, my - 6 * uy + 4 * ux), 0xC, 1)
        c.line((mx, my), (mx - 6 * ux + 4 * uy, my - 6 * uy - 4 * ux), 0xC, 1)
    for k in range(N_NODES):
        nx, ny = node_xy(k)
        a = math.radians(NODE_AZ[k]); tx, ty = math.cos(a), -math.sin(a)
        p_a = mp(nx - 1.35 * tx, ny - 1.35 * ty); p_b = mp(nx + 1.35 * tx, ny + 1.35 * ty)
        c.line(p_a, p_b, 0x9, 5); c.line(p_a, p_b, 0x3, 3)
        px, py = pts[k]
        c.rect(px - 3, py - 3, px + 4, py + 4, 0xF if k == TOKEN_NODE else 0x8)
        lx, ly = mp(*node_xy(k, RING_R + 2.4))
        c.text(lx - 8, ly - 4, f'{k:02d}', 0xF if k == TOKEN_NODE else 0xA)
    hx, hy = mp(0, 0); c.ring(hx, hy, 5, 0x8, 1)
    ex, ey = mp(cam.eye[0], cam.eye[1])
    for sign in (-1, 1):
        ang = math.radians(cam.az + sign * cam.hfov / 2)
        tx, ty = mp(cam.eye[0] + 32 * math.sin(ang), cam.eye[1] + 32 * math.cos(ang))
        c.line((ex, ey), (tx, ty), 0x3, 1)
    c.rect(0, 0, 640, 16, 0x0); c.text(8, 4, 'PLAN: TOKEN RING  R = 9.6 M  CLOCKWISE PASSING', 0xA)
    c.rect(0, 344, 640, 360, 0x0); c.text(8, 348, 'SCALE: 5 M GRID   ACTIVE TOKEN: STONE 03', 0x9)
    for k in range(16): c.rect(640 - 6 - (16 - k) * 6, 349, 640 - 6 - (16 - k) * 6 + 5, 354, k)
    c.save(out_path, scale=2)


if __name__ == '__main__':
    render()
