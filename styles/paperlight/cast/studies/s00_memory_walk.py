"""Study 0: a paper figure and a walk FROM MEMORY, before any research or reference. The baseline.
Self-contained on purpose. Run from the repository root: uv run python styles/paperlight/cast/studies/s00_memory_walk.py"""
import math
import numpy as np
from backlot import core, draw, comp, anim, screen

W, H, N = 640, 640, 24
HEAD = 62.0                        # one head, in pixels; the figure is 7.5 heads tall
GROUND = 590
OUT = 'out/cast/s00'

def capsule(a, b, ra, rb, n=10):
    a, b = np.array(a, float), np.array(b, float); d = b - a; ang = math.atan2(d[1], d[0])
    t1 = np.linspace(ang + math.pi / 2, ang + 3 * math.pi / 2, n); t2 = np.linspace(ang - math.pi / 2, ang + math.pi / 2, n)
    return np.r_[np.c_[a[0] + ra * np.cos(t1), a[1] + ra * np.sin(t1)], np.c_[b[0] + rb * np.cos(t2), b[1] + rb * np.sin(t2)]]

def down(p, length, angle_deg):
    """A point `length` from p, hanging down and swung forward (toward +x) by angle."""
    a = math.radians(angle_deg)
    return (p[0] + length * math.sin(a), p[1] + length * math.cos(a))

def pose(p):
    """What I remember a walk to be: legs swing like pendulums out of phase, the knee bends when the leg
    comes forward, arms swing against the legs."""
    s = math.sin(2 * math.pi * p); c = math.cos(2 * math.pi * p)
    hip = (W / 2, GROUND - 3.75 * HEAD)
    parts = []
    for side, sg in (('far', -1), ('near', 1)):
        th = 26 * s * sg; knee_bend = 42 * max(0.0, c * sg)
        k = down(hip, 1.9 * HEAD, th); an = down(k, 1.85 * HEAD, th - knee_bend); toe = (an[0] + .85 * HEAD, an[1] + 6)
        parts.append((side, [capsule(hip, k, 15, 11), capsule(k, an, 11, 7), capsule(an, toe, 7, 5)]))
    chest = (hip[0], hip[1] - 2.6 * HEAD)
    torso = capsule(hip, chest, 23, 26)
    neck = (chest[0], chest[1] - .28 * HEAD)
    head = capsule((neck[0] + 2, neck[1] - .5 * HEAD), (neck[0] + 6, neck[1] - .56 * HEAD), 29, 29)
    arms = []
    for side, sg in (('far', -1), ('near', 1)):
        sh = (chest[0], chest[1] + 10); ang = -24 * s * sg
        el = down(sh, 1.3 * HEAD, ang); wr = down(el, 1.2 * HEAD, ang + 14); hd = down(wr, .4 * HEAD, ang + 14)
        arms.append((side, [capsule(sh, el, 10, 8), capsule(el, wr, 8, 6), capsule(wr, hd, 7, 6)]))
    return parts, torso, neck, head, arms

def frame(i):
    p = i / N
    legs, torso, neck, head, arms = pose(p)
    img = core.canvas(W, H, '#e9e2cf')
    img = draw.paint(img, draw.rect(W, H, 0, GROUND + 8, W, H), '#b9b29c')
    def lay(polys, colour):
        nonlocal img
        img = draw.paint(img, draw.raster(polys, W, H), colour)
    lay(dict(arms)['far'], '#4a4f58'); lay(dict(legs)['far'], '#4a4f58')
    lay([torso, capsule(neck, (neck[0] + 2, neck[1] - 20), 9, 9), head], '#22262c')
    lay(dict(legs)['near'], '#22262c'); lay(dict(arms)['near'], '#22262c')
    return img

if __name__ == '__main__':
    pat = anim.render(frame, N, OUT + '/frames', workers=8)
    anim.encode(pat, 'styles/paperlight/cast/studies/s00_memory_walk.mp4', fps=12, loops=1, crf=20)
    screen.filmstrip(pat, 'styles/paperlight/cast/studies/s00_memory_walk.jpg', n=12, cols=6, cell_w=210)
    print('done')
