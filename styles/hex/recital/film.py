"""SPACE OPERA (IN ONE ACT): the picture. Ninety-six seconds at 24 frames a second.

    uv run python styles/hex/recital/film.py sheet [seconds ...]     a contact sheet
    uv run python styles/hex/recital/film.py                         every frame, then the film with its sound (after music.py)

Everything that moves here moves because of events.json, the list of notes the song was made from. A player is
dark until their first note, moves while they play, and is still when they do not. The band is from before 2000
(sprites, on twos); the ribbons, the rose window and the line of the melody are from now (on ones).
"""
import sys, json, math
from pathlib import Path
HERE = Path(__file__).resolve().parent; sys.path.insert(0, str(HERE.parent / 'uptime')); sys.path.insert(0, str(HERE.parent))
import numpy as np
import cv2
import ui as U
from ui import C, W, H
import sprites as SP
FPS, SECONDS = 24, 96; NF = FPS * SECONDS
EV = json.load(open(HERE / 'events.json'))['events']                      # (t, dur, voice, midi, gain)
VOICES = sorted({e[2] for e in EV}); ON = {v: np.array([e[0] for e in EV if e[2] == v]) for v in VOICES}; END = {v: np.array([e[0] + e[1] for e in EV if e[2] == v]) for v in VOICES}
FIRST = {v: float(ON[v][0]) for v in VOICES}
VCOL = dict(harp=0xC, whistle=0xA, fiddle=0xE, lead=0xD, guitar=0xD, bass=5, organ=0xB, choir=7, rats=9)
NAMES = ['C-', 'C#', 'D-', 'D#', 'E-', 'F-', 'F#', 'G-', 'G#', 'A-', 'A#', 'B-']
clamp = lambda v: min(max(v, 0.0), 1.0)
ease = lambda v: (lambda u: u * u * (3 - 2 * u))(clamp(v))
DIM = {k: (0 if k == 0 else 2) for k in range(16)}                       # how someone looks before their first note

def playing(v, t):
    if v not in ON: return False
    k = np.searchsorted(ON[v], t, 'right'); return bool(k and np.any(END[v][max(k - 16, 0):k] > t))
def since(v, t):
    if v not in ON: return 99.0
    k = np.searchsorted(ON[v], t, 'right'); return float(t - ON[v][k - 1]) if k else 99.0

# what the lights do, frame by frame, worked out once from the notes
PC = np.zeros((NF + 2, 12), np.float32); PCV = np.zeros((NF + 2, 12), np.int32); SPEC = np.zeros((NF + 2, 16), np.float32)
for t0, d, v, m, g in EV:
    if v not in VCOL: continue
    f0 = int(t0 * FPS); fr = np.arange(f0, min(f0 + int((d + 1.2) * FPS), NF)); tt = fr / FPS - t0
    a = np.clip(np.exp(-np.maximum(tt, 0) / .3) + .55 * (tt < d), 0, 1) * min(1.0, .5 + g * 1.6)
    up = a > PC[fr, m % 12]; PC[fr[up], m % 12] = a[up]; PCV[fr[up], m % 12] = VCOL[v]
    b = int(np.clip((m - 33) / 4, 0, 15)); SPEC[fr, b] = np.maximum(SPEC[fr, b], a)
MEL = [(e[0], e[1], e[3], e[2]) for e in EV if e[2] in ('whistle', 'lead')]
TR = {}                                                                   # the tracker: step (a sixteenth) -> channel -> text
for t0, d, v, m, g in EV:
    ch = {'whistle': 0, 'fiddle': 1, 'lead': 2, 'harp': 3, 'bass': 4}.get(v); st = int(round(t0 / .125))
    if ch is not None: TR.setdefault(st, {})[ch] = f'{NAMES[m % 12]}{m // 12 - 1} {min(int(g * 128), 255):02X}'
    elif v in ('kick', 'snare', 'drum'): TR.setdefault(st, {})[5] = 'S' if v == 'snare' else 'K'

rng = np.random.default_rng(16)
STARS = np.zeros((H, W, 3), np.float32)
for gy in range(0, 470, 26):
    for gx in range(0, W, 26):
        x, y = gx + int(rng.integers(0, 26)), gy + int(rng.integers(0, 26)); s_ = int(rng.integers(1, 3)); STARS[y:y + s_, x:x + s_] = C[(8, 9, 9, 0xA, 0xC)[int(rng.integers(0, 5))]] * .8
SEEDS = [(float(rng.uniform(0, W)), float(rng.uniform(20, 440)), float(rng.uniform(0, 6))) for _ in range(34)]
BAND = [('harp', SP.SPIDER, 118, 372, {9: 9}), ('whistle', SP.DRUID, 286, 470, None), ('fiddle', SP.COWBOY, 388, 470, None), ('guitar', SP.BLOC, 490, 470, None), ('drum', SP.ACOLYTE, 616, 446, None),
        ('lead', SP.BLOC, 838, 470, None), ('organ', SP.FACULTY, 968, 470, None)]      # voice, sprite, x, where the feet are, palette

def sprite(img, rows, x, base, scale, lit, bob=0, swap=None, flip=False):
    U.sprite(img, rows, x, base - len(rows) * scale - bob, scale, swap=(swap if lit else DIM), flip=flip)

def stage(t):
    f = min(int(t * FPS), NF); p = int(t * 12); beat = t / .5; img = np.empty((H, W, 3), np.float32); img[:] = U.vgrad(H, C[0], U.mix(1, 2, .55)); img += STARS
    energy = float(SPEC[f].mean()); hot = 34 <= t < 50 or 66 <= t < 89
    # ribbons in a flow field: from now, on ones, coloured by where the song is
    ca, cb = ((3, 0xB) if t < 34 else (0xB, 0xC) if t < 66 else (0xC, 7)); lay = np.zeros((H, W, 3), np.float32); tf = min(t, 89.0)
    for k, (sx, sy, ph) in enumerate(SEEDS):
        pts = [(sx, sy)]
        for _ in range(46):
            x, y = pts[-1]; a = math.sin(x * .0042 + tf * .22 + ph) + math.cos(y * .0065 - tf * .17 + ph * .7); pts.append((x + 9 * math.cos(a * 1.4), y + 9 * math.sin(a * 1.4)))
        cv2.polylines(lay, [np.array(pts, np.int32)], False, [float(v) for v in U.mix(ca, cb, k / len(SEEDS))], 2, cv2.LINE_AA)
    img += cv2.GaussianBlur(lay, (0, 0), 1.6) * (.10 + .75 * energy) * (1 if t < 89 else max(0.0, 1 - (t - 89) * 2))
    # the rose window: twelve lights, one for each pitch class; the middle is the kick
    cx, cy = 640, 212; cv2.circle(img, (cx, cy), 146, [float(v) for v in C[8]], -1, cv2.LINE_AA); cv2.circle(img, (cx, cy), 138, [float(v) for v in C[0]], -1, cv2.LINE_AA)
    for k in range(12):
        a0, a1 = math.radians(k * 30 - 90 + 2.5), math.radians(k * 30 - 60 - 2.5); arc = [a0 + (a1 - a0) * j / 6 for j in range(7)]
        poly = [(cx + 132 * math.cos(a), cy + 132 * math.sin(a)) for a in arc] + [(cx + 48 * math.cos(a), cy + 48 * math.sin(a)) for a in arc[::-1]]
        cv2.fillPoly(img, [np.array(poly, np.int32)], [float(v) for v in (U.mix(1, 2, .5) * (1 - PC[f, k]) + C[PCV[f, k]] * PC[f, k])], cv2.LINE_AA)
    kp = math.exp(-since('kick', t) / .09) if 'kick' in ON else 0; cv2.circle(img, (cx, cy), 40, [float(v) for v in (C[2] * (1 - kp) + C[0xA] * kp)], -1, cv2.LINE_AA)
    # the organ's pipes are also the meter
    org = t >= FIRST['organ']
    for k in range(12):
        hgt = 60 + 12 * (5.5 - abs(k - 5.5)) + (95 * SPEC[f, 2 + k] if org else 0); x = 946 + k * 19
        U.rect(img, x, 470 - hgt, x + 15, 470, U.vgrad(int(hgt), U.mix(9, 0xB, .6 * SPEC[f, 2 + k]) if org else C[2], C[8] if org else C[1])); U.rect(img, x, 470 - hgt, x + 15, 470 - hgt + 3, C[0xA] if org else C[2])
    # the deck, and the choir, which hovers
    U.rect(img, 0, 470, W, 552, C[0]); U.rect(img, 0, 470, W, 473, C[8])
    ch = t >= FIRST['choir']; sing = playing('choir', t)
    for k in range(10):
        bx, by = 300 + (k % 5) * 40 + (20 if k >= 5 else 0), 262 + (k // 5) * 36 + (3 if (sing and p % 2) else 0)
        U.sprite(img, SP.DRONE, bx, by, 3, swap=None if ch else DIM)
        if sing: U.rect(img, bx + 30, by + 15, bx + 36, by + 21, C[0])                                    # they open their mouths together
    # the band
    for v, rows, x, base, swap in BAND:
        lit = t >= FIRST[v]; pl = playing(v, t) or since(v, t) < .12; sprite(img, rows, x, base, 4, lit, 4 if (pl and p % 2) else 0, swap, flip=(v == 'lead'))
        if not lit: continue
        if v == 'whistle' and pl: U.rect(img, x + 44, base - 62, x + 70, base - 58, C[0xA])
        if v == 'fiddle': U.rect(img, x + 40, base - 58, x + 52, base - 36, C[0xE]); cv2.line(img, (x + 30, int(base - 64 + (6 if (pl and p % 2) else 0))), (x + 66, int(base - 34 - (6 if (pl and p % 2) else 0))), [float(c) for c in C[0xA]], 2, cv2.LINE_AA)
        if v in ('guitar', 'lead'):
            s_ = -1 if v == 'lead' else 1; gx = x + (8 if v == 'lead' else 40)
            cv2.fillPoly(img, [np.array([(gx, base - 34), (gx + s_ * 22, base - 46), (gx + s_ * 16, base - 30), (gx + s_ * 24, base - 16)], np.int32)], [float(c) for c in C[0xD]], cv2.LINE_AA); cv2.line(img, (gx, base - 34), (gx - s_ * 34, base - 52), [float(c) for c in C[9]], 3, cv2.LINE_AA)
        if v == 'drum':
            kk = math.exp(-since('kick', t) / .08) if 'kick' in ON else 0; cv2.circle(img, (x + 24, base - 4), int(22 + 4 * kk), [float(c) for c in C[9]], 3, cv2.LINE_AA); U.rect(img, x - 30, base - 30, x - 4, base - 22, C[0xA] if since('snare', t) < .08 else C[9])
            cv2.line(img, (x + 54, base - 58), (x + 84, base - 62 + (5 if since('crash', t) < .2 else 0)), [float(c) for c in (C[0xA] if since('crash', t) < .2 else C[8])], 3, cv2.LINE_AA)
        if v == 'organ': U.rect(img, x - 8, base - 34, x + 62, base - 26, C[8]); U.rect(img, x - 4, base - 26, x + 58, base, C[1])
    for j in range(9):                                                                                 # the spider's web is a harp
        hx = 96 + j * 12; tw_ = since('harp', t) < .16 and (j + p) % 3 == 0
        cv2.line(img, (hx, 372), (hx + (2 if tw_ else 0), 468), [float(c) for c in (C[0xA] if tw_ else C[9] if t >= FIRST['harp'] else C[2])], 1, cv2.LINE_AA)
    U.rect(img, 90, 368, 200, 372, C[8]); U.rect(img, 90, 372, 94, 470, C[8]); U.rect(img, 196, 372, 200, 470, C[8])
    lit = t >= FIRST['bass']; pl = playing('bass', t); U.sprite(img, SP.NEWT, 736, 470 - 24 - (4 if (pl and p % 2) else 0), 6, swap=None if lit else DIM)        # a newt, on bass
    if lit: U.rect(img, 770, 386, 776, 462, C[9]); U.rect(img, 762, 440, 786, 468, C[5])
    # the pit: rats, bowing together
    lit = t >= FIRST['rats']; pl = playing('rats', t)
    for j, x in enumerate((196, 298, 400, 502, 746, 848, 950, 1052)):
        U.sprite(img, SP.RAT, x, 510, 4, swap=None if lit else DIM, flip=j >= 4)
        if lit: dx = (8 * math.sin(beat * math.pi) if pl else 0) * (-1 if j >= 4 else 1); cv2.line(img, (int(x + (4 if j >= 4 else 42) + dx), 512), (int(x + (-14 if j >= 4 else 60) + dx), 544), [float(c) for c in C[0xA]], 2, cv2.LINE_AA)
    # the song as a skyline along the front of the stage: every note of the tune, where it fell
    U.rect(img, 0, 552, W, 632, C[0]); U.rect(img, 0, 552, W, 553, C[8]); U.rect(img, 0, 631, W, 632, C[8])
    for t0, d, m, v in MEL:
        if t0 > t: break
        x0 = 40 + t0 / 96 * 1200; U.rect(img, x0, 626 - (m - 52) * 1.9, x0 + max(d / 96 * 1200, 2) + 1, 629 - (m - 52) * 1.9, C[0xA] if v == 'whistle' else C[0xD])
    U.rect(img, 40 + min(t, 89) / 96 * 1200, 556, 41 + min(t, 89) / 96 * 1200, 630, C[9], .5)
    return img, f

def witch(img, t):
    """She conducts with her back to us and is the only thing on the stage that is never lit."""
    beat = t / .5; bi = int(beat) % 4; ph = beat % 1; P = [(716, 606), (664, 570), (768, 570), (716, 512)]
    if t < 2: tip = (716, 606 - 40 * max(0.0, 1 - ph * 3))                                              # the count-in: four taps
    elif t < 89: a, b = P[bi], P[(bi + 1) % 4]; u = ease((ph - .5) / .5); tip = (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u)
    else: u = ease((t - 90.4) / 1.2); tip = (790 - 66 * u, 520 + 130 * u)                                # the cut-off, held; then the arm comes down
    turn = -10 * ease((t - 93.3) / .8)                                                                  # after the last note she looks, once, at the spider
    k0 = [float(v) for v in U.mix(1, 2, .35)]; ink = [float(v) for v in C[0]]; rim = [float(v) for v in U.mix(0xF, 0, .35)]      # never lit, but a shade off the dark she stands in
    U.rect(img, 560, 610, 578, 617, C[0xF]); U.rect(img, 568, 617, 570, 700, C[8])                      # her lamp: the one tended light
    cloak = np.array([(596, 566), (688, 566), (716, 720), (568, 720)], np.int32); brim = np.array([(558 + turn, 546), (726 + turn, 546), (726 + turn, 562), (558 + turn, 562)], np.int32)
    cone = np.array([(604 + turn, 546), (680 + turn, 546), (642 + turn * 1.6, 424)], np.int32)
    for poly in (cloak, brim, cone): cv2.fillPoly(img, [poly], k0, cv2.LINE_AA); cv2.polylines(img, [poly], True, ink, 2, cv2.LINE_AA)
    cv2.line(img, (596, 568), (570, 716), rim, 3, cv2.LINE_AA); cv2.line(img, (int(558 + turn), 547), (int(604 + turn), 547), rim, 3, cv2.LINE_AA)      # the lamp catches one edge of her
    cv2.line(img, (int(604 + turn), 546), (int(642 + turn * 1.6), 424), rim, 3, cv2.LINE_AA)
    hand = (682 + (tip[0] - 682) * .55, 580 + (tip[1] - 580) * .55); cv2.line(img, (678, 578), (int(hand[0]), int(hand[1])), k0, 14, cv2.LINE_AA)
    cv2.circle(img, (int(hand[0]), int(hand[1])), 7, [float(v) for v in C[6]], -1, cv2.LINE_AA); cv2.line(img, (int(hand[0]), int(hand[1])), (int(tip[0]), int(tip[1])), [float(v) for v in C[0xA]], 3, cv2.LINE_AA)
    return hand

SCROLL = '*** R/V PERIMETER *** FACULTY RECITAL *** SPACE OPERA (IN ONE ACT) *** ALL VOICES LIVE *** NO APPLAUSE *** '
def hud(img, t, f):
    x, y, w, h = U.window(img, 16, 14, 372, 118, 'HEXAMP', 'sys'); k = int(t * 4) % len(SCROLL)
    U.text(img, x + 8, y + 8, (SCROLL * 2)[k:k + 22], C[7], 2); U.text(img, x + 8, y + 34, f'{int(t) // 60:02d}:{int(t) % 60:02d}', C[0xA], 3)
    U.text(img, x + 8, y + 64, 'KEY: D MINOR' if t < 66 else 'KEY: E MINOR', C[9] if t < 66 or t > 70 else C[0xE], 2)
    for b in range(16): hh = 4 + int(44 * SPEC[f, b]); U.rect(img, x + 216 + b * 9, y + 80 - hh, x + 223 + b * 9, y + 80, U.vgrad(hh, C[7], C[5]))
    x, y, w, h = U.window(img, W - 372, 14, 356, 206, 'SPACE_OPERA.MOD', 'sys'); st = int(t / .125)
    for r in range(-8, 9):
        s_ = st + r
        if s_ < 0: continue
        row = TR.get(s_, {}); txt = f'{s_ % 256:02X} ' + ' '.join(row.get(c_, '... ..') for c_ in range(5)) + ' ' + row.get(5, '.')
        if r == 0: U.rect(img, x + 2, y + 4 + 8 * 10, x + w - 2, y + 4 + 9 * 10, C[0xB])
        U.text(img, x + 6, y + 5 + (r + 8) * 10, txt, C[0xA] if r == 0 else C[7] if row else C[8], 1)

def frame(i):
    t = i / FPS; img, f = stage(t)
    img *= .18 + .82 * ease((t - 1.7) / 1.3)                                                             # the house lights are down until she has tapped four times
    if t >= 89: img *= 1 - .4 * ease((t - 89) / .15)                                                    # when she cuts it off the stage goes down with the sound
    hand = witch(img, t)
    hot = 34 <= t < 50 or 66 <= t < 89; bounce = 7 if (hot and (t / .5) % 1 < .25) else 0               # the crowd, in front of us, with its torches up
    for row, (base, off) in enumerate(((694, 0), (724, 22))):
        for x in range(-10 + off, W, 44): U.sprite(img, SP.MOB, x, base - 56 - (bounce if (x // 44 + row) % 2 == 0 else 0), 4, swap={2: 1 if row else 0, 9: 2, 0xA: 2, 8: 2})
    hud(img, t, f)
    if since('crash', t) < 3 / 24: img *= 1 + .14 * (1 - since('crash', t) * 8)
    if 90 <= t < 92.35:
        bt = U.dialog(img, 410, 236, 460, 'HEX', ['APPLAUSE?'], ['ALLOW', 'DENY', 'NEWTS'], 'sys', 1 if 92 <= t < 92.35 else None)[1]
        u = ease((t - 90.5) / 1.2); U.pointer(img, hand[0] + (bt[0] + bt[2] * .55 - hand[0]) * u, hand[1] + (bt[1] + bt[3] * .55 - hand[1]) * u, 6)
    img = U.glow(np.clip(img, 0, 1))
    if t >= 94.3:
        end = np.zeros((H, W, 3), np.float32); U.rect(end, 560, 610, 578, 617, C[0xF]); U.text(end, 60, 640, 'SPACE OPERA (IN ONE ACT)', C[0xA], 4); U.text(end, 64, 686, 'R/V PERIMETER. NO APPLAUSE.', C[7], 2); U.strip(end, W - 16 * 12 - 24, 684)
        u = ease((t - 94.3) / .7); img = img * (1 - u) + U.glow(end) * u
    return (np.clip(img, 0, 1) * 255).astype(np.uint8)

def _job(i):
    cv2.imwrite(f'out/hex/recital/frames/f_{i:04d}.png', frame(i)[..., ::-1]); return i

if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == 'sheet':
        ts = [float(v) for v in a[1:]] or [1.2, 6, 14, 22, 30, 40, 53, 62, 70, 86, 91.5, 95.5]
        cells = [cv2.resize(frame(int(t * FPS)), (640, 360), interpolation=cv2.INTER_AREA) for t in ts]
        for c, t in zip(cells, ts): cv2.putText(c, f'{t:g} s', (8, 352), cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255), 1, cv2.LINE_AA)
        rows = [np.concatenate(cells[k:k + 3], 1) for k in range(0, len(cells) - len(cells) % 3 or len(cells), 3)]
        Path('out/hex').mkdir(parents=True, exist_ok=True); cv2.imwrite('out/hex/recital_sheet.jpg', np.concatenate(rows, 0)[..., ::-1], [cv2.IMWRITE_JPEG_QUALITY, 88]); print('out/hex/recital_sheet.jpg')
    else:
        from multiprocessing import Pool
        import subprocess
        Path('out/hex/recital/frames').mkdir(parents=True, exist_ok=True)
        with Pool(10) as pool:
            for k, _ in enumerate(pool.imap_unordered(_job, range(NF), chunksize=8)):
                if k % 576 == 0: print(k, 'frames', flush=True)
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', 'out/hex/recital/frames/f_%04d.png', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-movflags', '+faststart', 'out/hex/recital/silent.mp4'], check=True)
        from backlot import sound as sd
        sd.mux('out/hex/recital/silent.mp4', 'out/hex/recital.wav', str(HERE / 'space_opera.mp4'), loop_video=False, crf=20)
        cv2.imwrite(str(HERE / 'space_opera_poster.png'), frame(int(40 * FPS))[..., ::-1]); print('wrote', HERE / 'space_opera.mp4')
