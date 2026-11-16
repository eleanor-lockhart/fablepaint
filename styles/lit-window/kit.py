# kit.py: a printmaker's bench on top of Fable Studio.
# Use from a studio script:   exec(open('../styles/lit-window/kit.py').read())
# Everything here assumes the studio script namespace (W, H, np, cv2, rng, layer, fill, ...).
#
# Vocabulary
#   block      a layer holding one flat pigment
#   marks      many small carved shapes of one pigment, rasterised together
#   cut        the same shapes removed from the block, so what is underneath shows
#   bokashi    a gradation of extra pigment wiped along one edge of a block
#   nezumi     a shadow block printed in multiply across several colour areas
#   key        the line block

RESET = dict(tip='round', size=20, hardness=.8, opacity=1, flow=1, spacing=.1, angle=0, roundness=1, follow=False,
             scatter=0, count=1, size_jitter=0, angle_jitter=0, flow_jitter=0, hue_jitter=0, sat_jitter=0,
             val_jitter=0, psize=True, pflow=False, taper=(0, 0), blend='normal', mix=0, grain=0, smooth=True)
def B(**kw):
    brush(**{**RESET, **kw})

_SS = 2                      # supersampling for marks
_CLIP = [None]               # optional canvas-sized array every mark is multiplied by (the image window)
PAPER = '#e9dfc9'
KEY = '#1a1d24'              # the line block: a warm blue-black, never pure black

# ------------------------------------------------------------------ geometry
def spline(pts, closed=False):
    """Smooth curve through the points, as an (N,2) array."""
    return np.asarray(path([tuple(p[:2]) for p in pts], closed=closed), float)[:, :2]

def resample(P, step=2.5):
    P = np.asarray(P, float)[:, :2]
    d = np.r_[0, np.cumsum(np.hypot(*np.diff(P, axis=0).T))]
    if d[-1] < 1e-6:
        return P
    t = np.linspace(0, d[-1], max(6, int(d[-1] / step) + 1))
    return np.c_[np.interp(t, d, P[:, 0]), np.interp(t, d, P[:, 1])]

def ribbon(pts, w=3.0, taper=(.15, .15), wob=.15, smooth=True, minw=.4):
    """A carved line as a polygon: width `w`, tapering in/out over those fractions, swelling gently.
    Returns the outline; draw with marks([...]) or key([...])."""
    P = spline(pts) if (smooth and len(pts) > 2) else np.asarray(pts, float)[:, :2]
    P = resample(P)
    d = np.r_[0, np.cumsum(np.hypot(*np.diff(P, axis=0).T))]
    L = max(d[-1], 1e-6)
    u = d / L
    prof = np.ones(len(P))
    if taper[0] > 0: prof *= np.clip(u / taper[0], 0, 1) ** .6
    if taper[1] > 0: prof *= np.clip((1 - u) / taper[1], 0, 1) ** .6
    if wob:
        ph = rng.uniform(0, 6.283, 3)
        k = L / 40.0
        prof *= 1 + wob * sum(np.sin((i + 1) * k * u * 1.7 + ph[i]) / (i + 1) for i in range(3)) / 1.6
    hw = np.maximum(w * prof, minw) / 2
    tg = np.gradient(P, axis=0)
    n = np.c_[-tg[:, 1], tg[:, 0]]
    n /= np.maximum(np.hypot(n[:, 0], n[:, 1]), 1e-9)[:, None]
    return np.r_[P + n * hw[:, None], (P - n * hw[:, None])[::-1]]

def seg(a, b, w=2.0, taper=(0, 0), wob=.1):
    """Straight carved line from a to b."""
    return ribbon([a, b], w=w, taper=taper, wob=wob, smooth=False)

def blob(cx, cy, rx, ry=None, n=9, rough=.25, rot=None):
    """An irregular rounded shape (a leaf clump, a snow chip, a stone)."""
    ry = rx if ry is None else ry
    a = np.sort(rng.uniform(0, 6.283, n)) + (rng.uniform(0, 6.283) if rot is None else rot)
    r = 1 + rng.uniform(-rough, rough, n)
    return np.c_[cx + rx * r * np.cos(a), cy + ry * r * np.sin(a)]

def chip(cx, cy, s):
    """A small angular fleck, the mark a knife leaves: 3-5 corners."""
    n = int(rng.integers(3, 6))
    a = np.sort(rng.uniform(0, 6.283, n))
    r = s * rng.uniform(.45, 1.0, n)
    return np.c_[cx + r * np.cos(a), cy + r * np.sin(a) * rng.uniform(.6, 1)]

def lens(x, y, ln, th, tilt=0.0):
    """A horizontal dash pointed at both ends (water ticks, reflections, cloud slivers)."""
    t = np.linspace(0, 1, 9)
    up = np.c_[x + ln * t, y - th / 2 * np.sin(np.pi * t) ** .8 + tilt * ln * (t - .5)]
    dn = np.c_[x + ln * t[::-1], y + th / 2 * np.sin(np.pi * t[::-1]) ** .8 + tilt * ln * (t[::-1] - .5)]
    return np.r_[up, dn]

def wobble(pts, amp=.7, step=14):
    """Take the ruler-straightness off a polygon: resample and nudge each point a little."""
    P = np.asarray(pts, float)[:, :2]
    out = []
    for i in range(len(P)):
        a, b = P[i], P[(i + 1) % len(P)]
        n = max(1, int(np.hypot(*(b - a)) / step))
        for j in range(n):
            out.append(a + (b - a) * j / n + (rng.normal(0, amp, 2) if j else 0))
    return np.array(out)

# ------------------------------------------------------------------ rasterising many marks at once
def raster(polys):
    """Float mask (H,W) of all the polygons, each filled on its own (overlaps do not cancel)."""
    m = np.zeros((H * _SS, W * _SS), np.uint8)
    for p in polys:
        q = np.asarray(p, np.float64)[:, :2]
        if len(q) >= 3:
            cv2.fillPoly(m, [np.round(q * (_SS * 16)).astype(np.int32)], 255, lineType=cv2.LINE_8, shift=4)
    m = cv2.resize(m, (W, H), interpolation=cv2.INTER_AREA).astype(np.float32) / 255
    return m if _CLIP[0] is None else m * _CLIP[0]

def marks(polys, color, opacity=1.0, blend='normal'):
    """Print many shapes in one pigment on the active layer. Ignores and clears any selection."""
    if len(polys):
        select_array(raster(polys)); fill(color, opacity=opacity, blend=blend); select_none()

def cut(polys, depth=1.0):
    """Carve the shapes out of the active layer, so the block below shows through."""
    if len(polys):
        modulate(1 - depth * raster(polys))

def window(x0, y0, x1, y1):
    """Declare the image area; marks stop at its edge. Returns the rect."""
    m = np.zeros((H, W), np.float32); m[int(y0):int(y1), int(x0):int(x1)] = 1
    _CLIP[0] = m
    return (x0, y0, x1, y1)

# ------------------------------------------------------------------ colour
def ramp(*cols, n=14, ease=1.0, a=None):
    """Gradient stops interpolated in display (sRGB) space, so a gradation looks even.
    cols: colours, or (colour, position) pairs. `a`: optional (alpha0, alpha1) to fade as well."""
    cs = [(c, i / (len(cols) - 1)) if not (isinstance(c, tuple) and len(c) == 2 and isinstance(c[0], str)) else c for i, c in enumerate(cols)]
    rgb = np.array([[int(c[0][i:i + 2], 16) for i in (1, 3, 5)] for c in cs], float)
    pos = np.array([c[1] for c in cs], float)
    out = []
    for i in range(n + 1):
        t = i / n
        te = t ** ease
        v = [np.interp(te, pos, rgb[:, k]) for k in range(3)]
        st = (t, '#%02x%02x%02x' % tuple(int(round(x)) for x in v))
        if a is not None:
            st += (float(a[0] + (a[1] - a[0]) * te),)
        out.append(st)
    return out

def fade(color, a0, a1=0.0, n=14, power=2.2):
    """Stops for one pigment thinning out from alpha a0 to a1 with a perceptually even fall."""
    return [(i / n, color, float(a1 + (a0 - a1) * (1 - i / n) ** power)) for i in range(n + 1)]

# ------------------------------------------------------------------ blocks and gradations
def block(name, color=None, pts=None, smooth=False, **kw):
    """New layer for one flat pigment, on TOP of the stack unless above=/below= says otherwise
    (a new block prints over what is already on the paper). Optionally fill a polygon at once."""
    layer(name, **kw)
    if 'above' not in kw and 'below' not in kw:
        move(name)
    if pts is not None:
        fill_poly([tuple(p) for p in np.asarray(pts, float)[:, :2]], color, smooth=smooth)

def bokashi(color, p0, p1, strength=.8, power=2.0, kind='linear'):
    """Wipe extra pigment onto the active block: full `strength` at p0, nothing at p1.
    Stays inside the block's existing shape."""
    lock(True)
    gradient(kind, p0, p1, fade(color, strength, 0, power=power))
    lock(False)

def nezumi(name, color='#4a5560', opacity=1.0, **kw):
    """A shadow block: multiply layer laid across everything below. Fill shapes into it."""
    layer(name, blend='multiply', opacity=opacity, **kw)

# ------------------------------------------------------------------ what the tools leave behind
def woodgrain(strength=.05, direction='v', scale=3.0, seed=0, patchy=.6):
    """Board grain in a flat area. Faint, and stronger in some places than others: uniform grain
    reads as a motion-blur filter, not as wood."""
    st = (70, 1) if direction == 'v' else (1, 70 * H / W)
    g = noise_field(scale=scale, octaves=3, seed=seed, stretch=st) * .5 + noise_field(scale=scale * 7, octaves=2, seed=seed + 7, stretch=st) * .5
    where = 1 - patchy * noise_field(scale=2.5, octaves=2, seed=seed + 13)
    modulate(1 - strength * g * where)

def baren(strength=.05, seed=0, goma=0.0):
    """Uneven pressure: soft mottling; goma > 0 adds a fine 'sesame' speckle of bare paper."""
    m = 1 - strength * noise_field(scale=7, octaves=4, seed=seed)
    if goma > 0:
        sp = noise_field(scale=W / 1.7, octaves=1, seed=seed + 3)
        m = m * (1 - np.clip((sp - (1 - goma)) / .12, 0, 1) * .55)
    modulate(m)

def finish(x0, y0, x1, y1, paper=PAPER, border=True, tooth=.3, seed=5):
    """Paper margin back over the bleed, a thin key border, and fine paper fibre over everything."""
    _CLIP[0] = None
    layer('margin'); move('margin')
    fill(paper); select_rect(x0, y0, x1, y1); clear(); select_none()
    if border:
        layer('border', blend='multiply')
        marks([seg(a, b, w=2.0, wob=.12) for a, b in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0)))], KEY)
    layer('tooth', blend='multiply')
    fib = noise_field(scale=W / 4, octaves=2, seed=seed, stretch=(3.0, .45))
    select_array(np.clip(tooth * fib, 0, 1)); fill('#6b5f4c', opacity=.4); select_none()

def seal(x, y, s=34, color='#b23b28', lamp='#ecd596'):
    """My chop: a vermilion square with one small lit window, low and to the right."""
    block('seal')
    marks([wobble([(x, y), (x + s, y), (x + s, y + s), (x, y + s)], amp=.5, step=9)], color)
    marks([wobble([(x + s * .56, y + s * .5), (x + s * .78, y + s * .5), (x + s * .78, y + s * .8), (x + s * .56, y + s * .8)], amp=.3, step=6)], lamp)

# ------------------------------------------------------------------ mark vocabularies
def ticks(x, y0, y1, width, n=None, grow=1.0, th=2.2, jitter=.35, gap=1.0):
    """Reflection of a light or a pale thing: stacked horizontal dashes that widen, wander and thin out downward."""
    out, y = [], y0
    while y < y1:
        f = (y - y0) / max(y1 - y0, 1)
        wd = width * (1 + (grow - 1) * f) * rng.uniform(.55, 1.15)
        cx = x + rng.normal(0, width * jitter * (.4 + f))
        t = th * (1 + .9 * f) * rng.uniform(.7, 1.2)
        if rng.uniform() > f * .55:
            out.append(lens(cx - wd / 2, y, wd, t))
        y += t * (1.5 + gap * (1 + 3.0 * f * f)) * rng.uniform(.8, 1.3)
    return out

def ripples(x0, y0, x1, y1, n=120, len0=18, len1=120, th0=1.0, th1=3.0, bias=1.6):
    """Sparse water dashes over an area: short, thin and close near y0 (far), long and thick near y1 (near)."""
    out = []
    for _ in range(n):
        f = rng.uniform() ** (1 / bias) if bias != 1 else rng.uniform()
        y = y0 + (y1 - y0) * f
        ln = (len0 + (len1 - len0) * f) * rng.uniform(.5, 1.4)
        out.append(lens(rng.uniform(x0 - ln / 2, x1 - ln / 2), y, ln, (th0 + (th1 - th0) * f) * rng.uniform(.7, 1.2), tilt=rng.normal(0, .004)))
    return out

def rain(x0, y0, x1, y1, n=160, angle=68, w=1.0, length=(.35, 1.0), spread=1.5):
    """Ruled rain: long straight hairlines at `angle` degrees from horizontal, in loose sheaves."""
    out = []
    span = math.hypot(x1 - x0, y1 - y0)
    for _ in range(n):
        a = math.radians(angle + rng.normal(0, spread))
        cx, cy = rng.uniform(x0 - 80, x1 + 80), rng.uniform(y0, y1)
        ln = span * rng.uniform(*length)
        dx, dy = math.cos(a) * ln / 2, math.sin(a) * ln / 2
        out.append(seg((cx - dx, cy - dy), (cx + dx, cy + dy), w=w * rng.uniform(.6, 1.5), taper=(.3, .3), wob=0))
    return out

def snowfall(x0, y0, x1, y1, n=2400, size=(.9, 2.3), density=None):
    """Falling snow: thousands of small angular chips of bare paper, a few of them larger."""
    out = []
    while len(out) < n:
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        if density is None or rng.uniform() < density(x, y):
            out.append(chip(x, y, rng.uniform(*size) * (1.7 if rng.uniform() < .07 else 1)))
    return out

def foliage(cx, cy, rx, ry, n=60, leaf=7, core=.55):
    """A leaf mass: a solid irregular core with a lace of small lobes round it. Returns polygons."""
    out = [blob(cx, cy, rx * core, ry * core, n=11, rough=.3)]
    for _ in range(n):
        a, r = rng.uniform(0, 6.283), rng.uniform(.25, 1) ** .6
        x, y = cx + rx * r * math.cos(a), cy + ry * r * math.sin(a)
        out.append(blob(x, y, leaf * rng.uniform(.6, 1.4), leaf * rng.uniform(.5, 1.1), n=7, rough=.35))
    return out

def blades(x, y, n=7, length=40, spread=50, w=2.2, lean=0.0):
    """A tuft of grass or reed: tapered blades fanning up from a point, some bent over."""
    out = []
    for _ in range(n):
        a = math.radians(-90 + rng.normal(lean, spread / 2.2))
        ln = length * rng.uniform(.55, 1.2)
        bend = rng.normal(0, .35) + (.5 if rng.uniform() < .2 else 0) * np.sign(math.cos(a) or 1)
        p1 = (x + math.cos(a) * ln * .5, y + math.sin(a) * ln * .5)
        p2 = (x + math.cos(a + bend) * ln, y + math.sin(a + bend) * ln * (1 - abs(bend) * .5))
        out.append(ribbon([(x + rng.normal(0, 3), y), p1, p2], w=w * rng.uniform(.7, 1.2), taper=(0, .75), wob=0))
    return out

def fir(x, base, height, width, tiers=None, droop=.35, seed=None):
    """A Douglas-fir / hemlock silhouette: a spire of drooping, ragged branch tiers, gaps between. Returns polygons."""
    out = [np.array([(x - width * .018, base), (x - .8, base - height), (x + .8, base - height), (x + width * .018, base)])]
    tiers = tiers or int(height / max(9, width * .11))
    for i in range(tiers):
        f = (i + rng.uniform(-.3, .3)) / tiers                      # 0 at top
        f = min(max(f, .015), 1)
        y = base - height * (1 - f * .93)
        for side in (-1, 1):
            if rng.uniform() < .1:
                continue
            ln = width / 2 * (f ** .8) * rng.uniform(.6, 1.12) + 2
            th = max(2.5, ln * rng.uniform(.14, .26))
            k = int(max(4, ln / 5))
            t = np.linspace(0, 1, k)
            top = np.c_[x + side * ln * t, y + droop * ln * t ** 1.6 - th * .3 * np.sin(np.pi * t)]
            bot = np.c_[x + side * ln * t[::-1], y + droop * ln * t[::-1] ** 1.6 + th * (.35 + .65 * np.sin(np.pi * t[::-1] ** .7))
                        + rng.uniform(0, th * .7, k) * (np.arange(k)[::-1] % 2)]
            out.append(np.r_[top, bot])
    return out

# ------------------------------------------------------------------ construction: don't guess perspective, compute it
def camera(eye, look, fov=40.0, centre=None, roll=0.0):
    """A pinhole camera. Returns P(x, y, z) -> (sx, sy) in canvas pixels. World: z is up.
    `fov` is the horizontal field of view across the canvas width; `centre` is where the look point lands."""
    e, l = np.array(eye, float), np.array(look, float)
    fwd = (l - e) / np.linalg.norm(l - e)
    right = np.cross(fwd, (0, 0, 1.0)); right /= np.linalg.norm(right)
    up = np.cross(right, fwd)
    f = (W / 2) / math.tan(math.radians(fov) / 2)
    cx, cy = centre if centre else (W / 2, H / 2)
    def P(x, y, z=0.0):
        d = np.array((x, y, z), float) - e
        zc = max(float(d @ fwd), 1e-3)
        return (cx + f * float(d @ right) / zc, cy - f * float(d @ up) / zc)
    return P

def extrude(P, outline, z0, z1, eye, only=None):
    """Visible wall quads of an upright prism (convex plan `outline` of (x, y)) between heights z0..z1,
    seen by the camera at `eye`. `only(mid_xy)` can restrict which wall segments are kept."""
    O = np.asarray(outline, float); ctr = O.mean(0); out = []
    for i in range(len(O)):
        a, b = O[i], O[(i + 1) % len(O)]
        mid = (a + b) / 2
        n = np.array([b[1] - a[1], -(b[0] - a[0])])
        if n @ (mid - ctr) < 0: n = -n
        if n @ (np.array(eye[:2], float) - mid) > 0 and (only is None or only(mid)):
            out.append(np.array([P(a[0], a[1], z0), P(b[0], b[1], z0), P(b[0], b[1], z1), P(a[0], a[1], z1)]))
    return out

def boxplan(xa, xb, ya, yb):
    return [(xa, ya), (xb, ya), (xb, yb), (xa, yb)]

def cloudband(x, y, ln, th, steps=5, ragged=.5):
    """A stratus sliver the way the block-cutters did it: long, flat, pointed at both ends,
    its edges stepping rather than curving."""
    n = max(6, int(ln / 26))
    xs = np.sort(np.r_[x, x + ln, rng.uniform(x + ln * .04, x + ln * .96, n)])
    env = np.sin(np.pi * (xs - x) / ln) ** .55
    top = np.round(rng.uniform(.35, 1, len(xs)) * steps) / steps * th * .5 * env
    bot = np.round(rng.uniform(.35, 1, len(xs)) * steps) / steps * th * .5 * env * (1 + ragged * rng.uniform(-.5, .5, len(xs)))
    up = np.c_[xs, y - top]; dn = np.c_[xs[::-1], y + bot[::-1]]
    return np.r_[up, dn[1:-1]]

def conifer(x, base, height, width, crown=.72, lean=0.0, n=None, trunk_w=None, sparse=.0, tuft=(7, 22), sag=0.0, body=0.0):
    """Douglas-fir / hemlock. Visible trunk; separate sprays of unequal length with sky between; low
    sprays hang, high ones rise, tips turn up; one side fuller. Tuft size is capped so a near tree
    gets more marks, not bigger ones. `sag` bends every bough down (snow load); `body` > 0 gives each
    bough depth below its spine (use about .2 for a large near tree with few boughs).
    Returns (trunk_polys, foliage_polys); conifer.spines holds (xs, ys, side, length) per bough."""
    top = (x + lean * height, base - height)
    tw = trunk_w or max(2.0, width * .055)
    trunk = [ribbon([(x, base), (x + lean * height * .5, base - height * .5), top], w=tw, taper=(0, .97), wob=.04)]
    fol = []
    conifer.spines = []
    n = n or int(height * crown / max(7.0, min(width * .075, 15)))
    bias = rng.choice([-1, 1]) * rng.uniform(.05, .3)
    f = .0
    for i in range(n * 3):
        f += rng.uniform(.45, 1.7) / n
        if f > 1: break
        if rng.uniform() < sparse: continue
        y = top[1] + height * crown * f
        xt = top[0] + (x - top[0]) * (crown * f)
        for side in (-1, 1):
            if rng.uniform() < .2: continue
            env = (.10 + .9 * min(f * 1.5, 1) ** .8) * (1 - .25 * max(f - .75, 0) / .25)
            ln = width / 2 * env * rng.uniform(.45, 1.12) * (1 + side * bias) + 3
            droop = (-.3 + .8 * f) * rng.uniform(.5, 1.35) + sag * rng.uniform(.7, 1.3)
            t = np.linspace(0, 1, max(5, int(ln / 5)))
            sx = xt + side * ln * t
            sy = y + ln * (droop * t ** 1.3 - .18 * t ** 3)
            trunk.append(ribbon(np.c_[sx, sy], w=max(1.0, min(tw * .3, 5.5) * (.5 + .5 * env)), taper=(0, .85), wob=0))
            conifer.spines.append((sx, sy, side, ln))
            tl0 = float(np.clip(ln * .3, tuft[0], tuft[1]))
            m = max(2, int(ln / (tl0 * .55) * (1 + 5 * body)))
            for q in range(m):
                u = rng.uniform(.14, 1.0)
                j = int(u * (len(t) - 1))
                tl = tl0 * rng.uniform(.6, 1.15) * (1 - .35 * u)
                dy = rng.uniform(0, body * ln * math.sin(math.pi * u ** .7)) if body else 0
                fol.append(_tuft(sx[j] - side * tl * .3, sy[j] - tl * .08 + dy, side, tl))
    return trunk, fol

def _tuft(px_, py_, side, tl):
    """One hanging three-fingered lobe of needles."""
    j = lambda: rng.uniform(.75, 1.25)
    pts = [(0, -tl * .1), (.9 * j(), .12 * j()), (.58, .22), (.6 * j(), .62 * j()), (.3, .34), (.14 * j(), .78 * j()), (-.22 * j(), .3 * j())]
    return np.array([(px_ + side * a * tl, py_ + b * tl) for a, b in pts])

def sheen(xa, xb, y0, y1, th0=2.0, th1=3.6, breakup=4.0, keep=.6, spread=.12):
    """Reflection of a long lit band (a row of windows, a strip of sky): whole-width dashes just
    under it, breaking into more and shorter pieces that drift apart toward the viewer."""
    out, y, w = [], y0, xb - xa
    while y < y1:
        f = (y - y0) / max(y1 - y0, 1)
        k = 1 + int(breakup * f * rng.uniform(.6, 1.4))
        th = (th0 + (th1 - th0) * f) * rng.uniform(.75, 1.2)
        lo, hi = xa - w * spread * f, xb + w * spread * f
        for _ in range(k):
            if rng.uniform() < 1 - (1 - keep) * f ** .7:
                ln = min((hi - lo) / k * rng.uniform(.45, 1.05) * (1 - .45 * f), (hi - lo) * .97)
                out.append(lens(rng.uniform(lo, hi - ln), y + rng.normal(0, th * .3), ln, th))
        y += th * (1.35 + 2.6 * f * f) * rng.uniform(.85, 1.25)
    return out

def ring(cx, cy, rx, squash=.26, w=1.1, arc=(0, 360)):
    """A raindrop ring on water: a thin ellipse (or part of one)."""
    a = np.radians(np.linspace(arc[0], arc[1], max(14, int(rx * 1.2))))
    return ribbon(np.c_[cx + rx * np.cos(a), cy + rx * squash * np.sin(a)], w=w, taper=(.15, .15), wob=0, smooth=False)

def snowload(spines, thick=.16, lo=6, hi=20, start=.22):
    """Snow lying along the top of each branch from conifer(): a lumpy cap, flat underneath."""
    out = []
    for sx, sy, side, ln in spines:
        if ln < 14: continue
        k = len(sx); a = int(k * start)
        th = float(np.clip(ln * thick, lo, hi))
        u = np.linspace(0, 1, k - a)
        lump = th * (np.sin(np.pi * u ** .8) ** .5) * (1 + .25 * np.sin(u * rng.uniform(6, 14) + rng.uniform(0, 6)))
        top = np.c_[sx[a:], sy[a:] - lump]
        bot = np.c_[sx[a:][::-1], sy[a:][::-1] + th * .12]
        out.append(np.r_[top, bot])
    return out

def shade(poly, color, p0, p1, strength=.85, power=1.6):
    """Ita-bokashi: a tone that is sharp along the edge of `poly` nearest p0 and fades out toward p1.
    This is how snow, mist and hollows get form without modelling."""
    select_array(raster([poly])); gradient('linear', p0, p1, fade(color, strength, 0, power=power)); select_none()

def snowpillows(spines, size=.085, lo=5, hi=30, start=.12, gap=.25):
    """Snow on boughs as it actually lies: separate lumpy pillows of different sizes with gaps
    where it has slid off, never one smooth cap (that reads as a white banana)."""
    out = []
    for sx, sy, side, ln in spines:
        if ln < 16: continue
        r0 = float(np.clip(ln * size, lo, hi))
        u = start
        while u < .98:
            r = r0 * rng.uniform(.55, 1.25) * (1 - .45 * u)
            j = int(u * (len(sx) - 1))
            if rng.uniform() > gap:
                out.append(blob(sx[j], sy[j] - r * .42, r * rng.uniform(1.1, 1.7), r * rng.uniform(.6, .85), n=int(rng.integers(8, 12)), rough=.22))
            u += r * rng.uniform(1.3, 2.2) / ln
    return out

def drift(xa, xb, y, depth, color, strength=.9, wave=5.0, power=1.5):
    """A wind crest in snow: sharp along its top edge, the shade below it thinning to nothing, and the
    whole thing tapering to a point at each end. Computed per pixel so no outline is left behind."""
    xa, xb = float(xa), float(xb)
    x = np.arange(W, dtype=np.float32)[None, :]
    yy = np.arange(H, dtype=np.float32)[:, None]
    t = np.clip((x - xa) / max(xb - xa, 1), 0, 1)
    k1, p1, k2, p2 = rng.uniform(4, 9), rng.uniform(0, 6), rng.uniform(11, 19), rng.uniform(0, 6)
    top = y + wave * (np.sin(t * k1 + p1) + .4 * np.sin(t * k2 + p2)) * np.sin(np.pi * t)
    d = np.maximum(depth * np.sin(np.pi * t) ** .6, 1e-3)
    a = np.clip(1 - (yy - top) / d, 0, 1) ** power
    a = np.where((yy >= top) & (x > xa) & (x < xb), a, 0) * np.clip((yy - top + 1), 0, 1)
    if _CLIP[0] is not None: a = a * _CLIP[0]
    select_array((strength * a).astype(np.float32)); fill(color); select_none()

def moonroad(cx, y0, y1, w0=120, w1=620, th0=1.6, th1=5.0, gap=1.0):
    """The moon's path on water: near the horizon a tight ladder of whole dashes; toward the viewer the
    rungs separate, break into pieces of unequal length, thicken and scatter sideways. (Long equal
    hairlines read as a venetian blind.)"""
    out, y = [], y0
    while y < y1:
        f = (y - y0) / max(y1 - y0, 1)
        hw = (w0 + (w1 - w0) * f ** 1.2) / 2
        th = (th0 + (th1 - th0) * f) * rng.uniform(.7, 1.25)
        k = 1 + int(rng.uniform(0, 1) + 4.5 * f)
        for _ in range(k):
            ln = hw * 2 / k * rng.uniform(.25, .95) * (1 - .3 * f)
            x = cx + rng.normal(0, hw * .42) - ln / 2
            if rng.uniform() < .92 - .35 * f:
                out.append(lens(x, y + rng.normal(0, th * .5), ln, th))
        y += th * (1.5 + gap * 3.2 * f ** 1.5) * rng.uniform(.8, 1.3)
    return out
