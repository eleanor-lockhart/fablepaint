# Print 2, notan: "Lookout, first snow". Three variants in three values.
exec(open('../styles/lit-window/kit.py').read())
D, M, L = '#262626', '#7f7f7f', '#e8e8e8'
layer('n'); fill('#ffffff')
def panel(i):
    ox, oy, w, h = 20 + 325 * i, 20, 305, 450
    window(ox, oy, ox + w, oy + h)
    def Pg(pts, col): marks([np.array([(ox + a * w, oy + b * h) for a, b in pts])], col)
    return Pg
def tower(Pg, x, y, s):
    Pg([(x - .05 * s, y), (x - .035 * s, y - .13 * s), (x + .035 * s, y - .13 * s), (x + .05 * s, y)], D)
    Pg([(x - .07 * s, y - .13 * s), (x + .07 * s, y - .13 * s), (x + .07 * s, y - .145 * s), (x - .07 * s, y - .145 * s)], D)
    Pg([(x - .05 * s, y - .145 * s), (x + .05 * s, y - .145 * s), (x + .05 * s, y - .185 * s), (x - .05 * s, y - .185 * s)], L)
    Pg([(x - .065 * s, y - .185 * s), (x + .065 * s, y - .185 * s), (x, y - .22 * s)], L)
def fir(Pg, x, top, w, col=D):
    Pg([(x, top), (x + w * .5, 1.02), (x - w * .5, 1.02)], col)
# A: tower on a knoll upper left, snow slope below, a near fir at the right running out of frame
Pg = panel(0)
Pg([(0, 0), (1, 0), (1, .45), (0, .45)], D); Pg([(0, .3), (1, .3), (1, .45), (0, .45)], M)
Pg([(0, .37), (.2, .34), (.36, .30), (.6, .37), (1, .43), (1, 1), (0, 1)], L)
Pg([(0, .62), (.3, .55), (.62, .66), (1, .6), (1, .74), (.5, .8), (0, .72)], M)
tower(Pg, .36, .305, 1.0)
Pg([(.84, 0), (.9, 0), (.92, 1), (.82, 1)], D)
for y, ln in ((.05, .2), (.16, .28), (.27, .22), (.4, .34), (.52, .26), (.66, .36), (.8, .3)):
    Pg([(.87, y), (.87 - ln, y + .07), (.87 - ln * .6, y + .1), (.87, y + .06)], D); Pg([(.87, y), (.87 + ln * .5, y + .06), (.87, y + .05)], D)
# B: looking up, tower tall and central against a dark sky, firs either side
Pg = panel(1)
Pg([(0, 0), (1, 0), (1, 1), (0, 1)], D); Pg([(0, .45), (1, .45), (1, .8), (0, .8)], M)
Pg([(0, .8), (.3, .74), (.7, .78), (1, .72), (1, 1), (0, 1)], L)
tower(Pg, .55, .76, 3.0)
fir(Pg, .1, .2, .3); fir(Pg, .93, .35, .25)
# C: lookout tiny on a far ridge, snow-laden firs big in front, mist between
Pg = panel(2)
Pg([(0, 0), (1, 0), (1, .3), (0, .3)], D); Pg([(0, .2), (1, .2), (1, .5), (0, .5)], M)
Pg([(0, .34), (.3, .3), (.72, .2), (1, .26), (1, .5), (0, .5)], L)
tower(Pg, .72, .2, .45)
Pg([(0, .5), (1, .5), (1, .66), (0, .66)], M)
for x, t, w in ((.08, .3, .34), (.3, .46, .3), (.55, .38, .36), (.82, .5, .3), (1.0, .34, .3)):
    fir(Pg, x, t, w)
Pg([(0, .88), (1, .84), (1, 1), (0, 1)], L)
_CLIP[0] = None
