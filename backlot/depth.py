"""backlot.depth: flat drawings in deep places (2.5D).

`backlot.space` says where things are. This says what they look like when the things are drawings: surfaces
painted on a grid that has a size in the world, cut-out figures standing among them, light that is cast and
blocked, and a camera that travels. Four ideas, and each one is a decision that used to be made by feel:

  a texel is a size in the world    every surface is painted on one grid (5 cm by default) and so is every figure
  light is worked out per texel     so a shadow's edge is the same hard square as the paint it falls on
  a figure is a card                a flat picture standing in the set: the set hides it, lights it, takes its shadow
  the camera moves, the paint stays parallax is one over distance and nothing else; nobody slides a layer by hand

    paint(S.box('wall', ...), skin=bricks)                  a tile of palette indices, repeated across the surface
    things = S.solids + [card('her', sprite, foot, cam.right)]      a frame's worth of things
    g = gbuffer(things, cam)                                what the lens sees: depth, paint, texel, normal
    lamp = Light((x, y, z), power=1, reach=3, aim=(0, 0, -1), cone=(30, 45)).bake(S.solids)
    level = lighting(g, [lamp], ambient=.05, moving=[her])  0 dark .. 1 fully lit, per pixel, constant per texel
    cam = fly([(0, eye0, look0, 28), (4, eye1, look1, 35)], t)       a camera move: keys of (seconds, eye, look, lens)

What colour a lit texel is, is the style's business: `g['index']` is the paint (a palette index) and `level` is
how much light it gets.
"""
import math
import numpy as np
from .space import Camera, Solid, _normal, triangles, _clip_near

HOLE = 255                                                       # in a skin: nothing here (the set shows through)

def paint(sol, skin=None, index=None, texel=None, glow=None, cast=None, flat=None, origin=None):
    """What a solid is painted with. skin: (h, w) uint8 palette indices, tiled over every face on a grid of
    `texel` metres anchored at `origin` (default the world's). index: one flat colour instead. glow: 0..1, how
    much of its own colour it shows with no light on it. cast: whether it throws a shadow. flat: lit the same
    from every side (a figure)."""
    for k, v in (('skin', skin), ('index', index), ('texel', texel), ('glow', glow), ('cast', cast), ('flat', flat), ('origin', origin)):
        if v is not None: setattr(sol, k, v)
    return sol

def _frame(n):
    """The paint grid of a plane with unit normal n: (U, V), unit vectors in the plane. U runs level (toward
    +x or +y), V runs down a wall (or toward -y on a floor), and neither depends on which side is looked at."""
    m = n if n[int(np.argmax(np.abs(n)))] > 0 else -n
    if abs(m[2]) > .999: return np.array([1., 0, 0]), np.array([0, -1., 0])
    U = np.cross((0, 0, 1.), m); U /= np.linalg.norm(U)
    if U[int(np.argmax(np.abs(U)))] < 0: U = -U
    V = np.cross(m, U); V /= np.linalg.norm(V)
    return U, (-V if V[2] > 0 else V)

def card(name, sprite, foot, right, texel=.05, anchor=.5, lean=0.0, **kw):
    """A flat figure standing in the set. sprite: (h, w) palette indices, HOLE where there is nothing. foot: the
    world point under its bottom row, `anchor` of the way along it. right: the world direction its rows run
    along (pass cam.right for a figure that always faces the lens; it is flattened to the ground). lean: degrees
    tipped back from upright. One sprite pixel is `texel` metres, the same grid the walls are painted on."""
    sprite = np.asarray(sprite, np.uint8); h, w = sprite.shape; r = np.array(right, float); r[2] = 0; r /= np.linalg.norm(r)
    back = np.cross(r, (0, 0, 1.)); up = np.array([0, 0, 1.]) * math.cos(math.radians(lean)) - back * math.sin(math.radians(lean))
    O = np.asarray(foot, float) - r * (w * anchor * texel) + up * (h * texel)
    s = Solid(name, [[O, O + r * w * texel, O + r * w * texel - up * h * texel, O - up * h * texel]], kind='card')
    s.skin, s.texel, s.frame, s.flat = sprite, texel, (O, r, -up), True
    for k, v in kw.items(): setattr(s, k, v)
    return s

def panel(name, skin, corner, across, down, texel=.05, **kw):
    """A flat painted rectangle anywhere: its top-left `corner`, and unit directions `across` and `down`. For a
    sign, a screen, a picture on a wall, a door."""
    skin = np.asarray(skin, np.uint8); h, w = skin.shape; O = np.asarray(corner, float); a = np.asarray(across, float); a = a / np.linalg.norm(a); d = np.asarray(down, float); d = d / np.linalg.norm(d)
    s = Solid(name, [[O, O + a * w * texel, O + a * w * texel + d * h * texel, O + d * h * texel]], kind='card')
    s.skin, s.texel, s.frame = skin, texel, (O, a, d)
    for k, v in kw.items(): setattr(s, k, v)
    return s

def _tris(sol):
    t = getattr(sol, '_tri', None)
    if t is None or len(t) != len(sol.faces): t = sol._tri = [triangles(f) for f in sol.faces]
    return t

def gbuffer(solids, cam, near=.1, depth_only=False):
    """Everything the lens sees, per pixel. Returns a dict:

      depth    metres along the axis (inf where nothing)       solid    index into `solids` (-1 where nothing)
      index    the paint: a palette index (HOLE where nothing) glow, flat    the solid's own, per pixel
      pos      the world point                                 normal   the surface normal, turned to the lens
      centre   the world point at the middle of the texel under the pixel: light it there and a whole texel
               takes one tone
      u, v     which texel (integers)
    With depth_only, just depth (for a shadow map: solids with cast=False are left out)."""
    W, H = cam.size; f, cx, cy = cam.f, cam.cx, cam.cy
    zbuf = np.full((H, W), np.inf); fid = np.full((H, W), -1, np.int32)
    FS, FN, FU, FV, FO, FT, FA, FW = [], [], [], [], [], [], [], []; atlas = []; apos = 0
    for si, sol in enumerate(solids):
        if getattr(sol, 'on', 'both') == 'drawing' or (depth_only and not getattr(sol, 'cast', True)): continue
        skin = getattr(sol, 'skin', None); fr = getattr(sol, 'frame', None); tex = getattr(sol, 'texel', .05); org = np.asarray(getattr(sol, 'origin', (0, 0, 0)), float)
        if skin is None: skin = np.array([[getattr(sol, 'index', 9)]], np.uint8)
        holes = fr is not None and bool((skin == HOLE).any())
        atlas.append(skin.ravel()); th, tw = skin.shape
        for face, tris in zip(sol.faces, _tris(sol)):
            n = _normal(face); U, V = (fr[1], fr[2]) if fr is not None else _frame(n); O = fr[0] if fr is not None else org
            me = len(FS); FS.append(si); FN.append(n); FU.append(U); FV.append(V); FO.append(O); FT.append(tex); FA.append((apos, tw, th)); FW.append(fr is None)
            for tri in tris:
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
                    if holes and m.any():                        # a cut-out: only where the sprite has paint
                        k = z / f; rx = (X - cx) * k; ry = -(Y - cy) * k
                        rel = (cam.eye - O)[None, None, :] + cam.fwd[None, None, :] * z[..., None] + cam.right[None, None, :] * rx[..., None] + cam.up[None, None, :] * ry[..., None]
                        uu = np.floor(np.nan_to_num(rel @ U) / tex).astype(int); vv = np.floor(np.nan_to_num(rel @ V) / tex).astype(int)
                        m &= (uu >= 0) & (uu < tw) & (vv >= 0) & (vv < th); m[m] = skin[vv[m], uu[m]] != HOLE
                    sub[m] = z[m]; fid[y0:y1 + 1, x0:x1 + 1][m] = me
        apos += skin.size
    out = dict(depth=zbuf.astype(np.float32), cam=cam)
    if depth_only: return out
    hit = fid >= 0; nf = len(FS); A = lambda L, pad: np.array(L + [pad])
    FS, FN, FU, FV, FO, FT, FA, FW = A(FS, -1), A(FN, [0, 0, 1.]), A(FU, [1., 0, 0]), A(FV, [0, 1., 0]), A(FO, [0., 0, 0]), A(FT, 1.0), A(FA, (0, 1, 1)), A(FW, True)
    atlas = np.concatenate(atlas + [np.array([HOLE], np.uint8)]) if atlas else np.array([HOLE], np.uint8)
    FA[nf] = (len(atlas) - 1, 1, 1)
    yy, xx = np.mgrid[:H, :W]; zz = np.where(hit, zbuf, 0.0)
    P = cam.eye + (cam.fwd[None, None, :] * f + cam.right[None, None, :] * (xx + .5 - cx)[..., None] - cam.up[None, None, :] * (yy + .5 - cy)[..., None]) * (zz / f)[..., None]
    n0 = FN[fid]; U, V, O, t = FU[fid], FV[fid], FO[fid], FT[fid]; rel = P - O
    u = np.floor((rel * U).sum(-1) / t).astype(np.int64); v = np.floor((rel * V).sum(-1) / t).astype(np.int64)
    off, tw, th = FA[fid][..., 0], FA[fid][..., 1], FA[fid][..., 2]; wrap = FW[fid]
    ui = np.where(wrap, u % tw, np.clip(u, 0, tw - 1)); vi = np.where(wrap, v % th, np.clip(v, 0, th - 1))
    centre = O + ((u + .5) * t)[..., None] * U + ((v + .5) * t)[..., None] * V + (rel * n0).sum(-1)[..., None] * n0
    sgn = np.where(((cam.eye - P) * n0).sum(-1) < 0, -1.0, 1.0)
    per = lambda name, default: np.array([float(getattr(s, name, default)) for s in solids] + [0.0])
    out.update(solid=FS[fid], index=np.where(hit, atlas[off + vi * tw + ui], HOLE).astype(np.uint8), pos=P, centre=centre, normal=n0 * sgn[..., None], u=u, v=v,
               glow=per('glow', 0.0)[FS[fid]].astype(np.float32), flat=per('flat', 0.0)[FS[fid]] > 0, hit=hit, names=[s.name for s in solids])
    return out

class Light:
    """A lamp in the set. power: the level it gives a surface facing it at arm's length; reach: the distance
    at which that has halved. aim and cone=(inner, outer) degrees make it a spot (a torch); without them it
    shines all round. It throws shadows: `bake` once for the things that never move, then pass the things
    that do to `lighting(moving=...)`. Set `lamp.still = True` on a lamp that should ignore the moving things."""
    def __init__(s, pos, power=1.0, reach=3.0, aim=None, cone=None, shadow=True, size=512, name='', near=.05):
        s.pos, s.power, s.reach, s.shadow, s.size, s.name, s.near = np.asarray(pos, float), power, reach, shadow, size, name, near
        s.aim = None if aim is None else np.asarray(aim, float) / np.linalg.norm(aim); s.cone = cone; s.maps = None
        if s.aim is not None and cone is not None and cone[1] < 62:      # one map looking down the beam
            s.cams = [Camera(s.pos, look=s.pos + s.aim, lens=18 / math.tan(math.radians(min(cone[1] + 4, 66))), size=(size, size))]
        else:                                                            # six, one through each face of a cube
            s.cams = [Camera(s.pos, look=s.pos + np.array(d, float), lens=18 / 1.02, size=(size, size)) for d in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))]
    def bake(s, solids):
        s.maps = [gbuffer(solids, c, near=s.near, depth_only=True)['depth'] for c in s.cams] if s.shadow else None; return s
    def seen(s, P, moving=None, bias=.06):
        """For world points P (..., 3): 1 where the lamp can see the point, 0 where something is in the way."""
        vis = np.ones(P.shape[:-1], bool)
        if not s.shadow: return vis
        if s.maps is None: s.bake([])
        flat = P.reshape(-1, 3); v = vis.reshape(-1)
        for c, zm in zip(s.cams, s.maps):
            if moving: zm = np.minimum(zm, gbuffer(moving, c, near=s.near, depth_only=True)['depth'])
            q = c.project(flat); x = np.floor(q[:, 0]).astype(int); y = np.floor(q[:, 1]).astype(int)
            ok = (q[:, 2] > s.near) & (x >= 0) & (x < s.size) & (y >= 0) & (y < s.size)
            v[ok] &= q[ok, 2] <= zm[y[ok], x[ok]] + bias + .01 * q[ok, 2]
        return vis

def lighting(g, lights, ambient=.05, moving=None, snap=True, lift=.03, wrap=.15, flat_floor=0.0):
    """How much light every pixel's texel gets: ambient plus, for each lamp, power x facing x falloff x beam x
    whether the lamp can see it. With snap (the default) the sum is done at the middle of each texel, so the
    light is as blocky as the paint. `wrap` lets light creep a little past the terminator; flat things (cards)
    ignore facing. Returns (h, w) float32; values above 1 are a surface closer to a lamp than arm's length."""
    P = (g['centre'] if snap else g['pos']) + g['normal'] * lift; n = g['normal']; out = np.full(P.shape[:2], float(ambient)); hit = g['hit']
    for L in lights:
        d = L.pos[None, None, :] - P; dist = np.sqrt((d * d).sum(-1)) + 1e-9
        lam = np.clip(((n * d).sum(-1) / dist + wrap) / (1 + wrap), 0, 1); lam = np.where(g['flat'], 1.0, lam)
        k = L.power * lam / (1 + (dist / L.reach) ** 2)
        if L.aim is not None and L.cone is not None:
            ca = -(d * L.aim[None, None, :]).sum(-1) / dist; c0, c1 = math.cos(math.radians(L.cone[0])), math.cos(math.radians(L.cone[1]))
            k = k * np.clip((ca - c1) / max(c0 - c1, 1e-6), 0, 1)
        m = hit & (k > 1e-4)
        if L.shadow and m.any():
            vis = np.zeros(P.shape[:2], bool); vis[m] = L.seen(P[m], None if getattr(L, 'still', False) else moving)
            k = k * vis
        out += np.where(hit, k, 0)
    if flat_floor: out = np.where(g['flat'], np.maximum(out, flat_floor), out)
    return out.astype(np.float32)

def ease(u): u = min(max(u, 0.0), 1.0); return u * u * (3 - 2 * u)

def fly(keys, t, size=(1280, 720), smooth=True):
    """A camera move. keys: [(seconds, eye, look, lens)], in order. Between keys the eye, the point looked at
    and the lens glide (eased, or linear with smooth=False). Before the first and after the last it holds."""
    if t <= keys[0][0]: k0 = k1 = keys[0]; u = 0.0
    elif t >= keys[-1][0]: k0 = k1 = keys[-1]; u = 0.0
    else:
        i = max(j for j in range(len(keys) - 1) if keys[j][0] <= t); k0, k1 = keys[i], keys[i + 1]; u = (t - k0[0]) / (k1[0] - k0[0]); u = ease(u) if smooth else u
    mix = lambda a, b: np.asarray(a, float) * (1 - u) + np.asarray(b, float) * u
    return Camera(mix(k0[1], k1[1]), look=mix(k0[2], k1[2]), lens=float(mix(k0[3], k1[3])), size=size)

def flakes(g, cam, pts, size=.04):
    """Small things in the air (snow, dust, sparks): world points (n, 3) -> (x, y, half-size in pixels, depth) of
    the ones in front of the lens and not hidden by the set. Draw them however the style likes."""
    q = cam.project(pts); W, H = cam.size; x = np.floor(q[:, 0]).astype(int); y = np.floor(q[:, 1]).astype(int)
    ok = (q[:, 2] > .2) & (x >= 0) & (x < W) & (y >= 0) & (y < H); ok[ok] &= q[ok, 2] < g['depth'][y[ok], x[ok]]
    return np.c_[q[ok, 0], q[ok, 1], np.maximum(cam.f * size / q[ok, 2] / 2, .5), q[ok, 2]]

def edges(g):
    """A matte of the lines a draughtsman would draw: wherever two neighbouring pixels belong to different
    planes or different solids. For a wireframe with the hidden lines removed."""
    key = g['solid'].astype(np.int64) * 8 + np.argmax(np.abs(g['normal']), -1) * 2 + (np.take_along_axis(g['normal'], np.argmax(np.abs(g['normal']), -1)[..., None], -1)[..., 0] > 0)
    e = np.zeros(key.shape, bool); e[:, 1:] |= key[:, 1:] != key[:, :-1]; e[1:, :] |= key[1:, :] != key[:-1, :]
    z = g['depth']; fin = np.isfinite(z); zz = np.where(fin, z, 0)
    e[:, 1:] |= fin[:, 1:] & fin[:, :-1] & (np.abs(zz[:, 1:] - zz[:, :-1]) > .12 * np.minimum(zz[:, 1:], zz[:, :-1]) + .05)
    e[1:, :] |= fin[1:, :] & fin[:-1, :] & (np.abs(zz[1:, :] - zz[:-1, :]) > .12 * np.minimum(zz[1:, :], zz[:-1, :]) + .05)
    return e
