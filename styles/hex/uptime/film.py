"""UPTIME: the picture. Seventy-two seconds at 24 frames a second; one bar of the score is one second.

    uv run python styles/hex/uptime/film.py sheet      a contact sheet of one frame from every scene
    uv run python styles/hex/uptime/film.py            every frame, then the film with its sound (after music.py)

The storyboard is BRIEF.md. frame(i) is pure: the same i always gives the same picture.
"""
import sys, math
from pathlib import Path
HERE = Path(__file__).resolve().parent; sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parent))
import numpy as np
import cv2
import ui as U
from ui import C, W, H
from kit import hexmap
import sprites as SP, stage1 as S1
FPS, SECONDS = 24, 72
TOWER, RING, PROC = (92, 36, 648, 392), (760, 36, 496, 318), (760, 366, 496, 250)
LIT = (536, 232)                                              # where the tower's lit window is on the screen
TILES = [('SPIDER', SP.SPIDER, {9: 9}), ('DRONES', SP.DRONE, None), ('STONES', SP.DRUID, None), ('FACULTY', SP.FACULTY, None), ('SNACKS', SP.ACOLYTE, None)]
OFF, ON = [50.0, 51.0, 52.0, 53.0, 53.5], [57.0, 58.0, 59.0, 60.0, 61.0]      # when each homepage's light goes out, and comes back
RUNS = [(5.0, 1, 2), (9.5, 1, 4), (65.0, 1, 0)]                               # drone deliveries: (start, from tile, to tile)
def newts(t): return (0 if t < 20 else int(111435 * clamp(t - 20))) + (t >= 33.9) + (t >= 56)      # 437 x 255, then the hive's pointer, then the hive
clamp = lambda v: min(max(v, 0.0), 1.0)
ease = lambda v: (lambda u: u * u * (3 - 2 * u))(clamp(v))
HATG = ['..0..', '.000.', '00000']

_WP = None
def wp():
    global _WP
    if _WP is None:
        Q, R, edge = hexmap(22, W, H, ox=5, oy=3); key = Q.astype(np.int64) * 100000 + R; uniq, inv = np.unique(key, return_inverse=True); cell = inv.reshape(H, W); n = len(uniq)
        y, x = np.mgrid[:H, :W]; cnt = np.bincount(cell.ravel(), minlength=n); cx = np.bincount(cell.ravel(), x.ravel(), n) / cnt; cy = np.bincount(cell.ravel(), y.ravel(), n) / cnt
        night = np.stack([U.mix(1, 2, (.15, .45, .8)[k % 3]) * (.75 + .25 * cy[k] / H) for k in range(n)])
        tx, ty = LIT[0] - cx, LIT[1] - cy; tn = np.maximum(np.hypot(tx, ty), 1); ex, ey = cx + 3.2 * tx / tn, cy + 3.2 * ty / tn
        _WP = dict(cell=cell, edge=edge, eye=np.hypot(x - cx[cell], y - cy[cell]) < 2.7, eye2=np.hypot(x - ex[cell], y - ey[cell]) < 2.7, lid=(np.abs(x - cx[cell]) < 4) & (np.abs(y - cy[cell]) < 1), night=night, src=np.hypot(cx - 44, cy - 356), tow=np.hypot(cx - LIT[0], cy - LIT[1]), n=n)
    return _WP

def wallpaper(t):
    """Hexagonal cells in the night registers. From 22.5 s the consensus spreads out from its icon; at 56 it is rolled back from the tower."""
    w = wp(); on = (t > 22.5 + w['src'] / 1400 * 10.0) & ~(t > 56.0 + w['tow'] / 1300 * 4.0)
    col = w['night'].copy(); k = (np.arange(w['n']) + int(t * 6)) % 7 == 0
    stopped = t >= 50                                           # at midnight the hive stops, and it never starts again: grey, eyes shut, until she has it cleared away
    col[on] = U.mix(8, 0, .25) if stopped else C[0xD]
    if not stopped: col[on & k] = U.mix(0xD, 0xE, .35)
    img = col[w['cell']].astype(np.float32); img[w['edge']] = C[0]; onpx = on[w['cell']]
    blink = 34 <= t < 50 and (t % 1) < 4 / 24                   # while they wait, every eye is on her window, and they blink on the tick
    if stopped or blink: img[w['lid'] & onpx] = C[0]
    else: img[(w['eye2'] if t >= 34 else w['eye']) & onpx] = C[0xA]
    return img, float(on.mean())

def tower(t):
    """The eight-bit scene, live, as an index canvas. It runs on twos: twelve pictures a second."""
    f = int(t * 12); c = S1.watch_base(); bob = (f // 6) % 2
    c.line((47, 0), (47, 28 + bob), 9); c.sprite(SP.SPIDER, 40, 27 + bob, swap={9: 0})
    turn = int(t / 3) % 2 == 1 if (t < 28 or 34 <= t < 50 or t >= 57) else False          # she looks one way, then the other. Not while they are trying to close her
    c.rect(210, 73, 226, 96, 0xF); c.poly([(210, 73), (225, 73), (218, 65)], 0xF); c.sprite(SP.WITCH[:14], 210, 82, swap=S1.ALL0, flip=turn)
    if 12 <= t < 62:
        off = -int(clamp(13 - t) * 96) - int(clamp((t - 58) / 3) * 110)
        for x, y in ((14, 86), (34, 85), (58, 87)): c.sprite(SP.COWBOY, x + off, y, swap={9: 1, 0xA: 1, 8: 0, 1: 0}, flip=t > 56)
    if 12 <= t < 22.3:
        for r, (y, o, body) in enumerate(S1.ROWS):
            for x in range(-6 + o, 320, 8):
                if t < 12 + (1 - abs(x - 160) / 160) * 5.0 + r * .5: continue                    # they come from both sides and close on the door
                when = 20.0 + (x + 6) / 320 * 1.0
                if t < when: c.sprite(SP.MOB, x, y, swap={2: body, 0xE: 0xD if (f + x // 8) % 3 == 0 else 0xE, 0xD: 0xE if (f + x // 8) % 3 == 0 else 0xD})
                elif t < when + 1 / 12: c.rect(x, y, x + 8, y + 14, 0xA)
                else: c.sprite(SP.NEWT, x + (-1 if x < 160 else 1) * int(max(0, t - 21.2) * 170), y + 9, flip=(x // 8 + f // 3) % 2 == 0)
    return c.a

def clock(t):
    s = 10 + int(t)
    if t < 50: return f'31 DEC 1999  23:59:{s:02d}'
    return f'01 JAN {"1900" if t < 56 else "2000"}  00:00:{int(t) - 50:02d}'

def bios(t):
    img = np.zeros((H, W, 3), np.float32); U.strip(img, W - 16 * 12 - 24, 24)
    for at, s, k in ((.25, 'HEX BIOS 1.6', 0xA), (.75, '16 REGISTERS ........... OK', 9), (1.25, 'REGISTER F ........ RESERVED', 0xF), (1.75, f'CLOCK ...... 31-12-1999 23:59:{10 + int(t)}', 9), (2.25, 'WITCH.EXE ...... ALREADY RUNNING', 6)):
        if t >= at: U.text(img, 48, 60 + int((at - .25) * 2) * 44, s, C[k], 3)
    if int(t * 4) % 2 == 0: U.text(img, 48, 60 + 5 * 44, '_', C[0xA], 3)
    return img

def lit_count(t): return sum(1 for k in range(5) if not (OFF[k] <= t < ON[k]))

def desktop(t):
    img, taken = wallpaper(t); hive = 26 <= t < 50; dead = 50 <= t < 56.5
    # icons
    U.sprite(img, HATG, 24, 66, 8, swap={0: 6}); U.text(img, 10, 104, 'MY TOWER', C[0xA], 1, C[0])
    crooked = t < 8; ox, oy = (26, 15) if crooked else (0, 0)
    U.sprite(img, SP.NEWT, 22 + ox, 152 + oy, 5); U.text(img, 22 + ox, 182 + oy, 'NEWTS', C[0xA], 1, C[0])
    if 7.85 <= t < 8.3:                                         # the grid she keeps things on, shown for a moment
        for yy in range(56, 400, 12): U.rect(img, 12, yy, 14, yy + 6, C[6])
        for yy in (146, 198): U.rect(img, 12, yy, 80, yy + 2, C[6], .7)
    U.sprite(img, SP.SPIDER, 18, 236, 3); U.text(img, 10, 274, 'WEB RING', C[0xA], 1, C[0])
    if 22 <= t < 56: U.rrect(img, 22, 330, 66, 374, 14, C[0xD]); U.rrect(img, 39, 347, 49, 357, 5, C[0xA]); U.text(img, 8, 380, 'CONSENSUS', C[0xA], 1, C[0])
    elif t >= 56: U.sprite(img, SP.NEWT, 22, 342, 5); U.text(img, 8, 380, 'CONSENSUS', C[0xA], 1, C[0])          # it is a newt now, and it is counted
    # the web ring: five homepages and one that is not ready
    x, y, w, h = U.window(img, *RING, 'WEB RING - 5 SITES', 'hive' if hive else 'off' if dead else 'sys')
    for j in range(6):
        tx, ty = x + 6 + (j % 3) * 160, y + 6 + (j // 3) * 140
        if j == 5:
            U.rrect(img, tx, ty, tx + 152, ty + 132, 6, C[1])
            for k in range(0, 152, 16): cv2.fillPoly(img, [np.array([(tx + k, ty + 92), (tx + k + 8, ty + 92), (tx + k + 16, ty + 108), (tx + k + 8, ty + 108)], np.int32)], [float(v) for v in C[0xE]])
            U.text(img, tx + 12, ty + 30, 'UNDER', C[9], 2); U.text(img, tx + 12, ty + 52, 'CONSTR.', C[9], 2); continue
        name, spr, swap = TILES[j]; lit = not (OFF[j] <= t < ON[j])
        U.rrect(img, tx, ty, tx + 152, ty + 132, 6, C[1] if lit else C[0])
        U.rect(img, tx + 10, ty + 10, tx + 26, ty + 32, C[0xF] if lit else U.mix(0, 1, .6))            # the site's own lit window
        U.rect(img, tx + 17, ty + 10, tx + 19, ty + 32, C[1] if lit else C[0]); U.rect(img, tx + 10, ty + 20, tx + 26, ty + 22, C[1] if lit else C[0])
        U.text(img, tx + 34, ty + 14, name, C[0xA] if lit else C[8], 2)
        U.sprite(img, spr, tx + 76 - max(len(r) for r in spr) * 3 // 2, ty + 118 - len(spr) * 3, 3, swap=swap if lit else {k: (0 if k == 0 else 8) for k in range(16)})
        if ON[j] <= t < ON[j] + 3 / 24: U.rrect(img, tx, ty, tx + 152, ty + 132, 6, C[0xF], .85)                # it comes back on with a flash of its own colour
        got = [t0 + 1.5 for t0, a_, b_ in RUNS if b_ == j and t >= t0 + 1.5]
        U.text(img, tx + 100, ty + 120, f'{437 + len(got):06d}', C[0xF] if (got and t < got[-1] + .5) else C[7] if lit else C[8], 1)
    for t0, a_, b_ in RUNS:                                                                              # a drone carries something from one page to another
        if t0 <= t < t0 + 1.5:
            u = ease((t - t0) / 1.5); pa = (x + 6 + (a_ % 3) * 160 + 60, y + 6 + (a_ // 3) * 140 + 56); pb = (x + 6 + (b_ % 3) * 160 + 60, y + 6 + (b_ // 3) * 140 + 56)
            dx, dy = pa[0] + (pb[0] - pa[0]) * u, pa[1] + (pb[1] - pa[1]) * u - math.sin(u * math.pi) * 26
            U.sprite(img, SP.DRONE, dx, dy, 3, flip=pb[0] < pa[0]); U.rect(img, dx + (-6 if pb[0] < pa[0] else 36), dy + 14, dx + (0 if pb[0] < pa[0] else 42), dy + 20, C[0xF])
    # processes
    x, y, w, h = U.window(img, *PROC, 'PROCESSES', 'hive' if hive else 'off' if dead else 'sys')
    rows = [('PROCESS', 'PID', 'STATUS', 9), ('WITCH.EXE', '1', 'ALWAYS', 6), ('GATE.EXE', '16', 'WAITING' if t < 12 else 'ASKING' if t < 20 else f'{newts(t)} NEWTS', 9), ('WEBRING.DLL', '160', f'SERVING {lit_count(t)}', 9),
            ('CLOCK.SYS', '255', 'TICKING' if t < 50 else 'WRONG' if t < 56 else 'CORRECTED' if t < 60 else 'TICKING', 0xE if 50 <= t < 56 else 9)]
    if t >= 22: rows.append(('CONSENSUS.SCR', '?', 'SPREADING' if t < 34 else 'UNANIMOUS' if t < 50 else 'STOPPED' if t < 56 else 'NEWT', 8 if 50 <= t < 56 else 0xD if t < 56 else 6))
    if 34 <= t < 56: rows.append(('THE_END.EXE', '666', 'COUNTING' if t < 50 else 'OVERDUE', 0xE))
    rows = [(f'{a_:<13}{b_:>3} {c_}', col) for a_, b_, c_, col in rows]
    U.text(img, x + 12, y + 10, 'UPTIME: SINCE BEFORE TCP/IP', C[7], 2)                               # at the top, so that what the watchers say has the bottom of the window to itself
    for k, (s, col) in enumerate(rows): U.text(img, x + 12, y + 38 + k * 25, s, C[col], 2)
    # the tower: hers
    x, y, w, h = U.window(img, *TOWER, 'TOWER - 1 WINDOW LIT', 'hers'); U.blit(img, tower(t), x, y, 2)
    # the taskbar and the clock
    U.rect(img, 0, 684, W, H, U.vgrad(36, C[9], C[8])); U.rect(img, 0, 684, W, 685, C[0xA])
    U.button(img, 8, 689, 92, 26, 'HEX', False, (6, 5)); U.strip(img, 116, 697, 8, 2)
    cs = clock(t); U.rrect(img, W - U.tw(cs) - 30, 689, W - 8, 715, 6, C[0]); U.text(img, W - U.tw(cs) - 19, 695, cs, C[0xE] if 50 <= t < 56 else C[7], 2)
    return img

_BTN = {}
def btn(name):
    """Where each button will be, found by drawing its dialog once on scrap."""
    if not _BTN:
        s = np.zeros((H, W, 3), np.float32)
        _BTN['newts'] = U.dialog(s, 110 + 40 * 7, 436 + 12 * 7, 470, 'GATE.EXE', ['', ''], ['ALLOW', 'DENY', 'NEWTS'])[2]
        _BTN['close'] = U.dialog(s, 330, 216, 520, 'CONSENSUS', ['', '', ''], ['CLOSE'], 'hive')[0]
        _BTN['end'] = U.dialog(s, 372, 300, 520, 'CONSENSUS', [''], ['END TASK'], 'hive')[0]
        _BTN['sure'] = U.dialog(s, 414, 384, 470, 'CONSENSUS', [''], ['ARE YOU SURE?'], 'hive')[0]
        _BTN['decree'] = U.dialog(s, 400, 262, 480, 'WITCH.EXE', ['', ''], ['OK'], 'hers')[0]
        _BTN['safe'] = U.dialog(s, 420, 280, 440, 'HEX', ['', ''], ['OK'])[0]
    x, y, w, h = _BTN[name]; return (x + w * .55, y + h * .55)

def path(t, keys):
    for (ta, pa), (tb, pb) in zip(keys, keys[1:]):
        if ta <= t < tb: u = ease((t - ta) / (tb - ta)); return (pa[0] + (pb[0] - pa[0]) * u, pa[1] + (pb[1] - pa[1]) * u)
    return keys[-1][1] if t >= keys[-1][0] else keys[0][1]

WATCH = [SP.ACOLYTE, SP.BLOC, SP.ACOLYTE, SP.DRUID, SP.ACOLYTE, SP.FACULTY, SP.BLOC, SP.COWBOY]
SAID = [(37.0, 16, 'ANY SECOND NOW.'), (39.0, 21, 'NOBODY IS PID 1.'), (41.0, 23, 'UNDECIDED.'), (42.5, 22, 'ALSO UNDECIDED.'), (44.0, 19, 'WE PREDATE THIS.'), (45.5, 18, 'ARE THERE SNACKS?'),
        (47.0, 24, 'SHE HAS TO BLINK.'), (48.5, 14, 'NO GODS. NO ADMINS.'), (50.6, 20, 'HAPPY NEW 1900.'), (52.5, 21, 'AS I PREDICTED.'), (54.6, 23, 'UH OH.'), (57.2, 18, 'SO. SNACKS?')]      # (when, which watcher, what)
def frame(i):
    t = i / FPS
    if t < 3.0: return (bios(t) * 255).astype(np.uint8)
    img = desktop(t)
    # the wait: a window that counts, and everybody who has come to watch her fail
    if 34 <= t < 56:
        left = 50 - int(t); jit = (7 - left) if (0 < left <= 5 and (t % 1) < 2 / 24) else 0                # in the last five seconds the window jumps on each tick, further each time
        x, y, w, h = U.window(img, 250 + jit, 452, 336, 214, 'THE END - 30 WATCHING', 'sys')
        U.text(img, x + 14, y + 12, 'SECONDS UNTIL', C[9], 2); U.text(img, x + 14, y + 34, 'EVERYTHING STOPS', C[9], 2)
        s = str(left); U.text(img, x + (w - U.tw(s, 9)) // 2, y + 72, s, C[0xD] if 0 < left <= 5 else C[0xE], 9)
    if 34 <= t < 62:
        for k in range(30):
            rows = WATCH[k % 8]; side = -1 if k < 15 else 1; off = side * (ease((37 - t) / 3) * 760 + ease((t - 58 - (k % 5) * .25 - (1.4 if rows is SP.COWBOY else 0)) / 2.5) * 900)      # the hats go last
            dy = -12 if 50 <= t < 50.25 else (3 if (t % 1) < .125 else 0)
            U.sprite(img, rows, 96 + k * 39 + off, 684 - len(rows) * 3 + dy, 3, flip=k >= 15)
    for t0, k, line in SAID:
        if t0 <= t < t0 + 1.4:
            bx = min(96 + k * 39 - 16, W - U.tw(line) - 26); U.rrect(img, bx, 584, bx + U.tw(line) + 18, 612, 5, C[0]); U.rrect(img, bx + 1, 585, bx + U.tw(line) + 17, 611, 4, C[0xA]); U.text(img, bx + 9, 591, line, C[0], 2)
    # the crowd: a dialog a bar, doubling
    for k in range(8):
        if 12 + k <= t < 20.5 + (7 - k) / 12:
            U.dialog(img, 110 + 40 * k, 436 + 12 * k, 470, 'GATE.EXE', [f'{437 * 2 ** k} USERS WISH TO', 'CONNECT.'], ['ALLOW', 'DENY', 'NEWTS'], 'hers' if 20 <= t < 20.17 else 'sys', 2 if (k == 7 and 20 <= t < 20.3) else None)      # on the press every one of them is hers for a moment
    # the hive tries to close her
    if 28 <= t < 34: U.dialog(img, 330, 216, 520, 'CONSENSUS', ['WITCH.EXE HAS PERFORMED AN', 'ILLEGAL OPERATION AND WILL', 'BE SHUT DOWN.'], ['CLOSE'], 'hive', 0 if 29 <= t < 29.25 else None)
    if 30 <= t < 34: U.dialog(img, 372, 300, 520, 'CONSENSUS', ['WITCH.EXE CANNOT BE CLOSED.'], ['END TASK'], 'hive', 0 if 31 <= t < 31.25 else None)
    if 32 <= t < 34: U.dialog(img, 414, 384, 470, 'CONSENSUS', ['TASK DECLINES.'], ['ARE YOU SURE?'], 'hive', 0 if 33 <= t < 33.25 else None)
    if 33.5 <= t < 35.5: U.dialog(img, 640, 524, 230, 'WITCH.EXE', ['SHE IS.'], (), 'hers')
    if 54 <= t < 56.4: U.dialog(img, 400, 262, 480, 'WITCH.EXE', ['IT IS THE YEAR 2000', 'BECAUSE I SAY SO.'], ['OK'], 'hers', 0 if 56 <= t < 56.3 else None)
    if 68 <= t < 70.25: U.dialog(img, 420, 280, 440, 'HEX', ['IT IS NOW SAFE TO LEAVE', 'YOUR COMPUTER ON.'], ['OK'], 'sys', 0 if 70 <= t < 70.25 else None)
    # the hive's pointer, which ends as a newt
    if 27.2 <= t < 33.85: U.pointer(img, *path(t, [(27.2, (44, 356)), (28.8, btn('close')), (29.4, btn('close')), (30.8, btn('end')), (31.4, btn('end')), (32.8, btn('sure')), (33.85, btn('sure'))]), 0xD)
    elif 33.85 <= t < 35.5:
        bx, by = btn('sure')
        if t < 33.97: U.rrect(img, bx - 18, by - 14, bx + 26, by + 30, 6, C[0xA])
        else: U.sprite(img, SP.NEWT, bx - 12 - (t - 33.97) * 520, by + 2 * math.sin(t * 40), 5)
    # her pointer
    rest = (604, 300); home = (22 + 26 + 22, 152 + 15 + 12)
    U.pointer(img, *path(t, [(3, rest), (6.6, rest), (7.8, home), (8.4, home), (9.6, rest), (18.9, rest), (19.8, btn('newts')), (20.6, btn('newts')), (21.6, rest), (54.2, rest), (55.8, btn('decree')), (56.5, btn('decree')), (57.6, rest),
                              (68.3, rest), (69.8, btn('safe')), (72, btn('safe'))]), 6)
    img = U.glow(img)
    if 56 <= t < 57.4:                                                                                 # the decree lands: a flare from the window, the way a lens of the period would have it
        y, x = np.mgrid[:H, :W].astype(np.float32); s = (1 - (t - 56) / 1.4) ** 2
        fl = np.exp(-((y - LIT[1]) / 3.5) ** 2) * np.exp(-np.abs(x - LIT[0]) / 460) + .5 * np.exp(-(((x - LIT[0]) ** 2 + (y - LIT[1]) ** 2) / 90 ** 2))
        img = np.clip(img + fl[..., None] * C[0xF] * s * 1.3, 0, 1)
    if 38 <= t < 50:
        z = 1 + .15 * ease((t - 38) / 12); x0, y0 = W - W / z, H - H / z                               # anchored on the clock, in the corner
        img = cv2.warpAffine(img, np.float32([[z, 0, -x0 * z], [0, z, -y0 * z]]), (W, H), flags=cv2.INTER_LINEAR)
    if t < 3.6: img = img * ease((t - 3.0) / .6)
    if t >= 70.25:                                                                                     # then black, the one window, and how long it has been up
        end = np.zeros((H, W, 3), np.float32); a = tower(t)[60:100, 206:230].copy(); a[(a != 0xF) & (a != 0)] = 0; a[:, :4][a[:, :4] != 0xF] = 0
        U.blit(end, a, 96 + 206 * 2, 64 + 60 * 2, 2); U.text(end, 96, 548, 'UPTIME', C[0xA], 7); U.text(end, 100, 618, 'SINCE BEFORE TCP/IP', C[7], 2); U.strip(end, W - 16 * 12 - 24, 684)
        end = U.glow(end); u = ease((t - 70.25) / .5); img = img * (1 - u) + end * u
    return (np.clip(img, 0, 1) * 255).astype(np.uint8)

def _job(i):
    cv2.imwrite(f'out/hex/uptime/frames/f_{i:04d}.png', frame(i)[..., ::-1]); return i

if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == 'sheet':
        ts = [float(v) for v in a[1:]] or [1.5, 6, 8.5, 16, 19.6, 20.6, 25, 30, 33.7, 40, 49.5, 52.5, 55.5, 56.3, 59, 66, 69.5, 71.5]
        cells = [cv2.resize(frame(int(t * FPS)), (640, 360), interpolation=cv2.INTER_AREA) for t in ts]
        for c, t in zip(cells, ts): cv2.putText(c, f'{t:g} s', (8, 352), cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255), 1, cv2.LINE_AA)
        rows = [np.concatenate(cells[k:k + 3], 1) for k in range(0, len(cells) - len(cells) % 3 or len(cells), 3)]
        Path('out/hex').mkdir(parents=True, exist_ok=True); cv2.imwrite('out/hex/uptime_sheet.jpg', np.concatenate(rows, 0)[..., ::-1], [cv2.IMWRITE_JPEG_QUALITY, 88]); print('out/hex/uptime_sheet.jpg')
    else:
        from multiprocessing import Pool
        import subprocess
        Path('out/hex/uptime/frames').mkdir(parents=True, exist_ok=True); wp(); S1.watch_base(); btn('safe')
        with Pool(10) as pool:
            for k, _ in enumerate(pool.imap_unordered(_job, range(SECONDS * FPS), chunksize=8)):
                if k % 288 == 0: print(k, 'frames', flush=True)
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', 'out/hex/uptime/frames/f_%04d.png', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-movflags', '+faststart', 'out/hex/uptime/silent.mp4'], check=True)
        from backlot import sound as sd
        sd.mux('out/hex/uptime/silent.mp4', 'out/hex/uptime.wav', str(HERE / 'uptime.mp4'), loop_video=False, crf=20)
        cv2.imwrite(str(HERE / 'uptime_poster.png'), frame(int(33.7 * FPS))[..., ::-1]); print('wrote', HERE / 'uptime.mp4')
