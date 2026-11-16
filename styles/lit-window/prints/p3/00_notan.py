# Print 3, notan: the assigned subject (orca, giant machine, full moon, battle) in three values.
exec(open('../styles/lit-window/kit.py').read())
D, M, L = '#262626', '#7f7f7f', '#e8e8e8'
layer('n'); fill('#ffffff')
def panel(i):
    ox, oy, w, h = 20 + 325 * i, 20, 305, 450
    window(ox, oy, ox + w, oy + h)
    def Pg(pts, col): marks([np.array([(ox + a * w, oy + b * h) for a, b in pts])], col)
    def road(xc, y0_, y1_, wd, g): marks(ticks(ox + xc * w, oy + y0_ * h, oy + y1_ * h, wd * w, grow=g, th=3.0, gap=.5), L)
    def moon(x, y, r): marks([blob(ox + x * w, oy + y * h, r * w, r * w, n=20, rough=.02)], L)
    return Pg, road, moon
def orca(Pg, x, y, s, k=1):          # leaping up and to the left (k=1) from (x, y)
    Pg([(x, y), (x - .05 * s * k, y - .12 * s), (x - .2 * s * k, y - .27 * s), (x - .3 * s * k, y - .3 * s), (x - .33 * s * k, y - .27 * s), (x - .2 * s * k, y - .12 * s), (x - .08 * s * k, y + .0 * s)], D)
    Pg([(x - .08 * s * k, y), (x - .2 * s * k, y - .12 * s), (x - .33 * s * k, y - .27 * s), (x - .3 * s * k, y - .22 * s), (x - .16 * s * k, y - .06 * s)], L)
# A: the machine whole, to its knees in the water at left; orca in the moon road
Pg, road, moon = panel(0)
Pg([(0, 0), (1, 0), (1, .34), (0, .34)], D); Pg([(0, .2), (1, .2), (1, .34), (0, .34)], M); Pg([(0, .34), (1, .34), (1, .78), (0, .78)], M); Pg([(0, .78), (1, .78), (1, 1), (0, 1)], D)
moon(.64, .14, .06); road(.64, .35, .98, .12, 4.0)
Pg([(.06, .8), (.08, .62), (.1, .5), (.0, .42), (.0, .36), (.03, .2), (.06, .2), (.08, .34), (.12, .3), (.16, .26), (.24, .25), (.28, .31), (.3, .2), (.33, .2), (.36, .36), (.36, .44), (.26, .5), (.28, .62), (.3, .8), (.22, .8), (.2, .64), (.16, .64), (.14, .8)], D)
orca(Pg, .62, .8, .7)
# B: only a leg and a hanging hand, cut by the frame; orca large, leaping at the hand, moon behind it
Pg, road, moon = panel(1)
Pg([(0, 0), (1, 0), (1, .3), (0, .3)], D); Pg([(0, .16), (1, .16), (1, .3), (0, .3)], M); Pg([(0, .3), (1, .3), (1, .8), (0, .8)], M); Pg([(0, .8), (1, .8), (1, 1), (0, 1)], D)
moon(.66, .2, .1); road(.66, .31, .98, .2, 3.0)
Pg([(0, 0), (.3, 0), (.34, .3), (.3, .62), (.36, .7), (.34, 1), (.06, 1), (.1, .7), (.04, .5), (0, .4)], D)
Pg([(.36, 0), (.46, 0), (.47, .2), (.5, .3), (.48, .42), (.45, .3), (.43, .4), (.4, .28), (.38, .2)], D)
orca(Pg, .8, .86, 1.5)
# C: the machine far off and small against the moon; the orca is the big foreground thing
Pg, road, moon = panel(2)
Pg([(0, 0), (1, 0), (1, .3), (0, .3)], D); Pg([(0, .14), (1, .14), (1, .3), (0, .3)], M); Pg([(0, .3), (1, .3), (1, .7), (0, .7)], M); Pg([(0, .7), (1, .7), (1, 1), (0, 1)], D)
moon(.4, .17, .12); road(.4, .31, .98, .24, 2.6)
Pg([(.36, .3), (.37, .2), (.34, .18), (.34, .13), (.36, .15), (.39, .12), (.42, .12), (.45, .15), (.47, .13), (.47, .18), (.44, .2), (.45, .3)], D)
orca(Pg, .2, .98, 2.4, k=-1)
_CLIP[0] = None
