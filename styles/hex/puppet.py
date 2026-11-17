"""A person in Hex who can be walked round: a jointed figure carved from the 5 cm grid.

A card (a flat sprite) is right from one side, and so every shot with a card in it is square-on. This is the
same small person as a solid: bones in metres, flesh carved round them cube by cube (`backlot.carve`), so the
camera may go anywhere and the figure may turn, walk toward the lens, reach and crouch.

    person(pose, look)              a Carving, its origin on the ground between the feet, facing its own +x
    walk(phase)                     the pose at `phase` (0..1) of a walking stride
    mix(a, b, t)                    a pose between two poses
    POSES                           stand, reach (an arm out to a lever), hold (a lamp held up), crouch, sit

A pose is a dict of angles in degrees. Legs and arms swing forward (+) and back (-) from straight down; `knee`
and `elbow` only bend one way; `out` lifts an arm sideways; `lean` tips the trunk forward; `turn` twists the
shoulders on the hips. `look` turns the head (degrees to its left).
"""
import sys, math
from functools import lru_cache
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent)); sys.path.insert(1, str(Path(__file__).resolve().parents[2]))
import numpy as np
from scipy.interpolate import PchipInterpolator
from backlot.carve import Carving
from backlot.depth import HOLE

STAND = dict(hipL=0, hipR=0, kneeL=0, kneeR=0, shL=0, shR=0, elL=8, elR=8, outL=4, outR=4, lean=0, turn=0, drop=0)
POSES = dict(
    stand=STAND,
    reach=dict(STAND, shR=75, elR=10, lean=8, hipL=-8, hipR=10, kneeR=10),              # the right hand out to a lever
    pull=dict(STAND, shR=40, elR=70, lean=-6, hipL=10, hipR=-12, kneeL=12),             # and drawn back
    hold=dict(STAND, shL=80, elL=20, outL=10, lean=2),                                  # a lamp held out in front (the left hand carries)
    crouch=dict(STAND, hipL=75, hipR=95, kneeL=120, kneeR=125, lean=30, shR=50, elR=40, shL=30, elL=50),
    push=dict(STAND, shL=55, shR=55, elL=20, elR=20, lean=8),                           # both hands on something wheeled
    look_up=dict(STAND, lean=-6, shL=-6, shR=-6),
)
# the suit: (suit, shade, boots, skin, cap, scarf)
SUIT = (0x9, 0x8, 0x2, 0xA, 0x3, 0xE)
_LEG = [0, .125, .25, .375, .5, .625, .75, .875]            # one leg through a stride, from its own heel strike
_HIP = PchipInterpolator(np.r_[np.array(_LEG) - 1, _LEG, np.array(_LEG) + 1], np.tile([25, 18, 5, -8, -22, -15, 8, 26], 3))
_KNEE = PchipInterpolator(np.r_[np.array(_LEG) - 1, _LEG, np.array(_LEG) + 1], np.tile([5, 15, 8, 5, 10, 45, 62, 30], 3))

def walk(phase, swing=1.0):
    """A stride: the left heel strikes at 0, the right at one half. Arms go against the legs."""
    a, b = phase % 1.0, (phase + .5) % 1.0
    return dict(STAND, hipL=float(_HIP(a)), kneeL=float(_KNEE(a)), hipR=float(_HIP(b)), kneeR=float(_KNEE(b)),
                shL=-22 * swing * math.cos(2 * math.pi * a), shR=-22 * swing * math.cos(2 * math.pi * b), elL=14 + 8 * math.cos(2 * math.pi * a), elR=14 + 8 * math.cos(2 * math.pi * b), lean=4)

def mix(a, b, t):
    t = min(max(t, 0.0), 1.0); t = t * t * (3 - 2 * t); return {k: a[k] * (1 - t) + b.get(k, a[k]) * t for k in a}

def _d(deg): a = math.radians(deg); return np.array([math.sin(a), 0.0, -math.cos(a)])        # from straight down, swung forward

def bones(pose):
    """Joint positions in metres, origin on the ground under the hips, facing +x. The lower foot is on the ground."""
    P = dict(STAND, **pose); J = {}; hw, sw = .09, .19
    for side, sg in (('L', 1), ('R', -1)):
        h = np.array([0, sg * hw, 0.0]); k = h + .44 * _d(P['hip' + side]); a = k + .43 * _d(P['hip' + side] - P['knee' + side])
        toe = a + .16 * _d(P['hip' + side] - P['knee' + side] + 90) * np.array([1, 1, 1]); J['hip' + side], J['knee' + side], J['ankle' + side], J['toe' + side] = h, k, a, toe
    low = min(J['ankleL'][2], J['ankleR'][2], J['toeL'][2], J['toeR'][2]) - .06                  # the sole
    up = np.array([0, 0, -low - P['drop']])
    for k in list(J): J[k] = J[k] + up
    ln = math.radians(P['lean']); tr = np.array([math.sin(ln), 0, math.cos(ln)]); J['pelvis'] = up.copy(); J['chest'] = up + tr * .34; J['neck'] = up + tr * .52; J['head'] = up + tr * .66
    tw = math.radians(P['turn']); fwd = np.array([math.cos(tw), math.sin(tw), 0]); left = np.array([-math.sin(tw), math.cos(tw), 0])
    for side, sg in (('L', 1), ('R', -1)):
        s = J['neck'] + left * sg * sw - tr * .05; a0 = math.radians(P['sh' + side] + P['lean'] * .5); o = math.radians(P['out' + side])
        d1 = fwd * math.sin(a0) * math.cos(o) + left * sg * math.sin(o) - np.array([0, 0, 1]) * math.cos(a0) * math.cos(o)
        e = s + .29 * d1; a1 = a0 + math.radians(P['el' + side]); d2 = fwd * math.sin(a1) * math.cos(o * .5) + left * sg * math.sin(o * .5) - np.array([0, 0, 1]) * math.cos(a1) * math.cos(o * .5)
        J['sh' + side], J['el' + side], J['hand' + side] = s, e, e + .27 * d2
    J['fwd'], J['left'] = fwd, left
    return J

def _key(pose): return tuple(sorted((k, round(float(v) / 3) * 3) for k, v in pose.items()))

@lru_cache(maxsize=512)
def _carve(key, look, carry, suit):
    pose = dict(key); J = bones(pose); su, shade, boots, skin, cap, scarf = suit
    c = Carving((-.75, -.5, 0), (.85, .5, 1.95))
    for side in 'LR':
        c.limb(J['hip' + side], J['knee' + side], .08, .06, su); c.limb(J['knee' + side], J['ankle' + side], .058, .045, shade if side == 'R' else su)
        c.limb(J['ankle' + side], J['toe' + side], .05, .045, boots); c.ball(J['ankle' + side], .055, boots)
    c.limb(J['pelvis'], J['chest'], .12, .135, su, flat=1.45); c.limb(J['chest'], J['neck'] - (0, 0, .03), .135, .1, su, flat=1.5)
    for side in 'LR':
        c.limb(J['sh' + side], J['el' + side], .055, .045, su); c.limb(J['el' + side], J['hand' + side], .045, .04, su); c.ball(J['hand' + side], .05, skin)
    c.limb(J['neck'] - (0, 0, .02), J['neck'] + (0, 0, .05), .085, .085, scarf)
    h = J['head']; c.ball(h, (.105, .1, .115), skin)
    la = math.radians(look); f = J['fwd'] * math.cos(la) + J['left'] * math.sin(la)                # which way the face is
    c.paint(lambda X, Y, Z: ((X - h[0]) * f[0] + (Y - h[1]) * f[1] < .035) & (Z > h[2] - .13) & ((X - h[0]) ** 2 + (Y - h[1]) ** 2 + (Z - h[2]) ** 2 < .04), shade, only=[skin])   # hair: everything but the face
    c.paint(lambda X, Y, Z: (Z > h[2] + .045) & ((X - h[0]) ** 2 + (Y - h[1]) ** 2 + (Z - h[2]) ** 2 < .04), cap, only=[skin, shade])
    c.limb(h + f * .06 + (0, 0, .06), h + f * .16 + (0, 0, .05), .04, .03, cap, flat=2.2)                                   # the peak of the cap: it shows where he looks
    if carry:                                                                                                               # something in the left hand (the right is for levers)
        hd = J['handL']; d = J['fwd']
        if carry == 'lamp':
            c.box(hd + d * .02 - (.07, .07, .2), hd + d * .02 + (.07, .07, -.04), 0x8); c.limb(hd + (0, 0, -.04), hd + (0, 0, .0), .02, .02, 0x9)
            c.box(hd + d * .1 - (.03, .06, .17), hd + d * .1 + (.03, .06, -.07), 0xF)                                        # the lens: the only F on him
        elif carry == 'can':
            c.box(hd - (.05, .05, .16), hd + (.05, .05, -.04), 0xD); c.limb(hd + d * .05 - (0, 0, .06), hd + d * .2 - (0, 0, .0), .02, .02, 0xD)
    return c

def person(pose, look=0.0, carry=None, suit=SUIT):
    return _carve(_key(dict(STAND, **pose)), round(look / 15) * 15, carry, suit)

def hand(pose, side='L'):
    """Where a hand is, in the figure's own metres (for putting a lamp's light there)."""
    return bones(dict(_key(dict(STAND, **pose))))['hand' + side]

if __name__ == '__main__':
    import cv2, deep
    from backlot import depth as D
    from backlot.space import Set, Camera
    out = Path(__file__).resolve().parents[2] / 'out' / 'hex' / 'persistence'; out.mkdir(parents=True, exist_ok=True)
    T = (deep.table()[:, ::-1] * 255).astype(np.uint8); cells = []
    for k in range(8):
        p = person(walk(k / 8)).print('side'); img = np.zeros(p.shape + (3,), np.uint8); img[:] = T[1]; img[p != HOLE] = T[p[p != HOLE]]; cells.append(cv2.resize(img, None, fx=5, fy=5, interpolation=cv2.INTER_NEAREST))
    cv2.imwrite(str(out / 'walk.png'), np.hstack(cells))
    S = Set('t'); S.box('floor', (-3, 3), (-3, 3), (-.1, 0)); D.paint(S.solids[0], index=2); cells = []
    shots = [('walk', walk(.0), 0, None, 0), ('walk', walk(.25), 0, None, 45), ('walk', walk(.5), 0, None, 90), ('walk', walk(.75), 0, None, 135), ('walk', walk(0), 0, None, 180), ('walk', walk(.25), 0, None, 270),
             ('stand', POSES['stand'], 60, None, 100), ('reach', POSES['reach'], 0, None, 20), ('pull', POSES['pull'], 0, None, 20), ('hold', POSES['hold'], -30, 'lamp', 60), ('crouch', POSES['crouch'], 0, 'can', 30), ('look_up', POSES['look_up'], 0, 'lamp', 200)]
    for name, pose, look, carry, az in shots:
        b = person(pose, look, carry).block('him', (0, 0, 0), turn=az); cam = Camera((0, -5.0, 1.5), look=(0, 0, .9), lens=60, size=(220, 300))
        lamp = D.Light((-2.5, -3.5, 3.0), power=1.5, reach=5).bake(S.solids + [b]); g = D.gbuffer(S.solids + [b], cam); lv = D.lighting(g, [lamp], ambient=.12)
        cells.append((deep.glow(deep.colour(g, lv, steps=6, dither=0))[..., ::-1] * 255).astype(np.uint8))
    cv2.imwrite(str(out / 'keeper.png'), np.vstack([np.hstack(cells[:6]), np.hstack(cells[6:])])); print('ok', person(STAND).count())
