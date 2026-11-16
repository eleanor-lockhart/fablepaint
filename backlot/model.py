"""backlot.model: the model shop. Turn 2D cut patterns into physical sheets in Blender, light them,
photograph them with a real lens, and bring the passes back.

    spec = model.Spec(size=(W, H), ppm=4)                 design canvas and pixels per millimetre
    spec.sheet('hills', matte, depth=30)                  a sheet of paper cut to a matte, 30 mm back
    spec.light('lamp', pos=(0, 40, 10), power=.4, color='#ffb060')
    spec.camera(pos=(0, -520, 0), look=(0, 40, 0), lens=85, fstop=2.8, focus=(0, 30, 0))
    frames = spec.render('out/shot', frames=[1], samples=96, res=(1280, 720))
    p = model.passes(frames[0])                           {'image', 'depth', 'index', 'emit', 'normal'}

Units are millimetres. X is right, Z is up, Y runs away from the camera (depth).
"""
import json, subprocess, os
from pathlib import Path
import numpy as np
from .core import F, read_exr
from .draw import trace

HERE = Path(__file__).resolve().parent

class Spec:
    def __init__(self, size, ppm=4.0):
        self.d = dict(size=list(size), ppm=ppm, sheets=[], panels=[], lights=[], materials={}, anim=[], camera={})
    def material(self, name, **m):
        """kind: paper | card | acetate | emit | mirror. color, translucency, through (colour of light passing), strength, stops."""
        self.d['materials'][name] = m; return name
    def sheet(self, name, matte=None, depth=0.0, cuts=None, material='paper', thickness=.25, tol=.5, **kw):
        """A sheet cut to a matte (white = paper) standing `depth` mm from the front. Extra: offset=[x, z] mm, tilt, turn (degrees)."""
        cuts = cuts if cuts is not None else trace(matte, tol=tol)
        self.d['sheets'].append(dict(name=name, depth=depth, cuts=cuts, material=material, thickness=thickness, **kw)); return name
    def panel(self, name, size, pos, material, rot=(0, 0, 0), **kw):
        """A plain rectangle (width, height mm) facing the camera unless rotated: back lights, walls, floors."""
        self.d['panels'].append(dict(name=name, size=list(size), pos=list(pos), rot=list(rot), material=material, **kw)); return name
    def light(self, name, pos, power=1.0, color='#ffffff', type='point', **kw):
        """type: point | spot | area. power in watts (tabletop scale: 0.05 to 5). spot: look=(x,y,z), cone, blend. area: size=[w,h], rot/look."""
        self.d['lights'].append(dict(name=name, pos=list(pos), power=power, color=color, type=type, **kw)); return name
    def haze(self, size, pos=(0, 0, 0), density=2.0, **kw):
        self.d['haze'] = dict(size=list(size), pos=list(pos), density=density, **kw)
    def ambient(self, color='#101216', strength=.02):
        self.d['ambient'] = dict(color=color, strength=strength)
    def camera(self, pos, look=(0, 0, 0), lens=85, fstop=None, focus=None):
        self.d['camera'] = dict(pos=list(pos), look=list(look), lens=lens, fstop=fstop, focus=list(focus) if focus else None)
    def key(self, target, path, keys, interp='LINEAR', index=None):
        """Animate: target is a sheet/light/panel name, 'cam', 'target' (what the camera looks at) or 'focus'.
        path: location | rotation_euler | data.energy | data.color | data.lens ...; keys: [(frame, value), ...]."""
        self.d['anim'].append(dict(target=target, path=path, keys=[[f, list(v) if isinstance(v, (list, tuple)) else v] for f, v in keys], interp=interp, index=index))
    def render(self, out, frames=(1,), samples=96, res=(1280, 720), denoise=True, noise=.02, bounces=10, save_blend=False, quiet=True):
        out = Path(out).resolve(); out.mkdir(parents=True, exist_ok=True)
        self.d['render'] = dict(out=str(out), frames=list(frames), samples=samples, res=list(res), denoise=denoise, noise=noise, bounces=bounces, save_blend=save_blend)
        sp = out / 'spec.json'; sp.write_text(json.dumps(self.d))
        r = subprocess.run(['blender', '-b', '--factory-startup', '--python', str(HERE / 'bl' / 'build.py'), '--', str(sp)], capture_output=True, text=True)
        log = r.stdout + r.stderr; (out / 'blender.log').write_text(log)
        done = [str(out / f'f_{f:04d}.exr') for f in frames if (out / f'f_{f:04d}.exr').exists()]
        if len(done) != len(list(frames)):
            raise RuntimeError('Blender failed; last lines of log:\n' + '\n'.join(log.strip().split('\n')[-14:]))
        return done

def passes(exr):
    """Read one rendered frame -> dict: image (H,W,4 linear), depth (metres from the camera), index (which
    sheet: 1 = first sheet added, 0 = anything else), emit (H,W,3), normal (H,W,3), noisy (before denoising)."""
    ch = read_exr(exr)
    img = ch['Combined']
    if img.shape[2] == 3:
        img = np.dstack([img, np.ones(img.shape[:2], F)])
    out = {'image': img.astype(F)}
    for key, name in (('depth', 'Depth'), ('index', 'Object Index'), ('emit', 'Emission'), ('normal', 'Normal'), ('noisy', 'Noisy Image')):
        if name in ch:
            out[key] = ch[name]
    return out

def sheet_matte(p, n):
    """Matte of the n-th sheet (1-based, in the order sheets were added) from a frame's index pass."""
    return (np.abs(p['index'] - n) < .5).astype(F)

def patterns(spec):
    """Every sheet's cut pattern as a matte, in the order the sheets were added: [(name, depth, matte), ...]."""
    from .draw import raster
    W, H = spec.d['size']; out = []
    for L in spec.d['sheets']:
        outer = [np.array(c['pts']) for c in L['cuts'] if not c['hole']]; holes = [np.array(c['pts']) for c in L['cuts'] if c['hole']]
        m = raster(outer, W, H, ss=1)
        if holes: m = m * (1 - raster(holes, W, H, ss=1))
        out.append((L['name'], L['depth'], m))
    return out

def making_of(spec, p, final, out, cell_w=420):
    """One sheet that shows how a box was made: the cut patterns front to back, then the render's
    depth and sheet-index passes, the raw render, and the finished frame."""
    from . import screen, comp
    from .core import l2s, canvas
    imgs, caps = [], []
    for name, depth, m in patterns(spec):
        imgs.append(comp.over(canvas(m.shape[1], m.shape[0], '#20242c'), comp.stencil(m, '#f1ede2'))); caps.append(f'cut: {name}  ({depth:g} mm back)')
    d = p['depth']; dn = np.clip((d - d.min()) / max(float(np.percentile(d, 99.5) - d.min()), 1e-6), 0, 1)
    imgs.append(np.dstack([dn ** 2.2] * 3 + [np.ones_like(dn)]).astype(F)); caps.append('depth pass')
    ix = p['index'] / max(float(p['index'].max()), 1)
    imgs.append(np.dstack([ix ** 2.2] * 3 + [np.ones_like(ix)]).astype(F)); caps.append('sheet index pass')
    raw = p['image'].copy(); raw[..., :3] = np.clip(raw[..., :3], 0, 1); imgs.append(raw); caps.append('raw render (clipped)')
    imgs.append(final); caps.append('finished frame')
    return screen.sheet(imgs, out, caps, cols=4, cell_w=cell_w)
