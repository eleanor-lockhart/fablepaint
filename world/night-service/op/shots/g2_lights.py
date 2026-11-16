"""g2_lights: minder, light, minder, light (bars 24-25). Eight cuts of six poses, a cut on every beat. Every light
is one light at the same place on black; every minder is at the cut-in size. Each cut is struck on its first two
poses and then settles, like a note."""
import math
import numpy as np
import common as C

N = 48
CX, CY = 640, 330
SKY = C.draw.gradient(C.W, C.H, (0, 0), (0, C.H), '#0d1626', '#22364e', '#3a5673')        # light enough that a dark figure reads against it

def hit(j, hi=2.0):
    return hi if j < 2 else 1.0

def minder(name, j, flip, pose=None, extra=None):
    img = SKY.copy()
    if extra: img = extra(img, j)
    x = 800 if flip else 480
    return C.figure(img, name, pose, x=x, ground=980, size=860, flip=flip, glow=5.0 * hit(j))

def lens(j):
    img = C.black()
    img = C.light(img, C.draw.disc(C.W, C.H, CX, CY, 54), C.LAMP, 4.0 * hit(j))
    frame_ = C.comp.subtract(C.draw.rect(C.W, C.H, CX - 86, CY - 104, CX + 86, CY + 104), C.draw.rect(C.W, C.H, CX - 72, CY - 90, CX + 72, CY + 90))
    bars = C.comp.union(C.draw.rect(C.W, C.H, CX - 3, CY - 104, CX + 3, CY + 104), C.draw.rect(C.W, C.H, CX - 86, CY + 96, CX + 86, CY + 120))
    return C.draw.paint(img, C.comp.union(frame_, bars), '#141a26')

def finder(j, i):
    img = C.black()
    ring = C.comp.subtract(C.draw.disc(C.W, C.H, CX, CY, 150), C.draw.disc(C.W, C.H, CX, CY, 134))
    vanes = C.comp.union(C.draw.rect(C.W, C.H, CX - 2, CY - 190, CX + 2, CY - 134), C.draw.rect(C.W, C.H, CX - 2, CY + 134, CX + 2, CY + 190))
    img = C.draw.paint(img, C.comp.union(ring, vanes), '#3a3220')
    img = C.draw.paint(img, C.draw.disc(C.W, C.H, CX, CY, 134), '#0b111c')
    x = CX + 30 - C.walk_speed('passenger', 210) * j
    img = C.figure(img, 'passenger', C.walk_pose('passenger', (i % 12) / 12), x=x, ground=CY + 128, size=210, flip=True, glow=5.0 * hit(j))
    return C.comp.over(C.black(), C.comp.mask(img, C.comp.union(C.draw.disc(C.W, C.H, CX, CY, 150), vanes)))

def board(j):
    img = C.black()
    img = C.draw.paint(img, C.draw.rect(C.W, C.H, CX - 12, CY, CX + 12, C.H), '#111722')                      # the mast
    img = C.draw.paint(img, C.draw.disc(C.W, C.H, CX, CY, 104), '#111722')                                  # the target plate
    img = C.draw.paint(img, C.draw.raster([np.array([(CX - 80, CY - 66), (CX, CY - 118), (CX + 80, CY - 66), (CX + 62, CY - 60), (CX, CY - 96), (CX - 62, CY - 60)])], C.W, C.H), '#1a2232')
    return C.light(img, C.draw.disc(C.W, C.H, CX, CY, 50), '#ff3b24', 4.0 * hit(j))

def boat(j):
    img = C.black()
    img = C.draw.paint(img, C.draw.rect(C.W, C.H, 0, CY - 150, C.W, CY + 150), '#111722')
    m = np.zeros((C.H, C.W), np.float32)
    for k in range(-1, 14):
        x = k * 132 - 14 * j
        if x + 70 > 0 and x < C.W:                                  # a rect that ends left of the frame would wrap round
            m = np.maximum(m, C.draw.rect(C.W, C.H, x, CY - 50, x + 70, CY + 50))
    return C.light(img, m, C.LAMP, 1.7 * hit(j))

def beam(img, j):
    wedge = C.comp.feather(C.draw.raster([np.array([(C.W + 40, -60), (C.W + 40, 210), (560, 250), (600, 170)])], C.W, C.H), 14)
    return C.light(img, wedge * .55, C.LAMP, .42 * hit(j, 2.4))

def red_rain(img, j):
    C.sh.setup(C.W, C.H, 40 + j // 2)
    pool = C.draw.disc(C.W, C.H, 820, 300, 210, soft=120)
    return C.light(img, C.draw.raster(C.sh.rain(520, 60, 1120, 560, n=46, angle=106, w=1.6, length=(.15, .35)), C.W, C.H) * pool, '#ff3b24', 1.4 * hit(j))

def lamp_cone(img, j):
    cone = C.comp.feather(C.draw.raster([np.array([(760, -10), (840, -10), (1010, C.H), (590, C.H)])], C.W, C.H), 18)
    return C.light(img, cone * .5, '#ffd9a0', .3 * hit(j, 2.2))

_S = C.CAST
ORRIN = dict(_S['keeper']['pose'], head=-14, lean=4)
RED_UP = dict(_S['red']['pose'], shN=100, elN=20)
DEE_PUNCH = dict(_S['dee']['pose'], shN=58, elN=62)

def frame(i):
    cut, j = divmod(i, 6)
    if cut == 0: return minder('keeper', j, False, ORRIN, beam)
    if cut == 1: return lens(j)
    if cut == 2: return minder('marisol', j, True)
    if cut == 3: return finder(j, i)
    if cut == 4: return minder('red', j, False, RED_UP, red_rain)
    if cut == 5: return board(j)
    if cut == 6:
        img = minder('dee', j, True, DEE_PUNCH, lamp_cone)
        y = 430 + 22 * j + 3 * j * j                                                                  # the chad falls
        return C.light(img, C.draw.rect(C.W, C.H, 606, y, 624, y + 24), C.LAMP, 6.0 * hit(j))
    return boat(j)
