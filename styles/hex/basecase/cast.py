"""Base Case: the cast, as text. One hex digit per pixel, '.' for nothing; one pixel is 5 cm, the same grid the
house is painted on. The child is 1.3 m: twenty-six pixels. Chrome skin like everyone who is not the witch,
title-bar blue pyjamas (she is the user), twilight hair, and a torch whose lens is register F because she is
minding a light.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
import deep as X
import sprites as SP

def rows(s): return s.strip('\n').split('\n')
HEAD_SIDE = rows("""
...33333....
..3333333...
.333333333..
.33339999...
.3339909A...
.33399999...
.3339999....
..33.99.....""")
BODY_SIDE = rows("""
...BBBB.....
..BBBBBB....
..BBBBBB....
..BCBBBB98F.
..BBBBBB....
..BBBBBB....
..BCCCCB....
..BBBBBB....""")
LEGS_STAND = rows("""
...BBBB.....
...BBBB.....
...BB.BB....
...BB.BB....
...BB.BB....
...BB.BB....
...BB.BB....
...CC.CC....
...AA.AA....
...AAA.AAA..""")
LEGS_STRIDE = rows("""
...BBBB.....
..BBBBBB....
..BB..BB....
.BB....BB...
.BB....BB...
BB......BB..
BB......BB..
CC......CC..
AA......AA..
AAA.....AAA.""")
LEGS_PASS = rows("""
...BBBB.....
...BBBB.....
...BBBB.....
...BBBBB....
...BB.BB....
...BB..BB...
...BB..CC...
...CC..AA...
...AA.......
...AAA......""")
BACK = rows("""
...3333...
..333333..
.33333333.
.33333333.
.33333333.
.33333333.
.33333333.
..333333..
..BBBBBB..
.BBBBBBBB.
.BBBBBBBB.
.BBBBBBBB.
.BBBBBBBBF
9BBBBBBBB8
.BCCCCCCB.
.BBBBBBBB.
..BBBBBB..
..BBBBBB..
..BBB.BBB.
..BBB.BBB.
..BBB.BBB.
..BBB.BBB.
..BBB.BBB.
..CCC.CCC.
..AAA.AAA.
..AAA.AAA.""")
BACK_B = BACK[:18] + rows("""
..BBB.BBB.
..BBB.BBB.
..BBB.BBB.
..BBB.BBB.
..BBB.CCC.
..CCC.AAA.
..AAA.....
..AAA.....""")
BACK_C = BACK[:18] + rows("""
..BBB.BBB.
..BBB.BBB.
..BBB.BBB.
..BBB.BBB.
..CCC.BBB.
..AAA.CCC.
......AAA.
......AAA.""")
KNEEL = BACK[:11] + rows("""
9BBBBBBBB9
9BBBBBBBB9
.BCCCCCCB.
.BBBBBBBB.
.BBBBBBBB.
.BBBBBBBB.
AAA....AAA""")
SIT_FRONT = rows("""
...3333...
..333333..
.33333333.
.33999933.
.39099093.
.39999993.
.33999933.
..339933..
..BBBBBB..
.BBBBBBBB.
.BBCBBCBB.
.BBBBBBBB.
.BBBBBBBB.
9BBBBBBBB9
.BCCCCCCB.
.BBBBBBBB.""")
SIT_BACK = BACK[:8] + rows("""
..BBBBBB..
.BBBBBBBB.
.BBBBBBBB.
.BBBBBBBB.
.BBBBBBBB.
9BBBBBBBB9
.BCCCCCCB.
.BBBBBBBB.""")
LIFT = BACK[:8] + rows("""
9.BBBBBB.9
9BBBBBBBB9
BBBBBBBBBB
.BBBBBBBB.
.BBBBBBBB.
.BBBBBBBB.
.BCCCCCCB.
.BBBBBBBB.""") + BACK[16:]
RATLET = rows("""
..99.......
.9909999...
9999999998.
.9...9...88""")
RATLET_B = rows("""
..99.......
.9909999...
9999999998.
..9.9.....8""")
# the shadow on the basement wall: head and shoulders in profile, looking left. A hat with a bent tip and a
# brim wider than the shoulders, a nose, a chin, and a neck (without the neck it is a fir tree: the first cold
# reader said so)
SHADOW = rows("""
...............00.....
..............000.....
.............000......
............0000......
...........00000......
...........000000.....
..........0000000.....
..........00000000....
.........000000000....
.........0000000000...
0000000000000000000000
..000000000000000000..
........00000000......
.......000000000......
....000000000000......
..00000000000000......
......0000000000......
.......000000000......
.....00000000000......
........0000000.......
.........00000........
........0000000.......
......00000000000.....
....000000000000000...
...00000000000000000..
...00000000000000000..
...00000000000000000..
..0000000000000000000.
..0000000000000000000.
..0000000000000000000.
.00000000000000000000.
.00000000000000000000.
.00000000000000000000.
0000000000000000000000
0000000000000000000000
0000000000000000000000
0000000000000000000000
0000000000000000000000""")
WEB = rows("""
9...9...9...9
.9..9..9..99.
..9.9.9.99...
...999999....
99999.9......
...9.9.9.....
..9..9..9....
.9...9...9...
9....9....9..""")
STONES = rows("""
..8......8......8.....8...
.888....888....888...888..
.888.8..888..8.888...888..
.888.88.888.88.888.8.888..
.888.88.888.88.888.8.888..""")
POT = rows("""
.8.....8.
88888888.
.8888888.
.8888888.
..88888..
..8...8..""")
BONE = rows("""
9.....9
.99999.
9.....9""")
SHELL = rows("""
..999..
.9...9.
9.99..9
9.9.9.9
9..99.9
.9...9.
..999..""")

def child(pose='stand', flip=False, dark=False):
    """The child as an index array. Poses: stand, stride, pass (profile, facing east unless flipped);
    back, back_b, back_c (walking away); kneel; sit_front; sit_back. dark: the torch is off."""
    r = dict(stand=HEAD_SIDE + BODY_SIDE + LEGS_STAND, stride=HEAD_SIDE + BODY_SIDE + LEGS_STRIDE, **{'pass': HEAD_SIDE + BODY_SIDE + LEGS_PASS},
             back=BACK, back_b=BACK_B, back_c=BACK_C, kneel=KNEEL, lift=LIFT, sit_front=SIT_FRONT, sit_back=SIT_BACK)[pose]
    a = X.sprite(r, flip=flip)
    if dark: a[a == 0xF] = 8
    return a
def witch(flip=False): return X.sprite(SP.WITCH, flip=flip)
def prop(name): return X.sprite(dict(rat=RATLET, rat_b=RATLET_B, shadow=SHADOW, web=WEB, stones=STONES, pot=POT, bone=BONE, shell=SHELL, spider=SP.SPIDER)[name])
HAND = dict(stand=(10.5, 11.5), stride=(10.5, 11.5), **{'pass': (10.5, 11.5)}, back=(9.5, 12.5), back_b=(9.5, 12.5), back_c=(9.5, 12.5))
EYE = (9.5, 13.5)                                                   # where the shadow's eye is, in SHADOW's pixels      # the torch's lens, in sprite pixels from the top-left

if __name__ == '__main__':
    import cv2
    T = X.table(); poses = ['stand', 'pass', 'stride', 'back', 'back_b', 'back_c', 'kneel', 'lift', 'sit_front', 'sit_back']; k = 10
    sheet = np.full((30 * k, (14 * (len(poses) + 2) + 26) * k, 3), T[1], np.float32)
    for i, p in enumerate(poses + ['WITCH', 'SHADOW']):
        a = witch() if p == 'WITCH' else (prop('shadow') if p == 'SHADOW' else child(p)); a = np.where(a == 0, 9, a) if p == 'SHADOW' else a; big = np.repeat(np.repeat(a, k, 0), k, 1); y0 = (28 - a.shape[0]) * k; x0 = (i * 14 + 1) * k
        m = big != X.HOLE; sheet[y0:y0 + big.shape[0], x0:x0 + big.shape[1]][m] = T[big][m]
    X.save('out/hex/basecase/cast.png', sheet)
