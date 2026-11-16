"""a_open: the cold open and the title (bars 1-4). Black; a far light; four ticket punches, and on each a lit
window snaps on in the dark; then the hit: the harbour, the four of them round their windows, the title."""
import math
import numpy as np
import common as C

N = 96
ROW = [('keeper', 452), ('red', 578), ('dee', 704), ('marisol', 830)]      # where they stand on pose 48
ON = {'keeper': 24, 'red': 30, 'dee': 36, 'marisol': 42}                   # the punches
SIZE, GROUND = 300, 610

def window_matte(name, x):
    """The matte of a character's chest window for the standing pose at (x, GROUND): lit before the figure is seen."""
    c = C.CAST[name]; fig = c['fig']; s = SIZE * c['height']
    P = fig.on_trunk(fig.joints(c['pose']), [(.250, -.002), (.250, .030), (.205, .030), (.205, -.002)])
    return C.draw.raster([np.c_[x + P[:, 0] * s, GROUND - P[:, 1] * s]], C.W, C.H)
WIN = {n: window_matte(n, x) for n, x in ROW}
FAR = C.draw.disc(C.W, C.H, 168, 424, 2.6)                                  # Tern Point, a long way off
TITLE = C.text((700, 104), 'NIGHT SERVICE', 122, track=15, anchor='m')
TAG = C.text((700, 262), 'SOMEBODY HAS TO STAY UP.', 32, track=11, anchor='m')
PILE = C.draw.rect(C.W, C.H, 1098, 560, 1118, 640)

def frame(i):
    if i < 48:
        img = C.black()
        if i < 3 or 12 <= i < 15:
            img = C.light(img, FAR, C.LAMP, 5.0)
        for name, x in ROW:
            if i >= ON[name]:
                k = 9.0 if i - ON[name] < 2 else 4.2 + .5 * math.sin(1.7 * (i // 2) + x)
                img = C.light(img, WIN[name], C.CAST[name]['window'], k)
        return img
    j = i - 48
    img = C.harbour(hz=430, moon=None, shimmer=i // 2)
    if (j % 24) < 3:
        img = C.light(img, FAR, C.LAMP, 6.0)
    img = C.draw.paint(img, C.draw.rect(C.W, C.H, 0, GROUND, C.W, C.H), C.DOCK)
    img = C.draw.paint(img, PILE, C.DOCK)
    img = C.heron(img, 1108, 560, s=.11, colour='#0c1119')
    for name, x in ROW:
        img = C.figure(img, name, None, x=x, ground=GROUND, size=SIZE, glow=9.0 if j < 2 else 5.0)
    flare = 2.2 if j < 2 else 1.0
    img = C.light(img, TITLE, C.INK, .92 * flare)
    img = C.sigil(img, 152, 132, 70, lit=1.6 if j < 2 else 1.0)
    if j >= 24:
        wipe = C.draw.rect(C.W, C.H, 0, 0, 370 + 660 * C.ease(C.clamp01((j - 24) / 7), 'out'), C.H)
        img = C.draw.paint(img, TAG * wipe, C.DIM)
    return img
