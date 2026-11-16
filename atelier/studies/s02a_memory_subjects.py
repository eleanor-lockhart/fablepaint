# Study 2a: a heron and a ferry drawn FROM MEMORY in the print kit, before looking at any photograph.
exec(open('../atelier/kit.py').read())
layer('paper'); fill(PAPER)
PAN = [(20, 20, 653, 620), (673, 20, 1306, 620)]
layer('base'); layer('mid'); layer('dark'); layer('light'); layer('key', blend='multiply')

# ---------------- heron, standing, facing left
x0, y0, x1, y1 = window(*PAN[0])
use('base'); select_rect(x0, y0, x1, y1); gradient('linear', (0, y0), (0, y1), ramp('#5d7478', '#93a49d', '#b9bca8')); select_none()
def L(pts): return [(x0 + x, y0 + y) for x, y in pts]
use('base'); marks([np.array(L([(0, 600), (0, 540), (633, 548), (633, 600)]))], '#48606a')
use('mid')
body = spline(L([(250, 322), (280, 276), (350, 298), (410, 368), (440, 418), (380, 402), (310, 396), (265, 366)]), closed=True)
marks([body], '#5b6f78')
neck = ribbon(L([(268, 318), (236, 262), (252, 210), (262, 165), (250, 128)]), w=30, taper=(0, .55), wob=0)
marks([neck], '#9aa39c')
marks([spline(L([(222, 118), (236, 104), (256, 108), (262, 122), (250, 134), (232, 132)]), closed=True)], '#e6e2d2')       # head
marks([np.array(L([(228, 112), (168, 126), (228, 128)]))], '#c59c50')                                                         # bill
marks([spline(L([(300, 380), (330, 372), (345, 400), (322, 420), (300, 410)]), closed=True)], '#8a6e58')                    # thigh
use('dark')
marks([ribbon(L([(238, 108), (262, 108), (296, 132)]), w=5, taper=(.1, .7), wob=0)], KEY)                                    # crown plume
marks([blob(x0 + 282, y0 + 302, 16, 10, n=8, rough=.15)], KEY)                                                              # shoulder patch
marks([ribbon(L(p), w=5.5, taper=(0, 0), wob=.05) for p in ([(318, 408), (322, 470), (306, 558)], [(336, 410), (346, 468), (336, 560)])], '#2a2c2e')
marks([ribbon(L(p), w=3, taper=(0, .6), wob=0) for p in ([(306, 558), (276, 562)], [(306, 558), (320, 566)], [(336, 560), (308, 566)], [(336, 560), (352, 566)])], '#2a2c2e')
marks([blob(x0 + 242, y0 + 116, 2.3, 2.3, n=8, rough=.05)], KEY)
use('light')
marks([ribbon(L([(262, 290 + i * 4), (256 + i * 5, 340 + i * 6)]), w=3, taper=(.1, .8), wob=0) for i in range(4)], '#d9d6c6')   # chest plumes
marks([ribbon(L([(330 + i * 16, 312 + i * 8), (380 + i * 14, 372 + i * 9)]), w=3.2, taper=(.1, .8), wob=0) for i in range(4)], '#7e9098')

# ---------------- ferry, three-quarter view, constructed from a remembered box model
x0, y0, x1, y1 = window(*PAN[1])
use('base'); select_rect(x0, y0, x1, y1); gradient('linear', (0, y0), (0, y1), ramp('#22323f', '#46606e', ('#a9b1a0', .5), ('#7f9698', .52), '#2a3d4e')); select_none()
P = camera(eye=(230, 150, 9), look=(0, 0, 9), fov=24, centre=((x0 + x1) / 2, y0 + 300))
def box(xa, xb, ya, yb, za, zb, side, end, top=None):
    """Draw the +y side and +x end (the two faces this camera sees) of a box."""
    polys = [(np.array([P(xa, yb, za), P(xb, yb, za), P(xb, yb, zb), P(xa, yb, zb)]), side),
             (np.array([P(xb, ya, za), P(xb, yb, za), P(xb, yb, zb), P(xb, ya, zb)]), end)]
    if top: polys.append((np.array([P(xa, ya, zb), P(xb, ya, zb), P(xb, yb, zb), P(xa, yb, zb)]), top))
    for p, c in polys: marks([p], c)
use('mid')
box(-66, 66, -13.5, 13.5, 0, 5, '#1b2a2a', '#141e1f')            # hull
box(-62, 62, -13.5, 13.5, 5, 10, '#b3bfbf', '#8d9c9f')           # car deck
box(-50, 50, -13, 13, 10, 16.5, '#b3bfbf', '#8d9c9f')            # passenger cabin
box(-8, 8, -4, 4, 16.5, 23, '#9aa9ab', '#7b8b8f')                # stack
box(38, 48, -5, 5, 16.5, 20, '#b3bfbf', '#8d9c9f'); box(-48, -38, -5, 5, 16.5, 20, '#b3bfbf', '#8d9c9f')   # pilot houses
use('dark')
marks([np.array([P(62, -9, 5.4), P(62, 9, 5.4), P(62, 9, 9.4), P(62, -9, 9.4)])], '#15191c')                # car deck mouth
marks([np.array([P(-8, 4, 19.5), P(8, 4, 19.5), P(8, 4, 21), P(-8, 4, 21)])], '#2c5a4a')                    # green band
use('light')
win = []
for z in (11.2, 14.0):
    for x in np.arange(-47, 47, 3.2):
        win.append(np.array([P(x, 13, z), P(x + 2, 13, z), P(x + 2, 13, z + 1.5), P(x, 13, z + 1.5)]))
for x in np.arange(-58, 58, 9):
    win.append(np.array([P(x, 13.5, 6.2), P(x + 5.5, 13.5, 6.2), P(x + 5.5, 13.5, 8.6), P(x, 13.5, 8.6)]))
marks(win, '#e8cf8c')
marks(sum([ticks(P(x, 13.5, 0)[0], P(x, 13.5, 0)[1] + 6, P(x, 13.5, 0)[1] + 120, 10, grow=1.5, th=2.0) for x in np.arange(-56, 60, 12)], []), '#dcbf7c')
use('key')
marks([seg(P(43, 0, 20), P(43, 0, 27), w=1.3), seg(P(-43, 0, 20), P(-43, 0, 27), w=1.2)], KEY)
finish(0, 0, W, H, border=False, tooth=.3)
use('key'); _CLIP[0] = None
marks([seg(a, b, w=1.6) for (a0, b0, a1, b1) in PAN for a, b in (((a0, b0), (a1, b0)), ((a1, b0), (a1, b1)), ((a1, b1), (a0, b1)), ((a0, b1), (a0, b0)))], KEY)
layer('gutter', below='key'); fill(PAPER)
m = np.ones((H, W), np.float32)
for (a0, b0, a1, b1) in PAN: m[b0:b1, a0:a1] = 0
modulate(m)
