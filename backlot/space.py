"""backlot.space: places in real units. One model, looked at from above, from the side, and through a lens.

World: metres. x is east, y is north, z is up. Bearings are compass degrees clockwise from north; altitudes
are degrees above the horizon. A lens is a focal length in millimetres on a 36 mm wide sensor.

    S = Set('Ebb Landing')                       the model: solids in metres, built once
    S.box('shed', (-70, -60), (-6, -2.5), (5, 8), kind='wall')
    S.cylinder('pile', (-30, 4), .2, -3, 5, kind='pile')
    drawing(S, 'plan', out='plan.svg', cameras=[cam])     plan, or 'from_south' / 'from_north' / 'from_east' / 'from_west'
    cam = Camera(eye=(-30, 0, 6.6), az=270, lens=28)      where it stands, which way it looks, what lens it carries
    p = render(S, cam)                           p['img'] (linear, premultiplied), p['depth'], p['solid'], p['line']
    cam.place((-88, 0, 5), 1.65)                 where a 1.65 m figure standing there lands, and how many pixels tall
    cam.sky(az, alt, .52)                        where a thing in the sky lands, and its radius in pixels
    moon(when_utc, lat, lon)                     where the moon really is, how much of it is lit, and which way up

What the picture looks like is not decided here: `render` gives flat tones per plane and mattes per solid, and the
style does the rest. What *is* decided here is everything that used to be chosen by feel: the horizon, every size,
every overlap, and where the moon is.
"""
import math, json, subprocess, tempfile
from pathlib import Path
import numpy as np
import cv2
from .core import F, col

# ------------------------------------------------------------------ lenses and directions
def fov(lens, sensor=36.0):
    """Horizontal field of view in degrees of a lens of `lens` mm on a sensor `sensor` mm wide."""
    return 2 * math.degrees(math.atan(sensor / 2 / lens))

def direction(az, alt=0.0):
    """Unit vector toward compass bearing `az`, `alt` degrees above the horizon."""
    a, h = math.radians(az), math.radians(alt)
    return np.array([math.sin(a) * math.cos(h), math.cos(a) * math.cos(h), math.sin(h)])

def bearing(v):
    """(az, alt) in degrees of a vector."""
    v = np.asarray(v, float); return math.degrees(math.atan2(v[0], v[1])) % 360, math.degrees(math.atan2(v[2], math.hypot(v[0], v[1])))

class Camera:
    """A pinhole camera in the world. Give `look` (a point) or `az` and `alt` (a direction)."""
    def __init__(s, eye, look=None, lens=35.0, size=(1280, 720), sensor=36.0, az=None, alt=0.0, roll=0.0, name=''):
        s.eye = np.array(eye, float); s.lens, s.sensor, s.size, s.roll, s.name = float(lens), float(sensor), tuple(size), roll, name
        s.fwd = direction(az, alt) if look is None else (np.array(look, float) - s.eye) / np.linalg.norm(np.array(look, float) - s.eye)
        r = np.cross(s.fwd, (0, 0, 1.0))
        r = np.array([1.0, 0, 0]) if np.linalg.norm(r) < 1e-9 else r / np.linalg.norm(r)
        u = np.cross(r, s.fwd)
        if roll:
            c, sn = math.cos(math.radians(roll)), math.sin(math.radians(roll)); r, u = c * r + sn * u, c * u - sn * r
        s.right, s.up = r, u
        s.f = s.size[0] * s.lens / s.sensor                     # focal length in pixels
        s.cx, s.cy = s.size[0] / 2, s.size[1] / 2
    hfov = property(lambda s: fov(s.lens, s.sensor))
    vfov = property(lambda s: 2 * math.degrees(math.atan(s.size[1] / 2 / s.f)))
    az = property(lambda s: bearing(s.fwd)[0]); alt = property(lambda s: bearing(s.fwd)[1])

    def but(s, **kw):
        """A copy with some things changed: cam.but(eye=..., lens=...). For moves."""
        d = dict(eye=s.eye, lens=s.lens, size=s.size, sensor=s.sensor, roll=s.roll, name=s.name)
        if 'look' not in kw and 'az' not in kw: d.update(az=s.az, alt=s.alt)
        d.update(kw); return Camera(**d)
    def cam(s, P):
        """World points (n, 3) -> camera coordinates (right, up, forward)."""
        d = np.atleast_2d(np.asarray(P, float)) - s.eye
        return np.c_[d @ s.right, d @ s.up, d @ s.fwd]
    def project(s, P):
        """World points -> (n, 3): screen x, screen y (down), depth along the axis in metres. Depth <= 0 is behind."""
        c = s.cam(P); z = np.where(np.abs(c[:, 2]) < 1e-9, 1e-9, c[:, 2])
        return np.c_[s.cx + s.f * c[:, 0] / z, s.cy - s.f * c[:, 1] / z, c[:, 2]]
    def p(s, x, y, z=0.0):
        q = s.project([(x, y, z)])[0]; return float(q[0]), float(q[1])
    def scale(s, dist):
        """Pixels per metre at `dist` metres along the axis."""
        return s.f / dist
    def place(s, P, height=1.0):
        """Where something standing at world point P and `height` metres tall lands: dict(x, foot, top, px, depth)."""
        a = s.project([P, np.asarray(P, float) + (0, 0, height)])
        return dict(x=float(a[0, 0]), foot=float(a[0, 1]), top=float(a[1, 1]), px=float(a[0, 1] - a[1, 1]), depth=float(a[0, 2]))
    def sky(s, az, alt, diameter=0.0):
        """A thing in the sky (at infinity): (x, y, radius in pixels), or None if it is behind the camera."""
        d = direction(az, alt); z = float(d @ s.fwd)
        if z <= 1e-6: return None
        return s.cx + s.f * float(d @ s.right) / z, s.cy - s.f * float(d @ s.up) / z, s.f * math.tan(math.radians(diameter / 2)) / z
    def horizon(s):
        """The y of the horizon (the sea's edge, ignoring the Earth's curve) for a camera that is not rolled:
        the centre of the frame when the camera is level, lower in the frame when it tilts up."""
        return s.cy + s.f * math.tan(math.radians(s.alt))
    def ray(s, sx, sy):
        """Unit direction in the world through a pixel."""
        d = s.fwd * s.f + s.right * (sx - s.cx) - s.up * (sy - s.cy); return d / np.linalg.norm(d)
    def ground(s, sx, sy, z=0.0):
        """The world point where a pixel's ray meets the level plane at height z, or None if it never does."""
        d = s.ray(sx, sy)
        if abs(d[2]) < 1e-9: return None
        t = (z - s.eye[2]) / d[2]
        return s.eye + d * t if t > 0 else None
    def describe(s):
        return f'{s.name or "camera"}: {s.lens:g} mm ({s.hfov:.1f} deg), eye at ({s.eye[0]:.1f}, {s.eye[1]:.1f}), {s.eye[2]:.1f} m up, looking {s.az:.0f} deg, {s.alt:+.1f} deg'

# ------------------------------------------------------------------ the model
KINDS = dict(water=('#101a28', '#16222f'), land=('#0b1016', '#222a30'), deck=('#161d28', '#3a4654'), wall=('#141a24', '#4d5b6b'), roof=('#0d1219', '#33404d'),
             pile=('#0a0e14', '#5b6878'), hull=('#10151e', '#596a7c'), cabin=('#1a222e', '#6f8092'), machine=('#13101b', '#7a6f8e'), rail=('#0b0f16', '#7b8794'),
             light=('#f2c56b', '#f2c56b'), cold=('#dbeeff', '#dbeeff'), track=('#0c1016', '#454f5a'), far=('#131c29', '#1b2634'))      # kind -> (colour in a night picture, fill on a drawing)

class Solid:
    def __init__(s, name, faces, kind='wall', colour=None, emit=0.0, on='both'):
        """on: 'both', or 'drawing' (only on plans and elevations: a footprint), or 'picture' (only through a lens)."""
        s.name, s.faces, s.kind, s.emit, s.on = name, [np.asarray(f, float) for f in faces], kind, emit, on
        s.colour = colour or KINDS.get(kind, KINDS['wall'])[0]
    def points(s): return np.vstack(s.faces)
    def move(s, dx=0.0, dy=0.0, dz=0.0):
        s.faces = [f + (dx, dy, dz) for f in s.faces]; return s
    def turn(s, deg, about=(0.0, 0.0)):
        """Rotate about a vertical axis, anticlockwise seen from above, by `deg`."""
        c, sn = math.cos(math.radians(deg)), math.sin(math.radians(deg)); ax, ay = about; out = []
        for f in s.faces:
            x, y = f[:, 0] - ax, f[:, 1] - ay
            out.append(np.c_[ax + c * x - sn * y, ay + sn * x + c * y, f[:, 2]])
        s.faces = out; return s

def _prism_faces(plan, z0, z1, plan1=None):
    a = [(x, y, z0) for x, y in plan]; b = [(x, y, z1) for x, y in (plan1 if plan1 is not None else plan)]; n = len(a)
    return [a[::-1], b] + [[a[i], a[(i + 1) % n], b[(i + 1) % n], b[i]] for i in range(n)]

class Set:
    """A place: named solids in metres, plus the labels and dimensions that belong on its drawings."""
    def __init__(s, name, lat=47.6, lon=-122.5):
        s.name, s.lat, s.lon, s.solids, s.labels, s.dims = name, lat, lon, [], [], []
    def add(s, solid): s.solids.append(solid); return solid
    def __getitem__(s, name): return [q for q in s.solids if q.name == name or q.name.startswith(name + '.')]
    def box(s, name, x, y, z, **kw):
        return s.add(Solid(name, _prism_faces([(x[0], y[0]), (x[1], y[0]), (x[1], y[1]), (x[0], y[1])], z[0], z[1]), **kw))
    def prism(s, name, plan, z0, z1, top=None, **kw):
        """An upright prism on a plan polygon; `top` is another polygon with as many points, for a taper or a lean."""
        return s.add(Solid(name, _prism_faces(plan, z0, z1, top), **kw))
    def cylinder(s, name, c, r, z0, z1, r1=None, n=10, **kw):
        ring = lambda rr: [(c[0] + rr * math.cos(2 * math.pi * k / n), c[1] + rr * math.sin(2 * math.pi * k / n)) for k in range(n)]
        return s.add(Solid(name, _prism_faces(ring(r), z0, z1, ring(r if r1 is None else r1)), **kw))
    def hexa(s, name, bottom, top, **kw):
        """Any six-sided block from four bottom corners and the four top corners above them (a ramp, a wedge)."""
        a, b = [tuple(p) for p in bottom], [tuple(p) for p in top]
        return s.add(Solid(name, [a[::-1], b] + [[a[i], a[(i + 1) % 4], b[(i + 1) % 4], b[i]] for i in range(4)], **kw))
    def gable(s, name, x, y, eave, ridge, along='x', over=.3, **kw):
        """A pitched roof over the rectangle x, y: ridge running along 'x' or 'y'."""
        x0, x1, y0, y1 = x[0] - over, x[1] + over, y[0] - over, y[1] + over
        if along == 'x':
            ym = (y0 + y1) / 2; r0, r1 = (x0, ym, ridge), (x1, ym, ridge)
            faces = [[(x0, y0, eave), (x1, y0, eave), r1, r0], [(x1, y1, eave), (x0, y1, eave), r0, r1], [(x0, y1, eave), (x0, y0, eave), r0], [(x1, y0, eave), (x1, y1, eave), r1]]
        else:
            xm = (x0 + x1) / 2; r0, r1 = (xm, y0, ridge), (xm, y1, ridge)
            faces = [[(x0, y0, eave), (x0, y1, eave), r1, r0], [(x1, y1, eave), (x1, y0, eave), r0, r1], [(x0, y0, eave), (x1, y0, eave), r0], [(x1, y1, eave), (x0, y1, eave), r1]]
        return s.add(Solid(name, faces, **{'kind': 'roof', **kw}))
    def tube(s, name, path, r, n=6, **kw):
        """A round bar along a path of 3D points: a rail, a chain, a cable as thick as a funnel."""
        P = [np.asarray(q, float) for q in path]; rings = []
        for i, q in enumerate(P):
            t = (P[min(i + 1, len(P) - 1)] - P[max(i - 1, 0)]); t = t / np.linalg.norm(t)
            a = np.cross(t, (0, 0, 1.0)); a = np.array([1.0, 0, 0]) if np.linalg.norm(a) < 1e-6 else a / np.linalg.norm(a); b = np.cross(a, t)
            rings.append([q + r * (math.cos(2 * math.pi * k / n) * a + math.sin(2 * math.pi * k / n) * b) for k in range(n)])
        faces = [rings[0][::-1], rings[-1]] + [[rings[i][k], rings[i][(k + 1) % n], rings[i + 1][(k + 1) % n], rings[i + 1][k]] for i in range(len(P) - 1) for k in range(n)]
        return s.add(Solid(name, faces, **kw))
    def card(s, name, polys, origin, heading, metres=1.0, flip=False, layer=0, **kw):
        """A flat paper cut-out standing in the world: polygons in its own units (u along the way it faces, v up,
        feet at v = 0), at `origin`, facing compass bearing `heading`, one unit = `metres`. Its near side (the
        side the drawing is meant to be seen from) is on its right hand; `layer` moves it 15 mm that way per
        step, so the parts of one puppet stack as they do on a table. It is a real object in the set: things in
        front hide it, and nearly edge-on it looks like what it is."""
        o = np.asarray(origin, float); d = direction(heading); side = direction(heading + 90) * .015 * layer; faces = []
        for q in polys:
            q = np.asarray(q, float); u = (-q[:, 0] if flip else q[:, 0]) * metres; v = q[:, 1] * metres
            faces.append(o[None, :] + side[None, :] + u[:, None] * d[None, :] + v[:, None] * np.array([0, 0, 1.0])[None, :])
        return s.add(Solid(name, faces, **kw))
    def face(s, name, pts, **kw):
        """One flat polygon: a window, a sign, the water."""
        return s.add(Solid(name, [pts], **kw))
    def label(s, text, at, small=False): s.labels.append((text, tuple(at), small)); return s
    def dim(s, a, b, text=None, off=3.0): s.dims.append((tuple(a), tuple(b), text, off)); return s
    def bounds(s):
        P = np.vstack([q.points() for q in s.solids if q.kind not in ('water', 'far')]); return P.min(0), P.max(0)

# ------------------------------------------------------------------ seeing it through a lens
def _normal(f):
    n = np.zeros(3)
    for i in range(len(f)):
        a, b = f[i], f[(i + 1) % len(f)]
        n += ((a[1] - b[1]) * (a[2] + b[2]), (a[2] - b[2]) * (a[0] + b[0]), (a[0] - b[0]) * (a[1] + b[1]))
    L = np.linalg.norm(n); return n / L if L > 1e-12 else np.array([0, 0, 1.0])

def _ears(P):
    """Triangles (index triples) of a simple polygon in 2D, by ear clipping."""
    n = len(P)
    if n < 3: return []
    if n == 3: return [(0, 1, 2)]
    area = sum(P[i][0] * P[(i + 1) % n][1] - P[(i + 1) % n][0] * P[i][1] for i in range(n))
    idx = list(range(n)) if area > 0 else list(range(n))[::-1]; out = []; guard = 0
    cross = lambda o, a, b: (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    while len(idx) > 3 and guard < 10 * n:
        guard += 1; m = len(idx); cut = False
        for k in range(m):
            i0, i1, i2 = idx[k - 1], idx[k], idx[(k + 1) % m]; a, b, c = P[i0], P[i1], P[i2]
            if cross(a, b, c) <= 1e-12: continue
            if any(j not in (i0, i1, i2) and cross(a, b, P[j]) >= 0 and cross(b, c, P[j]) >= 0 and cross(c, a, P[j]) >= 0 for j in idx): continue
            out.append((i0, i1, i2)); idx.pop(k); cut = True; break
        if not cut: break
    if len(idx) == 3: out.append(tuple(idx))
    else: out += [(idx[0], idx[k], idx[k + 1]) for k in range(1, len(idx) - 1)]
    return out

def triangles(f):
    """A planar polygon in 3D as a list of triangles (3, 3)."""
    n = _normal(f); a = np.array([1.0, 0, 0]) if abs(n[0]) < .9 else np.array([0, 1.0, 0])
    u = np.cross(n, a); u /= np.linalg.norm(u); v = np.cross(n, u)
    P = np.c_[f @ u, f @ v]
    return [f[list(t)] for t in _ears(P)]

def _clip_near(T, near):
    """Clip a polygon in camera coordinates to z >= near."""
    out = []
    for i in range(len(T)):
        a, b = T[i], T[(i + 1) % len(T)]
        if a[2] >= near: out.append(a)
        if (a[2] >= near) != (b[2] >= near):
            t = (near - a[2]) / (b[2] - a[2]); out.append(a + (b - a) * t)
    return out

def render(S, cam, light=None, lit=1.0, shade=.5, ss=2, near=.3, line=True, palette='picture'):
    """The set through the camera, with hidden surfaces removed. Returns a dict:

      img     linear premultiplied image, alpha 0 where there is only sky; each plane one flat tone, its colour
              times `lit` if it faces the `light` direction (a vector toward the light) and `shade` if not
      depth   metres along the axis (inf where sky)        solid   index into S.solids (-1 where sky)
      line    matte of outlines between solids and creases between planes, for a key block
      normal  the unit normal of the plane at each pixel, turned to face the camera (zero where sky)
      names   list of solid names, so  p['solid'] == names.index('shed')  is a matte
    """
    W, H = cam.size[0] * ss, cam.size[1] * ss; f, cx, cy = cam.f * ss, cam.cx * ss, cam.cy * ss
    zbuf = np.full((H, W), np.inf); fid = np.full((H, W), -1, np.int32)
    info = []                                                   # per face: (solid index, tone, plane id)
    L = None if light is None else np.asarray(light, float) / np.linalg.norm(light)
    for si, sol in enumerate(S.solids):
        if sol.on == 'drawing': continue
        base = col(KINDS.get(sol.kind, KINDS['wall'])[1]) if palette == 'drawing' else col(sol.colour) * (1.0 + sol.emit)      # 'drawing': the tones of the plans, for a layout sheet
        for face in sol.faces:
            n = _normal(face); ctr = face.mean(0)
            if n @ (cam.eye - ctr) < 0: n = -n
            k = 1.0 if (sol.emit > 0 or L is None) else (lit if n @ L > .12 else shade)
            me = len(info); info.append((si, base * k, hash((si, tuple(np.round(n, 2)), round(float(n @ ctr), 1))) & 0x7fffffff, n))
            for tri in triangles(face):
                T = _clip_near(list(cam.cam(tri)), near)
                for j in range(1, len(T) - 1):
                    a, b, c = T[0], T[j], T[j + 1]
                    ax, ay, bx, by, qx, qy = cx + f * a[0] / a[2], cy - f * a[1] / a[2], cx + f * b[0] / b[2], cy - f * b[1] / b[2], cx + f * c[0] / c[2], cy - f * c[1] / c[2]
                    x0, x1 = max(int(math.floor(min(ax, bx, qx))), 0), min(int(math.ceil(max(ax, bx, qx))), W - 1)
                    y0, y1 = max(int(math.floor(min(ay, by, qy))), 0), min(int(math.ceil(max(ay, by, qy))), H - 1)
                    if x1 < x0 or y1 < y0: continue
                    den = (by - qy) * (ax - qx) + (qx - bx) * (ay - qy)
                    if abs(den) < 1e-9: continue
                    X = (np.arange(x0, x1 + 1) + .5)[None, :]; Y = (np.arange(y0, y1 + 1) + .5)[:, None]
                    w0 = ((by - qy) * (X - qx) + (qx - bx) * (Y - qy)) / den; w1 = ((qy - ay) * (X - qx) + (ax - qx) * (Y - qy)) / den; w2 = 1 - w0 - w1
                    with np.errstate(divide='ignore', invalid='ignore'): z = 1.0 / (w0 / a[2] + w1 / b[2] + w2 / c[2])
                    sub = zbuf[y0:y1 + 1, x0:x1 + 1]; m = (w0 >= -1e-6) & (w1 >= -1e-6) & (w2 >= -1e-6) & (z < sub - 1e-6 * z)
                    sub[m] = z[m]; fid[y0:y1 + 1, x0:x1 + 1][m] = me
    tones = np.array([i[1] for i in info] + [[0, 0, 0]], np.float64); sol_of = np.array([i[0] for i in info] + [-1]); plane_of = np.array([i[2] for i in info] + [-1])
    rgb = tones[fid]; a = (fid >= 0).astype(np.float64)
    img = np.dstack([rgb * a[..., None], a]).astype(F)
    out = dict(img=cv2.resize(img, cam.size, interpolation=cv2.INTER_AREA), depth=zbuf[ss // 2::ss, ss // 2::ss].astype(F),
               solid=sol_of[fid][ss // 2::ss, ss // 2::ss], names=[q.name for q in S.solids],
               normal=np.array([i[3] for i in info] + [[0, 0, 0]], np.float32)[fid[ss // 2::ss, ss // 2::ss]])
    if line:
        pl = plane_of[fid]; e = np.zeros((H, W), np.float32)
        e[:, 1:] = np.maximum(e[:, 1:], pl[:, 1:] != pl[:, :-1]); e[1:, :] = np.maximum(e[1:, :], pl[1:, :] != pl[:-1, :])
        e = cv2.dilate(e, np.ones((ss, ss), np.uint8)) if ss > 1 else e
        out['line'] = cv2.resize(e, cam.size, interpolation=cv2.INTER_AREA)
    return out

def positions(p, cam):
    """The world point seen at every pixel of a render (h, w, 3); nan where there is only sky. With this a
    texture or a pool of light can be put on the place itself instead of on the picture: plank seams that
    converge because the deck does, light that falls off with real distance."""
    W, H = cam.size; y, x = np.mgrid[:H, :W].astype(np.float64)
    d = cam.fwd[None, None, :] * cam.f + cam.right[None, None, :] * (x + .5 - cam.cx)[..., None] - cam.up[None, None, :] * (y + .5 - cam.cy)[..., None]
    z = np.where(np.isfinite(p['depth']), p['depth'], np.nan)
    return cam.eye[None, None, :] + d * (z / cam.f)[..., None]

def pools(img, p, cam, lights, P=None):
    """Light landing on the place. `lights` is a list of (position, colour, strength, reach): each adds its
    colour to every surface that faces it, falling off with distance (half strength at `reach` metres). No
    shadows are cast: keep the reach short. This is the print rule (a light is shown by what it lands on) done
    by geometry."""
    P = positions(p, cam) if P is None else P; n = p['normal'].astype(np.float64); out = img.copy(); ok = np.isfinite(P[..., 0]); P = np.nan_to_num(P)
    ok = ok & (~np.isin(p['solid'], [i for i, nm in enumerate(p['names']) if nm == 'water']))      # water does not take a pool of light: it shows a light as broken reflections, and that is the style's job
    for pos, colour, k, reach in lights:
        L = np.asarray(pos, float)[None, None, :] - P; dist = np.sqrt((L ** 2).sum(-1)); dist = np.where(ok, dist, 1e9)
        lam = np.clip((n * L).sum(-1) / np.maximum(dist, 1e-6), 0, 1)
        out[..., :3] += (col(colour)[None, None, :] * (k * lam / (1 + (dist / reach) ** 2))[..., None] * ok[..., None]).astype(F)
    return out

def matte(p, *names):
    """Matte of the named solids (a name matches itself and anything that starts with it and a dot) from a render."""
    ids = [i for i, n in enumerate(p['names']) if any(n == q or n.startswith(q + '.') for q in names)]
    return np.isin(p['solid'], ids).astype(F)

def card(cam, polys, origin, heading, metres=1.0, flip=False):
    """A flat paper figure standing in the world. `polys` are 2D polygons in the figure's own units (u along the
    way it faces, v up, feet at v = 0); it stands at `origin` facing compass bearing `heading`; one unit is
    `metres`. Returns (polygons on screen, depth in metres of the feet). A card seen nearly edge-on looks like a
    card: keep the camera within about fifty degrees of square to it."""
    o = np.asarray(origin, float); d = direction(heading); out = []
    for q in polys:
        q = np.asarray(q, float); u = (-q[:, 0] if flip else q[:, 0]) * metres; v = q[:, 1] * metres
        P = o[None, :] + u[:, None] * d[None, :] + v[:, None] * np.array([0, 0, 1.0])[None, :]
        out.append(cam.project(P)[:, :2])
    return out, float(cam.project([o])[0, 2])

# ------------------------------------------------------------------ the sky
def _jd(when):
    """Julian date of a UTC datetime (1901 to 2099)."""
    Y, M, D = when.year, when.month, when.day; ut = when.hour + when.minute / 60 + when.second / 3600
    return 367 * Y - (7 * (Y + (M + 9) // 12)) // 4 + (275 * M) // 9 + D + 1721013.5 + ut / 24

def _altaz(ra, dec, lst, lat):
    Hh = math.radians((lst - ra) % 360); d, p = math.radians(dec), math.radians(lat)
    alt = math.asin(math.sin(p) * math.sin(d) + math.cos(p) * math.cos(d) * math.cos(Hh))
    az = math.atan2(-math.cos(d) * math.sin(Hh), math.sin(d) * math.cos(p) - math.cos(d) * math.cos(Hh) * math.sin(p))
    alt = math.degrees(alt)
    if alt > -1.5: alt += 1 / math.tan(math.radians(alt + 7.31 / (alt + 4.4))) / 60          # refraction lifts things near the horizon by about half a degree
    return math.degrees(az) % 360, alt

def sun(when, lat, lon):
    """The sun for a UTC datetime and a place (lon east positive): dict(az, alt, ra, dec). Good to about 0.02 degrees."""
    n = _jd(when) - 2451545.0; Ls = (280.460 + .9856474 * n) % 360; g = math.radians((357.528 + .9856003 * n) % 360)
    lam = math.radians(Ls + 1.915 * math.sin(g) + .020 * math.sin(2 * g)); eps = math.radians(23.439 - 4e-7 * n)
    ra = math.degrees(math.atan2(math.cos(eps) * math.sin(lam), math.cos(lam))) % 360; dec = math.degrees(math.asin(math.sin(eps) * math.sin(lam)))
    lst = (280.46061837 + 360.98564736629 * n + lon) % 360
    az, alt = _altaz(ra, dec, lst, lat)
    return dict(az=az, alt=alt, ra=ra, dec=dec)

def moon(when, lat, lon):
    """The moon for a UTC datetime and a place: dict(az, alt, lit, limb, diameter, age).

    az, alt as seen from the place (parallax and refraction included; good to about a third of a degree);
    lit is the fraction of the disc that is lit; diameter in degrees; `toward_sun` is the (az, alt) of a point a
    little way from the moon toward the sun, so that a camera can find which way the bright limb faces."""
    jd = _jd(when); T = (jd - 2451545.0) / 36525; r = math.radians; sn = lambda x: math.sin(r(x)); cs = lambda x: math.cos(r(x))
    lam = 218.32 + 481267.881 * T + 6.29 * sn(135.0 + 477198.87 * T) - 1.27 * sn(259.3 - 413335.36 * T) + .66 * sn(235.7 + 890534.22 * T) + .21 * sn(269.9 + 954397.74 * T) - .19 * sn(357.5 + 35999.05 * T) - .11 * sn(186.5 + 966404.03 * T)
    bet = 5.13 * sn(93.3 + 483202.02 * T) + .28 * sn(228.2 + 960400.89 * T) - .28 * sn(318.3 + 6003.15 * T) - .17 * sn(217.6 - 407332.21 * T)
    par = .9508 + .0518 * cs(135.0 + 477198.87 * T) + .0095 * cs(259.3 - 413335.36 * T) + .0078 * cs(235.7 + 890534.22 * T) + .0028 * cs(269.9 + 954397.74 * T)
    dist = 1 / sn(par)                                           # Earth radii
    l, m, n = cs(bet) * cs(lam), .9175 * cs(bet) * sn(lam) - .3978 * sn(bet), .3978 * cs(bet) * sn(lam) + .9175 * sn(bet)
    lst = (280.46061837 + 360.98564736629 * (jd - 2451545.0) + lon) % 360
    x, y, z = dist * l - cs(lat) * cs(lst), dist * m - cs(lat) * sn(lst), dist * n - sn(lat)      # seen from the place, not from the Earth's centre
    ra = math.degrees(math.atan2(y, x)) % 360; dec = math.degrees(math.asin(z / math.sqrt(x * x + y * y + z * z)))
    az, alt = _altaz(ra, dec, lst, lat); s_ = sun(when, lat, lon)
    dm, ds = direction(az, alt), direction(s_['az'], s_['alt']); elong = math.degrees(math.acos(float(np.clip(dm @ ds, -1, 1))))
    t = dm + .02 * ds; t /= np.linalg.norm(t)
    return dict(az=az, alt=alt, lit=(1 - math.cos(math.radians(elong))) / 2, elongation=elong, diameter=2 * .2724 * par, toward_sun=bearing(t), sun=s_)

def moon_matte(w, h, cx, cy, r, lit=1.0, toward=(1.0, 0.0), soft=1.0):
    """The lit part of the moon as a matte: a disc of radius r at (cx, cy), `lit` of it showing (0 new, .5 half,
    1 full), the bright limb facing the screen direction `toward` (dx, dy, y down)."""
    y, x = np.mgrid[:h, :w].astype(np.float64); t = np.asarray(toward, float); t = t / (np.linalg.norm(t) or 1)
    u = (x - cx) * t[0] + (y - cy) * t[1]; v = -(x - cx) * t[1] + (y - cy) * t[0]            # u toward the sun
    disc = np.clip((r - np.hypot(u, v)) / soft + .5, 0, 1)
    k = 2 * lit - 1                                              # the terminator is half an ellipse of half-width |k| r: bulging to the dark side when gibbous
    edge = -k * np.sqrt(np.clip(r * r - v * v, 0, None))
    return (disc * np.clip((u - edge) / soft + .5, 0, 1)).astype(F)

# ------------------------------------------------------------------ drawings: plan, elevation, section
VIEWS = dict(plan=((1, 0, 0), (0, -1, 0), (0, 0, 1)), from_south=((1, 0, 0), (0, 0, -1), (0, -1, 0)), from_north=((-1, 0, 0), (0, 0, -1), (0, 1, 0)),
             from_west=((0, -1, 0), (0, 0, -1), (-1, 0, 0)), from_east=((0, 1, 0), (0, 0, -1), (1, 0, 0)))     # view -> (u axis, v axis (down the page), toward the viewer)
TITLES = dict(plan='plan', from_south='elevation from the south', from_north='elevation from the north', from_west='elevation from the west', from_east='elevation from the east')
PAPER, LINE, RED, WARM = '#0d1420', '#c5cfdb', '#b23b28', '#f2c56b'

def drawing(S, view='plan', out=None, bounds=None, scale=4.0, cameras=(), grid=10.0, title=None, cut=None, notes=(), reach=70.0, margin=56, sky=None):
    """A measured drawing of the set as SVG (and a PNG beside it, for looking at).

    view     'plan' or 'from_south' / 'from_north' / 'from_east' / 'from_west'
    bounds   ((x0, x1), (y0, y1), (z0, z1)) in metres; default: everything but the water
    scale    pixels per metre           grid   spacing of the grid in metres
    cameras  Camera objects: drawn on a plan as a point, a field-of-view wedge and a number
    cut      a section: for an elevation, the coordinate of the cutting plane along the viewing axis; what is in
             front of it is removed and what it cuts through is filled solid
    sky      on a plan, (az, label) pairs drawn as bearings from the compass rose (the moon's, for instance)
    """
    U, V, T = (np.array(a, float) for a in VIEWS[view])
    lo, hi = S.bounds()
    if bounds is None: bounds = ((lo[0] - 8, hi[0] + 8), (lo[1] - 8, hi[1] + 8), (min(lo[2], -4), hi[2] + 4))
    corners = np.array([(x, y, z) for x in bounds[0] for y in bounds[1] for z in bounds[2]])
    u0, u1, v0, v1 = (corners @ U).min(), (corners @ U).max(), (corners @ V).min(), (corners @ V).max()
    Wd, Hd = (u1 - u0) * scale + 2 * margin, (v1 - v0) * scale + 2 * margin + 46
    X = lambda P: (margin + (float(np.dot(P, U)) - u0) * scale, margin + (float(np.dot(P, V)) - v0) * scale)
    inside = lambda P: all(bounds[k][0] - 1e-6 <= P[k] <= bounds[k][1] + 1e-6 for k in range(3))
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{Wd:.0f}" height="{Hd:.0f}" viewBox="0 0 {Wd:.0f} {Hd:.0f}" font-family="Open Sans Condensed, Open Sans, sans-serif">',
         f'<rect width="100%" height="100%" fill="{PAPER}"/>', f'<clipPath id="frame"><rect x="{margin}" y="{margin}" width="{(u1 - u0) * scale:.1f}" height="{(v1 - v0) * scale:.1f}"/></clipPath>', '<g clip-path="url(#frame)">']
    # grid
    ax_u, ax_v = int(np.argmax(np.abs(U))), int(np.argmax(np.abs(V)))
    for ax, vec, a0, a1 in ((ax_u, U, u0, u1), (ax_v, V, v0, v1)):
        k = math.ceil(min(a0, a1) / grid)
        while k * grid <= max(a0, a1):
            t = margin + (k * grid - (u0 if vec is U else v0)) * scale
            o.append(f'<line x1="{t if vec is U else margin:.1f}" y1="{margin if vec is U else t:.1f}" x2="{t if vec is U else margin + (u1 - u0) * scale:.1f}" y2="{margin + (v1 - v0) * scale if vec is U else t:.1f}" stroke="{LINE}" stroke-opacity="{.22 if k % 5 == 0 else .09}" stroke-width="1"/>')
            k += 1
    # faces, far to near
    items = []
    for sol in S.solids:
        if sol.on == 'picture': continue
        fill = KINDS.get(sol.kind, KINDS['wall'])[1]
        for face in sol.faces:
            f = face
            if cut is not None and view != 'plan':               # keep what is beyond the cutting plane
                d = f @ T; keep = []
                for i in range(len(f)):
                    a, b, da, db = f[i], f[(i + 1) % len(f)], d[i] - cut, d[(i + 1) % len(f)] - cut
                    if da <= 0: keep.append(a)
                    if (da <= 0) != (db <= 0): keep.append(a + (b - a) * (da / (da - db)))
                if len(keep) < 3: continue
                f = np.array(keep)
            n = _normal(f)
            if abs(n @ T) < 1e-6: continue                       # edge-on
            if sol.kind != 'water' and any(f[:, k].max() < bounds[k][0] or f[:, k].min() > bounds[k][1] for k in range(3)): continue      # outside the box being drawn
            items.append((float((f @ T).max() if view == 'plan' else (f @ T).mean()), f, fill, sol))
    for _, f, fill, sol in sorted(items, key=lambda it: it[0]):
        pts = ' '.join(f'{X(p)[0]:.1f},{X(p)[1]:.1f}' for p in f)
        glow = sol.kind in ('light', 'cold')
        o.append(f'<polygon points="{pts}" fill="{fill}" stroke="{fill if glow else LINE}" stroke-width="{.6 if sol.kind in ("water", "far", "land") else 1}" stroke-opacity="{.35 if sol.kind in ("water", "far") else .9}" stroke-linejoin="round"/>')
    if cut is not None and view != 'plan':                       # what the plane cuts through, filled solid
        for sol in S.solids:
            if sol.kind in ('water', 'far'): continue
            pts = []
            for f in sol.faces:
                d = f @ T - cut
                for i in range(len(f)):
                    a, b, da, db = f[i], f[(i + 1) % len(f)], d[i], d[(i + 1) % len(f)]
                    if (da <= 0) != (db <= 0): pts.append(a + (b - a) * (da / (da - db)))
            if len(pts) >= 3:
                q = np.array([X(p) for p in pts], np.float32); hull = cv2.convexHull(q)[:, 0]
                o.append(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in hull)}" fill="{RED}" fill-opacity=".85" stroke="{LINE}" stroke-width="1"/>')
    # water line on elevations
    if view != 'plan':
        yw = margin + (0 - v0) * scale
        o.append(f'<line x1="{margin}" y1="{yw:.1f}" x2="{margin + (u1 - u0) * scale:.1f}" y2="{yw:.1f}" stroke="{LINE}" stroke-width="1.4" stroke-dasharray="10 5" stroke-opacity=".7"/>')
    # dimensions
    for a, b, text, off in S.dims:
        a, b = np.array(a, float), np.array(b, float)
        if abs((b - a) @ T) > .3 * np.linalg.norm(b - a): continue          # a dimension that runs toward the viewer cannot be drawn in this view
        pa, pb = np.array(X(a)), np.array(X(b)); L = np.linalg.norm(pb - pa)
        if L < 12: continue
        nrm = np.array([-(pb - pa)[1], (pb - pa)[0]]) / L * off * scale; qa, qb = pa + nrm, pb + nrm; mid = (qa + qb) / 2
        ang = math.degrees(math.atan2(qb[1] - qa[1], qb[0] - qa[0])); ang = ang + 180 if ang > 90 or ang < -90 else ang
        o.append(f'<g stroke="{RED}" stroke-width="1" fill="none"><line x1="{pa[0]:.1f}" y1="{pa[1]:.1f}" x2="{qa[0]:.1f}" y2="{qa[1]:.1f}" stroke-opacity=".5"/><line x1="{pb[0]:.1f}" y1="{pb[1]:.1f}" x2="{qb[0]:.1f}" y2="{qb[1]:.1f}" stroke-opacity=".5"/><line x1="{qa[0]:.1f}" y1="{qa[1]:.1f}" x2="{qb[0]:.1f}" y2="{qb[1]:.1f}"/></g>')
        o.append(f'<text x="{mid[0]:.1f}" y="{mid[1] - 4:.1f}" fill="{RED}" font-size="12" text-anchor="middle" transform="rotate({ang:.1f} {mid[0]:.1f} {mid[1]:.1f})">{text or f"{np.linalg.norm(b - a):g} m"}</text>')
    # cameras
    for k, c in enumerate(cameras):
        e = np.array(X(c.eye)); nm = c.name or str(k + 1)
        if view == 'plan':
            R = min(reach, 4000 / c.hfov); a0, a1 = c.az - c.hfov / 2, c.az + c.hfov / 2
            pts = [e] + [np.array(X(c.eye + direction(a0 + (a1 - a0) * j / 12) * R)) for j in range(13)]
            o.append(f'<polygon points="{" ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in pts)}" fill="{WARM}" fill-opacity=".10" stroke="{WARM}" stroke-width="1" stroke-opacity=".8"/>')
            far = np.array(X(c.eye + direction(c.az) * R * 1.12))
            o.append(f'<line x1="{e[0]:.1f}" y1="{e[1]:.1f}" x2="{far[0]:.1f}" y2="{far[1]:.1f}" stroke="{WARM}" stroke-width="1" stroke-dasharray="3 4"/>')
        o.append(f'<circle cx="{e[0]:.1f}" cy="{e[1]:.1f}" r="5" fill="{WARM}"/><text x="{e[0] + 8:.1f}" y="{e[1] - 8:.1f}" fill="{WARM}" font-size="14" font-weight="bold">{nm}</text>')
    # labels
    for text, at, small in S.labels:
        if not inside(at): continue
        x, y = X(at)
        o.append(f'<text x="{x:.1f}" y="{y:.1f}" fill="{LINE}" font-size="{10 if small else 13}" text-anchor="middle" letter-spacing=".5">{text}</text>')
    o.append('</g>')
    # frame, title block, scale bar, north arrow or heights
    fx, fy, fw, fh = margin, margin, (u1 - u0) * scale, (v1 - v0) * scale
    o.append(f'<rect x="{fx}" y="{fy}" width="{fw:.1f}" height="{fh:.1f}" fill="none" stroke="{LINE}" stroke-width="1.5"/>')
    by = fy + fh + 30; bar = max([b for b in (1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000) if b * scale <= 240] or [1])
    o.append(f'<text x="{fx}" y="{by + 6:.1f}" fill="{LINE}" font-size="20" letter-spacing="3">{(S.name + " · " + (title or TITLES[view])).upper()}</text>')
    bx = fx + fw - bar * scale
    for j in range(2):
        o.append(f'<rect x="{bx + j * bar * scale / 2:.1f}" y="{by - 6:.1f}" width="{bar * scale / 2:.1f}" height="6" fill="{LINE if j == 0 else "none"}" stroke="{LINE}" stroke-width="1"/>')
    o.append(f'<text x="{bx - 8:.1f}" y="{by + 1:.1f}" fill="{LINE}" font-size="12" text-anchor="end">{bar:g} m · grid {grid:g} m · {"; ".join(notes) if notes else "metres"}</text>')
    if view == 'plan':
        nx, ny = fx + fw - 34, fy + 44
        o.append(f'<g stroke="{LINE}" fill="none" stroke-width="1.3"><circle cx="{nx}" cy="{ny}" r="20" stroke-opacity=".5"/><path d="M{nx},{ny + 20} L{nx},{ny - 26} M{nx - 6},{ny - 14} L{nx},{ny - 26} L{nx + 6},{ny - 14}"/></g><text x="{nx}" y="{ny - 30}" fill="{LINE}" font-size="13" text-anchor="middle">N</text>')
        for az, lab in (sky or ()):
            d = direction(az); ex, ey = nx + d[0] * 20, ny - d[1] * 20
            o.append(f'<line x1="{nx}" y1="{ny}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{WARM}" stroke-width="1.6"/><circle cx="{ex:.1f}" cy="{ey:.1f}" r="3.2" fill="{WARM}"/><text x="{nx}" y="{ny + 36}" fill="{WARM}" font-size="11" text-anchor="middle">{lab}</text>')
    else:
        k = math.ceil(bounds[2][0] / grid)
        while k * grid <= bounds[2][1]:
            yy = margin + (-k * grid - v0) * scale
            o.append(f'<text x="{fx - 6}" y="{yy + 4:.1f}" fill="{LINE}" font-size="11" text-anchor="end">{k * grid:+g}</text>'); k += 1
    o.append('</svg>'); svg = '\n'.join(o)
    if out:
        Path(out).parent.mkdir(parents=True, exist_ok=True); Path(out).write_text(svg)
        subprocess.run(['rsvg-convert', '-o', str(Path(out).with_suffix('.png')), str(out)], check=False)
    return svg

# ------------------------------------------------------------------ a second opinion: the same set through Blender's camera
_BL = r'''
import bpy, json, sys, mathutils
d = json.load(open(sys.argv[sys.argv.index('--') + 1]))
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
for i, s in enumerate(d['solids']):
    verts, faces = [], []
    for f in s['faces']:
        faces.append(list(range(len(verts), len(verts) + len(f)))); verts += f
    me = bpy.data.meshes.new(s['name']); me.from_pydata(verts, [], faces); me.update()
    ob = bpy.data.objects.new(s['name'], me); sc.collection.objects.link(ob)
    m = bpy.data.materials.new(s['name']); m.diffuse_color = (*s['rgb'], 1.0); me.materials.append(m)
cam = bpy.data.cameras.new('cam'); ob = bpy.data.objects.new('cam', cam); sc.collection.objects.link(ob); sc.camera = ob
cam.lens = d['lens']; cam.sensor_width = d['sensor']; cam.sensor_fit = 'HORIZONTAL'; cam.clip_start = d['near']; cam.clip_end = 1e5
ob.location = d['eye']; ob.rotation_euler = mathutils.Vector(d['fwd']).to_track_quat('-Z', 'Y').to_euler()
ob.rotation_euler.rotate_axis('Z', -d['roll'] * 3.141592653589793 / 180)
sc.render.engine = 'BLENDER_WORKBENCH'; sh = sc.display.shading; sh.light = 'FLAT'; sh.color_type = 'MATERIAL'
sc.display.render_aa = 'OFF'; sc.view_settings.view_transform = 'Standard'; sc.render.film_transparent = True
sc.render.resolution_x, sc.render.resolution_y = d['size']; sc.render.resolution_percentage = 100
sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'; sc.render.filepath = d['out']
bpy.ops.render.render(write_still=True)
'''

def blender_check(S, cam, out_png=None, near=.3):
    """Render the same set through Blender's own camera with each solid in its own flat colour, and compare,
    solid by solid, with what `render` drew. Returns dict(agree, worst): the fraction of pixels on which the two
    agree about which solid is in front, and the solids that differ most. This is the test that the projection,
    the lens and the hidden-surface removal here are right, done by a renderer that I did not write."""
    tmp = Path(tempfile.mkdtemp(prefix='space_check_')); out_png = out_png or str(tmp / 'blender.png')
    n = len(S.solids); ids = [((i % 16 * 16 + 8) / 255, (i // 16 % 16 * 16 + 8) / 255, (i // 256 * 16 + 8) / 255) for i in range(n)]      # a solid's number, written in its colour
    lin = lambda c: tuple(((v + .055) / 1.055) ** 2.4 if v > .04045 else v / 12.92 for v in c)
    spec = dict(solids=[dict(name=q.name, faces=[f.tolist() for f in q.faces], rgb=lin(ids[i])) for i, q in enumerate(S.solids) if q.on != 'drawing'],
                lens=cam.lens, sensor=cam.sensor, eye=cam.eye.tolist(), fwd=cam.fwd.tolist(), roll=cam.roll, size=list(cam.size), near=near, out=out_png)
    (tmp / 'spec.json').write_text(json.dumps(spec)); (tmp / 'run.py').write_text(_BL)
    r = subprocess.run(['blender', '-b', '--factory-startup', '-P', str(tmp / 'run.py'), '--', str(tmp / 'spec.json')], capture_output=True, text=True)
    if not Path(out_png).exists(): raise RuntimeError('Blender did not render: ' + r.stdout[-600:] + r.stderr[-600:])
    im = cv2.imread(out_png, cv2.IMREAD_UNCHANGED).astype(np.float64) / 255; rgb, a = im[..., 2::-1], im[..., 3]
    q = np.floor(rgb * 255 / 16 + 1e-6).astype(int); theirs = np.where(a > .5, q[..., 0] + q[..., 1] * 16 + q[..., 2] * 256, -1)
    mine = render(S, cam, ss=1, near=near, line=False)['solid']
    same = theirs == mine; worst = []
    for i in range(n):
        m = (mine == i) | (theirs == i)
        if m.sum() > 40: worst.append((round(float((same & m).sum() / m.sum()), 4), S.solids[i].name, int(m.sum())))
    return dict(agree=float(same.mean()), worst=sorted(worst)[:6], blender=out_png, differ=(~same).astype(F))
