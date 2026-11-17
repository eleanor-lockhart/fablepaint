"""backlot.carve: things carved out of the paint grid in three dimensions.

A card (`depth.card`) is a drawing standing up, and it is right from one side. A thing that will be walked
round, or that goes round, has to be the same from every side: carve it. A `Carving` is a small box of cubes,
each `texel` metres (5 cm, the size of a painted pixel on the walls), each holding a palette index. You carve in
metres, in the thing's own coordinates (x its forward, y its left, z up), and hand the result to the renderer:

    c = Carving((-.9, -.3, 0), (1.5, .3, 1.8))            the box it may occupy, in metres
    c.ball((0, 0, .9), (.62, .24, .28), paint=0xA)        a ball, or an egg with three radii
    c.limb((.4, .13, .8), (.42, .13, .45), .06, .04, 9)   a bone with flesh on it: fat end, thin end, never broken
    c.box((-.1, -.2, 1.1), (.2, .2, 1.2), 0xD)            a block
    c.paint(lambda X, Y, Z: Z > 1.05, 0xB)                recolour what is already there, by rule
    c.mirror()                                            make the right side the same as the left
    horse = c.block('horse', at=(x, y, z), turn=30)       a depth.block, placed by the carving's own origin
    c.print('side')                                       a flat picture of it (palette indices) for a sheet

    hull(side, front)                                     a carving from two drawings: what both of them allow

Later paint goes over earlier paint, like a brush; `keep=True` fills only empty cubes.
"""
import numpy as np
from .depth import HOLE, block as _block

class Carving:
    def __init__(s, lo, hi, texel=.05):
        s.texel = float(texel); s.lo = np.floor(np.asarray(lo, float) / texel + 1e-9).astype(int)
        hi = np.ceil(np.asarray(hi, float) / texel - 1e-9).astype(int); s.n = np.maximum(hi - s.lo, 1)
        s.grid = np.full(tuple(s.n), HOLE, np.uint8)
    def _span(s, lo, hi):
        """The cubes whose middles could lie in the box lo..hi (metres): slices, and the coordinates of their middles."""
        a = np.clip(np.floor(np.asarray(lo, float) / s.texel).astype(int) - s.lo, 0, s.n); b = np.clip(np.ceil(np.asarray(hi, float) / s.texel).astype(int) - s.lo + 1, 0, s.n)
        sl = tuple(slice(int(a[i]), int(b[i])) for i in range(3))
        ax = [(np.arange(a[i], b[i]) + s.lo[i] + .5) * s.texel for i in range(3)]
        X, Y, Z = np.meshgrid(*ax, indexing='ij'); return sl, X, Y, Z
    def _put(s, sl, mask, paint, keep):
        g = s.grid[sl]
        if keep: mask = mask & (g == HOLE)
        g[mask] = paint
    def ball(s, c, r, paint, keep=False):
        c = np.asarray(c, float); r = np.ones(3) * np.asarray(r, float)
        sl, X, Y, Z = s._span(c - r, c + r)
        s._put(sl, ((X - c[0]) / r[0]) ** 2 + ((Y - c[1]) / r[1]) ** 2 + ((Z - c[2]) / r[2]) ** 2 <= 1.0, paint, keep); return s
    def limb(s, a, b, ra, rb=None, paint=9, keep=False, flat=1.0):
        """From a to b, radius ra at a and rb at b. `flat` squashes it sideways (in y): a slab of muscle. However
        thin, it is never broken: the line of cubes from a to b is always filled."""
        a = np.asarray(a, float); b = np.asarray(b, float); rb = ra if rb is None else rb; R = max(ra, rb)
        sl, X, Y, Z = s._span(np.minimum(a, b) - R, np.maximum(a, b) + R)
        d = b - a; L2 = float(d @ d) or 1e-12
        u = np.clip(((X - a[0]) * d[0] + (Y - a[1]) * d[1] + (Z - a[2]) * d[2]) / L2, 0, 1)
        dist2 = (X - a[0] - u * d[0]) ** 2 + ((Y - a[1] - u * d[1]) / flat) ** 2 + (Z - a[2] - u * d[2]) ** 2
        s._put(sl, dist2 <= (ra + (rb - ra) * u) ** 2, paint, keep)
        k = int(np.sqrt(L2) / s.texel * 3) + 2; P = a[None, :] + np.linspace(0, 1, k)[:, None] * d[None, :]
        s.dots(P, paint, keep); return s
    def box(s, lo, hi, paint, keep=False):
        lo = np.asarray(lo, float); hi = np.asarray(hi, float); sl, X, Y, Z = s._span(lo, hi)
        s._put(sl, (X >= lo[0]) & (X <= hi[0]) & (Y >= lo[1]) & (Y <= hi[1]) & (Z >= lo[2]) & (Z <= hi[2]), paint, keep); return s
    def dots(s, pts, paint, keep=False):
        """Single cubes at these points (n, 3)."""
        i = np.floor(np.atleast_2d(np.asarray(pts, float)) / s.texel).astype(int) - s.lo; ok = ((i >= 0) & (i < s.n)).all(1); i = i[ok]
        if keep: i = i[s.grid[i[:, 0], i[:, 1], i[:, 2]] == HOLE]
        s.grid[i[:, 0], i[:, 1], i[:, 2]] = paint; return s
    def paint(s, where, paint, only=None):
        """Recolour cubes that are already there, where `where(X, Y, Z)` (metres) is true; `only`: just those now painted so."""
        sl, X, Y, Z = s._span(s.lo * s.texel, (s.lo + s.n) * s.texel); m = where(X, Y, Z) & (s.grid != HOLE)
        if only is not None: m &= np.isin(s.grid, only)
        s.grid[m] = paint; return s
    def surface(s):
        """The cubes with at least one bare face."""
        f = s.grid != HOLE; p = np.pad(f, 1)
        inside = p[:-2, 1:-1, 1:-1] & p[2:, 1:-1, 1:-1] & p[1:-1, :-2, 1:-1] & p[1:-1, 2:, 1:-1] & p[1:-1, 1:-1, :-2] & p[1:-1, 1:-1, 2:]
        return f & ~inside
    def mirror(s):
        """Left and right the same: whatever is on the +y side is copied to the -y side (the box must be symmetric in y)."""
        g = s.grid; n = g.shape[1]; h = n // 2; g[:, :h] = g[:, ::-1][:, :h]; return s
    def count(s): return int((s.grid != HOLE).sum())
    def block(s, name, at=(0, 0, 0), turn=0.0, **kw):
        """A depth.block of this carving, with the carving's own origin (0, 0, 0) put at `at` in the world."""
        return _block(name, s.grid, at, turn, s.texel, pivot=-s.lo.astype(float), **kw)
    def print(s, view='side', back=HOLE):
        """A flat picture: palette indices (HOLE where nothing). 'side' is seen from its right with the head to
        the right (x across, z up); 'front' from ahead (y across); 'top' from above (x across, y up the page)."""
        g = s.grid; f = g != HOLE
        def first(axis, rev):
            a = np.moveaxis(g, axis, 0); a = a[::-1] if rev else a; m = a != HOLE; i = m.argmax(0)
            return np.where(m.any(0), np.take_along_axis(a, i[None], 0)[0], back)
        if view == 'side': p = first(1, False); return p.T[::-1]                # seen from -y: x to the right, z up
        if view == 'front': p = first(0, True); return p.T[::-1]                # seen from +x: its left on our right
        p = first(2, True); return p.T[::-1]                                    # from above: x to the right, y up

def hull(side, front=None, texel=.05, width=None):
    """A carving from drawings. side: (h, w) palette indices seen from the right, nose to the right, HOLE
    outside. front: (h, wy) seen from ahead; without it the side drawing is given `width` texels of thickness
    (rounded: thinner toward its edges). A cube is there if both drawings have paint there; it takes the side
    drawing's paint, except on the faces looking forward and back, which take the front's."""
    side = np.asarray(side, np.uint8); h, w = side.shape
    if front is None:
        ny = int(width or max(2, min(h, w) // 3)); S = side[::-1].T != HOLE                    # (x, z)
        from scipy.ndimage import distance_transform_edt as edt
        d = edt(S); half = np.minimum(d, ny / 2.0); j = (np.arange(ny) + .5 - ny / 2.0)
        m = np.abs(j)[None, :, None] <= half[:, None, :]
        paint = np.broadcast_to(side[::-1].T[:, None, :], (w, ny, h))
    else:
        front = np.asarray(front, np.uint8); ny = front.shape[1]; S = side[::-1].T != HOLE; F = front[::-1].T != HOLE     # (x, z), (y, z)
        m = S[:, None, :] & F[None, :, :]; paint = np.broadcast_to(side[::-1].T[:, None, :], (w, ny, h)).copy()
        fr = np.broadcast_to(front[::-1].T[None, :, :], (w, ny, h)); edge = m & ~(np.roll(m, 1, 0) & np.roll(m, -1, 0))
        paint[edge] = fr[edge]
    c = Carving((0, -ny * texel / 2, 0), (w * texel, ny * texel / 2, h * texel), texel)
    c.grid[:] = np.where(m, paint, HOLE)[:, :, :] if c.grid.shape == m.shape else HOLE
    return c
