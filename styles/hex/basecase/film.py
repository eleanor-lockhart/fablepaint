"""BASE CASE: the picture. Ninety-six seconds at 24 frames a second, forty-eight bars of two seconds.

    uv run python styles/hex/basecase/film.py sheet [seconds ...]     a contact sheet
    uv run python styles/hex/basecase/film.py still 21.5              one frame, full size
    uv run python styles/hex/basecase/film.py                         every frame, then the film with its sound (after music.py)

One model of one house (house.py), looked at through a travelling camera and printed four ways: as it is now
(painted texels, cast light), and then, inside each computer in each basement, as an older kind of picture.
"""
import sys, json, math
from pathlib import Path
HERE = Path(__file__).resolve().parent; sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(HERE.parents[2])); sys.path.insert(0, str(HERE.parent / 'uptime'))
import numpy as np
import cv2
from backlot.space import Camera
from backlot import depth as D
import deep as X, house as Hs, cast as CA
from house import PX, FX, FLOOR, GRADE
FPS, SECONDS, W, H = 24, 96, 1280, 720; NF = FPS * SECONDS
T = X.table(); ease = D.ease
clamp = lambda v, a=0.0, b=1.0: min(max(v, a), b)
ramp = lambda t, a, b: ease((t - a) / (b - a))
S = Hs.build()
for q in S.solids:                                                  # what the night sky shows of things that are out in it
    n0 = q.name.split('.')[0]
    if n0 == 'earth': q.glow = .5
    elif n0 in ('snow',): q.glow = .5
    elif n0 in ('house', 'found', 'roof', 'gable', 'eave', 'wing', 'rail', 'step', 'door', 'birdhouse', 'spruce', 'chimney'): q.glow = .34 if n0 != 'spruce' else .55
_FIL = {}
def statics(omit=()):
    if omit not in _FIL: _FIL[omit] = [q for q in S.solids if not any(q.name == o or q.name.startswith(o + '.') for o in omit)]
    return _FIL[omit]
SCR = np.array(Hs.SPOT['screen']); CHAIR = np.array(Hs.SPOT['chair'])

# ------------------------------------------------------------------ the sky: stars at infinity, snow in the air
_r = np.random.default_rng(11)
STARS = np.c_[_r.uniform(0, 360, 700), np.degrees(np.arcsin(_r.uniform(.02, .95, 700))), _r.integers(0, 5, 700)]
NFL = 5200
FL = np.c_[_r.uniform(-18, 36, NFL), _r.uniform(-15, 17, NFL), _r.uniform(0, 17, NFL), _r.uniform(0, 6.28, NFL), _r.uniform(.8, 1.5, NFL)]
def sky(img, g, cam):
    for az, alt, k in STARS:
        p = cam.sky(az, alt)
        if p and 0 <= p[0] < W - 2 and 0 <= p[1] < H - 2 and not g['hit'][int(p[1]), int(p[0])]: img[int(p[1]):int(p[1]) + 2, int(p[0]):int(p[0]) + 2] = T[(8, 8, 9, 9, 0xC)[int(k)]]
def snow(img, g, cam, t):
    z = GRADE + (FL[:, 2] - FL[:, 4] * 1.1 * t) % 17; x = FL[:, 0] + .5 * np.sin(.6 * t + FL[:, 3]); P = np.c_[x, FL[:, 1], z]
    for px, py, hs, dz in D.flakes(g, cam, P, .045):
        s = int(max(2, round(hs * 2))); x0, y0 = int(px - s / 2), int(py - s / 2)
        img[max(y0, 0):y0 + s, max(x0, 0):x0 + s] = T[0xA] if dz < 18 else T[9]
def smoke(img, g, cam, t, t0):
    """What comes out of the chimney once the furnace is lit: squares of chrome, rising and thinning."""
    r = np.random.default_rng(5); n = 60; born = t0 + r.uniform(0, 12, n); age = (t - born) % 6.0; ok = (t > born)
    P = np.c_[FX + 5.6 + .5 * age * (.4 + .3 * r.random(n)) + .25 * np.sin(age * 1.3 + r.uniform(0, 6, n)), 5.3 + .2 * r.uniform(-1, 1, n), 5.6 + age * 1.15][ok]
    for (px, py, hs, dz), a in zip(D.flakes(g, cam, P, .34), age[ok]):
        s = int(max(2, round(hs * 2 * (1 - a / 8)))); x0, y0 = int(px - s / 2), int(py - s / 2); img[max(y0, 0):y0 + s, max(x0, 0):x0 + s] = T[9] if a < 3 else T[8]

def render(things, cam, lights, ambient=.06, moving=None, steps=6, size=None):
    g = D.gbuffer(things, cam); lv = D.lighting(g, lights, ambient=ambient, moving=moving)
    return X.colour(g, lv, steps=steps, dither=0), g

# ------------------------------------------------------------------ lamps
_BAKE = {}
def lamp(key, make, solids):
    """A lamp that does not move: its shadows are worked out once."""
    if key not in _BAKE: _BAKE[key] = make().bake(solids)
    return _BAKE[key]
def screen_lamp(power=1.2, omit=()):
    L = lamp(('screen', omit), lambda: D.Light(SCR + (0, .14, 0), 1.0, 1.7, name='screen'), statics(omit)); L.power = power; return L
def tube_lamp(power=1.8):
    L = lamp('tube', lambda: D.Light(np.array(Hs.SPOT['tube']), 1.0, 4.2, name='tube'), statics()); L.power = power; return L
def torch(pos, aim, solids, power=3.0):
    return D.Light(pos, power, 4.0, aim=aim, cone=(15, 27), name='torch', size=384).bake(solids)

_d = np.random.default_rng(21); DUST = np.c_[_d.uniform(.35, 3.3, 170), _d.uniform(-1, 1, 170), _d.uniform(-1, 1, 170), _d.uniform(0, 6.28, 170)]
def beam(img, g, cam, lamp, t):
    """Dust in the torch's beam: the only way to see light that has not landed on anything yet."""
    a = lamp.aim; u = np.cross(a, (0, 0, 1.)); u /= np.linalg.norm(u); v = np.cross(u, a); r = DUST[:, 0]; k = np.tan(np.radians(12)) * r
    P = lamp.pos + a * r[:, None] + u * (k * DUST[:, 1] * np.cos(.3 * t + DUST[:, 3]))[:, None] + v * (k * DUST[:, 2] * np.sin(.23 * t + DUST[:, 3]))[:, None]
    P = P[lamp.seen(P)]
    for px, py, hs, dz in D.flakes(g, cam, P, .03):
        s_ = int(max(2, round(hs * 2))); x0, y0 = int(px - s_ / 2), int(py - s_ / 2); img[max(y0, 0):y0 + s_, max(x0, 0):x0 + s_] = img[max(y0, 0):y0 + s_, max(x0, 0):x0 + s_] * .45 + T[0xF] * .55
def kid(pose, foot, cam, heading=None, flip=False, dark=False, glow=.42, cast=False):
    """The child's card and where her torch is. heading: the way she faces, as (dx, dy), for the torch."""
    c = D.card('child', CA.child(pose, flip, dark), foot, cam.right, glow=glow, cast=cast)
    hd = np.array([heading[0], heading[1], 0.0]) if heading is not None else np.array([1., 0, 0]); hd /= np.linalg.norm(hd)
    side = np.cross(hd, (0, 0, 1.))                                # her right-hand side
    hand = np.asarray(foot, float) + hd * .3 + (side * .22 if pose.startswith('back') or pose == 'kneel' else 0) + (0, 0, .72 if pose != 'kneel' else .45)
    return c, hand, hd

# ------------------------------------------------------------------ level 0: the house as it is
def s1(t):
    """Outside, in section. The windows are lit; then they are not; the screen in the basement still is."""
    cam = D.fly([(0, (9.25, -22, 1.9), (9.25, 0, 1.2), 35), (8, (9.25, -17.5, .9), (9.25, 0, .1), 35)], t)
    on = t < 5.0; lit = [on, on, False, on, on, False, on]
    things = statics() + Hs.windows(lit) + Hs.lid(0) + Hs.screen() + Hs.tube(0)
    img, g = render(things, cam, [screen_lamp()], .05); sky(img, g, cam); snow(img, g, cam, t)
    return img
def s2(t):
    """The pantry, from the kitchen. A line of light round the trap door. She lifts it and goes down."""
    cam = D.fly([(8, (PX - 2.8, 4.85, 1.45), (PX + 2.5, 4.85, .45), 32), (11.5, (PX - 1.9, 4.85, 1.5), (PX + 2.2, 4.85, .2), 32), (16, (PX - .7, 4.85, 1.8), (PX + 1.9, 4.85, -.5), 32)], t)
    ang = 78 * ramp(t, 11.6, 12.8); lidp = Hs.lid(ang)
    if t < 10.4:                                                    # in from the kitchen
        u = ramp(t, 8.2, 10.4) if False else clamp((t - 8.2) / 2.2); a, b = np.array([PX - .9, 4.2, 0]), np.array([PX + .95, 4.85, 0]); foot = a + (b - a) * u
        pose = ('back', 'back_b', 'back', 'back_c')[int(t * 4) % 4] if 0 < u < 1 else 'back'; hd = (b - a)[:2]
    elif t < 13.0: foot = np.array([PX + .95, 4.85, 0]); pose = 'kneel' if 10.9 <= t < 11.6 else ('lift' if t < 12.9 else 'back'); hd = (1, 0)
    else:
        k = min(int((t - 13.0) / .5) + 1, 12); foot = Hs.stair(k); pose = ('back_b', 'back_c')[k % 2] if (t - 13.0) % .5 < .25 else 'back'; hd = (1, 0)
    c, hand, hd = kid(pose, foot, cam, hd)
    aim = hd + (0, 0, -.45 if t < 13.0 else -.7)
    lights = [torch(hand, aim, statics() + lidp)]
    if ang > 1: lights.append(D.Light((PX + 1.9, 4.85, -.45), .45 * ang / 78 if t < 12.8 else 1.5 + 1.3 * math.exp(-(t - 12.8) * 4), 2.2, name='below').bake(statics()))
    things = statics() + lidp + (Hs.leak() if ang < 1 else []) + [c]
    img, g = render(things, cam, lights, .05, moving=lidp); beam(img, g, cam, lights[0], t)
    return img
def path(t):
    """Where she is in the basement, and how she stands. 16.0 to 20.5 she comes down the last nine steps, one
    each half second; then five metres of floor, round the end of the desk, and she sits."""
    if t < 20.5:
        k = clamp(int((t - 16.0) / .5) + 3, 3, 12); u = ((t - 16.0) % .5) / .5
        return Hs.stair(k), ('pass' if u < .5 else 'stand'), (1, 0)
    pts = [(PX + 3.6, 4.85), (FX + 4.1, 4.3), (FX + 6.95, 4.3), (FX + 7.05, 5.0), (FX + 7.8, 5.0)]; seg = [math.dist(pts[i], pts[i + 1]) for i in range(4)]
    d = (t - 20.5) * 1.0; tot = sum(seg)
    if d >= tot: return np.array([FX + 7.8, 5.0, FLOOR]), 'stand', (1, 0)
    i = 0
    while d > seg[i]: d -= seg[i]; i += 1
    a, b = np.array(pts[i]), np.array(pts[i + 1]); p = a + (b - a) * d / seg[i]; u = ((t - 20.5) % .5) / .5
    return np.array([p[0], p[1], FLOOR]), ('stride' if u < .5 else 'pass'), tuple(b - a)
_tt = np.arange(14.0, 28.0, 1 / 24); _x = np.interp(_tt, [16.0, 18.5, 20.5, 25.2, 26.0], [PX + 2.5, PX + 3.3, PX + 4.5, FX + 7.35, FX + 7.4])
_k = np.exp(-.5 * (np.arange(-30, 31) / 11.0) ** 2); TRACK = (_tt, np.convolve(np.pad(_x, 30, mode='edge'), _k / _k.sum(), 'valid'))      # a dolly's path: straight runs, rounded off
def s3(t):
    """The basement, in section, the camera going along with her."""
    foot, pose, hd = path(t); cx = float(np.interp(t, TRACK[0], TRACK[1]))
    cam = Camera((cx, -3.2, -1.5), look=(cx, 3, -1.5), lens=35)
    c, hand, hdv = kid(pose, foot, cam, hd, flip=hd[0] < -.3)
    lights = [screen_lamp()]
    lights.append(torch(hand, hdv + (0, 0, -.22), statics()))
    extras = []
    if 21.5 <= t < 22.9:                                            # a rat, leaving, the way she came
        u = (t - 21.5) / 1.4; extras.append(D.card('rat', CA.prop('rat' if int(t * 12) % 2 else 'rat_b'), (FX + 6.3 - 3.6 * u, 3.9 - .5 * u, FLOOR), cam.right, glow=.5, cast=False))
    z = -.5 - .75 * ramp(t, 20.5, 24.5); sx = 8.4 + .55                                                    # the spider comes down too
    extras.append(D.card('spider', CA.prop('spider'), (sx, 2.4, z - .12), cam.right, texel=.012, glow=.3, cast=False)); extras.append(D.card('thread', np.full((max(int((-.46 - z) / .012), 1), 1), 9, np.uint8), (sx, 2.4, z), cam.right, texel=.012, glow=.25, cast=False))
    things = statics() + Hs.lid(78) + Hs.screen() + Hs.tube(0) + [c] + extras
    img, g = render(things, cam, lights, .06, moving=[c]); beam(img, g, cam, lights[-1], t)
    return img

POV = Camera((SCR[0] + .2 - .2, 4.405 + .575, SCR[2] + .1 - .1), look=(SCR[0], 4.405, SCR[2]), lens=35)      # her eyes: square on to the glass, 57 cm from it
SC = np.array([Hs.SCREEN['corner'][0] - .2, 4.405, Hs.SCREEN['corner'][2] - .1125])                                # the middle of the glass
def s4(t, skin=None, back=False):
    """Behind her, then over her shoulder, then into the glass. (Run backwards, with back=True, it is the way out.)"""
    keys = [(26, (SC[0] - 1.5, 6.6, -.9), (SC[0] + .1, 4.4, SC[2] - .05), 35), (28.6, (SC[0] - .42, 5.15, SC[2] + .1), (SC[0], 4.4, SC[2]), 35), (30.3, (SC[0], 4.405 + .46, SC[2]), SC, 35), (32, (SC[0], 4.405 + .3888, SC[2]), SC, 35)]
    cam = D.fly(keys, t); om = ('wall.n', 'earth.n', 'pipe')
    c = D.card('child', CA.child('sit_back'), (CHAIR[0], CHAIR[1], FLOOR + .46), (-1, 0, 0), glow=.3, cast=False)
    things = statics(om) + Hs.cut() + Hs.screen(skin, 1.0) + Hs.tube(1.0 if back else 0) + Hs.led(1.0 if back else 0) + ([c] if t < 29.6 else [])
    lights = [screen_lamp(1.3 if not back else 2.2, om)] + ([tube_lamp()] if back else [])
    img, g = render(things, cam, lights, .06, moving=[c])
    return img
def flick(t, t0=83.0):
    """A fluorescent tube catching: three tries, then it holds."""
    d = t - t0
    return 1.0 if d >= 1.0 else float(any(a <= d < b for a, b in ((0, .07), (.3, .4), (.62, .78))))
def s5(t):
    """The light is back. The screen throws her shadow on the wall behind her, and the shadow wears a hat."""
    cam = D.fly([(80, (FX + 5.05, 1.9, -1.6), (FX + 7.45, 5.3, -1.17), 40), (88, (FX + 5.5, 2.6, -1.55), (FX + 7.5, 5.3, -1.17), 40)], t, smooth=False)
    c = D.card('child', CA.child('sit_front'), (CHAIR[0], CHAIR[1], FLOOR + .46), cam.right, glow=.5, cast=False)
    # her shadow. The light that throws it is low and to her right (the glass, off the desk top), so it falls on the clear wall to
    # her left, twice her size; and it is not her shape. It looks toward her
    Lp = np.array([CHAIR[0] + .45, 4.56, FLOOR + .85]); TX = .0125; sh = np.ascontiguousarray(CA.prop('shadow')[:, ::-1]); cp = np.array([CHAIR[0] - .02, CHAIR[1] - .02, FLOOR + .75])
    d = cp - Lp; rt = np.array([d[1], -d[0], 0.0]); rt /= np.linalg.norm(rt); rt = rt if rt[0] > 0 else -rt; hat = D.card('shadow', sh, cp, rt, texel=TX)
    e = cp + rt * ((sh.shape[1] - CA.EYE[0] - sh.shape[1] / 2) * TX) + np.array([0, 0, (sh.shape[0] - CA.EYE[1]) * TX]); w = Lp + (e - Lp) * ((5.6 - Lp[1]) / (e[1] - Lp[1]))      # where its eye falls on the wall
    eye = [D.panel('eye', np.full((1, 2), 6, np.uint8), (w[0] - .05, 5.594, w[2] + .025), (1, 0, 0), (0, 0, -1), glow=1.0, cast=False)] if t >= 82.0 else []
    f = flick(t); k = (1.6 + 2.0 * math.exp(-(t - 80) * 1.2)) * (.3 if 82.0 <= t < 82.16 else 1.0)       # at 82.0 the light dips for four frames; when it is back the shadow has an eye
    rats = [D.card(f'rat{i}', CA.prop('rat'), (x, y, FLOOR), cam.right, glow=.35, cast=False) for i, (x, y) in enumerate(((FX + 6.75, 4.55), (FX + 7.05, 4.95)))]
    things = statics() + Hs.lid(78) + Hs.screen() + Hs.tube(f) + Hs.led(float(t > 85)) + [c] + rats + eye
    face = screen_lamp(.2 * k / 1.6); face.still = True; low = lamp('low', lambda: D.Light(Lp, 1.0, 2.3, name='low'), statics()); low.power = k
    lights = [face, low] + ([tube_lamp(.42)] if f else [])
    img, g = render(things, cam, lights, .05, moving=[hat])
    return img
def s6(t):
    """Out and up: the basement under the house, the house in the snow, the windows coming back one at a time."""
    cam = D.fly([(88, (9.25, -8.5, -1.2), (9.25, 3, -1.25), 35), (90.4, (9.25, -18, 1.55), (9.25, 0, .9), 35), (96, (9.25, -19.6, 1.8), (9.25, 0, 1.0), 35)], t)
    lit = [t >= 90.0 + .25 * k - 1e-6 for k in (0, 1, 2, 3, 4, 5, 6)]
    c = D.card('child', CA.child('sit_front'), (CHAIR[0], CHAIR[1], FLOOR + .46), cam.right, glow=.5, cast=False)
    things = statics() + Hs.windows(lit) + Hs.lid(78) + Hs.screen() + Hs.tube(1) + Hs.led(1) + [c]
    img, g = render(things, cam, [screen_lamp(1.5), tube_lamp(1.5)], .07); sky(img, g, cam); smoke(img, g, cam, t, 89.0); snow(img, g, cam, t)
    return img

import levels as LV
import ui as U
C = U.C
# ------------------------------------------------------------------ the pictures inside the pictures, made once
_K = {}
def keep(name, make):
    if name not in _K: _K[name] = make()
    return _K[name]
def final3(): return keep('i3', lambda: LV.l3(71.5, True))                                               # level 3 after RETURN (indices)
def final2(): return keep('i2', lambda: LV.nest(LV.card('D', True), LV.R2, final3()))                     # level 2 lit, with level 3 on its screen
def final1(): return keep('i1', lambda: LV.l1_pov(True, final2()))                                        # level 1 lit, with level 2 on its screen, with level 3 on its screen
def pic3F(): return keep('p3', lambda: LV.up(final3(), 4))
def pic2F(): return keep('p2', lambda: LV.zoom(LV.up(LV.card('D', True), 2), [v * 2 for v in LV.R2], pic3F(), 0))
def pic1F(): return keep('p1', lambda: LV.zoom(LV.up(LV.l1_pov(True), 4), [v * 4 for v in LV.R1], pic2F(), 0))

# ------------------------------------------------------------------ what the system has to say: the stack, and her
PUSH = [(13.0, 'DESCEND(1998)', 80.0), (35.2, 'DESCEND(1989)', 76.0), (43.0, 'DESCEND(1987)', 74.0), (51.0, 'DESCEND(1980)', 72.0), (54.0, 'WITCH() BASE CASE', 70.0)]      # (pushed, what, returned)
def hud(img, t):
    if t >= 92.0: return
    rows = [(k, name, t >= ret) for k, (t0, name, ret) in enumerate(PUSH) if t0 <= t < ret + .8]
    x, y, w = W - 416, 14, 402; h = 36 + max(len(rows), 1) * 22 + 6 + 30
    cx, cy, cw, ch = U.window(img, x, y, w, h, 'STACK', 'hers' if any(k == 4 for k, _, _ in rows) else 'sys', close=False)
    if not rows: U.text(img, cx + 8, cy + 6, '(EMPTY)', C[8], 2)
    for j, (k, name, back) in enumerate(rows):
        s = ' ' * k + f'{k} ' + name; col = C[6] if k == 4 else (C[0xA] if j == len(rows) - 1 else C[9])
        U.text(img, cx + 8, cy + 6 + j * 22, s, col, 2)
        if back: U.text(img, cx + 8 + U.tw(s + ' '), cy + 6 + j * 22, '= F', C[0xF], 2)
    sx, sy = cx + 10, cy + ch - 26                                    # the signature: sixteen registers in order, named, the last one lit
    for k in range(16):
        U.rect(img, sx + k * 24, sy, sx + k * 24 + 20, sy + 10, C[k]); U.text(img, sx + k * 24 + 6, sy + 13, '0123456789ABCDEF'[k], C[0xF] if k == 15 else C[8], 1)
    for tp in (70.0, 72.0, 74.0, 76.0, 80.0):                       # and it answers when F is returned
        if 0 <= t - tp < .7: U.rect(img, sx + 15 * 24 - 4, sy - 4, sx + 15 * 24 + 24, sy + 24, C[0xF], .6 * (1 - (t - tp) / .7))
def notice(img, t):
    """5.5 to 7.9: the house says what happened, and what did not."""
    if 5.5 <= t < 7.9: U.dialog(img, 44, 548, 404, 'HOUSE', ['THE POWER IS OUT.', '1 LIGHT IS STILL ON.'])
def decree(img, t):
    """66 to 70.4: her dialog. She does not move unless she is deciding something; this is her deciding."""
    if not 66.0 <= t < 70.4: return
    bx = U.dialog(img, 60, 150, 480, 'WITCH', ['IT IS DARK IN MY HOUSE.', 'I DID NOT ALLOW THAT.'], ['RETURN'], bar='hers', pressed=0 if t >= 70.0 else None)[0]
    if t >= 67.0:
        u = ease((t - 67.0) / 2.4); x0, y0 = LV.hand3(); x1, y1 = bx[0] + bx[2] * .6, bx[1] + bx[3] * .55
        U.pointer(img, x0 + (x1 - x0) * u, y0 + (y1 - y0) * u, 6)
def endcard(img, t):
    if t < 92.0: return
    a = ramp(t, 92.0, 92.4); s = 'BASE CASE'; x = (W - U.tw(s, 9)) // 2
    if a >= 1 or int(t * 12) % 2: U.text(img, x, 556, s, C[0xA], 9, shadow=C[0])
    if t >= 93.0: s2 = 'EVERY HOUSE HAS ONE.'; U.text(img, (W - U.tw(s2, 3)) // 2, 650, s2, C[9], 3, shadow=C[0])

def picture(t):
    """The frame at time t, before the system writes on it."""
    if t < 8: return s1(t)
    if t < 16: return s2(t)
    if t < 26: return s3(t)
    if t < 32: return s4(t, keep('title', LV.l1_title))
    if t < 38.6: return LV.up(LV.l1(t), 4)
    if t < 40: return LV.zoom(keep('pov1', lambda: LV.up(LV.l1_pov(), 4)), [v * 4 for v in LV.R1], keep('c2a', lambda: LV.up(LV.l2(40.0), 2)), ease((t - 38.6) / 1.4))
    if t < 46: return LV.up(LV.l2(t), 2)
    if t < 48: return LV.zoom(keep('pov2', lambda: LV.up(LV.card('D'), 2)), [v * 2 for v in LV.R2], keep('c3a', lambda: LV.up(LV.l3(48.0), 4)), ease((t - 46) / 2))
    if t < 72:
        img = LV.up(LV.l3(t), 4)
        if t >= 70.0: img = img + (C[0xF] - img) * (.5 * math.exp(-(t - 70.0) * 9))
        return img
    if t < 74: return LV.zoom(pic2F(), [v * 2 for v in LV.R2], pic3F(), 1 - ease((t - 72) / 1.6))
    if t < 76: return LV.zoom(pic1F(), [v * 4 for v in LV.R1], pic2F(), 1 - ease((t - 74) / 1.6))
    if t < 80: return s4(32 - (t - 76) * 1.5, final1(), back=True)
    if t < 88: return s5(t)
    return s6(t)
def frame(i):
    t = i / FPS; img = np.ascontiguousarray(picture(t), np.float32)
    for tp in (72.0, 74.0, 76.0, 80.0):
        if 0 <= t - tp < .5: img = img + (C[0xF] - img) * (.42 * math.exp(-(t - tp) * 8))
    img = X.glow(img)
    notice(img, t); decree(img, t); hud(img, t); endcard(img, t)
    return img

POINTS = [(5.0, 'the lights go out'), (5.5, 'THE POWER IS OUT'), (8.0, 'cut: the pantry'), (12.8334, 'the trap door is open'), (13.0, 'first step down'), (16.0, 'cut: the basement'), (20.5, 'she reaches the floor'), (26.0, 'cut: behind her'),
          (32.8334, 'any key: the game'), (34.0, 'IT IS HEAVY'), (34.625, 'the lid, in the game'), (36.0, 'cut: the game basement'), (38.625, 'cut: its screen'), (41.0, 'click: the lid'), (43.0, 'click: the stairs'), (45.0, 'click: the computer'),
          (48.0, '1980'), (51.0, 'DOWN'), (54.0, 'THERE IS A WITCH HERE'), (58.0, 'SHE DOES NOT TAKE REQUESTS'), (61.0, 'I DON\'T KNOW THE WORD'), (64.0, 'SHE WAS ALREADY LOOKING'), (66.0, 'her dialog'), (70.0, 'RETURN'),
          (72.0, 'F reaches 1987'), (74.0, 'F reaches 1989'), (76.0, 'F reaches the real screen'), (80.0, 'cut: her shadow'), (82.0, 'the shadow opens an eye'), (83.0, 'the shop light tries'), (84.0, 'the shop light holds'), (88.0, 'cut: out and up'),
          (90.0, 'window 1'), (90.5, 'window 3'), (91.0, 'window 5'), (91.5, 'window 7'), (92.0, 'title')]
def _job(i): X.save(f'out/hex/basecase/frames/f_{i:04d}.png', frame(i)); return i
if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == 'sheet':
        ts = [float(v) for v in a[1:]] or [2, 6, 10, 12.5, 14.5, 18, 21.5, 24.5, 27, 30, 31.9, 32.4, 34.3, 35.6, 36.6, 37.8, 39.3, 40.6, 42.5, 44.4, 47, 49.6, 52.5, 55, 61.5, 64.4, 68.5, 70.1, 71.5, 72.8, 74.8, 77, 79, 80.3, 83.35, 86, 89, 91, 95.5]
        from multiprocessing import Pool
        with Pool(min(len(ts), 14)) as pool: ims = pool.map(frame, [int(t * FPS) for t in ts])
        cols = 3; small = [(np.clip(cv2.resize(im, (640, 360), interpolation=cv2.INTER_AREA), 0, 1) * 255).astype(np.uint8) for im in ims]
        for im, t in zip(small, ts): cv2.putText(im, f'{t:g}s', (8, 20), cv2.FONT_HERSHEY_SIMPLEX, .55, (255, 255, 255), 1, cv2.LINE_AA)
        while len(small) % cols: small.append(np.zeros_like(small[0]))
        cv2.imwrite('out/hex/basecase_sheet.jpg', np.vstack([np.hstack(small[k:k + cols]) for k in range(0, len(small), cols)])[..., ::-1], [cv2.IMWRITE_JPEG_QUALITY, 90])
    elif a and a[0] in ('sync', 'pops', 'travel'):
        from backlot import sync
        fr = 'out/hex/basecase/frames'
        if a[0] == 'sync': sync.check(POINTS, fr, 'out/hex/basecase.wav', fps=FPS, out_jpg=str(HERE / 'basecase_sync.jpg'), out_json='out/hex/basecase_sync.json')
        elif a[0] == 'pops':
            for row in sync.pops(POINTS, fr, fps=FPS, allow=[int(t * FPS) + k for t in (83.0, 83.3, 83.62) for k in range(0, 5)]): print(row)
        else:
            st, summ = sync.travel(fr); print(summ)
    elif a and a[0] == 'still':
        for v in a[1:]: X.save(f'out/hex/basecase_still_{v}.png', frame(int(float(v) * FPS)))
    else:
        from multiprocessing import Pool
        import subprocess
        from backlot import sound as sd
        Path('out/hex/basecase/frames').mkdir(parents=True, exist_ok=True)
        todo = list(range(NF)) if not a else list(range(int(float(a[0]) * FPS), int(float(a[1]) * FPS)))
        with Pool(28) as pool:
            for k, _ in enumerate(pool.imap_unordered(_job, todo, chunksize=4)):
                if k % 288 == 0: print(k, 'frames', flush=True)
        if not a or len(todo) == NF or (len(a) > 2 and a[2] == 'mux'):
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', 'out/hex/basecase/frames/f_%04d.png', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-movflags', '+faststart', 'out/hex/basecase/silent.mp4'], check=True)
            sd.mux('out/hex/basecase/silent.mp4', 'out/hex/basecase.wav', str(HERE / 'base_case.mp4'), loop_video=False, crf=21)
            X.save(str(HERE / 'base_case_poster.png'), frame(int(94.5 * FPS)))
            print('wrote', HERE / 'base_case.mp4')
