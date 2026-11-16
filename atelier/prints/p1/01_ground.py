exec(open('../atelier/prints/p1/common.py').read())
window(X0, Y0, X1, Y1)
layer('paper'); fill(PAPER)
# ---- sky: one gradation, darkest at the top
block('sky'); select_rect(X0 - 4, Y0 - 4, X1 + 4, HZ + 6)
gradient('linear', (0, Y0), (0, HZ), ramp(PAL['night'], ('#1d2c3b', .45), ('#3c5160', .8), PAL['mid']))
woodgrain(.025, 'v', seed=2); select_none()
# stepped cloud bands low in the sky, and the last light under them
block('clouds')
marks([cloudband(X0 + 330, HZ - 150, 620, 30), cloudband(X0 + 640, HZ - 108, 560, 24), cloudband(X0 + 250, HZ - 86, 420, 16)], '#22313f')
block('sliver')
marks([cloudband(X0 + 380, HZ - 44, 800, 26, ragged=.3), cloudband(X0 + 300, HZ - 18, 520, 12, ragged=.3)], PAL['pale'])
marks([cloudband(X0 + 520, HZ - 62, 560, 9, ragged=.3)], '#7f9193')
# ---- water: light at the far edge, dark at our feet
block('water'); select_rect(X0 - 4, HZ, X1 + 4, Y1 + 4)
gradient('linear', (0, HZ), (0, Y1), ramp('#8b9a98', ('#5d717b', .10), ('#3a4f5f', .34), ('#22323f', .62), PAL['night']))
woodgrain(.02, 'h', seed=4); select_none()
# ---- far shore: a low dark line with a few house lights
block('shore')
xs = np.arange(X0 - 10, X1 + 30, 22.0)
ridge = [(x, HZ - 9 - 13 * max(0, math.sin((x - 300) / 210.0)) - 5 * math.sin(x / 47.0) - rng.uniform(0, 4)) for x in xs]
marks([np.array([(X0 - 10, HZ + 2)] + ridge + [(X1 + 30, HZ + 2)])], '#1b2228')
tr, fo = [], []
for x in np.arange(X0 + 420, X1, 9.0):
    if rng.uniform() < .55:
        t_, f_ = conifer(x, HZ - 6, rng.uniform(12, 30), rng.uniform(7, 12), crown=.9)
        tr += t_; fo += f_
marks(tr + fo, '#1b2228')
block('shorelights')
pts = [(X0 + 462, HZ - 5), (X0 + 498, HZ - 7), (X0 + 1008, HZ - 6), (X0 + 1040, HZ - 9), (X0 + 1090, HZ - 5)]
marks([np.array([(x, y), (x + 3, y), (x + 3, y + 2.6), (x, y + 2.6)]) for x, y in pts], PAL['lamp2'])
marks(sum([ticks(x + 1.5, HZ + 5, HZ + 26, 4, th=1.4, gap=.5) for x, y in pts], []), PAL['lamp2'], opacity=.8)
