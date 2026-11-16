"""g1_walk: the night shift walking across the moon (bars 22-23). Shadow theatre: four dark profiles, four windows,
a foot down on every beat. Each walks their own walk at their own speed, so they drift against each other."""
import math
import numpy as np
import common as C

N = 48
SIZE, GROUND, MOON = 300, 600, (640, 330, 250)
WALKERS = [('marisol', 300, .5), ('dee', 452, 0.0), ('red', 604, .5), ('keeper', 900, 0.0)]     # name, x at pose 0, stride phase
CAM = (C.walk_speed('red', SIZE) + C.walk_speed('dee', SIZE)) / 2                              # px a pose
SPACING = 330
DECK = C.draw.rect(C.W, C.H, 0, GROUND, C.W, C.H)
RAILTOP = C.draw.rect(C.W, C.H, 0, GROUND, C.W, GROUND + 3)

def frame(i):
    img = C.harbour(hz=470, moon=MOON, shimmer=i // 2)
    # No. 4, far off: only its legs, sliding by slowly, the cut cable hanging
    cx = 1168 - 3.0 * i
    img = C.no4(img, cx, 476, 1150, colour='#101622', cable=False, stencil=False)
    hang = [(cx - 215, -10), (cx - 222, 120), (cx - 208, 230), (cx - 226, 300)]
    C.sh.setup(C.W, C.H, 5)
    img = C.draw.paint(img, C.draw.raster([C.sh.ribbon(hang, w=9, taper=(0, .2), wob=0)], C.W, C.H), '#101622')
    # the dock and its piles slide past at the camera's speed; one of them has the heron on it
    img = C.draw.paint(img, DECK, C.DOCK)
    off = (CAM * i) % SPACING
    for k in range(-1, 6):
        x = k * SPACING - off + 90
        img = C.draw.paint(img, C.draw.rect(C.W, C.H, x, 548, x + 22, GROUND + 40), '#0a0e17')
    hx = 90 + ((2 * SPACING + 920) - CAM * i)
    if -60 < hx < C.W + 60:
        img = C.heron(img, hx + 11, 548, s=.10, colour='#0a0e17')
    img = C.draw.paint(img, RAILTOP, '#27324a')
    for name, x0, ph in WALKERS:
        x = x0 + (C.walk_speed(name, SIZE) - CAM) * i
        over = dict(shN=14, elN=10) if name == 'red' else {}
        img = C.figure(img, name, C.walk_pose(name, (i % 12) / 12 + ph, **over), x=x, ground=GROUND, size=SIZE)
    return img
