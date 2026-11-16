"""Pictures of a place, derived from its model: a layout sheet (what the camera sees, measured) and a night frame.

    uv run python world/night-service/places/shots.py            the three baseline cameras at Ebb Landing, both ways
    uv run python world/night-service/places/shots.py lenses     one subject held the same size at five focal lengths

Nothing here places anything by eye. The horizon, the size of every figure, what hides what, where the moon is
and which way up, and where its road lies on the water all come from the camera and the almanac.
"""
import sys, math
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parent))
import numpy as np
import cv2
from backlot import core, draw, lab, comp, screen, space as sp, shapes as sh
import ebb_landing as EL

FACE = 'Open Sans:style=Condensed Regular'
SKY = [(-2, '#31475f'), (0, '#3a5673'), (4, '#2b4460'), (14, '#16263e'), (40, '#0b1322'), (90, '#070b14')]      # altitude in degrees -> colour: lightest just above the sea
HAZE = '#2f4660'

def _ramp(v, stops):
    xs = [s[0] for s in stops]; cs = np.array([core.col(s[1]) for s in stops])
    return np.stack([np.interp(v, xs, cs[:, k]) for k in range(3)], -1)

def altitude(cam):
    """Altitude in degrees of the sky seen through every pixel."""
    W, H = cam.size; y, x = np.mgrid[:H, :W].astype(np.float64)
    d = cam.fwd[None, None, :] * cam.f + cam.right[None, None, :] * (x - cam.cx)[..., None] - cam.up[None, None, :] * (y - cam.cy)[..., None]
    return np.degrees(np.arctan2(d[..., 2], np.hypot(d[..., 0], d[..., 1])))

def sky(cam, moon, stars=1400, seed=7):
    """The night sky through this camera: a gradation by true altitude, stars at fixed directions, and the moon
    where the almanac puts it, the right size for the lens, lit on the side the sun is."""
    W, H = cam.size; img = np.zeros((H, W, 4), np.float32); img[..., :3] = _ramp(altitude(cam), SKY); img[..., 3] = 1
    r = np.random.default_rng(seed); az = r.uniform(0, 360, stars); alt = np.degrees(np.arcsin(r.uniform(0.02, 1, stars))); mag = r.pareto(2.2, stars) * .5 + .25
    dim = 1 - .75 * moon['lit']                                              # a bright moon washes the small stars out
    for a, h, m in zip(az, alt, mag):
        q = cam.sky(a, h)
        if q and 0 <= q[0] < W - 1 and 0 <= q[1] < H - 1:
            sep = math.degrees(math.acos(float(np.clip(sp.direction(a, h) @ sp.direction(moon['az'], moon['alt']), -1, 1))))
            k = min(m, 4.0) * dim * min(1.0, sep / 25) * min(1.0, h / 8)
            if k > .12: img[int(q[1]), int(q[0]), :3] += np.array([.8, .9, 1.0]) * k
    q = cam.sky(moon['az'], moon['alt'], moon['diameter']); road = None
    if q:
        t = cam.sky(*moon['toward_sun']); toward = (t[0] - q[0], t[1] - q[1]) if t else (1, 0)
        m = sp.moon_matte(W, H, q[0], q[1], max(q[2], 1.2), moon['lit'], toward)
        img[..., :3] = img[..., :3] * (1 - m[..., None]) + core.col('#efe6cc')[None, None, :] * 5.0 * m[..., None]
    return img

def water(img, p, cam, moon):
    """Water as it is at night: dark near the feet, pale toward the horizon where it mirrors the sky, with the
    moon's road under the moon. The road's place comes from the moon's bearing, its length from the moon's height."""
    W, H = cam.size; wm = sp.matte(p, 'water'); d = np.where(np.isfinite(p['depth']), p['depth'], 1e6)
    t = np.clip(1 - np.exp(-d / 420.0), 0, 1)[..., None]
    tone = core.col('#0a111b')[None, None, :] * (1 - t) + core.col('#2c425a')[None, None, :] * t
    img[..., :3] = img[..., :3] * (1 - wm[..., None]) + tone * wm[..., None]
    q = cam.sky(moon['az'], moon['alt'], moon['diameter'])
    if q and moon['alt'] > 0:
        hz = cam.horizon(); sh.setup(W, H, 11)
        w0 = max(2 * q[2] * 1.3, 6.0); w1 = max(w0 * 3, cam.f * math.tan(math.radians(6.0)) * .5)       # the glitter spreads to a few degrees near the viewer
        polys = sh.moonroad(q[0], hz + 2, H - 2, w0=w0, w1=min(w1, W * .5), th0=1.2, th1=4.0)
        rm = draw.raster(polys, W, H) * wm
        img[..., :3] += core.col('#efe6cc')[None, None, :] * 1.5 * rm[..., None] * moon['lit']
    return img

def night(S, cam, when=EL.SAILING, moon=None, dark=('dee', 'heron', 'no4'), frame=0, finish=True):
    """A finished night frame of the set through the camera. Returns (image, passes)."""
    m = moon or sp.moon(when, S.lat, S.lon)
    p = sp.render(S, cam, light=sp.direction(m['az'], max(m['alt'], 12.0)), lit=2.6, shade=1.0)      # one flat lighter plane on the side the moon is
    img = sky(cam, m)
    a = p['img'][..., 3:]; body = p['img'].copy()
    d = np.where(np.isfinite(p['depth']), p['depth'], 0.0); fog = (1 - np.exp(-d / 2600.0))[..., None] * a       # night air: far things go toward the colour of the horizon
    body[..., :3] = body[..., :3] * (1 - fog) + core.col(HAZE)[None, None, :] * fog * .55
    img = comp.over(img, body)
    img = water(img, p, cam, m)
    P = sp.positions(p, cam)
    # planking: seams across every deck, a metre and a half apart, drawn on the place and not on the picture
    dk = sp.matte(p, 'trestle.deck', 'span', 'creektrestle.deck') * (p['normal'][..., 2] > .9)
    along = np.where(sp.matte(p, 'creektrestle.deck') > 0, P[..., 1], P[..., 0]); px = cam.f / np.maximum(d, 1e-3)          # pixels per metre there
    seam = (np.mod(np.nan_to_num(along), 1.5) < .09) * dk * np.clip(px * .09 / .7, 0, 1)                                 # fade where a seam is thinner than a pixel
    img = draw.paint(img, seam.astype(np.float32), '#05080d', .5)
    img = sp.pools(img, p, cam, EL.lights(), P)
    wm = sp.matte(p, 'water'); ln = p['line'] * (1 - wm) * (a[..., 0] > .5)
    img = draw.paint(img, ln * np.clip(1.4 - d / 260.0, .15, 1), '#35435c', .55)                                 # the key block: creases and outlines, fading with distance
    if not finish: return img, p
    sil = sp.matte(p, *dark)
    img = lab.bloom(img, r=9, strength=.5, threshold=1.0, layers=3, protect=sil)
    img = lab.tonemap(img, 'filmic', white=6); img = lab.vignette(img, .28, radius=.75)
    return lab.grain(img, .02, size=1.3, frame=frame), p

def layout(S, cam, when=EL.SAILING, moon=None, title='', notes=()):
    """A layout sheet: what this camera sees, as a measured drawing. Horizon, centre, the moon, and a caption that
    says where the camera stands, how high, which way it looks and what lens it has."""
    m = moon or sp.moon(when, S.lat, S.lon); W, H = cam.size
    p = sp.render(S, cam, palette='drawing')
    img = core.canvas(W, H, sp.PAPER); img = comp.over(img, p['img'])
    img = draw.paint(img, p['line'], sp.LINE, .85)
    hz = cam.horizon()
    if 0 <= hz < H:
        dash = np.zeros((H, W), np.float32); dash[int(hz):int(hz) + 2, :] = 1; dash[:, (np.arange(W) // 12) % 2 == 1] = 0
        img = draw.paint(img, dash, sp.RED); img = draw.paint(img, draw.text(W, H, (W - 14, hz - 22), f'horizon: eye {cam.eye[2]:.1f} m above the water', 15, FACE, anchor='r'), sp.RED)
    cross = np.zeros((H, W), np.float32); cross[int(cam.cy) - 9:int(cam.cy) + 10, int(cam.cx)] = 1; cross[int(cam.cy), int(cam.cx) - 9:int(cam.cx) + 10] = 1
    img = draw.paint(img, cross, sp.WARM)
    q = cam.sky(m['az'], m['alt'], m['diameter'])
    if q and -50 < q[0] < W + 50 and -50 < q[1] < H + 50:
        t = cam.sky(*m['toward_sun']); toward = (t[0] - q[0], t[1] - q[1]) if t else (1, 0)
        img = draw.paint(img, sp.moon_matte(W, H, q[0], q[1], max(q[2], 2.0), m['lit'], toward), sp.WARM)
        img = draw.paint(img, draw.text(W, H, (q[0] + max(q[2], 2) + 8, q[1] - 9), f'moon {2 * q[2]:.0f} px', 14, FACE), sp.WARM)
    band = draw.rect(W, H, 0, H - 46, W, H); img = draw.paint(img, band, '#05080d', .82)
    img = draw.paint(img, draw.text(W, H, (16, H - 37), (title + '   ' if title else '') + cam.describe().split(': ', 1)[1], 19, FACE, track=1), sp.LINE)
    img = draw.paint(img, draw.text(W, H, (W - 16, H - 35), '   '.join(notes), 16, FACE, anchor='r'), sp.WARM)
    return img, p

def baseline(out=EL.OUT):
    S = EL.stage(); C = EL.cameras(); m = EL.night(); out.mkdir(exist_ok=True); made = []
    for k, c in C.items():
        L, p = layout(S, c, moon=m, title=f'EBB LANDING, CAMERA {k}', notes=[f'Dee: {c.place(EL.DEE_AT, EL.STATURE * .92)["px"]:.0f} px', f'No. 4: {c.place(EL.NO4_AT, 40)["px"]:.0f} px', '01:35'])
        core.save(str(out / f'cam{k}_layout.png'), L)
        N, _ = night(S, c, moon=m); core.save(str(out / f'cam{k}_night.png'), N); made += [L, N]
    screen.sheet(made, str(out / 'cameras.jpg'), [f'{k} {w}' for k in C for w in ('layout', 'night')], cols=2, cell_w=800)
    print('wrote', out / 'cameras.jpg')

def lenses(out=EL.OUT):
    """One subject held the same size at five focal lengths. Dee stays 230 px tall; the camera backs away down the
    trestle as the lens lengthens. What changes is everything behind her."""
    S = EL.build(); at = (-88.0, 0.0, EL.DECK); EL.stand(S, 'dee', at, 0.0); EL.perch(S, (-178, 16.5, 6.0), 200.0); m = EL.night(); made = []; caps = []
    # She stands in the middle of the chain for this, and the camera backs straight down the middle of the deck. From
    # her usual post on the south side the two longest lenses cannot be used at all: at 26 m the camera would be
    # inside the waiting shed, and at 77 m the shed is between it and her. A plan knows that; a guess does not.
    for mm in (18, 28, 50, 100, 300):
        f = 1280 * mm / 36; dist = f * EL.STATURE * .92 / 230
        c = sp.Camera(eye=(at[0] + dist, at[1] + .2, EL.DECK + 1.45), az=270, alt=0, lens=mm)
        N, _ = night(S, c, moon=m); made.append(N); caps.append(f'{mm} mm from {dist:.1f} m: the moon is {2 * c.sky(m["az"], m["alt"], m["diameter"])[2]:.0f} px, the towers {c.place((-115, 5.2, -6), 25)["px"]:.0f} px')
    screen.sheet(made, str(out / 'lenses.jpg'), caps, cols=5, cell_w=640); print('wrote', out / 'lenses.jpg')

# ------------------------------------------------------------------ "Two lenses": the same four people at the same minute, wide and long
WHO = [('marisol', -2.7, .5), ('dee', -1.0, 0.0), ('red', .7, .5), ('keeper', 3.9, 0.0)]      # name, metres along the track from the middle of the group, stride phase
TRACK_X, TIES = 35.0, EL.DECK + .4
_BASE = None; _OP = None

def _setup():
    """The moment: the moon about one degree up and going down; the boat gone; the Cable cut and the eye dark.
    The long lens stands 312 m east of the track on the tide flat, on the line from the moon through the walkers,
    and the walkers are put where that line also passes between No. 4's legs."""
    global _BASE, _OP
    if _BASE is not None: return _BASE
    sys.path.insert(0, str(HERE.parent / 'op'))
    import common as C; _OP = C
    lo, hi = EL.pst(2, 10), EL.pst(2, 32)
    for _ in range(30):                                          # the minute when the moon's centre is 0.95 degrees up
        mid = lo + (hi - lo) / 2
        if sp.moon(mid, EL.LAT, EL.LON)['alt'] > .95: lo = mid
        else: hi = mid
    when = lo; m = sp.moon(when, EL.LAT, EL.LON)
    d = sp.direction(m['az']); t = (TRACK_X - EL.NO4_AT[0]) / -d[0]; yw = EL.NO4_AT[1] - d[1] * t          # where the moon-to-No. 4 line crosses the track
    yw -= 9.5          # ...and then ten metres south of that. On the line itself No. 4's legs are wider than the moon and eclipse it: all that shows is a white slot between two pylons.
    tele_eye = np.array([TRACK_X - d[0] * 312.0, yw - d[1] * 312.0, 1.7])
    speed = {n: C.walker(n).stride * C.CAST[n]['height'] * EL.STATURE for n, _, _ in WHO}                  # metres a second: one stride cycle a second
    _BASE = dict(S=EL.build(boat=False, cable=False, eye=False), when=when, moon=m, yw=yw, tele_eye=tele_eye, speed=speed, cam_speed=(speed['red'] + speed['dee']) / 2)
    return _BASE

def _walkers(S0, t, y0, ones):
    """The set with the four walking north along the track at time t (seconds). On twos the drawing and its
    place in the world are both held for two frames; on ones neither is."""
    B = _setup(); S = sp.Set(S0.name, S0.lat, S0.lon); S.solids = list(S0.solids)
    tt = t if ones else math.floor(t * 12) / 12
    for n, off, ph in WHO:
        over = dict(shN=14, elN=10) if n == 'red' else {}
        EL.stand(S, n, (TRACK_X, y0 + off + B['speed'][n] * tt, TIES), 0.0, pose=_OP.walk_pose(n, tt + ph, **over))
    return S

def frame_wide(i):
    """35 mm from the tide flat, 26 m east of the trestle, walking north with them. Figures on ones, because a
    drawing held on twos slips against a camera that moves on ones."""
    B = _setup(); t = i / 24.0; y0 = B['yw'] - 17.0          # six seconds before the long lens's moment, so that the walkers arrive where it is aimed
    S = _walkers(B['S'], t, y0, ones=True)
    cam = sp.Camera(eye=(TRACK_X + 26.0, y0 + 1.5 + B['cam_speed'] * t, 1.9), az=B['moon']['az'] - 9.0, alt=7.5, lens=35)
    img, p = night(S, cam, moon=B['moon'], dark=('marisol', 'dee', 'red', 'keeper', 'no4', 'creektrestle'), frame=i)
    return img

def frame_long(i):
    """1,550 mm, locked off, 312 m away. The same minute. Figures on twos."""
    B = _setup(); t = i / 24.0; y0 = B['yw'] - 2.7
    S = _walkers(B['S'], t, y0, ones=False)
    cam = sp.Camera(eye=B['tele_eye'], look=(TRACK_X, B['yw'], TIES + .85 + .5), lens=1549)
    img, p = night(S, cam, moon=B['moon'], dark=('marisol', 'dee', 'red', 'keeper', 'no4', 'creektrestle'), frame=i + 96)
    return img

def frame_two(i): return frame_wide(i) if i < 96 else frame_long(i - 96)

def two_lenses(out='out/space/two_lenses'):
    from backlot import anim
    B = _setup(); print('the minute:', (B['when'] - __import__('datetime').timedelta(hours=8)).strftime('%H:%M:%S'), 'PST; moon az %.2f alt %.2f lit %.2f; walkers cross the line at y = %.1f; long lens at (%.1f, %.1f)' % (B['moon']['az'], B['moon']['alt'], B['moon']['lit'], B['yw'], B['tele_eye'][0], B['tele_eye'][1]))
    pattern = anim.render(frame_two, 192, out + '/frames', workers=10)
    anim.encode(pattern, str(EL.OUT / 'two_lenses.mp4'), fps=24, crf=20)
    screen.filmstrip(pattern, str(EL.OUT / 'two_lenses_strip.jpg'), n=8, cols=4, cell_w=480)
    print('wrote', EL.OUT / 'two_lenses.mp4')

def stills():
    """One frame of each lens, to look at before rendering the film."""
    core.save('out/space/wide_test.png', frame_wide(40)); core.save('out/space/long_test.png', frame_long(40))
    screen.sheet([core.load('out/space/wide_test.png'), core.load('out/space/long_test.png')], 'out/space/two_test.jpg', ['35 mm, tracking', '1549 mm, locked off'], cols=2, cell_w=800)

if __name__ == '__main__':
    a = sys.argv[1:] or ['baseline']
    {'baseline': baseline, 'lenses': lenses, 'two': two_lenses, 'stills': stills}[a[0]]()
