"""Keepalive, the film: a recorded walk through the game. 84 seconds, 24 a second; a beat is a second.

The camera never moves. Every picture is one of the stills in game.py, in registers; between two places is a
dissolve of pixels; the sea is colour cycling, six steps a second; the hand and the log are drawn in registers
too. So every pixel of every frame is one of the sixteen.

    python film.py            render, add the sound, write keepalive.mp4
    python film.py sheet      a contact sheet            python film.py sync | pops
"""
import sys, math
from pathlib import Path
HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE)); sys.path.insert(1, str(HERE.parent)); sys.path.insert(2, str(ROOT))
import numpy as np, cv2
import stage2 as S2, game as G, deep as X, kit

FPS, SECONDS = 24, 84; NF = FPS * SECONDS; W, H = S2.W, S2.H; OUT = G.OUT; FRAMES = OUT / 'frames'
SEG = [(0, 'jetty'), (4, 'path'), (7, 'shelter'), (10, 'book'), (15, 'beacon'), (18, 'lookout'), (23, 'beacon'), (29, 'lookout'), (33, 'book'), (36, 'beacon'), (38, 'lookout'),
       (42, 'beacon'), (49, 'lookout'), (53, 'glass'), (64, 'book'), (70, 'sea'), (84, None)]
HER1, HER2 = [20.0, 20.5, 21.0], [39.0, 39.5, 40.0, 40.5, 41.0]             # she sends three; then five
MINE1, MINE2 = [27.5, 28.0, 28.5], [45.5, 46.0, 46.5, 47.0, 47.5, 48.0]     # you answer three (wrong); then six
DIAL = [(24.5, 1), (25.0, 2), (25.5, 3), (43.0, 4), (43.5, 5), (44.0, 6)]
ALIVE = [(62.0, 'her'), (63.0, 'me'), (72.0, 'her'), (72.5, 'me'), (76.0, 'her'), (76.5, 'me'), (80.0, 'her'), (80.5, 'me')]
BL = .25                                                                      # how long a blink or a dip lasts
def _in(t, ts): return any(a <= t < a + BL for a in ts)

def state(t):
    """What is so at time t: (lamp, lever, dial, lit, linked)."""
    dial = max([d for a, d in DIAL if t >= a] + [0])
    if t < 17.0: lamp = lever = False
    elif t < 31.0: lamp = lever = True
    elif t < 37.0: lamp = lever = False                                       # refused: the beacon is put out
    else: lamp = lever = True
    if _in(t, [27.0, 45.0]): lever = False                                    # the lever worked, to send
    if _in(t, MINE1 + MINE2) or _in(t, [a for a, w in ALIVE if w == 'me']): lamp = False
    lit = t >= 50.0 and not _in(t, [a for a, w in ALIVE if w == 'her'])
    if _in(t, HER1 + HER2): lit = True
    return dict(lamp=lamp, lever=lever, dial=dial, lit=lit, linked=t >= 50.0)

def node(t): return [n for a, n in SEG if a <= t][-1]
def view(nd, st):
    """The still for a place in a state (only what that place can see goes into the key)."""
    if nd == 'book': return G.still('book', linked=st['linked'])
    if nd == 'beacon': return G.still('beacon', lamp=st['lamp'], lever=st['lever'], dial=st['dial'])
    if nd == 'glass': return G.still('glass', lit=st['lit'])
    if nd in ('lookout', 'sea'): return G.still(nd, lamp=st['lamp'], lit=st['lit'])
    return G.still(nd)
def all_views():
    seen = {}
    for i in range(NF):
        t = i / FPS; nd = node(t); st = state(t); k = (nd, tuple(sorted(st.items()))) if nd in ('beacon', 'lookout', 'sea', 'glass', 'book') else (nd,)
        seen[(nd, st['lamp'], st['lever'], st['dial'], st['lit'], st['linked'])] = (nd, st)
    return list(seen.values())

# ------------------------------------------------------------------ the hand
HAND = ['..00.........', '.0AA0........', '.0AA0........', '.0AA0........', '.0AA000......', '.0AA0AA000...', '.0AA0AA0AA00.', '00AA0AA0AA0A0', '0A0AAAAAAAAA0', '0AAAAAAAAAAA0', '0AAAAAAAAAAA0', '.0AAAAAAAAAA0', '.0AAAAAAAAA0.', '..0AAAAAAAA0.', '..0AAAAAAA0..', '...0000000...']
def _spr(rows): return np.array([[255 if c == '.' else int(c, 16) for c in r] for r in rows], np.uint8)
HANDS = dict(up=_spr(HAND), down=_spr([r.replace('A', '9') for r in HAND]))
def C(nd, name): return G.centre(nd, name)
BOT = (320, 338)
def keys():
    """Where the hand is: (seconds, x, y). It goes to a thing, then presses."""
    k = [(1.0, 300, 320), (3.5, *C('jetty', 'path')), (4.0, *C('jetty', 'path')), (6.5, *C('path', 'shelter')), (7.0, *C('path', 'shelter')), (9.5, *C('shelter', 'book')), (10.0, *C('shelter', 'book')),
         (11.0, 44, 86), (12.3, 44, 122), (13.6, 44, 158), (14.7, *BOT), (15.0, *BOT), (16.6, *C('beacon', 'lever')), (17.2, *C('beacon', 'lever')), (17.9, *C('beacon', 'lookout')), (18.0, *C('beacon', 'lookout')),
         (19.0, 210, 250), (22.2, 210, 250), (22.8, *BOT), (23.0, *BOT), (24.2, *C('beacon', 'dial')), (25.8, *C('beacon', 'dial')), (26.7, *C('beacon', 'lever')), (27.3, *C('beacon', 'lever')), (28.8, *C('beacon', 'lookout')), (29.0, *C('beacon', 'lookout')),
         (30.0, 210, 250), (31.3, 210, 250), (31.5, 222, 250), (31.7, 198, 250), (31.9, 222, 250), (32.1, 210, 250), (32.8, *BOT), (33.0, *BOT), (34.0, 44, 122), (35.3, 250, 142), (35.8, *BOT), (36.0, *BOT),
         (36.7, *C('beacon', 'lever')), (37.2, *C('beacon', 'lever')), (37.9, *C('beacon', 'lookout')), (38.0, *C('beacon', 'lookout')), (39.0, 210, 250), (41.3, 210, 250), (41.8, *BOT), (42.0, *BOT),
         (42.7, *C('beacon', 'dial')), (44.2, *C('beacon', 'dial')), (44.7, *C('beacon', 'lever')), (45.3, *C('beacon', 'lever')), (48.8, *C('beacon', 'lookout')), (49.0, *C('beacon', 'lookout')),
         (50.0, 210, 250), (51.5, 210, 250), (52.6, *C('lookout', 'glass')), (53.0, *C('lookout', 'glass')), (55.0, 420, 250), (57.6, 400, 200)]
    k += [(58.0 + j * .2, 400 + (16 if j % 2 else -16), 196) for j in range(9)] + [(60.0, 400, 200), (63.2, 400, 200), (63.7, *BOT), (64.0, *BOT), (66.0, 470, 290), (69.2, 470, 290), (69.7, *BOT), (70.0, *BOT)]
    return k
CLICKS = [4, 7, 10, 15, 17, 18, 23, 24.5, 25, 25.5, 27, 29, 33, 36, 37, 38, 42, 43, 43.5, 44, 45, 49, 53, 64, 70]
_K = None
def hand(idx, t):
    global _K
    if _K is None: _K = keys()
    if not 1.0 <= t < 70.3: return
    a = [k for k in _K if k[0] <= t][-1]; b = ([k for k in _K if k[0] > t] or [a])[0]; u = 0 if b[0] == a[0] else (t - a[0]) / (b[0] - a[0]); u = u * u * (3 - 2 * u)
    x, y = int(a[1] + (b[1] - a[1]) * u), int(a[2] + (b[2] - a[2]) * u); sp = HANDS['down' if any(0 <= t - c < .14 for c in CLICKS) else 'up']
    x0, y0 = min(max(x - 3, 0), W - sp.shape[1]), min(max(y, 0), H - sp.shape[0]); sub = idx[y0:y0 + sp.shape[0], x0:x0 + sp.shape[1]]; m = sp != 255; sub[m] = sp[m]

# ------------------------------------------------------------------ the log: literal, and never wrong
def lines():
    L = [(17.0, '> HELLO', 0xA)] + [(a, '< %d' % (k + 1), 6) for k, a in enumerate(HER1)] + [(a, '> %d' % (k + 1), 0xA) for k, a in enumerate(MINE1)] + [(31.0, '< NO.', 6), (31.75, 'YOUR LAMP IS OUT.', 9), (37.0, '> HELLO', 0xA)]
    L += [(a, '< %d' % (k + 1), 6) for k, a in enumerate(HER2)] + [(a, '> %d' % (k + 1), 0xA) for k, a in enumerate(MINE2)] + [(50.0, '< YES.  LINK UP.', 6), (58.0, '> (YOU WAVE.)', 0xA), (60.0, '<', 6), (62.0, '< STILL HERE.', 6), (63.0, '> STILL HERE.', 0xA), (66.0, '0 WORDS SENT.  0 RECEIVED.', 9)]
    L += [(a, ('< ' if w == 'her' else '> ') + 'STILL HERE.', 6 if w == 'her' else 0xA) for a, w in ALIVE if a >= 70]
    return sorted(L)
_L = None
def log(idx, t):
    global _L
    if _L is None: _L = lines()
    S2.rect(idx, 0, H - 14, W, H, 0)
    for k in range(16): S2.rect(idx, W - 6 - (16 - k) * 6, H - 10, W - 6 - (16 - k) * 6 + 5, H - 5, k)
    got = [l for l in _L if l[0] <= t]
    if got: S2.text(idx, 8, H - 11, got[-1][1], got[-1][2])
    if len(got) > 1 and t - got[-1][0] < 3 and got[-2][0] > got[-1][0] - 6: S2.text(idx, 200, H - 11, got[-2][1], 8 if got[-2][2] != 6 else 5)
def big(idx, x, y, s, reg, k=4):
    for i, ch in enumerate(s):
        g = np.kron(kit.glyph(ch), np.ones((k, k), bool)); sub = idx[y:y + 8 * k, x + i * 8 * k:x + (i + 1) * 8 * k]; sub[g[:sub.shape[0], :sub.shape[1]]] = reg
def title(idx, t):
    if t >= 76.0: s = 'KEEPALIVE'; S2.rect(idx, 0, 40, W, 132, 0); big(idx, (W - len(s) * 32) // 2, 52, s, 0xF, 4)
    if t >= 80.0: s = 'NOTHING TO SEND.  STILL HERE.'; S2.text(idx, (W - len(s) * 8) // 2, 104, s, 0xA)

def picture(i):
    t = i / FPS; nd = node(t); idx, cyc = view(nd, state(t)); img = cyc.at(idx, i // 4)
    t0 = max(a for a, n in SEG if a <= t); k = i - int(t0 * FPS)
    if t0 > 0 and k < 5:                                                   # the change of place: half of it at once, on the beat, the rest in four frames
        pn = node(t0 - .01); pidx, pcyc = view(pn, state(t0 - .01)); img = S2.dissolve(pcyc.at(pidx, i // 4), img, (.5, .68, .82, .92, .97)[k])
    return img
def frame(i):
    t = i / FPS; idx = picture(i).copy(); log(idx, t); title(idx, t); hand(idx, t); return idx
def save(i): X.save(str(FRAMES / ('f_%04d.png' % i)), S2.rgb(frame(i), 2)); return i

POINTS = [(4, 'to the path'), (7, 'to the shelter'), (10, 'the book'), (15, 'to the beacon'), (17, 'the lever: HELLO'), (18, 'to the lookout'), (20.0, 'she blinks'), (20.5, 'she blinks'), (21.0, 'she blinks'), (23, 'to the beacon'),
          (24.5, 'dial 1'), (25, 'dial 2'), (25.5, 'dial 3'), (27, 'the lever: send'), (27.5, 'a dip'), (28, 'a dip'), (28.5, 'a dip'), (29, 'to the lookout'), (31, 'NO: the beacon goes out'), (33, 'the book again'), (36, 'to the beacon'), (37, 'the lever: HELLO'),
          (38, 'to the lookout'), (39, 'she blinks'), (41, 'she blinks, the fifth'), (42, 'to the beacon'), (43, 'dial 4'), (44, 'dial 6'), (45, 'the lever: send'), (45.5, 'a dip'), (48, 'a dip, the sixth'), (49, 'to the lookout'), (50, 'her window lights: LINK UP'),
          (53, 'the spyglass'), (58, 'the wave'), (62, 'her lamp dips'), (64, 'the book'), (70, 'from the sea'), (72, 'her lamp dips'), (72.5, 'the beacon answers'), (76, 'title'), (80, 'NOTHING TO SEND')]
if __name__ == '__main__':
    a = sys.argv[1:]; from multiprocessing import Pool
    if not a or a[0] == 'sheet':
        vs = all_views(); print(len(vs), 'stills')
        with Pool(14) as pool: pool.starmap(view, vs)
    if a and a[0] == 'sheet':
        ts = [float(v) for v in a[1:]] or [2, 5.5, 8.5, 12, 16, 17.5, 20.1, 24, 25.6, 27.6, 30, 31.5, 34.5, 37.5, 40.6, 44.5, 46.1, 50.5, 55, 58.6, 62.1, 67, 72.1, 72.6, 78, 82]
        ims = [(S2.rgb(frame(int(round(t * FPS))), 1)[..., ::-1] * 255).astype(np.uint8) for t in ts]
        for im, t in zip(ims, ts): cv2.putText(im, '%gs' % t, (6, 14), cv2.FONT_HERSHEY_SIMPLEX, .45, (255, 255, 255), 1, cv2.LINE_AA)
        while len(ims) % 3: ims.append(np.zeros_like(ims[0]))
        for k in range(0, len(ims), 12): cv2.imwrite(str(OUT / ('sheet_%d.jpg' % (k // 12))), np.vstack([np.hstack(ims[j:j + 3]) for j in range(k, min(k + 12, len(ims)), 3)]), [cv2.IMWRITE_JPEG_QUALITY, 92])
    elif a and a[0] in ('sync', 'pops'):
        from backlot import sync
        if a[0] == 'sync': sync.check(POINTS, str(FRAMES), str(OUT / 'keepalive.wav'), fps=FPS, out_jpg=str(HERE / 'keepalive_sync.jpg'), out_json=str(OUT / 'sync.json'))
        else:
            for row in sync.pops(POINTS, str(FRAMES), fps=FPS): print(row)
    else:
        import subprocess
        FRAMES.mkdir(parents=True, exist_ok=True)
        with Pool(24) as pool: list(pool.imap_unordered(save, range(NF), chunksize=24))
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', str(FRAMES / 'f_%04d.png'), '-i', str(OUT / 'keepalive.wav'), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-preset', 'slow',
                        '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', '-shortest', str(HERE / 'keepalive.mp4')], check=True)
        X.save(str(HERE / 'keepalive_poster.png'), S2.rgb(frame(int(51 * FPS)), 2)); print('wrote', HERE / 'keepalive.mp4')
