"""Hex, stage 1: drafts within eight-bit limits. 320 x 180, sixteen colours, hard pixels.

    uv run python styles/hex/stage1.py            three stills and one loop into styles/hex/stage1/
"""
import sys, math
from pathlib import Path
HERE = Path(__file__).resolve().parent; sys.path.insert(0, str(HERE))
import numpy as np
from kit import Canvas, hexmap, stars, movie, bayer, W, H
import sprites as SP
OUT = HERE / 'stage1'
ALL0 = {k: 0 for k in range(16)}

def strip(c, x, y):
    """The signature: the sixteen registers in order. The last one is lit."""
    c.rect(x - 2, y - 2, x + 16 * 4 + 1, y + 5, 0)
    for k in range(16): c.rect(x + k * 4, y, x + k * 4 + 3, y + 3, k)
    return c

# ------------------------------------------------------------------ fig. 1: the cast
def cast():
    c = Canvas(fill=1); Q, R, edge = hexmap(9); c.mask(edge, 2)
    c.rect(0, 0, W, 13, 0); c.text(4, 3, 'FIG. 1  PERSONS OF INTEREST', 0xA); strip(c, W - 68, 5)
    rows = [(SP.WITCH, 'WITCH', 'ON DUTY', None), (SP.SPIDER, 'FAMILIAR', '8 LEGS, 0 NOTES', {9: 0}), (SP.COWBOY, 'COWBOY', 'UNDECIDED', None), (SP.BLOC, 'BLOC', 'ALSO UNDECIDED', None), (SP.MOB, 'CROWD x437', 'HOSTILE', None),
            (SP.DRUID, 'DRUID', 'PREDATES TCP/IP', None), (SP.FACULTY, 'FACULTY', 'REVIEWER 2', None), (SP.ACOLYTE, 'ACOLYTE', 'HERE FOR SNACKS', None), (SP.DRONE, 'DRONE (+)', 'CARRIES THINGS', None), (SP.DRONE, 'DRONE (-)', 'HAS OPINIONS', {0xE: 0xD, 0xC: 8, 0xA: 9})]
    for k, (spr, name, status, swap) in enumerate(rows):
        x = 4 + (k // 5) * 160; y = 16 + (k % 5) * 33
        c.rect(x, y, x + 156, y + 31, 0); c.rect(x + 1, y + 1, x + 27, y + 30, 9 if name == 'FAMILIAR' else 1 if name == 'ACOLYTE' else 3)
        c.sprite(spr, x + 14 - max(len(r) for r in spr) // 2, y + 30 - len(spr) - (0 if len(spr) > 12 else 8), swap=swap)
        c.text(x + 31, y + 5, name, 0xA); c.text(x + 31, y + 18, status, 0xD if status in ('HOSTILE', 'HAS OPINIONS') else 7)
    return c

# ------------------------------------------------------------------ fig. 2: the watch (a still, and a loop called GATE.EXE)
ROWS = ((143, 0, 1), (152, 4, 2), (161, 1, 1), (169, 5, 2))
_BASE = None
def watch_base():
    """Everything that holds still: sky, moon, web, ridge, tower."""
    global _BASE
    if _BASE is not None: return _BASE.copy()
    c = Canvas(); c.grad(0, 132, [0, 0, 1, 1, 2, 3], power=1.3); stars(c, 126, seed=5, step=8)
    c.disc(48, 34, 15, 0xA)
    for x, y, r in ((42, 29, 3), (54, 38, 4), (50, 24, 2), (40, 41, 2)): c.disc(x, y, r, 9)
    for k, a in enumerate((262, 276, 292, 306)): c.line((W - 1, 0), (a, (0, 22, 38, 46)[k]), 8)      # a web in the top corner, because of course
    for rr in (16, 30, 44): c.line((W - rr, 0), (W - rr + 4, rr * .55), 8); c.line((W - rr + 4, rr * .55), (W - rr * .45, rr * .9), 8); c.line((W - rr * .45, rr * .9), (W - 1, rr), 8)
    c.poly([(0, 120), (40, 104), (96, 108), (150, 124), (W, 118), (W, H), (0, H)], 1)                 # the far ridge
    x0, x1, top, base = 190, 246, 44, 150
    c.poly([(x0 - 16, base), (x0, 96), (x0, base)], 1); c.poly([(x1 + 16, base), (x1, 96), (x1, base)], 1)   # buttresses
    c.rect(x0, top, x1, base, 2)
    for y in range(top + 5, base, 6):                                                                 # coursed stone: the wall is made of something
        c.rect(x0, y, x1, y + 1, 1)
        for x in range(x0 + (4 if (y // 6) % 2 else 0), x1, 8): c.rect(x, y - 5, x + 1, y, 1)
    c.rect(x0, top, x0 + 3, base, 3); c.rect(x1 - 7, top, x1, base, 1)
    for x in range(x0 - 2, x1 + 2, 8): c.rect(x, top - 5, x + 5, top, 2); c.rect(x, top - 5, x + 1, top, 3)   # battlements
    c.poly([(x0 + 4, top - 5), (x1 - 4, top - 5), ((x0 + x1) // 2, 8)], 1); c.line((x0 + 4, top - 5), ((x0 + x1) // 2, 8), 3)
    c.line(((x0 + x1) // 2, 8), ((x0 + x1) // 2, 2), 9); c.px((x0 + x1) // 2, 1, 0xA)
    for wx in (196, 236):
        for wy in (58, 84, 110): c.rect(wx, wy + 2, wx + 4, wy + 12, 0); c.rect(wx + 1, wy, wx + 3, wy + 2, 0)
    wx0, wx1, wy0, wy1 = 210, 226, 68, 96                                                             # the one lit window, register F
    c.rect(wx0 - 1, wy0 + 4, wx1 + 1, wy1 + 1, 1)
    c.rect(wx0, wy0 + 5, wx1, wy1, 0xF); c.poly([(wx0, wy0 + 5), (wx1 - 1, wy0 + 5), ((wx0 + wx1) // 2, wy0 - 3)], 0xF)
    c.sprite(SP.WITCH[:14], wx0, wy1 - 14, swap=ALL0)                                                 # and who is in it
    c.rect(212, 128, 224, base, 0); c.poly([(212, 128), (223, 128), (218, 121)], 0)
    c.rect(185, 62, 190, 64, 8); c.px(184, 61, 8); c.rect(246, 62, 251, 64, 8); c.px(251, 61, 8)      # gargoyles, on principle
    c.rect(0, 146, W, H, 0)
    _BASE = c; return c.copy()

def tween(a, b, t): t = min(max(t, 0.0), 1.0); t = t * t * (3 - 2 * t); return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)

def watch_frame(f, n=120):
    """GATE.EXE. Ten seconds at twelve frames a second, and a bar of the tune is fifteen frames, so everything
    sits on a bar line: 0 they arrive; 15 the dialog; the pointer tries ALLOW, then DENY, and presses NEWTS on 45;
    49-79 the conversion runs left to right; 90 a second dialog reports; OK on 105; 108-119 everybody leaves."""
    c = watch_base()
    c.line((47, 0), (47, 28 + (f // 6) % 2), 9); c.sprite(SP.SPIDER, 40, 27 + (f // 6) % 2, swap={9: 0})         # the familiar, on its thread
    if (f // 4) % 3 == 0: c.px(218, 1, 0xD)
    cow = -(12 - f) * 8 if f < 12 else 0 if f < 75 else -(f - 75) * 3                                            # the cowboys make up their minds
    for x, y in ((14, 86), (34, 85), (58, 87)): c.sprite(SP.COWBOY, x + cow, y, swap={9: 1, 0xA: 1, 8: 0, 1: 0}, flip=f >= 60)
    for y, off, body in ROWS:
        for x in range(-6 + off, W, 8):
            side = -1 if x < W / 2 else 1; when = 49 + (x + 6) / W * 30
            if f < when:
                xx = x + (side * (12 - f) * 14 if f < 12 else 0)
                c.sprite(SP.MOB, xx, y, swap={2: body, 0xE: 0xD if (f + x // 8) % 3 == 0 else 0xE, 0xD: 0xE if (f + x // 8) % 3 == 0 else 0xD})
            elif f < when + 1: c.rect(x, y, x + 8, y + 14, 0xA)                                                  # one frame of white: the conversion
            else:
                xx = x + (side * (f - 107) * 14 if f >= 108 else 0)
                c.sprite(SP.NEWT, xx, y + 9, flip=(x // 8 + (f // 3 if f >= 108 else 0)) % 2 == 0)
    d1 = dict(x=6, y=108, w=156, h=60)
    if 15 <= f < 49:
        c.window(d1['x'], d1['y'], d1['w'], d1['h'], 'GATE.EXE', ['437 USERS WISH TO', 'CONNECT.'], ['ALLOW', 'DENY', 'NEWTS'])
        if 45 <= f: c.bevel(108, 152, 156, 164, 9, 8, 0xA); c.text(113, 155, 'NEWTS', 0)
    if 90 <= f < 108:
        c.window(d1['x'], d1['y'], d1['w'], d1['h'], 'GATE.EXE', ['437 USERS ARE NOW', 'NEWTS.'], ['OK'])
        if 105 <= f: c.bevel(12, 152, 36, 164, 9, 8, 0xA); c.text(17, 155, 'OK', 0)
    P = [(0, (300, 96)), (15, (300, 96)), (25, (38, 160)), (30, (38, 160)), (35, (86, 160)), (40, (86, 160)), (44, (140, 160)), (90, (140, 160)), (102, (26, 160)), (112, (26, 160)), (120, (300, 96))]
    for (fa, pa), (fb, pb) in zip(P, P[1:]):
        if fa <= f < fb: px_, py_ = tween(pa, pb, (f - fa) / (fb - fa))
    c.sprite(SP.POINTER, round(px_), round(py_))
    strip(c, W - 68, H - 7)
    return c

def watch(): return watch_frame(30)

# ------------------------------------------------------------------ fig. 3: the research vessel
def ship():
    c = Canvas(); y, x = np.mgrid[:H, :W].astype(np.float64)
    v = np.sin(x / 23 + 1.7 * np.sin(y / 31)) + np.sin(y / 17 - x / 41) + np.sin(np.hypot(x - 236, y - 52) / 19)
    v = (v - v.min()) / (v.max() - v.min()); cols = np.array([0, 0, 1, 1, 2, 3, 2, 1, 4, 1, 0, 0]); u = v * (len(cols) - 1); k = np.minimum(u.astype(int), len(cols) - 2)
    c.a = np.where(bayer(H, W) < (u - k), cols[k + 1], cols[k]).astype(np.uint8)          # a nebula: three sines, quantised
    stars(c, H - 12, seed=9, step=10)
    # exhaust: a broom
    for X in range(0, 58):
        half = 3 + (58 - X) * .32; t = X / 58
        for Y in range(int(101 - half), int(101 + half) + 1):
            if (X * 7 + Y * 3) % 5 < 2 + 3 * t: c.px(X, Y, 0xC if t > .6 else 0xB if t > .25 else 3)
    c.rect(70, 84, 232, 118, 8); c.rect(70, 84, 232, 86, 9); c.rect(70, 114, 232, 118, 2)        # the nave
    c.poly([(74, 84), (228, 84), (222, 70), (80, 70)], 2); c.line((80, 70), (222, 70), 9)        # its roof
    for k_ in range(12):                                                                          # clerestory; somebody is still up
        wx = 82 + k_ * 12; lit = k_ == 8
        c.rect(wx, 92, wx + 5, 103, 0xF if lit else 4); c.rect(wx + 1, 90, wx + 4, 92, 0xF if lit else 4); c.px(wx + 2, 89, 0xF if lit else 0xC)
    c.text(84, 106, 'R/V PERIMETER', 0)
    for px_ in range(84, 224, 12): c.poly([(px_, 70), (px_ + 4, 70), (px_ + 2, 62)], 2); c.px(px_ + 2, 61, 9)      # pinnacles along the roof
    for k_ in range(6):                                                                           # flying buttresses, to the engines
        bx = 88 + k_ * 24; c.line((bx, 118), (bx + 8, 131), 8); c.line((bx + 16, 118), (bx + 8, 131), 8); c.rect(bx + 4, 131, bx + 13, 135, 9); c.px(bx + 3, 133, 0xC)
    c.disc(70, 101, 17, 8); c.ring(70, 101, 11, 0xC, 2)                                           # the apse; the rose window is the drive
    for a in range(0, 360, 45): c.line((70, 101), (70 + 10 * math.cos(math.radians(a)), 101 + 10 * math.sin(math.radians(a))), 0xA)
    c.disc(70, 101, 3, 0xA)
    c.rect(226, 52, 250, 122, 8); c.rect(226, 52, 228, 122, 9); c.rect(246, 52, 250, 122, 2)      # the west front is the bow
    c.poly([(226, 52), (249, 52), (238, 26)], 2); c.line((226, 52), (238, 26), 9)
    for wy in (60, 78, 96): c.rect(233, wy + 2, 237, wy + 12, 0); c.rect(239, wy + 2, 243, wy + 12, 0)
    c.poly([(250, 94), (274, 108), (250, 122)], 8); c.line((250, 94), (274, 108), 9)
    c.line((150, 70), (150, 38), 9); c.px(150, 37, 0xD)                                           # the fleche; a light on top of it
    for hx, hy in ((8, 20), (40, 34), (16, 52), (62, 12), (92, 30)): c.sprite(SP.HAT, hx, hy)     # the posse
    for t in np.linspace(0, 1, 26):                                                               # a lasso, which is a tractor beam
        px_, py_ = 110 + (144 - 110) * t, 34 + 10 * math.sin(t * math.pi) * -1 + (40 - 34) * t
        if int(t * 25) % 2 == 0: c.px(px_, py_, 0xA)
    for a in range(0, 360, 20): c.px(150 + 7 * math.cos(math.radians(a)), 41 + 3 * math.sin(math.radians(a)), 0xA)
    c.rect(0, H - 12, W, H, 0); c.text(4, H - 10, 'FIG. 3  R/V PERIMETER + POSSE', 0xA); strip(c, W - 68, H - 7)
    return c

# ------------------------------------------------------------------ fig. 4: consensus, with one dissent (a loop)
DIRS = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
BASE = {0: (3, 2), 1: (5, 4), 2: (0xB, 0xC), 3: (0xD, 0xD)}                       # each opinion and the colour it shimmers to
HATGLYPH = ['..0..', '.000.', '00000']

def consensus(n=120, size=5, seed=4):
    Q, R, edge = hexmap(size, ox=2, oy=1); cells = sorted(set(zip(Q.ravel().tolist(), R.ravel().tolist()))); idx = {qr: i for i, qr in enumerate(cells)}
    cell_of = np.vectorize(lambda q, r: idx[(q, r)])(Q, R); nb = [[idx[(q + a, r + b)] for a, b in DIRS if (q + a, r + b) in idx] for q, r in cells]
    cx = np.array([np.mean(np.nonzero(cell_of == i)[1]) for i in range(len(cells))]); cy = np.array([np.mean(np.nonzero(cell_of == i)[0]) for i in range(len(cells))])
    post = int(np.argmin((cx - 206) ** 2 + (cy - 80) ** 2)); ring = sorted(nb[post], key=lambda i: math.atan2(cy[i] - cy[post], cx[i] - cx[post]))
    rng = np.random.default_rng(seed); first = rng.integers(0, 4, len(cells)); st = first.copy(); held = np.zeros(len(cells), int); frames = []; lit = set()
    for f in range(n):
        if 0 < f < 108 and f % 2 == 0:                                  # the rule: do what most of your neighbours do. One opinion shouts.
            new = st.copy()
            for i in np.nonzero(rng.random(len(cells)) < (.45 if f < 62 else .8))[0]:
                if i == post: continue
                votes = np.bincount([st[j] for j in nb[i] if j != post] + [st[i]], minlength=4).astype(float)
                if votes[3] >= 2: votes[3] += max(0.0, (f - 26) / 30)          # ...quietly at first
                if (f >= 62 and votes[3] >= 2) or (f >= 74 and votes[3] >= 1): votes[3] += 9          # ...and then not quietly
                new[i] = int(np.argmax(votes + rng.random(4) * .1))
            held = np.where(new == st, held + 1, 0); st = new
        if 86 <= f < 108 and (f - 86) % 3 == 0 and len(lit) < 6: lit.add(ring[len(lit)])      # then, one at a time, the cells beside the post
        if f >= 108:                                                    # reboot: static sweeps in from the left and it all starts again
            edge_x = (f - 107) / 12 * (W + 40) - 20
            back = cx < edge_x; st = np.where(back, first, st); lit = {i for i in lit if not back[i]}
        c = Canvas(); col = np.zeros(len(cells), np.uint8)
        for i, (q, r) in enumerate(cells):
            a, b = BASE[int(st[i])]; col[i] = b if (q - r + f // 3) % 4 == 0 else a
        col[post] = 0xF
        for i in lit: col[i] = 0xF
        c.a = col[cell_of]; c.mask(edge, 0)
        for i in np.nonzero((st == 3) & (held > 2))[0]:                 # an opinion held long enough grows an eye
            if i != post and i not in lit: c.px(round(cx[i]), round(cy[i]), 0xA)
        c.sprite(HATGLYPH, round(cx[post]) - 2, round(cy[post]) - 1)
        agree = (st == 3); agree[post] = False; agree[list(lit)] = False; pct = 100.0 * agree.sum() / len(cells)          # the arithmetic is honest: the post and its neighbours are not counted in
        if f in (61, 85, 107): print('frame', f, 'consensus %.1f%%' % pct, 'dissent', 1 + len(lit))
        c.rect(0, H - 12, W, H, 0); c.text(4, H - 10, f'CONSENSUS {pct:5.1f}%  DISSENT {1 + len(lit)}', 0xA if len(lit) == 0 else 0xF); strip(c, W - 68, H - 7)
        frames.append(c)
    return frames

if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    cast().save(OUT / 'fig1_cast.png'); watch().save(OUT / 'fig2_watch.png'); ship().save(OUT / 'fig3_perimeter.png')
    movie([watch_frame(f) for f in range(120)], OUT / 'fig2_gate_exe_silent.mp4')
    fr = consensus(); movie(fr, OUT / 'fig4_consensus.mp4'); fr[70].save(OUT / 'fig4_consensus_a.png'); fr[107].save(OUT / 'fig4_consensus_b.png')
    print('stage 1 written to', OUT)
