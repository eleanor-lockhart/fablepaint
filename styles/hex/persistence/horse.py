"""The horse: carved once, in twelve poses.

The poses are taken off Muybridge's photographs of the mare Sallie Gardner at a gallop (Palo Alto, 19 June 1878;
public domain; the card is looked at and measured, and is not in this repository). One stride is about nine
and a half of his frames. For each frame I read the slope of each leg bone against a grid, wrote the numbers
down below, and joined them into curves; the twelve carved horses are that curve at twelve equal steps.

    carving(k, row)     horse number k (0..11) as a backlot.carve.Carving, origin where the pole goes through
    joints(phi)         where every joint is at phase phi (0..1), for drawing a skeleton over the plate
    python horse.py     writes the sheet of twelve and the turnaround
"""
import sys, math
from functools import lru_cache
from pathlib import Path
HERE = Path(__file__).resolve().parent; sys.path.insert(0, str(HERE)); sys.path.insert(1, str(HERE.parent)); sys.path.insert(2, str(HERE.parents[2]))
import numpy as np
from scipy.interpolate import PchipInterpolator
from backlot.carve import Carving
from backlot.depth import HOLE

N = 12                                                           # horses to a ring, and frames to a stride
NECK = .58
# the phase of each of his frames, taking frame 2 (all four feet off the ground, gathered) as 0
PH = [0.0, .105, .21, .315, .42, .525, .63, .735, .84, .945]
# slopes in degrees from straight down, forward positive.  frames:  2     3     4     5     6     7     8     9    10    11
FORE = dict(forearm=[-30,  10,  45,  55,  65,  75,  70,  45,   0, -25],        # the leading foreleg (lands last)
            cannon= [-75, -100, -30, -10, 30,  70,  65,  45,   0, -25],
            pastern=[-95, -120, -40, -10, 35,  75,  75,  60,  35,   0])
HIND = dict(femur=  [ 60,  70,  55,  45,  25,  15,  15,  20,  30,  45],        # the hind leg that lands first
            gaskin= [-10,  10, -20, -45, -56, -68, -65, -50, -30, -25],
            cannon= [ 35,  70,  48,  27, -18, -64, -75, -90, -40,  22],
            pastern=[ 20,  60,  55,  50,  20, -70, -90, -110, -60,   0])
LAG_FORE, LAG_HIND = .21, -.16         # the other foreleg is two frames ahead of the leader; the other hind a frame and a half behind
LEN = dict(forearm=.36, fcannon=.27, pastern=.12, femur=.30, gaskin=.36, hcannon=.30)
ELBOW, HIP = (.38, .13, -.16), (-.42, .13, .06)                  # on the body, metres from the pole

def _curve(vals):
    x = np.r_[np.array(PH) - 1, PH, np.array(PH) + 1]; y = np.r_[vals, vals, vals]
    return PchipInterpolator(x, y)
_F = {k: _curve(v) for k, v in FORE.items()}; _H = {k: _curve(v) for k, v in HIND.items()}
def _dir(deg): a = math.radians(float(deg)); return np.array([math.sin(a), 0.0, -math.cos(a)])

def joints(phi):
    """Every joint at phase phi, in the horse's own metres (x forward, y left, z up; origin where the pole goes
    through the body). Legs: 'fl' is the leading foreleg (on its left), 'fr', 'hl', 'hr'."""
    phi = phi % 1.0; pitch = math.radians(4.0 * math.cos(2 * math.pi * (phi - .38)))
    cp, sp = math.cos(pitch), math.sin(pitch)
    def B(p): x, y, z = p; return np.array([x * cp - z * sp, y, x * sp + z * cp])           # the body pitches about the pole
    J = dict(pitch=pitch)
    for name, side, ph in (('fl', 1, phi), ('fr', -1, phi + LAG_FORE)):
        e = B((ELBOW[0], side * ELBOW[1], ELBOW[2])); k = e + LEN['forearm'] * _dir(_F['forearm'](ph % 1)); f = k + LEN['fcannon'] * _dir(_F['cannon'](ph % 1)); t = f + LEN['pastern'] * _dir(_F['pastern'](ph % 1))
        J[name] = [e, k, f, t]
    for name, side, ph in (('hr', -1, phi), ('hl', 1, phi + LAG_HIND)):
        h = B((HIP[0], side * HIP[1], HIP[2])); s = h + LEN['femur'] * _dir(_H['femur'](ph % 1)); k = s + LEN['gaskin'] * _dir(_H['gaskin'](ph % 1)); f = k + LEN['hcannon'] * _dir(_H['cannon'](ph % 1)); t = f + LEN['pastern'] * _dir(_H['pastern'](ph % 1))
        J[name] = [h, s, k, f, t]
    na = math.radians(44 + 7 * math.cos(2 * math.pi * (phi - .2))) + pitch                # the neck reaches out and down when the forelegs carry her
    J['neck'] = B((.40, 0, .12)); J['poll'] = J['neck'] + NECK * np.array([math.cos(na), 0, math.sin(na)])
    ha = na - math.radians(88); J['muzzle'] = J['poll'] + .52 * np.array([math.cos(ha), 0, math.sin(ha)])
    J['dock'] = B((-.62, 0, .14)); w = 2 * math.pi * (phi - .1); ang = lambda deg: np.array([math.cos(math.radians(deg)), 0, math.sin(math.radians(deg))])
    a = 186 + 12 * math.sin(w); b = a + 12 + 10 * math.sin(w - 1.2); c_ = b + 14 + 10 * math.sin(w - 2.4)
    t1 = J['dock'] + .26 * ang(a); t2 = t1 + .26 * ang(b); t3 = t2 + .24 * ang(c_)
    J['tail'] = [J['dock'], t1, t2, t3]; J['B'] = B
    return J

# coats: (coat, shade, mane, hoof, saddle, blanket, harness)
ROWS = {0: (0xA, 0x9, 0xE, 0xE, 0xD, 0xB, 0xE), 1: (0xA, 0x9, 0x3, 0x3, 0xB, 0xE, 0xD), 2: (0x3, 0x2, 0x9, 0x8, 0xE, 0xC, 0xD)}

@lru_cache(maxsize=None)
def carving(k, row=0, texel=.05):
    """Horse k of twelve (its phase is k/12), in the colours of its row (0 outside, 2 inside)."""
    coat, shade, mane, hoof, saddle, blanket, harness = ROWS[row]; J = joints(k / N); B = J['B']; body, sock = 250, coat
    c = Carving((-1.25, -.3, -1.15), (1.6, .3, .95), texel)
    # legs first, so the body covers their tops
    for name in ('fl', 'fr'):
        e, kn, f, t = J[name]; up = e + np.array([.02, 0, .22])
        c.limb(up, e, .13, .095, coat, flat=.75); c.limb(e, kn, .075, .05, coat); c.limb(kn, f, .042, .036, sock); c.limb(f, t, .04, .05, sock); c.ball(t, .055, hoof)
    for name in ('hl', 'hr'):
        h, s, kn, f, t = J[name]
        c.limb(h, s, .2, .13, coat, flat=.6); c.limb(s, kn, .1, .05, coat, flat=.8); c.limb(kn, f, .042, .036, sock); c.limb(f, t, .04, .05, sock); c.ball(t, .055, hoof)
    # the tail, then the body over its root
    T = J['tail']; c.limb(T[0], T[1], .07, .09, mane, flat=.7); c.limb(T[1], T[2], .09, .08, mane, flat=.7); c.limb(T[2], T[3], .08, .04, mane, flat=.7)
    c.ball(B((0, 0, 0)), (.55, .22, .265), body); c.ball(B((.38, 0, -.03)), (.28, .22, .34), body); c.ball(B((-.40, 0, .06)), (.31, .23, .32), body); c.ball(B((.28, 0, .2)), (.2, .1, .13), body)
    # belly in shade, by rule: the underside of the barrel
    P = J['pitch']; cp, sp = math.cos(P), math.sin(P)
    loc = lambda X, Y, Z: (X * cp + Z * sp, Y, -X * sp + Z * cp)                          # world of the horse -> the body's own axes
    c.paint(lambda X, Y, Z: loc(X, Y, Z)[2] < -.19, shade, only=[body])
    # trappings, painted on the trunk by rule (while the trunk is still its own paint, so the legs are left alone)
    def on(fn): return lambda X, Y, Z: fn(*loc(X, Y, Z))
    c.paint(on(lambda x, y, z: (x > -.3) & (x < .24) & (z > .0) & (z < .3)), blanket, only=[body])
    c.paint(on(lambda x, y, z: (x > -.2) & (x < .14) & (z > .12)), saddle, only=[body, blanket])
    c.paint(on(lambda x, y, z: (x > .02) & (x < .08) & (z <= .0)), harness, only=[body, shade])                           # the girth
    c.paint(on(lambda x, y, z: (x > .5) & (z > -.08) & (z < .0)), harness, only=[body])                                    # the breast collar
    c.paint(lambda X, Y, Z: X > -9, coat, only=[body])
    c.ball(B((-.22, 0, .27)), (.06, .13, .07), saddle); c.ball(B((.15, 0, .3)), (.05, .07, .06), saddle)
    # neck, head, mane, ears, eye
    nk, po, mu = J['neck'], J['poll'], J['muzzle']
    c.limb(nk + np.array([-.05, 0, -.06]), po, .27, .14, coat, flat=.52); c.limb(po, mu, .155, .095, coat, flat=.62)
    d = (po - nk); d /= np.linalg.norm(d); up = np.array([-d[2], 0, d[0]])
    for u in np.linspace(.05, 1.0, 40):
        r = .27 + (.14 - .27) * u; p = nk + d * (NECK * u) + up * (r + .01)
        c.dots([p, p + (0, .05, 0), p - (0, .05, 0), p - up * .05], mane)
    c.dots([po + up * .15 + (0, .06, 0), po + up * .15 - (0, .06, 0), po + up * .2 + (0, .06, 0), po + up * .2 - (0, .06, 0)], coat)   # ears
    hd = (mu - po); hd /= np.linalg.norm(hd); hu = np.array([-hd[2], 0, hd[0]])
    c.ball(po + hd * .12 - hu * .06, (.14, .095, .14), coat)                                                               # the cheek
    for sgn in (1, -1): c.dots([po + hd * .17 + hu * .06 + (0, sgn * .1, 0)], 0)                                           # eyes
    c.paint(lambda X, Y, Z: (np.abs((X - po[0]) * hd[0] + (Z - po[2]) * hd[2] - .34) < .028), harness, only=[coat])   # the noseband
    c.ball(mu + hd * .02, .075, shade)
    return c

def skeleton_sheet(out, scale=6):
    """The twelve, side on, in rows of four like his card, with the ground he ran on left out (they are on poles)."""
    import cv2, deep
    T = (deep.table()[:, ::-1] * 255).astype(np.uint8); cells = []
    for k in range(N):
        p = carving(k).print('side'); img = np.zeros(p.shape + (3,), np.uint8); img[:] = T[1]; img[p != HOLE] = T[p[p != HOLE]]
        img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST)
        cv2.putText(img, '%02d' % (k + 1), (8, 22), cv2.FONT_HERSHEY_SIMPLEX, .6, (112, 216, 255), 2); cells.append(img)
    rows = [np.hstack(cells[i:i + 4]) for i in range(0, N, 4)]; sheet = np.vstack(rows); cv2.imwrite(str(out), sheet); return sheet

def turnaround(out, k=6, n=8, size=(330, 300)):
    """One horse seen from n sides through the lens, lit: the test that it is a solid and not a drawing."""
    import cv2, deep
    from backlot import depth as D
    from backlot.space import Set, Camera
    S = Set('t'); S.box('floor', (-3, 3), (-3, 3), (-1.3, -1.2)); D.paint(S.solids[0], index=2); cells = []
    for i in range(n):
        az = 360 * i / n; h = carving(k).block('horse', (0, 0, 0), turn=az); cam = Camera((0, -5.2, .9), look=(0, 0, -.1), lens=50, size=size)
        lamp = D.Light((-2.5, -3.5, 3.0), power=1.5, reach=5).bake(S.solids + [h]); g = D.gbuffer(S.solids + [h], cam); lv = D.lighting(g, [lamp], ambient=.12)
        cells.append((deep.colour(g, lv, steps=6, dither=0)[..., ::-1] * 255).astype(np.uint8))
    sheet = np.vstack([np.hstack(cells[:n // 2]), np.hstack(cells[n // 2:])]); cv2.imwrite(str(out), sheet); return sheet

if __name__ == '__main__':
    out = HERE.parents[2] / 'out' / 'hex' / 'persistence'; out.mkdir(parents=True, exist_ok=True)
    s = skeleton_sheet(out / 'twelve.png'); print(s.shape, carving(0).count(), 'cubes', carving(0).grid.shape); turnaround(out / 'turnaround.png')
