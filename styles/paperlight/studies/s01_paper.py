"""Study 1: does simulated paper behave like paper? Five sheets, a lit back panel, nothing else."""
import numpy as np
from backlot import core, draw, comp, lab, model, screen, shapes as sh
W, H = 1200, 800                      # design pixels; at 4 px/mm the box is 300 x 200 mm
sh.setup(W, H, 2)
frame = comp.subtract(np.ones((H, W), np.float32), draw.rect(W, H, 60, 60, W - 60, H - 60))
def hill(y0, amp, seed):
    r = np.random.default_rng(seed); xs = np.linspace(-20, W + 20, 9)
    pts = [(x, y0 + amp * np.sin(x / 190.0 + seed) + r.uniform(-20, 20)) for x in xs]
    return draw.raster([np.vstack([sh.spline(pts), [(W + 20, H + 20), (-20, H + 20)]])], W, H)
trees = []
for x in range(120, W - 60, 150):
    t_, f_ = sh.conifer(x + sh.rng.normal(0, 20), 640, sh.rng.uniform(260, 380), sh.rng.uniform(110, 150), crown=.86)
    trees += t_ + f_
spec = model.Spec((W, H), ppm=4)
spec.material('back', kind='emit', strength=14.0, stops=[[0, '#ff9a4a'], [.45, '#ffd9a8'], [1, '#bcd4ff']], axis='Z')
spec.panel('back', (340, 240), (0, 62, 0), 'back')
moon = comp.subtract(np.ones((H, W), np.float32), draw.disc(W, H, 820, 230, 70))
spec.sheet('sky', comp.union(frame, moon), depth=50)                                  # a full sheet with a moon cut out of it
spec.sheet('far', comp.union(frame, hill(470, 40, 1)), depth=38)
spec.sheet('mid', comp.union(frame, hill(560, 50, 2)), depth=26)
spec.sheet('trees', comp.union(frame, comp.union(hill(660, 30, 3), draw.raster(trees, W, H))), depth=14)
spec.sheet('front', comp.union(frame, hill(730, 24, 4)), depth=2)
spec.ambient('#20242c', .15)
spec.camera(pos=(0, -620, 0), look=(0, 30, 0), lens=85, fstop=4.0, focus=(0, 26, 0))
fr = spec.render('out/paperlight/s01', frames=[1], samples=96, res=(1200, 800))
p = model.passes(fr[0])
print('passes', {k: v.shape for k, v in p.items()})
print('image range', float(p['image'][..., :3].min()), float(p['image'][..., :3].max()), 'depth', float(p['depth'].min()), float(np.percentile(p['depth'], 99)) if 'depth' in p else None)
img = lab.tonemap(p['image'], 'filmic', white=6)
core.save('out/paperlight/s01/look.png', img)
d = p['depth']; core.save('out/paperlight/s01/depth.png', np.clip((d - d.min()) / (np.percentile(d, 99.5) - d.min()), 0, 1))
core.save('out/paperlight/s01/index.png', p['index'] / max(float(p['index'].max()), 1))
