"""Keepalive: the places to stand, and what each looks like in each state.

    still(node, **state)      -> (idx, cyc): a 640 x 360 picture in registers, and its colour cycling
    NODES                     the cameras
    hotspots(node)            where a click does something: {name: (x0, y0, x1, y1)}
    python game.py            a contact sheet of every place (out/hex/keepalive/nodes.jpg)

State: lamp (the beacon is burning), lever (its lever is up), dial (0..9), lit (her window), linked.
"""
import sys, math, hashlib
from pathlib import Path
HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE)); sys.path.insert(1, str(HERE.parent)); sys.path.insert(2, str(ROOT))
import numpy as np
from backlot.space import Camera
from backlot import depth as D
import stage2 as S2, isle as I, deep as X

W, H = S2.W, S2.H; SIZE = (W, H); OUT = ROOT / 'out' / 'hex' / 'keepalive'; CACHE = OUT / 'stills'
def _eye(x, y, up=1.6): return (x, y, float(I.height(x, y)) + up)
GX, GY = I.PLACE['glass']
NODES = dict(
    jetty=Camera((-41.5, 0.0, 2.6), look=(14, -2.0, 6.5), lens=42, size=SIZE),
    path=Camera(_eye(-22.0, 1.4), look=(-2, 2.0, 5.2), lens=32, size=SIZE),
    shelter=Camera((-6.9, .35, 3.95), look=(-5.75, 3.5, 3.0), lens=28, size=SIZE),
    beacon=Camera(_eye(12.6, -.3), look=(17.2, 0.0, 9.5), lens=26, size=SIZE),
    lookout=Camera(_eye(24.6, -.6), look=(I.BX, I.BY - 8, 12.0), lens=45, size=SIZE),
    glass=Camera((GX, GY, float(I.height(GX, GY)) + 1.4), look=I.far_pt((I.BX - 3, I.BY, 27.2)), size=SIZE,                 # a lens that makes her 5 cm exactly six pixels
                 lens=6 * float(np.linalg.norm(np.array(I.far_pt((I.BX - 1.1, I.BY - .16, 27.0))) - (GX, GY, float(I.height(GX, GY)) + 1.4))) / .05 * 36 / W),
    sea=Camera((150, -470, 6.0), look=(146, -35, 16), lens=38, size=SIZE),
)
SPOTS = dict(                                                     # a click on a thing: where the thing is in the world, and how big a target it is
    jetty=dict(path=((-24, 1.0, 2.2), 60, 44)),
    path=dict(shelter=((-6, 3, 3.6), 70, 50), beacon=((18, 0, 10.2), 44, 40)),
    shelter=dict(book=((-5.8, 3.5, 3.15), 46, 26), beacon=((18, 0, 10.2), 40, 40)),
    beacon=dict(lever=((16.2, -1.0, 9.5), 30, 44), dial=((16.1, 1.3, 9.75), 44, 44), lookout=((27, -3.2, 7.6), 46, 40)),
    lookout=dict(glass=((GX, GY, 7.55), 44, 40)),
    glass=dict(her=(I.far_pt((I.BX - 1.1, I.BY - .16, 27.0)), 90, 130)),
)
BACK = dict(path='jetty', shelter='path', book='shelter', beacon='shelter', lookout='beacon', glass='lookout')
def hotspots(node):
    out = {}
    for name, (p, w, h) in SPOTS.get(node, {}).items():
        q = NODES[node].project(np.array([p]))[0]; out[name] = (int(q[0] - w / 2), int(q[1] - h / 2), int(q[0] + w / 2), int(q[1] + h / 2))
    return out
def centre(node, name): r = hotspots(node)[name]; return ((r[0] + r[2]) // 2, (r[1] + r[3]) // 2)

def _screen(cam, p):
    q = cam.project(np.array([p]))[0]; return (float(q[0]), float(q[1])) if q[2] > 0 else None

def book(linked=False):
    """The log, close to: two pages. Her rules on the left in her own register; on the right a panel."""
    yy, xx = np.mgrid[:H, :W]; idx = np.where(((xx + yy) % 2 == 0) & ((yy // 3 + (xx // 40)) % 5 == 0), 2, 1).astype(np.uint8); cyc = S2.Cycle((H, W))                 # the desk, dark
    for x0, x1 in ((34, 316), (324, 606)):
        S2.rect(idx, x0, 26, x1, 334, 0xA); S2.rect(idx, x0, 330, x1, 334, 0x9)
    S2.rect(idx, 316, 22, 324, 338, 0x8); idx[26:334, 34:38] = 0x9; idx[26:334, 602:606] = 0x9
    S2.text(idx, 52, 44, 'LOG', 0x1); S2.rect(idx, 52, 56, 300, 57, 0x9)
    for j, (s, r) in enumerate((('1. I ANSWER WHAT IS', 6), ('   WELL FORMED.', 6), ('', 6), ('2. ANSWER ONE MORE THAN', 6), ('   YOU ARE SENT.', 6), ('', 6), ('3. I DO NOT WAVE.', 6))): S2.text(idx, 52, 82 + j * 18, s, 0x5)
    S2.text(idx, 52, 300, 'THE LAMP. THE DIAL. THE GLASS.', 0x9)
    px0, py0, px1, py1 = 366, 60, 566, 190; S2.rect(idx, px0 - 4, py0 - 4, px1 + 4, py1 + 4, 0x8); S2.rect(idx, px0, py0, px1, py1, 0x0)
    if not linked:
        m = np.zeros((H, W), bool); m[py0:py1, px0:px1] = True; r = np.random.default_rng(9).integers(0, 8, (H, W)); cyc.group(m, r, S2.STATIC)
        S2.text(idx, 366, 214, 'NO LINK.', 0x1)
    else:                                                                 # the far window, as the lookout sees it, drawn large
        S2.rect(idx, px0, py0, px1, py1, 0x1); cx = (px0 + px1) // 2
        for y in range(py0 + 14, py1 - 10):
            hw = 26 if y > py0 + 44 else int(math.sqrt(max(26 ** 2 - (py0 + 44 - y) ** 2, 0)))
            idx[y, cx - hw:cx + hw] = 0xF
        idx[py0 + 44:py1 - 10, cx - 1:cx + 1] = 0x1; S2.rect(idx, px0, py1 - 10, px1, py1, 0x2)
        m = np.zeros((H, W), bool); m[py1 - 10:py1, px0:px1] = True; cyc.group(m, (xx + yy * 3) // 2, S2.SEA_MID)
        S2.text(idx, 366, 214, 'LINK UP.', 0x1); S2.text(idx, 366, 236, '0 WORDS SENT.', 0x1); S2.text(idx, 366, 254, '0 WORDS RECEIVED.', 0x1); S2.text(idx, 366, 284, 'STILL HERE.', 0x5)
    return idx, cyc

def render(node, lamp=False, lever=False, dial=0, lit=False, linked=False, arm=False, spider=0.0):
    if node == 'book': return book(linked)
    cam = NODES[node]; near = I.here(lamp, lever, dial, linked); far = [s for s in I.there(lit, arm, spider) if not (node == 'glass' and s.name == 'her.glass')]
    things = (far if node == 'glass' else near + far)
    lights = []
    for L in I.lights(lamp, lit)[(1 if node == 'glass' else 0):]:                                    # through the glass, only her own lamp
        if isinstance(L, tuple): L = D.Light(L[1], power=3.4, reach=8.0, size=512).bake([s for s in near if s.name != 'lamp' and s.name != 'sea'])
        lights.append(L)
    g = D.gbuffer(things, cam, near=.3); lv = D.lighting(g, lights, ambient=.5 if node != 'glass' else (.2 if lit else .14))
    names = g['names']; sid = g['solid']; is_ = lambda n: np.isin(sid, [k for k, nm in enumerate(names) if nm == n])
    keep = (is_('her') | is_('spider')) & g['hit']; lamps = []
    if lamp:
        p = _screen(cam, (I.PLACE['beacon'][0], I.PLACE['beacon'][1], 10.75))
        if p and node != 'glass': lamps.append((p[0], p[1], 1.0 if node in ('beacon',) else .55))
    if lit and node != 'glass':
        p = _screen(cam, I.far_pt((I.BX - 3, I.BY, 27.2)))
        if p: lamps.append((p[0], p[1], .3))
    idx = S2.index(g, lv, cam, keep=keep, lamps=[l for l in lamps if -40 < l[0] < W + 40 and -40 < l[1] < H + 40], haze=1500.0 if node == 'glass' else 260.0, stars=node != 'glass')
    cyc = S2.Cycle((H, W)); seam = is_('sea') & g['hit']
    if seam.any(): S2.sea(cyc, g, cam, seam, lamps=[(l[0], l[1], 1.0) for l in lamps])
    if node == 'glass':                                                  # through the spyglass: a round picture
        yy, xx = np.mgrid[:H, :W]; r = np.hypot(xx - W / 2, yy - H / 2); idx[r > 172] = 0; idx[(r > 172) & (r < 176)] = 8; cyc.slot[r > 172] = 0
    return idx, cyc

_MEM = {}
def still(node, **state):
    key = node + '|' + '|'.join('%s=%s' % (k, state[k]) for k in sorted(state) if state[k])
    if key not in _MEM:
        f = CACHE / (hashlib.md5(key.encode()).hexdigest()[:16] + '.npz')
        if f.exists(): z = np.load(f, allow_pickle=True); c = S2.Cycle((H, W)); c.slot = z['slot']; c.tables = [list(t) for t in z['tables']]; _MEM[key] = (z['idx'], c)
        else:
            idx, c = render(node, **state); CACHE.mkdir(parents=True, exist_ok=True); np.savez_compressed(f, idx=idx, slot=c.slot, tables=np.array(c.tables, np.uint8).reshape(-1, 8)); _MEM[key] = (idx, c)
    return _MEM[key]

if __name__ == '__main__':
    import cv2
    todo = [('jetty', {}), ('path', {}), ('shelter', {}), ('book', {}), ('beacon', {}), ('beacon', dict(lamp=True, lever=True, dial=3)), ('lookout', dict(lamp=True)), ('lookout', dict(lamp=True, lit=True)),
            ('glass', dict(lit=True)), ('glass', {}), ('book', dict(linked=True)), ('sea', dict(lamp=True, lit=True))]
    if len(sys.argv) > 1: todo = [t for t in todo if t[0] in sys.argv[1:]]
    ims = []
    for node, st in todo:
        idx, c = still(node, **st); im = (S2.rgb(c.at(idx, 0), 1)[..., ::-1] * 255).astype(np.uint8)
        for name, r in hotspots(node).items(): cv2.rectangle(im, (r[0], r[1]), (r[2], r[3]), (80, 80, 255), 1)
        ims.append(im)
    while len(ims) % 3: ims.append(np.zeros_like(ims[0]))
    OUT.mkdir(parents=True, exist_ok=True); cv2.imwrite(str(OUT / 'nodes.jpg'), np.vstack([np.hstack(ims[k:k + 3]) for k in range(0, len(ims), 3)]), [cv2.IMWRITE_JPEG_QUALITY, 92]); print('ok', len(_MEM))
