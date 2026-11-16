"""One-off: lift the pure-geometry vocabulary out of the Lit Window kit into backlot/shapes.py."""
import ast
from pathlib import Path
root = Path(__file__).resolve().parent.parent
src = (root / 'styles/lit-window/kit.py').read_text()
lines = src.split('\n')
want = ['resample', 'ribbon', 'seg', 'blob', 'chip', 'lens', 'wobble', 'ramp', 'fade', 'ticks', 'ripples', 'rain', 'snowfall', 'foliage', 'blades',
        'camera', 'extrude', 'boxplan', 'cloudband', '_tuft', 'conifer', 'sheen', 'ring', 'snowload', 'snowpillows', 'moonroad']
defs = {n.name: '\n'.join(lines[n.lineno - 1:n.end_lineno]) for n in ast.parse(src).body if isinstance(n, ast.FunctionDef)}
pre = '''"""backlot.shapes: a vocabulary of carved shapes, each returned as a polygon (N x 2 array of pixels).

Lifted from the Lit Window kit (styles/lit-window/kit.py) so every style and every department can
use it without a paint session. Functions read the module's canvas size and random generator:
call `setup(w, h, seed)` first. Rasterise polygons with backlot.draw.raster().
"""
import math
import numpy as np

W, H = 1280, 720
rng = np.random.default_rng(0)

def setup(w, h, seed=0):
    """Set the canvas size (used by camera() and nothing else) and reseed the generator."""
    global W, H, rng
    W, H = int(w), int(h); rng = np.random.default_rng(seed)

def seed(n):
    global rng
    rng = np.random.default_rng(n)

def spline(pts, closed=False, n=12):
    """Catmull-Rom curve through the points -> (N, 2) array."""
    P = np.asarray([p[:2] for p in pts], float)
    if len(P) < 3:
        return P
    Q = np.vstack([P[-1], P, P[0], P[1]]) if closed else np.vstack([2 * P[0] - P[1], P, 2 * P[-1] - P[-2]])
    out = []
    t = np.linspace(0, 1, n, endpoint=False)[:, None]
    for i in range(len(Q) - 3):
        p0, p1, p2, p3 = Q[i], Q[i + 1], Q[i + 2], Q[i + 3]
        out.append(.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t ** 2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out = np.vstack(out)
    return out if closed else np.vstack([out, P[-1]])

'''
(root / 'backlot/shapes.py').write_text(pre + '\n\n'.join(defs[n] for n in want) + '\n')
print('shapes.py:', len(want), 'functions')
