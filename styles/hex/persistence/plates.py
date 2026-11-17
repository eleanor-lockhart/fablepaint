"""The explanatory pictures for Persistence, made from the rendered frames and from the models.

    one_place.png       twelve consecutive pictures of one place on the ride (36.0 s onward), laid out like
                        Muybridge's card: it is a different horse every time
    twelve_horses.png   the twelve carved horses, side on
    turnaround.png      one of them from eight sides, lit
    keeper.png          the keeper: a stride, and his few working poses
    slice.png           one twelfth of the ride, and the twelve of them
"""
import sys, shutil
from pathlib import Path
HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE)); sys.path.insert(1, str(HERE.parent)); sys.path.insert(2, str(ROOT)); sys.path.insert(3, str(HERE.parent / 'uptime'))
import numpy as np, cv2
OUT = ROOT / 'out' / 'hex' / 'persistence'; FR = OUT / 'frames'; FPS = 24

def one_place():
    cells = []; x0, x1, y0, y1 = 250, 1030, 96, 640
    for k in range(12):
        i = 36 * FPS + k; im = cv2.imread(str(FR / ('f_%04d.png' % i)))[y0:y1, x0:x1]; im = cv2.resize(im, (440, 307), interpolation=cv2.INTER_AREA)
        cv2.rectangle(im, (0, 0), (150, 24), (18, 10, 10), -1); cv2.putText(im, 'PICTURE %d' % i, (6, 17), cv2.FONT_HERSHEY_SIMPLEX, .5, (244, 236, 232), 1, cv2.LINE_AA); cells.append(im)
    g = 6; rows = [np.hstack([np.pad(c, ((g, g), (g, g), (0, 0)), constant_values=18) for c in cells[r:r + 4]]) for r in (0, 4, 8)]
    cv2.imwrite(str(HERE / 'one_place.png'), np.vstack(rows))

def slice_plate():
    import deep, ride as R
    from backlot import depth as D
    from backlot.space import Camera
    cam = Camera((0, -14.5, 18.0), look=(0, -.3, 1.0), lens=30, size=(960, 600)); fl = [s for s in R.shed() if s.name == 'floor']; ims = []
    for which in ('one', 'all'):
        sec = [s for s in R.sector() if s.name != 'canopy']; hs = R.horses(0.0)
        if which == 'one': things = fl + [D.turned(s, -90) for s in sec] + [b for n, b, _, _ in hs if n in ('horse.0.9', 'horse.1.9')]
        else: things = fl + R.ride(0.0, cut=True)
        g = D.gbuffer(things, cam); lv = D.lighting(g, [D.Light((6, -9, 9), power=1.6, reach=14).bake(things)], ambient=.38)
        ims.append((deep.colour(g, lv, steps=6, dither=0)[..., ::-1] * 255).astype(np.uint8))
    cv2.imwrite(str(HERE / 'slice.png'), np.hstack(ims))

if __name__ == '__main__':
    import horse, puppet
    horse.skeleton_sheet(HERE / 'twelve_horses.png'); horse.turnaround(HERE / 'turnaround.png')
    slice_plate()
    if FR.exists(): one_place()
    print('plates written')
