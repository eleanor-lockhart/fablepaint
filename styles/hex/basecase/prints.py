"""Base Case: one basement, four prints. The same model through the same camera, as each machine would show it.

    uv run python styles/hex/basecase/prints.py      writes four_prints.png (and a camera move as a strip: travel.jpg)
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
for q in (HERE.parent / 'uptime', HERE.parents[2], HERE.parent, HERE): sys.path.insert(0, str(q))          # this folder first: uptime has a film.py too
import numpy as np
import cv2
import film as F, levels as LV, deep as X, house as Hs, cast as CA, ui as U
from backlot import depth as D
from backlot.space import Camera
C = U.C
def now(w=640, h=360):
    cam = LV.camera('room', 1280, 720); c = D.card('child', CA.child('stride'), (Hs.FX + 5.2, 4.3, Hs.FLOOR), cam.right, glow=.42, cast=False)
    img, g = F.render(F.statics() + Hs.lid(78) + Hs.screen() + Hs.tube(0) + [c], cam, [F.screen_lamp(), F.torch(np.array([Hs.FX + 5.5, 4.3, Hs.FLOOR + .72]), (1, 0, -.22), F.statics())], .06, moving=[c])
    return cv2.resize(X.glow(img), (w, h), interpolation=cv2.INTER_AREA)
def sheet():
    ego = ('stride', Hs.FX + 5.2, 4.3, Hs.FLOOR, False)
    g, lv = LV.scene('room', 320, 180, lid=78, ego=ego); p1 = LV.up(LV.print16(g, lv), 2)
    g, lv = LV.scene('room', 640, 360, lid=78); p2 = LV.up(LV.print1(g, lv), 1)
    g, lv = LV.scene('room', 320, 180, lid=78, computer=False, who=True); p3 = LV.up(LV.printL(g), 2)
    out = np.zeros((720, 1280, 3), np.float32)
    for k, (im, year, what) in enumerate(((now(), 'NOW', 'PAINT ON A 5 CM GRID, CAST LIGHT, A CAMERA THAT TRAVELS'), (p1, '1989', '16 COLOURS, A DITHER, A FIGURE THAT SHRINKS'), (p2, '1987', 'ONE BIT, EDGES INKED'), (p3, '1980', 'LINES. NO COMPUTER HERE. A WITCH'))):
        x, y = (k % 2) * 640, (k // 2) * 360; out[y:y + 360, x:x + 640] = im
        U.rect(out, x, y + 336, x + 640, y + 360, C[0], .78); U.text(out, x + 8, y + 340, year, C[0xF] if k == 0 else C[0xA], 2); U.text(out, x + 8 + U.tw(year + ' ', 2), y + 344, what, C[9], 1)
    out[358:362] = C[0]; out[:, 638:642] = C[0]
    X.save(HERE / 'four_prints.png', out)
def travel():
    """Six frames of the tracking shot, to show that near things pass faster than far ones."""
    ims = [cv2.resize(F.frame(int(t * 24)), (640, 360), interpolation=cv2.INTER_AREA) for t in (21.0, 21.8, 22.6, 23.4, 24.2, 25.0)]
    X.save(HERE / 'travel.jpg', np.vstack([np.hstack(ims[:3]), np.hstack(ims[3:])]))
if __name__ == '__main__':
    sheet(); travel()
