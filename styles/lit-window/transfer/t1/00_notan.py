# Transfer print 1, notan: "Red board, rain". Three variants in three flat greys.
# Sentence: deep dusk, steady rain on the shore line; a block signal holds red over empty track,
# its light lying on the wet rails; a coyote has stopped to look.
exec(open('../atelier/kit.py').read())
D, M, L = '#262626', '#7f7f7f', '#e8e8e8'
layer('n'); fill('#ffffff')
def panel(i):
    ox, oy, w, h = 20 + 325 * i, 20, 305, 450
    window(ox, oy, ox + w, oy + h)
    def Pg(pts, col): marks([np.array([(ox + a * w, oy + b * h) for a, b in pts])], col)
    def Ln(a, b, wd, col): marks([seg((ox + a[0] * w, oy + a[1] * h), (ox + b[0] * w, oy + b[1] * h), w=wd, wob=0)], col)
    return Pg, Ln
def signal(Pg, x, y, s):                   # foot of mast at (x, y), s = height of mast
    Pg([(x - .006, y), (x + .006, y), (x + .006, y - s), (x - .006, y - s)], D)
    r = .14 * s
    Pg([(x + r * math.cos(a) * 1.0, y - s - r * .2 + r * math.sin(a) * .68) for a in np.linspace(0, 6.283, 14)], D)
    Pg([(x - .008, y - s - r * .2 - .006), (x + .008, y - s - r * .2 - .006), (x + .008, y - s - r * .2 + .006), (x - .008, y - s - r * .2 + .006)], L)
    Pg([(x + .02, y), (x + .06, y), (x + .06, y - .2 * s), (x + .02, y - .2 * s)], D)        # relay case
def coyote(Pg, x, y, s, col=D):            # feet at (x, y), s = body length; faces right
    Pg([(x - .5 * s, y - .5 * s), (x + .35 * s, y - .55 * s), (x + .52 * s, y - .78 * s), (x + .62 * s, y - .62 * s), (x + .4 * s, y - .32 * s), (x - .4 * s, y - .28 * s)], col)
    for dx in (-.38, -.3, .28, .36):
        Pg([(x + dx * s - .03 * s, y - .35 * s), (x + dx * s + .03 * s, y - .35 * s), (x + dx * s + .02 * s, y), (x + dx * s - .02 * s, y)], col)
    Pg([(x - .5 * s, y - .5 * s), (x - .7 * s, y - .2 * s), (x - .62 * s, y - .15 * s), (x - .42 * s, y - .42 * s)], col)
def firs(Pg, pts, col=D):                  # a ragged skyline of spires: (x, top, base, halfwidth)
    for x, t, b, hw in pts:
        Pg([(x, t), (x + hw, b), (x - hw, b)], col)

# ---- A: standing in the track, low eye. The rails rush at you; signal and coyote ahead; bluff at left.
Pg, Ln = panel(0)
Pg([(0, 0), (1, 0), (1, .16), (0, .16)], D); Pg([(0, .16), (1, .16), (1, .32), (0, .32)], M); Pg([(0, .32), (1, .32), (1, .47), (0, .47)], L)
Pg([(.45, .37), (.7, .355), (1, .365), (1, .385), (.6, .39)], M)                          # one cloud sliver
Pg([(.36, .445), (.6, .44), (1, .45), (1, .47), (.36, .47)], M)                           # far shore
Pg([(.37, .47), (1, .47), (1, .52)], L); Pg([(.37, .47), (1, .52), (1, .585)], M)         # water wedge
Pg([(0, 0), (.2, 0), (.24, .12), (.29, .24), (.33, .37), (.375, .47), (0, .47)], D)       # bluff
firs(Pg, [(.25, .02, .2, .05), (.3, .14, .3, .04), (.34, .26, .4, .03)])
Pg([(0, .47), (.375, .47), (1, .585), (1, 1), (0, 1)], D)                                 # trackbed
for y_ in (.62, .70, .80, .93):                                                           # near ties catching the sky
    xa = .37 - (.37 - .16) * (y_ - .47) / .53; xb = .37 + (1.0 - .37) * (y_ - .47) / .36
    Pg([(xa - .03, y_), (min(xb, 1) + .03, y_), (min(xb, 1) + .03, y_ + .028 * (y_ - .4) * 4), (xa - .04, y_ + .028 * (y_ - .4) * 4)], M)
Ln((.372, .47), (.16, 1.0), 2.2, L); Ln((.378, .47), (1.0, .83), 2.2, L)                  # the rails, lit
signal(Pg, .56, .525, .22)
coyote(Pg, .80, .575, .13)

# ---- B: from the bluff, high eye. The track is a diagonal along the shore; water is the pool of light.
Pg, Ln = panel(1)
Pg([(0, 0), (1, 0), (1, .07), (0, .07)], D); Pg([(0, .07), (1, .07), (1, .15), (0, .15)], M); Pg([(0, .15), (1, .15), (1, .235), (0, .235)], L)
Pg([(.3, .215), (.46, .195), (.63, .205), (.82, .19), (1, .2), (1, .235), (.3, .235)], M)   # far islands
Pg([(.26, .235), (1, .235), (1, .50), (.607, .50)], L)                                      # far water
Pg([(.607, .50), (1, .50), (1, .80)], M)                                                    # near water
Pg([(.235, .235), (.265, .235), (1, .80), (1, 1), (.50, 1)], M)                             # trackbed
Pg([(0, .09), (.07, .12), (.14, .17), (.21, .21), (.265, .232), (.235, .24), (.50, 1), (0, 1)], D)   # headland and near slope
firs(Pg, [(.05, .03, .14, .03), (.11, .08, .18, .028), (.17, .13, .21, .022), (.215, .17, .23, .016)])
Pg([(0, 0), (.065, 0), (.085, 1), (0, 1)], D)                                               # near fir trunk at the frame edge
for y_, ln in ((.02, .30), (.12, .22), (.30, .26), (.48, .18)):
    Pg([(.07, y_), (.07 + ln, y_ + .075), (.07 + ln * .6, y_ + .11), (.07, y_ + .07)], D)
Pg([(0, .86), (.3, .83), (.52, .9), (.74, .955), (1, .975), (1, 1), (0, 1)], D)             # brush along the bottom
Ln((.37, .41), (.72, .93), 1.8, L); Ln((.40, .405), (.86, .93), 1.8, L)                     # rails, lit below the signal
signal(Pg, .50, .43, .15)
coyote(Pg, .70, .70, .11)

# ---- C: from the beach, below the grade. Embankment and bluff at left, driftwood across the bottom.
Pg, Ln = panel(2)
Pg([(0, 0), (1, 0), (1, .14), (0, .14)], D); Pg([(0, .14), (1, .14), (1, .30), (0, .30)], M); Pg([(0, .30), (1, .30), (1, .46), (0, .46)], L)
Pg([(.5, .36), (.8, .345), (1, .355), (1, .375), (.66, .38)], M)
Pg([(.40, .435), (.7, .43), (1, .44), (1, .46), (.40, .46)], M)                             # far shore
Pg([(.40, .46), (1, .46), (1, .57)], L)                                                     # water
Pg([(.40, .46), (1, .57), (1, 1), (0, 1), (0, .80)], M)                                     # wet beach
Pg([(0, 0), (.12, 0), (.18, .1), (.24, .22), (.31, .36), (.40, .455), (0, .26)], D)         # bluff behind the grade
firs(Pg, [(.15, .01, .15, .04), (.21, .1, .26, .035), (.28, .22, .36, .03)])
Pg([(0, .26), (.40, .455), (.40, .465), (0, .82)], D)                                       # embankment face
Pg([(0, .86), (.22, .80), (.5, .81), (.8, .86), (1, .9), (1, 1), (0, 1)], D)                # driftwood log
Pg([(.12, .82), (.1, .68), (.16, .7), (.2, .6), (.24, .72), (.3, .66), (.3, .81)], D)       # its root wad
signal(Pg, .19, .352, .24)
coyote(Pg, .30, .405, .075)
_CLIP[0] = None
