"""backlot.figure: a jointed human figure in profile. A skeleton in real proportions, joint angles,
forward kinematics, a ground, puppet parts, cycles, and ways to check a walk without watching it.

Everything is in units of stature (the figure is 1.0 tall) with y up; the figure faces +x.
Segment lengths are the anthropometric fractions of height from Winter, *Biomechanics and Motor
Control of Human Movement* (after Drillis & Contini): the same numbers a gait lab uses.

    fig = Figure()                     # or Figure(build=dict(...)) to change widths and proportions
    pose = walk(0.25)                  # a pose is a dict of joint angles in degrees
    J = fig.joints(pose)               # joint positions, feet on the ground
    parts = fig.parts(pose)            # [(name, polygon, layer), ...] far to near, in stature units
    img = draw_figure(img, fig, pose, scale=420, origin=(320, 560))

Angles (degrees): hip, shoulder: + is flexion (limb swings forward). knee: + bends the shin back.
elbow: + bends the forearm forward. ankle: + lifts the toes. lean: + tips the trunk forward.
Suffix N is the near limb (drawn in front), F the far one.
"""
import math
import numpy as np

SEG = dict(thigh=.245, shank=.246, ankle_h=.039, foot_back=.045, foot_fwd=.107, trunk=.288, neck=.067,
           upper_arm=.186, forearm=.146, hand=.108, head=.130)
WIDTH = dict(hip=.050, knee=.033, calf=.036, ankle=.019, chest=.062, waist=.050, shoulder=.029, elbow=.023, wrist=.016, neck=.024, head=1.0)
REST = dict(root=(0.0, 0.0), lean=3.0, head=0.0, hipN=0, kneeN=0, ankleN=0, hipF=0, kneeF=0, ankleF=0, shN=0, elN=8, wrN=0, shF=0, elF=8, wrF=0, shoulder_shift=0.0)

def _down(p, length, ang):
    a = math.radians(ang); return (p[0] + length * math.sin(a), p[1] - length * math.cos(a))

def _up(p, length, ang):
    a = math.radians(ang); return (p[0] + length * math.sin(a), p[1] + length * math.cos(a))

def _rot(v, ang):
    a = math.radians(ang); c, s = math.cos(a), math.sin(a)
    return (v[0] * c - v[1] * s, v[0] * s + v[1] * c)

def capsule(a, b, ra, rb, n=9):
    """A limb segment as paper: two round ends of different radius, joined. The round end at a joint is
    what lets one part turn over another without a gap."""
    a, b = np.array(a, float), np.array(b, float); d = b - a; ang = math.atan2(d[1], d[0])
    t1 = np.linspace(ang + math.pi / 2, ang + 3 * math.pi / 2, n); t2 = np.linspace(ang - math.pi / 2, ang + math.pi / 2, n)
    return np.r_[np.c_[a[0] + ra * np.cos(t1), a[1] + ra * np.sin(t1)], np.c_[b[0] + rb * np.cos(t2), b[1] + rb * np.sin(t2)]]

HEAD_PROFILE = [(-.050, .030), (-.046, .068), (-.012, .094), (.034, .086), (.050, .058), (.047, .041), (.066, .020), (.051, .011), (.054, -.001), (.049, -.012),
                (.046, -.031), (.022, -.041), (-.008, -.030), (-.030, -.022), (-.048, .000)]
TRUNK_PROFILE = [(0.0, -.050), (.10, -.046), (.20, -.056), (.275, -.050), (.325, -.024), (.325, .022), (.270, .056), (.170, .060), (.080, .052), (0.0, .050),
                 (-.050, .040), (-.062, .000), (-.048, -.046)]            # (along the spine from the hip, forward of it)

class Figure:
    def __init__(self, build=None, seg=None):
        self.seg = dict(SEG, **(seg or {})); self.w = dict(WIDTH, **(build or {}))

    # ---------------------------------------------------------------- skeleton
    def joints(self, pose, grounded=True):
        """Joint positions for a pose. With grounded=True the whole figure is lifted or lowered so that
        its lowest foot point rests on y = 0: the pelvis rises and falls by itself as the legs move."""
        p = dict(REST, **pose); s = self.seg; J = {}
        hip = p['root']; J['hip'] = hip
        J['chest'] = _up(hip, s['trunk'], p['lean']); J['headpivot'] = _up(hip, s['trunk'] + s['neck'], p['lean'])
        for k, sg in (('N', 1), ('F', -1)):
            knee = _down(hip, s['thigh'], p['hip' + k]); shin = p['hip' + k] - p['knee' + k]
            ankle = _down(knee, s['shank'], shin); phi = shin + p['ankle' + k]
            J['knee' + k], J['ankle' + k] = knee, ankle
            for nm, v in (('heel', (-s['foot_back'], -s['ankle_h'])), ('ball', (s['foot_fwd'] * .68, -s['ankle_h'])), ('toe', (s['foot_fwd'], -s['ankle_h'] * .75))):
                r = _rot(v, phi); J[nm + k] = (ankle[0] + r[0], ankle[1] + r[1])
            sh = (J['chest'][0] + sg * p['shoulder_shift'], J['chest'][1] - .012)
            el = _down(sh, s['upper_arm'], p['sh' + k]); wr = _down(el, s['forearm'], p['sh' + k] + p['el' + k])
            J['shoulder' + k], J['elbow' + k], J['wrist' + k] = sh, el, wr
            J['hand' + k] = _down(wr, s['hand'], p['sh' + k] + p['el' + k] + p['wr' + k])
        if grounded and not p.get('fixed'):
            lo = min(J[n + k][1] for n in ('heel', 'ball', 'toe') for k in 'NF')
            J = {k: (v[0], v[1] - lo) for k, v in J.items()}
        J['_lean'] = p['lean']; J['_head'] = p['lean'] + p['head']
        return J

    # ---------------------------------------------------------------- the paper parts
    def parts(self, pose, grounded=True):
        """The puppet: [(name, polygon in stature units, layer)], ordered far to near. layer -1 = far limbs, 0 = body, 1 = near limbs."""
        J = self.joints(pose, grounded); w = self.w; out = []
        def leg(k, layer):
            out.append(('thigh' + k, capsule(J['hip'], J['knee' + k], w['hip'], w['knee']), layer))
            out.append(('shin' + k, capsule(J['knee' + k], J['ankle' + k], w['calf'], w['ankle']), layer))
            a, h, b, t = (np.array(J[n + k]) for n in ('ankle', 'heel', 'ball', 'toe'))
            up = (a - (h + b) / 2); up = up / max(np.hypot(*up), 1e-9)
            out.append(('foot' + k, np.array([h + up * .004, h - up * .006, b - up * .008, t - up * .004, t + up * .012, a + up * w['ankle'] * .9 + (t - h) * .08, a + up * w['ankle'] * .9 - (t - h) * .16]), layer))
        def arm(k, layer):
            out.append(('upperarm' + k, capsule(J['shoulder' + k], J['elbow' + k], w['shoulder'], w['elbow']), layer))
            out.append(('forearm' + k, capsule(J['elbow' + k], J['wrist' + k], w['elbow'], w['wrist']), layer))
            out.append(('hand' + k, capsule(J['wrist' + k], J['hand' + k], w['wrist'] * 1.05, w['wrist'] * .8), layer))
        arm('F', -1); leg('F', -1)
        hip = np.array(J['hip']); lean = J['_lean']
        ax, fw = np.array(_rot((0, 1), -lean)), np.array(_rot((1, 0), -lean))
        sc = w['chest'] / .062
        out.append(('trunk', np.array([hip + ax * u + fw * v * (sc if u > .05 else w['hip'] / .050) for u, v in TRUNK_PROFILE]), 0))
        out.append(('neck', capsule(J['chest'], J['headpivot'], w['neck'], w['neck'] * .9), 0))
        hp = np.array(J['headpivot']); hs = self.seg['head'] / .130 * w['head']
        out.append(('head', np.array([hp + np.array(_rot((x * hs, y * hs), -J['_head'])) for x, y in HEAD_PROFILE]), 0))
        leg('N', 1); arm('N', 1)
        return out

# -------------------------------------------------------------------- cycles
def periodic(keys):
    """Smooth periodic curve through (phase, value) keys on 0..1: Catmull-Rom round the circle."""
    ks = sorted(keys); ph = np.array([k[0] for k in ks]); v = np.array([k[1] for k in ks], float)
    if ph[-1] >= 1.0: ph, v = ph[:-1], v[:-1]
    n = len(ph)
    def f(g):
        g = g % 1.0
        i = int(np.searchsorted(ph, g, side='right') - 1) % n
        p0, p1, p2, p3 = v[(i - 1) % n], v[i], v[(i + 1) % n], v[(i + 2) % n]
        a, b = ph[i], ph[(i + 1) % n] + (1.0 if i == n - 1 else 0.0)
        t = ((g - a) % 1.0) / max(b - a, 1e-9)
        return float(.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    return f

# One leg's sagittal joint angles over a stride, phase 0 = that leg's heel strike. Normative adult
# walking (Winter; Perry & Burnfield): stance about 60%, swing 40%.
GAIT = dict(
    hip=periodic([(0, 28), (.12, 22), (.30, 5), (.50, -10), (.60, -6), (.72, 12), (.85, 27), (.94, 30)]),
    knee=periodic([(0, 4), (.14, 18), (.40, 5), (.50, 10), (.60, 38), (.72, 63), (.85, 30), (.95, 5)]),
    ankle=periodic([(0, -2), (.07, -8), (.25, 4), (.45, 11), (.55, 2), (.62, -18), (.72, -8), (.85, 0)]),
)

def walk(g, gait=GAIT, arm=1.0, lean=4.0, bounce=1.0):
    """Pose at phase g of a walking stride (0 = near heel strikes). arm scales the arm swing."""
    p = {}
    for k, off in (('N', 0.0), ('F', .5)):
        q = g + off
        p['hip' + k], p['knee' + k], p['ankle' + k] = gait['hip'](q), gait['knee'](q), gait['ankle'](q)
        c = math.cos(2 * math.pi * q)
        p['sh' + k] = arm * (-21 * c - 3)                         # the arm is back when its own leg is forward
        p['el' + k] = 12 + arm * 12 * (1 - c)                     # and bends as it comes forward
        p['wr' + k] = 6
    p['lean'] = lean + 1.2 * math.cos(4 * math.pi * g)
    p['head'] = -(p['lean'] - lean) * .8
    p['shoulder_shift'] = .010 * math.cos(2 * math.pi * g)
    return p

def ik2(hip, target, l1, l2):
    """Two-bone leg IK with the knee forward: where must the thigh and knee be for the ankle to reach `target`?
    Returns (hip flexion, knee flexion) in degrees."""
    dx, dy = target[0] - hip[0], hip[1] - target[1]
    d = min(max(math.hypot(dx, dy), abs(l1 - l2) + 1e-6), l1 + l2 - 1e-6)
    alpha = math.atan2(dx, dy)
    beta = math.acos(max(-1, min(1, (l1 * l1 + d * d - l2 * l2) / (2 * l1 * d))))
    kappa = math.pi - math.acos(max(-1, min(1, (l1 * l1 + l2 * l2 - d * d) / (2 * l1 * l2))))
    return math.degrees(alpha + beta), math.degrees(kappa)

def _sm(t):
    t = min(max(t, 0.0), 1.0); return t * t * (3 - 2 * t)

class Walk:
    """A walk whose feet stay where they are put. The planted foot is fixed to the ground (which moves back
    under a figure walking on the spot), rolling from heel to flat to ball; the pelvis rides over it at the
    height the stance knee allows; the legs are solved backwards from the feet. The free foot is carried
    along a path from toe-off to the next heel strike. Change the numbers and it is a different walk.

        w = Walk(fig, stride=.80)      # stride in statures per cycle; stance = share of the cycle a foot is down
        pose = w.pose(g)               # g in 0..1; phase 0 = near heel strike
    """
    def __init__(s, fig, stride=.80, stance=.62, strike_pitch=18.0, toeoff_pitch=-38.0, lift=.050, stance_knee=((0, 5), (.14, 17), (.40, 6), (.50, 9)),
                 lean=4.0, arm=1.0, elbow=10.0, n=120):
        s.fig, s.stride, s.stance, s.lean, s.arm, s.elbow, s.n = fig, stride, stance, lean, arm, elbow, n
        g_ = fig.seg; l1, l2 = g_['thigh'], g_['shank']
        fb, ff, ah = g_['foot_back'], g_['foot_fwd'] * .68, g_['ankle_h']
        x0 = stride * .30 - fb                                   # heel strike lands this far ahead, so the ankle is under the hip at mid-stance
        kn = lambda q: float(np.interp(q, [k[0] for k in stance_knee], [k[1] for k in stance_knee]))
        def pitch(q):                                            # the foot's angle to the ground through the stride
            if q < .10: return strike_pitch * (1 - _sm(q / .10))
            if q < .40: return 0.0
            if q < stance: return toeoff_pitch * _sm((q - .40) / (stance - .40)) ** 1.6
            t = (q - stance) / (1 - stance)
            return toeoff_pitch + (-8 - toeoff_pitch) * _sm(t / .45) if t < .45 else -8 + (strike_pitch + 8) * _sm((t - .45) / .55)
        def planted(q):                                          # ankle position while the foot is down
            hx, ph = x0 - stride * q, pitch(q)
            if ph >= 0:
                r = _rot((fb, ah), ph); return (hx + r[0], r[1])
            r = _rot((-ff, ah), ph); return (hx + fb + ff + r[0], r[1])
        a_off, a_on = planted(stance), planted(0.0)
        def ankle(q):
            if q < stance: return planted(q)
            t = (q - stance) / (1 - stance)
            return (a_off[0] + (a_on[0] - a_off[0]) * _sm(t), a_off[1] + (a_on[1] - a_off[1]) * t + lift * math.sin(math.pi * t ** .8))
        G = np.arange(n) / n
        hy = np.zeros(n)
        for i, g in enumerate(G):
            est = []
            for off in (0.0, .5):
                q = (g + off) % 1.0
                if q < stance:
                    a = ankle(q); k = math.radians(kn(q)) if q < .5 else 0.0
                    d = math.sqrt(l1 * l1 + l2 * l2 + 2 * l1 * l2 * math.cos(k)) * (1.0 if q < .5 else .999)
                    est.append(a[1] + math.sqrt(max(d * d - a[0] * a[0], 1e-6)))
            hy[i] = min(est)
        for _ in range(3):                                       # take the corners off the pelvis path
            hy = (np.roll(hy, 2) + 2 * np.roll(hy, 1) + 3 * hy + 2 * np.roll(hy, -1) + np.roll(hy, -2)) / 9
        hy -= max(0.0, max(hy[i] - (ankle((G[i] + off) % 1.0)[1] + math.sqrt(max((l1 + l2) ** 2 * .998 - ankle((G[i] + off) % 1.0)[0] ** 2, 1e-6)))
                           for i in range(n) for off in (0.0, .5) if (G[i] + off) % 1.0 < stance))      # never higher than a planted leg can reach
        s.t = {k: np.zeros(n) for k in ('hipN', 'kneeN', 'ankleN', 'hipF', 'kneeF', 'ankleF')}; s.hy = hy
        for i, g in enumerate(G):
            for nm, off in (('N', 0.0), ('F', .5)):
                q = (g + off) % 1.0
                h, k = ik2((0.0, hy[i]), ankle(q), l1, l2)
                s.t['hip' + nm][i], s.t['knee' + nm][i], s.t['ankle' + nm][i] = h, k, pitch(q) - (h - k)

    def pose(s, g):
        x = (g % 1.0) * s.n; i = int(x) % s.n; j = (i + 1) % s.n; f = x - int(x)
        p = {k: float(v[i] + (v[j] - v[i]) * f) for k, v in s.t.items()}
        p['root'] = (0.0, float(s.hy[i] + (s.hy[j] - s.hy[i]) * f)); p['fixed'] = True
        for k, off in (('N', 0.0), ('F', .5)):
            c = math.cos(2 * math.pi * (g + off))
            p['sh' + k] = s.arm * (-20 * c - 3); p['el' + k] = s.elbow + s.arm * 8 * (1 - c); p['wr' + k] = 6
        p['lean'] = s.lean + 1.0 * math.cos(4 * math.pi * g); p['head'] = -(p['lean'] - s.lean) * .8
        p['shoulder_shift'] = .010 * math.cos(2 * math.pi * g)
        return p

def blend(a, b, t):
    """Mix two poses."""
    out = {}
    for k in set(a) | set(b):
        va, vb = a.get(k, REST.get(k, 0)), b.get(k, REST.get(k, 0))
        out[k] = tuple(x + (y - x) * t for x, y in zip(va, vb)) if isinstance(va, tuple) else va + (vb - va) * t
    return out

# -------------------------------------------------------------------- checking a walk without watching it
def gait_report(fig, cycle, n=48):
    """Numbers for a cycle(g) -> pose: how far the planted foot slides, how much the pelvis rises and falls,
    stride length, and what share of the stride each foot spends on the ground."""
    g = np.arange(n) / n
    J = [fig.joints(cycle(x)) for x in g]
    out = {}
    hipy = np.array([j['hip'][1] for j in J]); out['pelvis_bob'] = float(hipy.max() - hipy.min())
    for k in 'NF':
        low = np.array([min(j['heel' + k][1], j['ball' + k][1], j['toe' + k][1]) for j in J])
        down = low < .004
        ax = np.array([j['ball' + k][0] for j in J])
        v = np.diff(np.r_[ax, ax[0]])                                   # per-step horizontal travel of the foot relative to the hip
        st = down & np.roll(down, -1)
        out['stance' + k] = float(down.mean())
        if st.sum() > 2:
            out['speed' + k] = float(-np.median(v[st]) * n)             # statures per stride: the ground speed the stance foot implies
            out['slide' + k] = float(np.abs(v[st] - np.median(v[st])).mean() * n)
    out['stride'] = float(np.mean([out.get('speedN', 0), out.get('speedF', 0)]))
    return out

def draw_figure(img, fig, pose, scale, origin, colours=('#4a4f58', '#22262c', '#22262c'), grounded=True, joints=False):
    """Lay the puppet onto an image. origin = pixel position of (x=0, ground). colours = (far limbs, body, near limbs)."""
    from .draw import raster, paint
    h, w = img.shape[:2]
    for layer in (-1, 0, 1):
        polys = [np.c_[origin[0] + P[:, 0] * scale, origin[1] - P[:, 1] * scale] for _, P, L in fig.parts(pose, grounded) if L == layer]
        img = paint(img, raster(polys, w, h), colours[layer + 1])
    if joints:
        J = fig.joints(pose, grounded)
        dots = [capsule((origin[0] + J[k][0] * scale, origin[1] - J[k][1] * scale), (origin[0] + J[k][0] * scale + .01, origin[1] - J[k][1] * scale), 2.2, 2.2)
                for k in J if not k.startswith('_') and k not in ('ballN', 'ballF')]
        img = paint(img, raster(dots, w, h), '#e9e2cf')
    return img

def arcs(fig, cycle, scale, origin, w, h, names=('headpivot', 'hip', 'wristN', 'ankleN', 'toeN'), n=48, travel=0.0):
    """The paths joints trace over a cycle, as an image. Good motion moves along arcs; kinks show as corners."""
    import cv2
    from .core import canvas, col
    img = canvas(w, h, '#e9e2cf')
    cols = ['#b23b28', '#22364a', '#4f8f6a', '#8a5a2a', '#6a4a8a']
    for nm, c in zip(names, cols):
        pts = []
        for i in range(n + 1):
            j = fig.joints(cycle(i / n)); pts.append((origin[0] + (j[nm][0] + travel * i / n) * scale, origin[1] - j[nm][1] * scale))
        rgb = tuple(float(v) for v in col(c))
        cv2.polylines(img, [np.round(np.array(pts) * 16).astype(np.int32)], False, rgb + (1.0,), 2, cv2.LINE_AA, 4)
    return img
