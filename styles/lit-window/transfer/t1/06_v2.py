# v2: the one revision pass, after measuring v1.
#   v1 measured: dark 45 / mid 39 / light 16; chroma 4.8; warm 0.4%; cool 1%; detail 7.8%.
# Critique of v1 against the rules, worst first:
#   1. Rule 6. Chroma 4.8 is under the 6-15 range and the cool share is 1%: I greyed every pigment and lost the
#      hue family. The notan is right; the colour is a grey photograph. Push one blue through sky, water, ballast.
#   2. Faults list, "marks spread evenly become wallpaper": the salal mounds are polka dots on a brown wall.
#      Gather them into three drifts and leave the rest of the bank empty; wipe the far end of the bank paler.
#   3. Rule 5. Sixty rain lines, the pale ones running the whole height of the dark bank, read as scratches.
#      About half as many, shorter, and the pale ones kept to the upper half.
#   4. Rule 4. The coyote's ears touch the rail web. Move it onto open ballast with clear space all round.
# Left alone on purpose: the track, the signal, the red on the rails, the sky bands. They read; stop.
exec(open('../styles/lit-window/transfer/t1/common.py').read())
exec(open('../styles/lit-window/transfer/t1/coyote.py').read())
src = open('../styles/lit-window/transfer/t1/04_bank.py').read()
exec(src[src.index('def pxm'):src.index('# ---- trees down the line')])         # pxm, E, frond, fern, mound
window(X0, Y0, X1, Y1)

# ---- 1. one hue family: the same blocks reprinted in a bluer pigment, same values
use('sky'); clear(); select_rect(X0 - 4, Y0 - 4, X1 + 4, HZ + 6)
gradient('linear', (0, Y0), (0, HZ), ramp('#101c2a', ('#243f55', .16), ('#527488', .40), ('#93a8ad', .60), (PALE, .84), PALE))
woodgrain(.02, 'v', seed=2); select_none()
use('water'); clear(); select_rect(X0 - 4, HZ, X1 + 4, U(0, .70)[1])
gradient('linear', (0, HZ), (0, U(0, .66)[1]), ramp('#bfc6b9', ('#a6b7b6', .22), ('#8ea5ab', .42), ('#5f8194', .64), ('#3a5a72', .84), '#234058'))
woodgrain(.018, 'h', seed=4); select_none()
use('bed'); lock(True); gradient('linear', T(110), T(11), ramp('#84939a', ('#65737b', .45), '#505a61')); lock(False)

# ---- 2. the bank: far end wiped paler and bluer (a tone step), salal in three drifts, the rest left empty
use('bank'); bokashi('#2b3b45', U(0, .37), U(0, .68), .9, power=1.5)
use('thicket'); clear()
body, cap = [], []
spots = []
for s in (18.4, 19.5, 20.6, 22.2, 23.4, 25.2, 26.5, 28.6, 30.4, 32.8, 35.5):          # a hedge along the foot of the cut
    spots.append((E(s, .5 + rng.uniform(0, .5)), float(np.clip(.6 * pxm(s, TOE) * rng.uniform(.75, 1.2), 14, 74))))
for s, r in ((44, 30), (52, 25), (63, 20), (79, 15), (102, 11)):                      # and its far end, small
    spots.append((E(s, .45), r))
spots += [(U(a, b), r) for a, b, r in ((.07, .60, 95), (.17, .635, 122), (.27, .60, 84), (.12, .70, 112), (.24, .69, 90), (.03, .68, 80),     # a drift on the mid bank
                                       (.43, .875, 120), (.50, .94, 108), (.37, .80, 94), (.46, .80, 68))]                                 # a drift beside the ledge
for (x, y), r in spots:
    b_, c_ = mound(x, y - r * .2, r, r * .46, float(np.clip(r * .075, 3.2, 8)))
    body += b_; cap += c_
marks(body, FIR)
marks(cap, '#27423d')
use('brush'); clear()
dk, lt = [], []
for a, b, ln, n in ((.105, .905, 190, 10), (.30, .965, 170, 9), (.245, .822, 150, 9)):
    d_, l_ = fern(*U(a, b), ln, n); dk += d_; lt += l_
for s, ln, n in ((11.4, 150, 9), (12.7, 118, 8), (21.4, 80, 8), (27.4, 60, 7), (33.6, 46, 7)):
    x, y = E(s, .15)
    d_, l_ = fern(x, y, ln, n); dk += d_; lt += l_
gr, grl = [], []
for s in (20.0, 24.3, 29.4, 31.2, 37.5, 41.0, 46.5, 55.0, 60.0, 70.0):             # no grass near where the coyote stands
    x, y = E(s, .05)
    k = pxm(s, TOE)
    tuft = blades(x, y, n=int(rng.integers(5, 10)), length=float(np.clip(.36 * k, 8, 50)), spread=58, w=float(np.clip(.02 * k, 1.1, 2.6)), lean=rng.normal(8, 8))
    (grl if rng.uniform() < .3 else gr).extend(tuft)
marks(dk + gr, FIR)
marks(lt + grl, '#38584f')

# ---- 4. the coyote, clear of the rail and clear of the brush
use('coyote'); clear()
cs, co = 15.7, -2.3
fx, fy = T(cs, co, -.15)
k = (T(cs, co, 0)[1] - T(cs, co, .6)[1]) / 592.0
coyote(fx, fy, k, '#1f1c1a', rim=RED2)
print('coyote feet', round(fx), round(fy), 'x', round(fx - 228 * k), 'to', round(fx + 310 * k), 'ears y', round(fy - 792 * k),
      '| rail web at ears:', [round(v) for v in T(cs + 1.2, -GAUGE - .09)], '| bank edge:', [round(v) for v in E(cs)], [round(v) for v in E(cs + 1.5)])

# ---- 3. rain at half: dark hairlines where the picture is light, a few pale ones high up where it is dark
use('rain_dark'); clear(); use('rain_pale'); clear()
dk, pl = [], []
for cx in (470, 700, 930, 1130):
    dk += rain(cx - 100, U(0, .12)[1], cx + 100, Y1, n=4, angle=101, w=1.0, length=(.2, .5), spread=1.0)
for cx in (170, 520, 900):
    pl += rain(cx - 140, Y0, cx + 140, U(0, .5)[1], n=4, angle=101, w=.9, length=(.3, .8), spread=1.0)
use('rain_dark'); marks(dk, '#0b1016', opacity=.5)
use('rain_pale'); marks(pl, '#9fb0b3', opacity=.24)
