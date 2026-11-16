"""g1_walk: the night shift walking across the moon (bars 22-23). Shadow theatre: four dark profiles, four windows,
a foot down on every beat. Each walks their own walk at their own speed, so they drift against each other.

v1.1, after the outside review. v1 "did not read as travelling" (the moon and water are rightly still, and the only
thing that slid was a few thin posts on a dark band), and a library bug drew a black slab behind the walkers'
shins that popped every eighteen poses. Now they walk along a pier: a deck on piles with the moonlit water showing
between the piles, so that the ground visibly streams past under their feet."""
import math
import numpy as np
import common as C

N = 36                                  # v1.1: the first second of bar 22 now belongs to No. 4's eye going out (f15_eye_out)
SIZE, GROUND, MOON = 300, 600, (640, 330, 250)
WALKERS = [('marisol', 300, .5), ('dee', 452, 0.0), ('red', 604, .5), ('keeper', 900, 0.0)]     # name, x at pose 0, stride phase
CAM = (C.walk_speed('red', SIZE) + C.walk_speed('dee', SIZE)) / 2                              # px a pose: the pier slides by at this
BAY = 172                                                                                      # pile spacing
INK = '#090c13'

def pier(off):
    """The deck slab, its piles and one cross-brace per bay, as a matte, slid left by `off` pixels."""
    m = C.draw.rect(C.W, C.H, 0, GROUND, C.W, GROUND + 15)
    polys = []
    for k in range(-1, C.W // BAY + 3):
        x = k * BAY - (off % BAY)
        m = np.maximum(m, C.draw.rect(C.W, C.H, x, GROUND + 15, x + 22, C.H))
        polys.append(np.array([(x + 22, GROUND + 22), (x + 28, GROUND + 15), (x + BAY, GROUND + 104), (x + BAY, GROUND + 114)], np.float32))
    return np.maximum(m, C.draw.raster(polys, C.W, C.H))

def frame(i):
    img = C.harbour(hz=470, moon=MOON, shimmer=i // 2)
    # No. 4, far off: only its legs, sliding by slowly, the cut cable hanging
    cx = 1168 - 3.0 * i
    img = C.no4(img, cx, 476, 1150, colour='#101622', cable=False, stencil=False)
    C.sh.setup(C.W, C.H, 5)
    hang = [(cx - 215, -10), (cx - 222, 120), (cx - 208, 230), (cx - 226, 300)]
    img = C.draw.paint(img, C.draw.raster([C.sh.ribbon(hang, w=30, taper=(0, .1), wob=0)], C.W, C.H), '#101622')      # the severed hose, as thick as e_no4 draws it
    off = CAM * i
    img = C.draw.paint(img, pier(off), INK)
    # the deck's moonlit edge, broken by plank seams that slide with it
    edge = C.draw.rect(C.W, C.H, 0, GROUND, C.W, GROUND + 3)
    for k in range(-1, C.W // 43 + 2):
        x = k * 43 - (off % 43)
        edge = edge * (1 - C.draw.rect(C.W, C.H, x, GROUND, x + 5, GROUND + 3))
    img = C.draw.paint(img, edge, '#3a4a66')
    # a mooring post every third bay, standing above the deck; the heron is on one of them
    for k in range(-1, 5):
        x = k * 3 * BAY - (off % (3 * BAY)) + 60
        img = C.draw.paint(img, C.draw.rect(C.W, C.H, x, GROUND - 46, x + 20, GROUND), INK)
    hx = 60 + 9 * BAY - off
    if -60 < hx < C.W + 60:
        img = C.heron(img, hx + 10, GROUND - 46, s=.10, colour=INK)
    for name, x0, ph in WALKERS:
        x = x0 + (C.walk_speed(name, SIZE) - CAM) * i
        over = dict(shN=14, elN=10) if name == 'red' else {}
        img = C.figure(img, name, C.walk_pose(name, (i % 12) / 12 + ph, **over), x=x, ground=GROUND, size=SIZE)
    return img
