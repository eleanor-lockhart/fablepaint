"""Base Case: the older pictures. The same house, printed the way each machine in each basement would print it.

    level 1   1989: sixteen colours, ordered dither, a figure that shrinks as she walks away, a parser
    level 2   1987: one bit, a window with a striped title bar, cards that change with a visual effect
    level 3   1980: white lines on black, forty columns of text, and nothing else. This is where she lives.

All three are the model in house.py through `backlot.depth`, at the machine's own resolution, with a different
`print` at the end. Nothing here is drawn twice.
"""
import sys, math
from functools import lru_cache
from pathlib import Path
HERE = Path(__file__).resolve().parent; sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(HERE.parents[2]))
import numpy as np
import cv2
from backlot.space import Camera
from backlot import depth as D
import deep as X, house as Hs, cast as CA
from kit import Canvas, BAYER
from house import PX, FX, FLOOR
W, H = 1280, 720; T = X.table(); S = Hs.build()
SC = np.array([Hs.SCREEN['corner'][0] - .2, 4.405, Hs.SCREEN['corner'][2] - .1125]); CHAIR = np.array(Hs.SPOT['chair'])
CAMS = dict(section=((9.25, -19, 1.7), (9.25, 0, .95), 35), pantry=((PX - 1.9, 4.85, 1.5), (PX + 2.2, 4.85, .2), 32), room=((FX + 5.3, -5.6, -1.5), (FX + 5.3, 3, -1.5), 35), room3=((FX + 7.4, -5.6, -1.45), (FX + 7.4, 3, -1.45), 35),
            trap=((PX - .2, 4.85, 1.55), (PX + 2.3, 4.85, .15), 26), stair=((PX + 3.9, 4.45, FLOOR + 1.3), (FX + 7.6, 4.95, FLOOR + .95), 28), pov=((SC[0], 4.405 + .575, SC[2]), tuple(SC), 35))
COMPUTER = ('monitor', 'tower', 'keyboard')
def camera(view, w, h): e, l, lens = CAMS[view]; return Camera(e, look=l, lens=lens, size=(w, h))

@lru_cache(maxsize=96)
def scene(view, w, h, lid=0, lit=False, ego=None, who=False, computer=True, leak=False):
    """The model through one of the fixed cameras, at w x h. ego: (pose, x, y, z, flip). Returns (g, level)."""
    cam = camera(view, w, h); om = (('wall.n', 'earth.n', 'pipe') if view == 'pov' else ()) + (() if computer else COMPUTER)
    things = [q for q in S.solids if not any(q.name == o or q.name.startswith(o + '.') for o in om)] + Hs.lid(lid) + Hs.tube(float(lit)) + Hs.led(float(lit)) + Hs.bulb(float(lit))
    if view == 'section': things += Hs.windows([lit] * 7)
    if view == 'pov': things += Hs.cut()
    if computer: things += Hs.screen(None, 1.0 if lit else 0.0, 0xF if lit and view != 'pov' else 0)
    if leak: things += Hs.leak(0.0, 0)
    if ego: things.append(D.card('ego', CA.child(ego[0], ego[4], dark=True), ego[1:4], cam.right, cast=False))
    if who: things.append(D.card('witch', CA.witch(flip=True), (CHAIR[0] - .15, CHAIR[1] - .3, FLOOR), cam.right, texel=.078, cast=False))
    g = D.gbuffer(things, cam)
    lv = D.lighting(g, [D.Light(cam.eye + (0, 0, .4), .8, 7.0, shadow=False)] + ([D.Light(np.array(Hs.SPOT['tube']), .9, 4.5, shadow=False)] if lit else []), ambient=.62 if lit else .4)
    return g, lv

# ------------------------------------------------------------------ three ways to print
CAND = np.array([0, 1, 2, 3, 4, 8, 9, 10, 11, 12, 13, 14])           # no F until it is returned; no green, ever, but hers
def print16(g, lv):
    """Sixteen colours and a 4 x 4 ordered dither, as a paint program of the time would have reduced it."""
    rgb = X.colour(g, np.where(g['flat'], 1.0, lv), steps=255, dither=0); h, w = lv.shape; yy, xx = np.mgrid[:h, :w]
    q = rgb + ((BAYER[yy % 4, xx % 4] - .5) * .15)[..., None]
    idx = CAND[np.argmin(((q[:, :, None, :] - T[CAND][None, None]) ** 2).sum(-1), -1)].astype(np.uint8)
    keep = g['flat'] & (g['index'] < 16); idx[keep] = g['index'][keep]; idx[(g['index'] == 0xF) & (g['glow'] > 0)] = 0xF; idx[~g['hit']] = 0
    return idx
def print1(g, lv):
    """One bit: tone becomes pattern, and every edge gets a black line."""
    rgb = X.colour(g, lv, steps=255, dither=0); L = (rgb @ np.array([.3, .59, .11], np.float32)) ** .75; h, w = lv.shape; yy, xx = np.mgrid[:h, :w]
    idx = np.where(L > BAYER[yy % 4, xx % 4] * .78 + .02, 0xA, 0).astype(np.uint8); idx[D.edges(g)] = 0
    idx[(g['index'] == 0xF) & (g['glow'] > 0)] = 0xF; idx[~g['hit']] = 0
    return idx
def printL(g, ink=0xA, upto=1.0):
    """Lines only, hidden lines removed. upto: how much of it the plotter has drawn so far (solid by solid)."""
    e = D.edges(g); order = g['solid'].astype(np.float64); n = max(order.max(), 1)
    idx = np.where(e & (order / n <= upto), ink, 0).astype(np.uint8); keep = g['flat'] & (g['index'] < 16)
    idx[cv2.dilate(keep.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0] = ink; idx[keep] = g['index'][keep]      # a figure gets a line round it too, or a black hat on a black screen is no hat
    return idx

def up(idx, k):
    """An index canvas as a full-size picture, hard pixels."""
    return np.repeat(np.repeat(T[idx], k, 0), k, 1)
def zoom(outer, rect, inner, u):
    """Go into a screen. outer, inner: full-size pictures. rect: (x0, y0, x1, y1) in outer, 16:9. u: 0 is the
    outer picture as it is, 1 is the rectangle filling the frame. The inner picture is always sharp."""
    x0, y0, x1, y1 = rect; s1 = W / (x1 - x0); s = s1 ** u; fx, fy = x0 * s1 / (s1 - 1), y0 * s1 / (s1 - 1)
    out = cv2.warpAffine(outer, np.float32([[s, 0, fx * (1 - s)], [0, s, fy * (1 - s)]]), (W, H), flags=cv2.INTER_NEAREST)
    a0, b0, a1, b1 = [int(round(v)) for v in ((x0 - fx) * s + fx, (y0 - fy) * s + fy, (x1 - fx) * s + fx, (y1 - fy) * s + fy)]
    a0, b0, a1, b1 = max(a0, 0), max(b0, 0), min(a1, W), min(b1, H)
    if a1 > a0 and b1 > b0: out[b0:b1, a0:a1] = cv2.resize(inner, (a1 - a0, b1 - b0), interpolation=cv2.INTER_AREA)
    return out
def nest(idx, rect, inner):
    """An index canvas with another, smaller, pasted where its screen is (for a screen in a screen in a screen)."""
    x0, y0, x1, y1 = [int(round(v)) for v in rect]; out = idx.copy(); out[y0:y1, x0:x1] = cv2.resize(inner, (x1 - x0, y1 - y0), interpolation=cv2.INTER_NEAREST); return out
def typed(s, t, t0, cps=14.0): return s[:max(0, int((t - t0) * cps))]
def wipe(a, b, u):
    """Curtains opening from the middle."""
    out = a.copy(); w = a.shape[1]; k = int(w / 2 * u); out[:, w // 2 - k:w // 2 + k] = b[:, w // 2 - k:w // 2 + k]; return out
def iris(a, b, u):
    h, w = a.shape[:2]; yy, xx = np.mgrid[:h, :w]; m = np.hypot(xx - w / 2, yy - h / 2) < u * math.hypot(w, h) / 2; out = a.copy(); out[m] = b[m]; return out
_dz = np.random.default_rng(3).random((360, 640))
def dissolve(a, b, u): out = a.copy(); m = _dz[:a.shape[0], :a.shape[1]] < u; out[m] = b[m]; return out

# ------------------------------------------------------------------ level 1: 1989
def _box(c, lines, y=None):
    w = max(len(l) for l in lines) * 8 + 16; h = len(lines) * 10 + 12; x = (320 - w) // 2; y = (180 - h) // 2 if y is None else y
    c.rect(x - 2, y - 2, x + w + 2, y + h + 2, 0); c.rect(x, y, x + w, y + h, 0xA); c.rect(x + 2, y + 2, x + w - 2, y + 3, 0xB); c.rect(x + 2, y + h - 3, x + w - 2, y + h - 2, 0xB); c.rect(x + 2, y + 2, x + 3, y + h - 2, 0xB); c.rect(x + w - 3, y + 2, x + w - 2, y + h - 2, 0xB)
    for k, l in enumerate(lines): c.text(x + 8, y + 7 + k * 10, l, 0)
def _l1(idx, lit, parser=None):
    c = Canvas(320, 180); c.a = idx.copy(); c.rect(0, 0, 320, 9, 0xA); c.text(4, 1, 'BASE CASE', 0); c.text(96, 1, 'LIGHTS: %d OF 5' % (7 if lit else 0), 0)
    if parser is not None: c.rect(0, 170, 320, 180, 0); c.text(2, 171, parser, 0xA)
    return c
R1 = (160 - .3382 * 320, 90 - .3382 * 180, 160 + .3382 * 320, 90 + .3382 * 180)      # where the glass is in the 320 x 180 view from her eyes
def l1_title():
    g, lv = scene('section', 320, 180); c = _l1(print16(g, lv), False); _box(c, ['SO YOU WANT THE LIGHTS ON', '', '      PRESS ANY KEY'], 104); return c.a
def l1_pov(lit=False, inner=None):
    g, lv = scene('pov', 320, 180, lit=lit); c = _l1(print16(g, lv), lit); a = c.a
    return nest(a, R1, inner) if inner is not None else a
def l1(t, lit=False):
    """Level 1 at time t (32 to 38.6): a 320 x 180 index canvas."""
    tq = math.floor(t * 8) / 8                                      # on threes, as these games were
    P = lambda f: (round(float(f[0]), 3), round(float(f[1]), 3), round(float(f[2]), 3))
    if t < 32.8: return l1_title()
    if t < 36.0:                                                    # the pantry: she is already at the hatch
        ang = 0 if tq < 34.6 else (40 if tq < 34.85 else 78)
        if tq < 35.2: f = np.array([PX + .95, 4.85, 0]); pose = 'kneel' if 34.4 <= tq < 35.0 else 'back'
        else: k = min(int((tq - 35.2) / .13) + 1, 7); f = Hs.stair(k); pose = ('back_b', 'back_c')[k % 2]
        g, lv = scene('pantry', 320, 180, lid=ang, ego=(pose, *P(f), False), leak=ang == 0)
        c = _l1(print16(g, lv), False, '>' + typed('LIFT TRAPDOOR', t, 32.9) + ('_' if int(t * 4) % 2 and t < 34.0 else '') if t < 35.7 else '>')
        if 34.0 <= t < 35.7: _box(c, ['IT IS HEAVY. YOU ARE NINE.', 'IT OPENS ANYWAY.'], 38)
        return c.a
    d = tq - 36.1                                                   # the basement: down the last steps, along, round the desk
    if d < .84: k = int(np.clip(int(d / .12) + 6, 6, 12)); f = Hs.stair(k); pose = ('pass', 'stand')[k % 2]
    else:
        pts = [(PX + 3.6, 4.85), (FX + 4.1, 4.3), (FX + 6.95, 4.3), (FX + 7.05, 5.0), (FX + 7.8, 5.0)]; seg = [math.dist(pts[i], pts[i + 1]) for i in range(4)]; far = (d - .84) * 3.4; dd = min(far, sum(seg) - 1e-3); i = 0
        while dd > seg[i]: dd -= seg[i]; i += 1
        p = np.array(pts[i]) + (np.array(pts[i + 1]) - np.array(pts[i])) * dd / seg[i]; f = np.array([p[0], p[1], FLOOR]); pose = ('stride', 'pass')[int(tq * 8) % 2] if far < sum(seg) else 'stand'
    g, lv = scene('room', 320, 180, lid=78, ego=(pose, *P(f), False))
    c = _l1(print16(g, lv), False, '>')
    if 37.2 <= t < 38.6: _box(c, ['A COMPUTER, LEFT ON.', 'OF COURSE THERE IS.'], 38)
    return c.a

# ------------------------------------------------------------------ level 2: 1987
PIC2 = (80, 46, 560, 316)                                           # where the picture sits in the 640 x 360 screen: 480 x 270
R2 = (PIC2[0] + 240 - .3382 * 480, PIC2[1] + 135 - .3382 * 270, PIC2[0] + 240 + .3382 * 480, PIC2[1] + 135 + .3382 * 270)
CARDS = dict(A=('trap', dict(lid=0, leak=True), 'A TRAP DOOR. YOU HAVE TO LIFT IT.', (322, 262)), B=('trap', dict(lid=78), 'STAIRS. THEY GO DOWN.', (322, 250)),
             C=('stair', dict(lid=78), 'A BASEMENT. A COMPUTER, LEFT ON.', (452, 196)), D=('pov', dict(lid=78), 'YOU KNOW HOW THIS GOES.', (330, 180)))
ARROW = ['0', '00', '0A0', '0AA0', '0AAA0', '0AAAA0', '0AAAAA0', '0AAAAAA0', '0AAAAA000', '0AA0AA0', '0A0.0AA0', '00..0AA0', '.....0AA0', '.....0AA0', '......00']
@lru_cache(maxsize=16)
def card(name, lit=False):
    view, kw, text, _ = CARDS[name]; g, lv = scene(view, 480, 270, lit=lit, **kw); pic = print1(g, lv)
    c = Canvas(640, 360, 0xA); yy, xx = np.mgrid[:360, :640]; c.a[13:] = np.where((yy[13:] + xx[13:]) % 2 == 0, 0, 0xA)      # the grey desktop
    c.rect(0, 0, 640, 12, 0xA); c.rect(0, 12, 640, 13, 0); c.text(10, 2, '\x7f  File  Edit  Go  Cards', 0)
    x0, y0, x1, y1 = PIC2; c.rect(x0 - 3, y0 - 20, x1 + 5, y1 + 30, 0); c.rect(x0 - 2, y0 - 19, x1 + 2, y1 + 27, 0xA)
    for y in range(y0 - 16, y0 - 5, 2): c.rect(x0, y, x1, y + 1, 0)
    title = ' The House '; tx = (x0 + x1) // 2 - len(title) * 4; c.rect(tx, y0 - 17, tx + len(title) * 8, y0 - 4, 0xA); c.text(tx, y0 - 15, title, 0); c.rect(x0 + 8, y0 - 16, x0 + 19, y0 - 5, 0xA); c.rect(x0 + 9, y0 - 15, x0 + 18, y0 - 6, 0); c.rect(x0 + 10, y0 - 14, x0 + 17, y0 - 7, 0xA)
    c.rect(x0 - 2, y0 - 3, x1 + 2, y0 - 2, 0); c.a[y0:y1, x0:x1] = pic; c.rect(x0 - 2, y1, x1 + 2, y1 + 1, 0); c.text(x0 + 6, y1 + 10, text, 0)
    return c.a
def l2(t, lit=False):
    """Level 2 at time t (40 to 46): a 640 x 360 index canvas with the pointer on it."""
    seq = [('A', 40.0, 41.0, 'B', iris), ('B', 41.4, 43.0, 'C', dissolve), ('C', 43.4, 45.0, 'D', iris), ('D', 45.4, 46.0, None, None)]
    for name, t0, t1, nxt, fx in seq:
        if t < t1 + .4 or nxt is None:
            a = card(name, lit).copy()
            if nxt and t >= t1 + .2: a = fx(a, card(nxt, lit), .12 + .88 * (t - t1 - .2) / .2)
            tx, ty = CARDS[name][3]; px, py = (430, 300) if name == 'A' else CARDS[seq[[s[0] for s in seq].index(name) - 1][0]][3]
            u = D.ease((t - t0 - .2) / (t1 - t0 - .45)); x, y = int(px + (tx - px) * u), int(py + (ty - py) * u)
            c = Canvas(640, 360); c.a = a; c.sprite(ARROW, x, y)
            if t1 - .02 <= t < t1 + .2: x0, y0, x1, y1 = PIC2; c.a[y0:y1, x0:x1] = np.where(c.a[y0:y1, x0:x1] == 0, 0xA, 0)      # the click: the card answers by turning inside out for five frames
            return c.a
    return card('D', lit)

# ------------------------------------------------------------------ level 3: 1980
SCRIPT = [(48.3, 'M', 'PANTRY. THERE IS A TRAPDOOR HERE.'), (49.2, 'T', '>LIFT TRAPDOOR'), (50.3, 'M', 'OK.'), (50.6, 'T', '>DOWN'), (51.2, 'M', 'BASEMENT. THERE IS NO COMPUTER HERE.'), (54.0, 'M', 'THERE IS A WITCH HERE.'),
          (56.0, 'T', '>ASK WITCH FOR LIGHT'), (58.0, 'M', 'SHE DOES NOT TAKE REQUESTS.'), (59.6, 'T', '>SAY PLEASE'), (61.0, 'M', 'I DON\'T KNOW THE WORD "PLEASE".'), (62.4, 'T', '>LOOK AT WITCH'), (64.0, 'M', 'SHE WAS ALREADY LOOKING AT YOU.'),
          (64.6, 'T', '>'), (70.0, 'M', 'SHE PRESSES RETURN. THE VALUE IS F.'), (71.0, 'M', 'F IS A LIT WINDOW.')]
HAND3 = None
def hand3():
    """Where the witch's hand is on the full-size frame, in level 3's basement picture (her pointer starts there)."""
    cam = camera('room3', 320, 112); q = cam.project([(CHAIR[0] - .15, CHAIR[1] - .3, FLOOR + .5)])[0]
    return (q[0] - 7.5 * .078 * cam.f / q[2]) * 4, q[1] * 4
def l3(t, lit=None):
    """Level 3 at time t (48 to 72): a 320 x 180 index canvas. lit: None follows the story; True is after RETURN."""
    lit = (t >= 70.0) if lit is None else lit; ink = 0xF if lit else 0xA; c = Canvas(320, 180)
    if t < 51.0: g, _ = scene('trap', 320, 112, lid=0 if t < 50.3 else 78, computer=False); pic = printL(g, ink, (t - 48.2) / 1.2)
    else: g, _ = scene('room3', 320, 112, lid=78, computer=False, who=t >= 54.0); pic = printL(g, ink, (t - 51.0) / 2.2)        # the section again: the view she came in by, twice already
    c.a[:112] = pic; c.rect(0, 113, 320, 114, ink)
    lines = [(typed(s, t, t0) if k == 'T' else s) for t0, k, s in SCRIPT if t >= t0]
    if lines and t < 70.0 and int(t * 3) % 2 and len(lines[-1]) == len([s for t0, k, s in SCRIPT if t >= t0][-1]) and [k for t0, k, s in SCRIPT if t >= t0][-1] == 'T': lines[-1] += '_'
    for k, s in enumerate(lines[-7:]): c.text(2, 117 + k * 9, s, 0xF if (' F' in s[-3:] or s.startswith('F IS')) and t >= 70.0 else 0xA)
    return c.a
