exec(open('../atelier/transfer/t1/common.py').read())
window(X0, Y0, X1, Y1)
def pxm(s, off=0.0):
    a, b = T(s, off - .5), T(s, off + .5)
    return math.hypot(b[0] - a[0], b[1] - a[1])
def E(s, back=0.0): return T(s, toe_off(s) - back, -.5)          # the foot of the cut, where bank meets ballast

# ---- sword fern, from the ones behind the coyote in refs/coyote_portland.jpg (grid_fern.jpg):
# a frond is a comb, about .3 as wide as long, widest a third of the way up, pinnae at ~65 degrees
# pointing to the tip; the fronds leave a crown in a fan and fall over at the ends.
def frond(base, ang, ln, arch=1.0, cap=26, keep=.92):
    x, y = base; a = math.radians(ang)
    n = max(9, int(ln / 6.5)); step = ln / n
    sgn = -1 if math.cos(a) >= 0 else 1
    spine, tang = [], []
    for i in range(n + 1):
        spine.append((x, y)); tang.append(a)
        x += math.cos(a) * step; y -= math.sin(a) * step
        a += sgn * arch * (.4 + 1.6 * i / n) / n
    out = [ribbon(spine, w=max(1.6, ln * .016), taper=(0, .6), wob=0)]
    pl0 = min(cap, .16 * ln)
    for i in range(1, n):
        u = i / n
        prof = (.5 + .5 * min(u / .28, 1)) * min(1.0, (1 - u) / .5) ** .8
        for side in (-1, 1):
            if rng.uniform() > keep: continue
            pl = pl0 * prof * rng.uniform(.8, 1.12)
            d = tang[i] + side * math.radians(64 + rng.normal(0, 5))
            qx, qy = spine[i]
            tx, ty = math.cos(tang[i]) * step * .42, -math.sin(tang[i]) * step * .42
            out.append(np.array([(qx - tx, qy - ty), (qx + math.cos(d) * pl, qy - math.sin(d) * pl), (qx + tx, qy + ty)]))
    return out
def fern(cx, cy, ln, n=9, lit_share=.3):
    dark, lit = [], []
    for ang in np.linspace(16, 164, n) + rng.normal(0, 7, n):
        f = frond((cx + rng.normal(0, ln * .03), cy + rng.normal(0, ln * .02)), ang, ln * rng.uniform(.6, 1.0), arch=rng.uniform(.7, 1.5))
        (lit if (ang < 100 and rng.uniform() < lit_share * 1.6) else dark).extend(f)
    return dark, lit

def mound(cx, cy, rx, ry, leaf):
    """A salal mound seen from above: a dark body with a lace edge, and a cap of lit leaves on its upper side
    (the sky lights the top; that one lighter plane is what makes it a mound and not a hole)."""
    body = foliage(cx, cy, rx, ry, n=int(rx * ry / leaf ** 2 * .45), leaf=leaf)
    lit = []
    for _ in range(int(rx * ry / leaf ** 2 * 1.5)):
        a = rng.uniform(math.pi, 2 * math.pi); r = rng.uniform() ** .5
        if rng.uniform() < .15 + .85 * (-math.sin(a)) * r:
            lit.append(blob(cx + rx * r * math.cos(a) * .95, cy + ry * r * math.sin(a) * .95 + ry * .12, leaf * rng.uniform(.6, 1.3), leaf * rng.uniform(.4, .8), n=6, rough=.35))
    return body, lit

# ---- trees down the line on our side, in tone steps: the stand behind is paler, the near fir runs out of the top
block('trees_mid')
tr, fo, core = [], [], []
for a, b, hgt, wd in ((.226, .392, 190, 84), (.182, .425, 380, 132), (.118, .47, 455, 170)):
    x, y = U(a, b)
    t_, f_ = conifer(x, y, hgt, wd, crown=.88, lean=rng.normal(0, .008), body=.12)
    tr += t_; fo += f_
    core.append(wobble(np.array([(x - 1.5, y - hgt * .93), (x + wd * .17, y - hgt * .3), (x + wd * .24, y), (x - wd * .24, y), (x - wd * .17, y - hgt * .3)]), 2.2, 16))
marks(tr + fo + core, FIR2)
marks([wobble(Us([(-.02, .34), (.05, .385), (.14, .37), (.215, .366), (.262, .374), (.24, .44), (-.02, .60)]), .8, 24)], FIR2)
block('fir_tall')
x, y = U(.03, .60)
t_, f_ = conifer(x, y, 1260, 360, crown=.9, lean=.004, trunk_w=22, tuft=(8, 22), sag=.12, body=.16)
marks(t_ + f_ + [wobble(np.array([(x - 4, y - 900), (x + 34, y - 300), (x + 50, y), (x - 60, y), (x - 40, y - 300)]), 2.5, 20)], FIR)

# ---- the bank: brown-black, down to the ballast
block('bank')
ss = np.r_[np.arange(8.0, 40, 1.0), np.arange(40, 160, 4.0)]
edge = [E(s) for s in ss]
bank = np.array(edge + [U(.19, .372), U(-.02, .40), U(-.02, 1.03), (edge[0][0], Y1 + 40)])
marks([bank], EARTH)
# the ledge we stand on: its wet top is a lit plane, broken along the bedding
ledge = Us([(-.02, .818), (.055, .80), (.07, .79), (.15, .802), (.165, .818), (.235, .835), (.29, .868), (.30, .89), (.345, .925), (.365, .97), (.39, 1.03), (-.02, 1.03)])
marks([wobble(ledge, 1.0, 34)], EARTH2)
bed_lines = []
for a, b, ln in ((.0, .86, .2), (.12, .845, .16), (.02, .905, .27), (.2, .905, .12), (.05, .955, .2), (.24, .975, .11), (.0, .995, .12)):
    p0, p1 = U(a, b), U(a + ln, b + ln * .2)
    bed_lines.append(ribbon([p0, ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2 + rng.normal(0, 3)), p1], w=rng.uniform(1.6, 3.2), taper=(.2, .5), wob=.25))
marks(bed_lines, EARTH)

# ---- salal on the bank: mounds, bigger and fewer near us, with gaps left between
block('thicket')
body, cap = [], []
spots = [(E(s, .45), r) for s, r in ((10.6, 118), (12.4, 96), (19.6, 70), (22.5, 60), (27.5, 50), (33, 42), (40, 34), (49, 27), (61, 21), (80, 16), (104, 12))]
spots += [(U(a, b), r) for a, b, r in ((.44, .90, 105), (.34, .775, 92), (.19, .715, 96), (.045, .735, 84), (.285, .645, 72), (.12, .60, 70), (.325, .555, 52),
                                       (.215, .515, 54), (.07, .49, 50), (.265, .455, 38), (.16, .43, 36))]
for (x, y), r in spots:
    b_, c_ = mound(x, y - r * .2, r, r * .46, float(np.clip(r * .075, 3.2, 8)))
    body += b_; cap += c_
marks(body, FIR)
marks(cap, '#2c3a37')

# ---- ferns on the ledge and at the foot of the cut; grass where the bank meets the ballast
block('brush')
dk, lt = [], []
for a, b, ln, n in ((.105, .905, 190, 10), (.30, .965, 170, 9), (.245, .822, 150, 9)):
    d_, l_ = fern(*U(a, b), ln, n); dk += d_; lt += l_
for s, ln, n in ((11.5, 150, 9), (18.6, 96, 8), (24.6, 70, 7), (30.5, 52, 7)):
    x, y = E(s, .15)
    d_, l_ = fern(x, y, ln, n); dk += d_; lt += l_
gr, grl = [], []
for s in (13.6, 14.8, 16.0, 17.2, 21.0, 26.0, 29.0, 35.5, 37.5, 44.0, 53.0, 56.0, 68.0):
    x, y = E(s, .05)
    k = pxm(s, TOE)
    tuft = blades(x, y, n=int(rng.integers(5, 10)), length=float(np.clip(.36 * k, 8, 50)), spread=58, w=float(np.clip(.02 * k, 1.1, 2.6)), lean=rng.normal(8, 8))
    (grl if rng.uniform() < .3 else gr).extend(tuft)
marks(dk + gr, FIR)
marks(lt + grl, MOSS)
print('edge at s=10,15,25,40:', [[round(v) for v in E(s)] for s in (10, 15, 25, 40)])
