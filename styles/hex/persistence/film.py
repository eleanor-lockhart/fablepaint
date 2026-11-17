"""Persistence: 72 seconds, 1728 pictures. The brief is BRIEF.md; the model is ride.py; the horse is horse.py.

    python film.py                  render everything, add the sound, write persistence.mp4
    python film.py A B [mux]        render seconds A to B
    python film.py sheet [t ...]    a contact sheet of stills
    python film.py still t ...      single frames
    python film.py sync | pops | travel
"""
import sys, json, math
from pathlib import Path
HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE)); sys.path.insert(1, str(HERE.parent)); sys.path.insert(2, str(ROOT)); sys.path.insert(3, str(HERE.parent / 'uptime'))
import numpy as np
import cv2
from backlot.space import Camera
from backlot import depth as D
import deep as X, ride as R, puppet as P
import ui as U
from ui import C

FPS, SECONDS, W, H = 24, 72, 1280, 720; NF = FPS * SECONDS; SIZE = (W, H)
OUT = ROOT / 'out' / 'hex' / 'persistence'; FRAMES = OUT / 'frames'
T = X.table()
ease = D.ease
LOCK0, LOCK1 = 36.0, 60.0

# ------------------------------------------------------------------ how fast the ride turns, degrees a frame
def omega(t):
    if t < 12: return 0.0
    if t < 14: return 1.5 * ease((t - 12) / 2)
    if t < 28.5: return 1.5
    if t < 30: return 1.5 + 2.5 * ease((t - 28.5) / 1.5)
    if t < 32.5: return 4 + 22 * (t - 30) / 2.5
    if t < 36: return 30 - 4 * (1 - (t - 32.5) / 3.5) ** 2
    if t < 60: return 30.0
    if t < 62: return 30 - 3 * ((t - 60) / 2) ** 2
    if t < 64: return 27 - 25.5 * ease((t - 62) / 2)
    if t < 66: return 1.5 * (1 - ease((t - 64) / 2))
    return 0.0
_w = np.array([omega(i / FPS) for i in range(NF)]); TH = np.r_[0.0, np.cumsum(_w)[:-1]]
_i0 = int(LOCK0 * FPS); TH = TH - TH[_i0]                         # locked, a horse of the outer ring is on every thirtieth degree
for _i in range(_i0, int(LOCK1 * FPS) + 1): TH[_i] = 30.0 * (_i - _i0)
TH[int(LOCK1 * FPS) + 1:] = TH[int(LOCK1 * FPS)] + np.cumsum(_w[int(LOCK1 * FPS):-1])
def theta(t): return float(TH[min(int(round(t * FPS)), NF - 1)])
def passing(t): return omega(t) * FPS / 30.0                      # horses a second past any one place
def lit(t): return (12.0 <= t < 27.0) or (63.0 <= t < 66.5)      # the ride's own lights
def strobing(t): return 27.125 <= t < 63.0                      # the lights go out at 27.0; the lamp comes on three pictures later

# ------------------------------------------------------------------ lights
_BAKE = {}
def baked(key, make, solids):
    if key not in _BAKE: _BAKE[key] = make().bake(solids)
    return _BAKE[key]
def house_lights(statics):
    ring = [D.Light(R.pol(R.RIM + .3, 30 * k + 15, R.TOP - .45), power=.9, reach=3.4, shadow=False) for k in range(12)]
    ring += [D.Light(R.pol(5.3, 60 * k, R.TOP - .35), power=.7, reach=3.2, shadow=False) for k in range(6)]
    key = baked('key', lambda: D.Light((-7.5, -8.5, 7.0), power=1.5, reach=12, aim=(.62, .66, -.48), cone=(46, 60), size=768), statics)
    return ring + [key]
SLENS = np.array(R.PLACE['strobe']); SAIM = np.array([-.874, .486, .02]); SAIM = SAIM / np.linalg.norm(SAIM)
def strobe_light(statics):
    return baked('strobe', lambda: D.Light(SLENS + SAIM * .3, power=2.7, reach=8.0, aim=SAIM, cone=(50, 61), size=1024), statics)

# ------------------------------------------------------------------ the keeper
KP = np.array([8.31, -3.1, 0.0]); REG = np.array([R.PLACE['regulator'][0], R.PLACE['regulator'][1], 0.0]); NORTH, RIDEWARD = 90.0, 150.0
def _hd(a, b): return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
def _lerp(a, b, u): return np.asarray(a, float) * (1 - u) + np.asarray(b, float) * u
def _walk(t, a, b, t0, t1, carry='lamp', pose=None, rate=1.0):
    u = (t - t0) / (t1 - t0); p = P.walk(t * rate) if pose is None else dict(P.walk(t * rate), **pose); return p, _lerp(a, b, u), _hd(a, b), 0.0, carry
A_DOOR, A_IN, A_SW = (0.3, -11.6, 0), (1.2, -9.4, 0), (2.5, -9.9, 0); A_BENCH = (8.8, -8.2, 0)
PARK, SPOT = np.array(R.PLACE['strobe_park']), np.array(R.PLACE['strobe'])
def strobe_at(t):
    if t < 23: return PARK
    if t < 25: return _lerp(PARK, SPOT, ease((t - 23) / 2))
    return SPOT
def keeper_in(t):
    """Inside the shed: (pose, where his feet are, heading, where he looks, what he carries)."""
    S, RE, PU, UP = P.POSES['stand'], P.POSES['reach'], P.POSES['pull'], P.POSES['look_up']
    if t < 7.5: return _walk(t, A_DOOR, A_IN, 6.0, 7.5)
    if t < 9.0: return P.POSES['hold'], A_IN, 60 + 60 * ease((t - 7.5) / 1.5), 0.0, 'lamp'
    if t < 9.5: return P.mix(P.POSES['hold'], S, (t - 9.0) / .5), A_IN, 120 - 141 * ease((t - 9.0) / .5), 0.0, 'lamp'
    if t < 10.5: return _walk(t, A_IN, A_SW, 9.5, 10.5)
    if t < 12.4:
        u = ease((t - 10.5) / .9); pose = P.mix(S, RE, u) if t < 12.0 else PU
        return pose, A_SW, -21 + (-52 + 21) * u, 0.0, 'lamp'
    if t < 13.0: return P.mix(PU, S, (t - 12.4) / .6), A_SW, -52 + 69 * ease((t - 12.4) / .6), 30.0, 'lamp'
    if t < 18.0: return UP, A_SW, 17 + 95 * ease((t - 13.0) / 1.5), 10.0, 'lamp'
    if t < 23.0: return S, A_BENCH, 60.0, 0.0, None
    d = (SPOT - PARK)[:2]; d = d / np.linalg.norm(d)
    if t < 25.0:
        s = strobe_at(t); return dict(P.walk(t), **{k: P.POSES['push'][k] for k in ('shL', 'shR', 'elL', 'elR', 'lean')}), (s[0] - d[0] * .75, s[1] - d[1] * .75, 0), _hd((0, 0), d), 0.0, None
    a = (SPOT[0] - d[0] * .75, SPOT[1] - d[1] * .75, 0)
    if t < 26.5: return _walk(t, a, KP, 25.0, 26.5, carry=None, rate=1.4)
    if t < 27.3: return P.mix(S, RE, (t - 26.5) / .3), KP, NORTH, 0.0, None                                          # the lights: off at 27.0
    if t < 28.5: return P.mix(RE, PU, (t - 27.3) / .9), KP, NORTH, 20.0, None                                       # his hand goes to the regulator
    if t < 30.0: return P.mix(PU, RE, lever_at(t)), KP, NORTH, 0.0, None                                            # opened, a notch at a time
    if t < 31.0: return P.mix(RE, UP, (t - 30.0) / 1.0), KP, NORTH + (RIDEWARD - NORTH) * ease(t - 30.0), 10.0, None
    if t < 59.0: return UP, KP, RIDEWARD, 10.0, None                                                                # he does not move again until he closes it
    if t < 60.0: return P.mix(UP, RE, (t - 59.0) / .9), KP, RIDEWARD + (NORTH - RIDEWARD) * ease(t - 59.0), 0.0, None
    if t < 61.6: return P.mix(PU, RE, lever_at(t)), KP, NORTH, 0.0, None
    if t < 62.6: return P.mix(PU, S, (t - 61.6) / .6), KP, NORTH, 30.0, None
    if t < 63.3: return P.mix(S, RE, (t - 62.6) / .3), KP, NORTH, 0.0, None                                          # the lights: on at 63.0
    return P.mix(RE, S, (t - 63.3) / .6), KP, NORTH + (RIDEWARD - NORTH) * ease((t - 63.3) / 1.0), 20.0, None
def lever_at(t):
    if t < 28.5: return 0.0                                          # six notches, a quarter of a second apart
    if t < 30.0: return min(math.floor((t - 28.5) / .25 + 1e-6) + 1, 6) / 6
    if t < 60.0: return 1.0
    return 1 - min(math.floor((t - 60.0) / .25 + 1e-6) + 1, 6) / 6
def keeper(state):
    """The keeper's block, the little panel that is his lamp's lens, and where the lamp is and points."""
    pose, at, heading, look, carry = state; at = np.asarray(at, float)
    b = P.person(pose, look, carry).block('keeper', tuple(at), turn=heading); out = [b]; lamp = None
    if carry == 'lamp':
        h = P.hand(pose); a = math.radians(heading); f = np.array([math.cos(a), math.sin(a), 0]); l = np.array([-math.sin(a), math.cos(a), 0])
        hw = at + f * h[0] + l * h[1] + np.array([0, 0, h[2]]); lens = hw + f * .16 - np.array([0, 0, .12])
        out.append(D.panel('lamp.lens', np.full((2, 2), 0xF, np.uint8), lens + l * .05 + np.array([0, 0, .05]), -l, (0, 0, -1), glow=1.0, cast=False)); lamp = (lens + f * .05, f)
    return out, lamp

# ------------------------------------------------------------------ the sky, the snow, the numbers
_r = np.random.default_rng(4)
STARS = [(az + _r.uniform(-.5, .5), alt + _r.uniform(-.5, .5), _r.integers(0, 5)) for alt in np.arange(3, 62, 3.2) for az in np.arange(-180, 180, 3.2) if _r.random() < .8]
FL = np.c_[_r.uniform(-40, 40, 2600), _r.uniform(-45, 5, 2600), _r.uniform(0, 17, 2600), _r.uniform(0, 6.28, 2600), _r.uniform(.6, 1.3, 2600)]
def sky(img, g, cam):
    for az, alt, k in STARS:
        p = cam.sky(az, alt)
        if p and 0 <= p[0] < W - 2 and 0 <= p[1] < H - 2 and not g['hit'][int(p[1]), int(p[0])]: img[int(p[1]):int(p[1]) + 2, int(p[0]):int(p[0]) + 2] = T[(8, 8, 9, 9, 0xC)[int(k)]]
def snow(img, g, cam, t):
    z = (FL[:, 2] - FL[:, 4] * 1.1 * t) % 17; x = FL[:, 0] + .5 * np.sin(.6 * t + FL[:, 3]); Q = np.c_[x, FL[:, 1], z]
    for px, py, hs, dz in D.flakes(g, cam, Q, .045):
        s = int(max(2, round(hs * 2))); x0, y0 = int(px - s / 2), int(py - s / 2)
        img[max(y0, 0):y0 + s, max(x0, 0):x0 + s] = T[0xA] if dz < 18 else T[9]
def numbers(img, g, cam, th, reach=11.0, rings=(0,)):
    """Leave the rule showing: over every horse of the outer ring, which of the twelve it is."""
    for name, b, n, pos in R.horses(th):
        if int(name.split('.')[1]) not in rings: continue
        q = cam.project(np.array([pos + (0, 0, 1.02)]))[0]
        if not (q[2] > .5 and q[2] < reach and 20 <= q[0] < W - 20 and 12 <= q[1] < H - 12): continue
        if g['depth'][int(q[1]), int(q[0])] < q[2] - .6: continue
        k = 3 if q[2] < 7.5 else 2; s = '%02d' % n; x, y = int(q[0]) - 8 * k, int(q[1]) - 4 * k
        U.rect(img, x - 4, y - 3, x + 16 * k + 4, y + 8 * k + 3, C[0], .78); U.text(img, x, y, s, C[0xC], k)

def render(things, cam, lights, ambient=.06, moving=None):
    g = D.gbuffer(things, cam); lv = D.lighting(g, lights, ambient=ambient, moving=moving)
    return X.colour(g, lv, steps=6, dither=0), g

# ------------------------------------------------------------------ the shots
STAT = None; STAT_PLAN = None
def statics():
    global STAT, STAT_PLAN
    if STAT is None:
        STAT = list(R.shed()); STAT_PLAN = [s for s in STAT if not (s.name.startswith('beam') or s.name.startswith('houselamp') or s.name == 'ceiling')]
    return STAT

def interior(t, cam, plan=False, show_numbers=False, rings=(0,), reach=11.0):
    """Any shot inside the shed at time t through `cam`."""
    S = statics(); S = STAT_PLAN if plan else S; th = theta(t); on = lit(t); i = int(round(t * FPS))
    mov = R.ride(th, 'chase' if on else 'off', frame=i, cut=plan) + R.lever(lever_at(t)) + R.switch(t >= 12.0) + R.strobe(tuple(strobe_at(t)), lit=strobing(t), aim=(SAIM[0], SAIM[1]))
    kp, lamp = keeper(keeper_in(t)); mov += kp
    if on: lights = house_lights(statics()); amb = .11
    elif strobing(t): lights = [strobe_light(statics()), D.Light(SLENS - SAIM * .5 + np.array([0, 0, .25]), power=.95, reach=3.6, shadow=False)]; amb = .125 if not plan else .42
    else:
        lights = []; amb = .075
        if lamp is not None: lights = [D.Light(lamp[0], power=2.6, reach=6.5, aim=lamp[1] + np.array([0, 0, -.04]), cone=(17, 31), size=512).bake(S), D.Light(lamp[0] - lamp[1] * .3 + np.array([0, 0, .3]), power=.7, reach=1.4, shadow=False)]
    img, g = render(S + mov, cam, lights, amb, moving=mov)
    if show_numbers: img = np.ascontiguousarray(img); numbers(img, g, cam, th, reach, rings)
    return img

def exterior(t, cam, leaving=False):
    S = [q for q in R.yard(window_lit=leaving) if q.name != 'door']; far, near = np.array((-3.9, -17.6, 0)), np.array((0.4, -12.0, 0)); W_ = R.SHED + .25
    push = dict(P.POSES['stand'], shR=60, elR=25, lean=6)
    if leaving:
        gap = 1 - ease((t - 66.0) / .9); state = (push, near, 90.0, 0.0, 'lamp') if t < 67.0 else (P.walk(t), _lerp(near, far, (t - 67.0) / 5.0), _hd(near, far), 0.0, 'lamp')
    else:
        gap = ease((t - 5.0) / .9); state = (P.walk(t), _lerp(far, near, t / 5.0), _hd(far, near), 0.0, 'lamp') if t < 5.0 else (push, near, 90.0, 0.0, 'lamp')
    dx = -4.2 * gap; door = D.paint(R.Set('d').box('door', (-2.2 + dx, 2.2 + dx), (-W_ - .11, -W_ - .05), (0, 4.6)), skin=R.skins()['door']); S.append(door)
    kp, lamp = keeper(state); wx, wy = R.PLACE['wagon']
    lights = [D.Light((wx + 2.9, wy, 2.1), power=2.0, reach=3.6, aim=(.75, 0, -.66), cone=(34, 52), shadow=False), D.Light((wx + .9, wy + 1.3, 2.1), power=1.6, reach=3.0, aim=(0, .7, -.7), cone=(34, 52), shadow=False),
              D.Light(lamp[0], power=2.4, reach=5.0, aim=lamp[1] + np.array([0, 0, -.55]), cone=(20, 36), size=512).bake(S), D.Light(lamp[0] - lamp[1] * .3 + np.array([0, 0, .3]), power=.7, reach=1.4, shadow=False)]
    if leaving: lights.append(D.Light((R.PLACE['window'][0], R.PLACE['window'][1] - .3, 2.2), power=2.4, reach=4.0, aim=(0, -.62, -.78), cone=(36, 54), shadow=False))
    lights.append(D.Light((-150, -260, 300), power=.4, reach=1e5, shadow=False))                       # what light a night with snow on the ground has
    img, g = render(S + kp, cam, lights, .2, moving=kp); img = np.ascontiguousarray(img); sky(img, g, cam); snow(img, g, cam, t)
    return img

RIMCAM = lambda: Camera(R.pol(9.5, -30, 1.95), look=R.pol(R.R_OUT, -30, 2.0), lens=24, size=SIZE)
def picture(t):
    if t < 6.0: return exterior(t, D.fly([(0, (8.5, -41.0, 2.0), (-2.6, -12, 4.6), 35), (6, (7.2, -38.5, 2.5), (-2.2, -12, 4.6), 35)], t, SIZE))
    if t < 12.0: return interior(t, D.fly([(6, (-7.6, -8.6, 1.8), (2.0, -7.3, 1.7), 24), (12, (-7.0, -9.2, 1.9), (2.0, -6.4, 1.9), 24)], t, SIZE))
    if t < 18.0: return interior(t, D.fly([(12, (9.6, -10.3, 2.5), (0, 0, 2.3), 20), (18, (7.2, -10.5, 3.0), (0, 0, 2.2), 20)], t, SIZE), show_numbers=t >= 15.0, reach=14.0)
    if t < 24.0: return interior(t, RIMCAM(), show_numbers=True)
    if 28.5 <= t < 30.0: return interior(t, D.fly([(28.5, (10.62, -3.35, 1.62), (8.4, -2.7, 1.3), 30), (30, (10.5, -3.3, 1.62), (8.4, -2.7, 1.3), 30)], t, SIZE))     # his hand on the regulator
    if t < 36.0: return interior(t, D.fly([(24, (7.9, -10.7, 2.3), (8.3, -3.2, 1.5), 24), (27, (8.0, -10.4, 2.2), (7.9, -2.8, 1.6), 24), (36, (8.5, -9.4, 2.1), (6.2, -1.8, 1.8), 24)], t, SIZE), show_numbers=t >= 30.0, reach=9.5)
    if t < 40.0:                                                      # locked: the view the numbered horses went by in, drifting sideways (the ride is still; the camera is not)
        u = (t - 36) / 4; d = (-.3 + .6 * u); e = np.array(R.pol(9.5, -30, 1.95)) + d * np.array([math.sin(math.radians(30)), math.cos(math.radians(30)), 0]); return interior(t, Camera(e, look=R.pol(R.R_OUT, -30, 2.0), lens=24, size=SIZE), show_numbers=True)
    if t < 44.0: return interior(t, D.fly([(40, (9.2, -9.7, 2.2), (2.9, -.6, 2.1), 24), (44, (9.0, -9.3, 2.1), (2.9, -.6, 2.1), 24)], t, SIZE), show_numbers=True, reach=9.0)
    if t < 48.0:
        u = (t - 44) / 4; a = -33 - 32 * u; return interior(t, Camera(R.pol(9.2, a, 1.8 + .5 * u), look=(0, 0, 1.9), lens=20, size=SIZE), show_numbers=True, reach=9.0)   # round the lit side, away from the lamp: the shadows come out from behind the horses
    if t < 52.0: return interior(t, D.fly([(48, (9.9, -6.9, 2.7), (2.6, -1.3, 2.2), 35), (52, (9.5, -7.4, 2.5), (2.6, -1.3, 2.2), 35)], t, SIZE))
    if t < 56.0: return interior(t, D.fly([(52, (9.72, -3.42, 1.78), (5.3, -.86, 1.55), 22), (56, (9.62, -3.3, 1.8), (5.3, -.86, 1.55), 22)], t, SIZE))
    if t < 60.0: return interior(t, D.fly([(56, (0, -15.5, 16.5), (0, -.2, 1.0), 32), (60, (0, -14.6, 15.9), (0, -.2, 1.0), 32)], t, SIZE), plan=True, show_numbers=True, reach=40.0, rings=(0, 1))
    if t < 66.0: return interior(t, D.fly([(60, (9.2, -9.7, 2.2), (2.9, -.6, 2.1), 24), (66, (9.3, -10.1, 2.4), (2.6, -.6, 2.1), 24)], t, SIZE))
    return exterior(t, D.fly([(66, (7.2, -38.5, 2.5), (-2.2, -12, 4.6), 35), (72, (9.4, -44.0, 3.4), (-2.6, -12, 5.2), 35)], t, SIZE), leaving=True)

# ------------------------------------------------------------------ the system's type
def caption(img, t):
    if 1.0 <= t < 5.6:
        U.rect(img, 36, 598, 36 + 40 * 16 + 24, 598 + 86, C[0], .7); U.text(img, 48, 608, 'WINTER QUARTERS.', C[0xA], 2)
        if t >= 2.5: U.text(img, 48, 634, 'ONCE A YEAR THE RIDE IS RUN, FOR NOBODY,', C[9], 2); U.text(img, 48, 656, 'TO SEE THAT IT STILL RUNS.', C[9], 2)
def hud(img, t):
    if not 12.0 <= t < 66.0: return
    full = t >= 24.5; x, y, w = W - 462, 14, 448; h = (36 + 4 * 22 + 8 + 30) if full else (36 + 22 + 8 + 30)
    cx, cy, cw, ch = U.window(img, x, y, w, h, 'RIDE', 'sys', close=False)
    rpm = omega(t) * FPS / 360 * 60; over = rpm > 6.5
    U.text(img, cx + 8, cy + 6, 'TURNS %5.1f /MIN' % rpm, C[0xD] if over else C[0xA], 2); U.text(img, cx + 8 + U.tw('TURNS 000.0 /MIN '), cy + 6, '(RATED 6)', C[9], 2)
    if full:
        U.text(img, cx + 8, cy + 28, 'HORSES PASSING %4.1f /S' % passing(t), C[0xA], 2)
        U.text(img, cx + 8, cy + 50, 'LAMP FLASHES   24.0 /S', C[0xA] if strobing(t) else C[8], 2)
        locked = LOCK0 <= t < LOCK1
        U.text(img, cx + 8, cy + 72, 'LOCKED: 1 HORSE A FLASH' if locked else 'NOT LOCKED', C[0xF] if locked else C[8], 2)
    U.strip(img, cx + 10, cy + ch - 24)
_CARD = None
def _card():
    """The twelve horses of the outer ring, side on, as small pictures: his card, redrawn."""
    global _CARD
    if _CARD is None:
        import horse as Hh
        pr = [Hh.carving(k, 0).print('side') for k in range(12)]; m = np.any([q != D.HOLE for q in pr], 0); ys, xs = np.nonzero(m); y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
        _CARD = [np.kron(q[y0:y1, x0:x1], np.ones((2, 2), np.uint8)) for q in pr]
    return _CARD
def at_lamp(i):
    """Which horse of the outer ring (1..12) is in front of the lamp in picture i."""
    return int((-round((-30.0 - TH[i]) / 30.0)) % 12) + 1
def card(img, t):
    """Leave the rule showing: every horse that passes the lamp is put on the card, in its place. By the time
    the lamp is lit the card is his card, a stride in twelve pictures; locked, the mark runs along it at 24 a second."""
    if not 15.0 <= t < 66.0: return
    i = min(int(round(t * FPS)), NF - 1); cells = _card(); ch, cw = cells[0].shape; gap = 4; x0 = (W - 12 * (cw + gap) + gap) // 2; y0 = H - ch - 14
    seen = {at_lamp(j) for j in range(15 * FPS, i + 1, 2)} | {at_lamp(i)}; now = at_lamp(i)
    U.rect(img, x0 - 8, y0 - 28, x0 + 12 * (cw + gap) + 4, H - 4, C[0], .8)
    U.text(img, x0, y0 - 23, 'IN FRONT OF THE LAMP: HORSE %02d' % now, C[0xA], 2); U.text(img, x0 + 12 * (cw + gap) - gap - 16 * 29, y0 - 23, '%2d OF 12 ON THE CARD' % len(seen) if len(seen) < 12 else 'ONE STRIDE, IN TWELVE HORSES.', C[9], 2)
    for k in range(12):
        x = x0 + k * (cw + gap); hot = (k + 1 == now)
        U.rect(img, x, y0, x + cw, y0 + ch, C[2] if hot else C[1], 1.0)
        if k + 1 in seen:
            q = cells[k]; m = q != D.HOLE; sub = img[y0:y0 + ch, x:x + cw]; sub[m] = T[q[m]]
        if hot: U.rect(img, x, y0 + ch, x + cw, y0 + ch + 3, C[0xF], 1.0); U.rect(img, x, y0 - 3, x + cw, y0, C[0xF], 1.0)
        U.text(img, x + 2, y0 + 2, '%02d' % (k + 1), C[0xF] if hot else C[8], 1)
def endcard(img, t):
    if t >= 69.0:
        s = 'PERSISTENCE'; U.rect(img, 0, 40, W, 236, C[0], .78); U.text(img, (W - len(s) * 8 * 6) // 2, 62, s, C[0xF], 6)
        if t >= 70.5: s2 = '1728 PICTURES. NONE OF THEM MOVED.'; U.text(img, (W - len(s2) * 8 * 3) // 2, 146, s2, C[0xA], 3)
        if t >= 70.5: s3 = 'THE HORSES ARE FROM MUYBRIDGE, 1878.'; U.text(img, (W - len(s3) * 16) // 2, 196, s3, C[9], 2)

CUTS = [0, 6, 12, 18, 24, 27, 28.5, 30, 36, 40, 44, 48, 52, 56, 60, 63, 66]
RAW = OUT / 'raw'
def smear(t):
    """How much of the last three pictures is left in this one, 0..1. Under the lamp a ride that is neither slow
    nor locked is a different picture every twenty-fourth of a second, all over the frame: hard to look at, and
    for some people dangerous. So there the film keeps what an eye keeps, and the ride is a smear of ghosts that
    comes sharp as it locks. Slow, or locked, nothing is kept: every picture is clean."""
    w = omega(t); s = max(0.0, min((w - 3) / 5, 1.0)) * max(0.0, min((30 - w) / 2.5, 1.0))
    return max(s, .8) if 28.5 <= t < 30.0 else s                  # close on the regulator the horses behind it are near and fast: ghosts, and the hand stays sharp
def base(i):
    t = i / FPS; img = np.ascontiguousarray(picture(t), np.float32)
    for tp, k in ((12.0, .3), (36.0, .2), (63.0, .25)):                 # the lights; the lock
        if 0 <= t - tp < .4: img = img + (C[0xF] - img) * (k * math.exp(-(t - tp) * 9))
    return X.glow(img)
def _raw(i):
    f = RAW / ('f_%04d.png' % i)
    if f.exists(): return cv2.imread(str(f))[..., ::-1].astype(np.float32) / 255
    return base(i)
def taps(i):
    """The earlier pictures that leave a ghost in picture i, with their weights (never across a cut)."""
    t = i / FPS; sm = smear(t); first = int(max(c for c in CUTS if c <= t + 1e-9) * FPS)
    if sm < .02: return []
    return [(i - k, w * sm) for k, w in ((1, .30), (2, .20), (3, .12)) if i - k >= first]
def frame(i):
    t = i / FPS; tp = taps(i)
    if tp:
        img = _raw(i) * (1 - sum(w for _, w in tp))
        for j, w in tp: img = img + _raw(j) * w
        img = np.ascontiguousarray(img, np.float32)
    else: img = _raw(i) if (RAW / ('f_%04d.png' % i)).exists() else base(i)
    caption(img, t); hud(img, t); card(img, t); endcard(img, t)
    return img

POINTS = [(1.0, 'WINTER QUARTERS'), (6.0, 'cut: inside'), (12.0, 'the lights'), (18.0, 'cut: the rim'), (24.0, 'cut: the stroboscope'), (27.0, 'lights out'), (27.125, 'the lamp'), (28.5, 'cut: his hand on the regulator'), (30.0, 'cut: it goes faster'),
          (36.0, 'LOCKED, and cut: the rim again'), (40.0, 'cut: three quarters'), (44.0, 'cut: going round'), (48.0, 'cut: the shadows'), (52.0, 'cut: over his shoulder'), (56.0, 'cut: from above'),
          (60.0, 'the regulator closed'), (63.0, 'lights on'), (66.0, 'cut: outside'), (69.0, 'title'), (70.5, 'NONE OF THEM MOVED')]
NEEDED = None
def _job(i):
    """First pass: a picture that leaves a ghost in a later one, or takes one, is kept clean in raw/ (the second pass mixes them)."""
    if i in NEEDED: X.save(str(RAW / ('f_%04d.png' % i)), base(i))
    else: X.save(str(FRAMES / ('f_%04d.png' % i)), frame(i))
    return i
def _job2(i): X.save(str(FRAMES / ('f_%04d.png' % i)), frame(i)); return i
if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == 'sheet':
        ts = [float(v) for v in a[1:]] or [1, 3, 5.5, 6.5, 8.5, 11, 12.5, 15, 17.5, 18.5, 20, 22, 24.5, 26, 27.5, 29.5, 31, 32.5, 33.5, 35, 36.5, 38, 40.5, 43, 45, 47, 48.5, 51, 52.5, 55, 56.5, 59, 60.5, 62, 63.5, 65.5, 67, 69.5, 71]
        from multiprocessing import Pool
        with Pool(min(len(ts), 20)) as pool: ims = pool.map(frame, [int(round(t * FPS)) for t in ts])
        cols = 3; small = [(np.clip(cv2.resize(im, (640, 360), interpolation=cv2.INTER_AREA), 0, 1) * 255).astype(np.uint8) for im in ims]
        for im, t in zip(small, ts): cv2.putText(im, f'{t:g}s', (8, 352), cv2.FONT_HERSHEY_SIMPLEX, .55, (255, 255, 255), 1, cv2.LINE_AA)
        while len(small) % cols: small.append(np.zeros_like(small[0]))
        per = 12
        for k in range(0, len(small), per):
            cv2.imwrite(str(OUT / ('sheet_%d.jpg' % (k // per))), np.vstack([np.hstack(small[j:j + cols]) for j in range(k, min(k + per, len(small)), cols)])[..., ::-1], [cv2.IMWRITE_JPEG_QUALITY, 88])
    elif a and a[0] in ('sync', 'pops', 'travel'):
        from backlot import sync
        if a[0] == 'sync': sync.check(POINTS, str(FRAMES), str(OUT / 'persistence.wav'), fps=FPS, out_jpg=str(HERE / 'persistence_sync.jpg'), out_json=str(OUT / 'sync.json'))
        elif a[0] == 'pops':
            for row in sync.pops(POINTS, str(FRAMES), fps=FPS): print(row)
        else: print(sync.travel(str(FRAMES))[1])
    elif a and a[0] == 'still':
        for v in a[1:]: X.save(str(OUT / ('still_%s.png' % v)), frame(int(round(float(v) * FPS))))
    else:
        from multiprocessing import Pool
        import subprocess
        from backlot import sound as sd
        FRAMES.mkdir(parents=True, exist_ok=True); RAW.mkdir(parents=True, exist_ok=True)
        todo = list(range(NF)) if not a else list(range(int(float(a[0]) * FPS), int(float(a[1]) * FPS)))
        mixed = [i for i in range(NF) if taps(i)]; NEEDED = set(mixed) | {j for i in mixed for j, _ in taps(i)}
        with Pool(28) as pool:
            for k, _ in enumerate(pool.imap_unordered(_job, todo, chunksize=2)):
                if k % 288 == 0: print(k, 'frames', flush=True)
        with Pool(28) as pool: list(pool.imap_unordered(_job2, [i for i in todo if i in NEEDED], chunksize=4))
        if not a or len(todo) == NF or (len(a) > 2 and a[2] == 'mux'):
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', str(FRAMES / 'f_%04d.png'), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-movflags', '+faststart', str(OUT / 'silent.mp4')], check=True)
            sd.mux(str(OUT / 'silent.mp4'), str(OUT / 'persistence.wav'), str(HERE / 'persistence.mp4'), loop_video=False, crf=27)
            X.save(str(HERE / 'persistence_poster.png'), frame(int(38.0 * FPS)))
            print('wrote', HERE / 'persistence.mp4')
