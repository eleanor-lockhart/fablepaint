# A complete first picture: dusk sky, sun, hills, a tree. Run with:  ./studio.py run demo examples/hello.py
RESET = dict(tip='round', size=20, hardness=.8, opacity=1, flow=1, spacing=.1, angle=0, roundness=1, follow=False,
             scatter=0, count=1, size_jitter=0, angle_jitter=0, flow_jitter=0, hue_jitter=0, sat_jitter=0,
             val_jitter=0, psize=True, pflow=False, taper=(0, 0), blend='normal', mix=0, grain=0, smooth=True)
def B(**kw):                       # brush settings persist, so always set them from a known state
    brush(**{**RESET, **kw})

use('Background')
gradient('linear', (0, 0), (0, H), [(0, '#1b2a55'), (.6, '#d9785a'), (1, '#f6c98a')])

layer('sun', blend='add')          # light goes on 'add' layers
gradient('radial', (W * .7, H * .62), (W * .7 + 420, H * .62), [(0, '#ffd9a0', 1), (.12, '#ff9a50', .8), (1, '#ff9a50', 0)])

layer('hills')
fill_poly([(0, H * .7), (W * .25, H * .6), (W * .5, H * .68), (W * .8, H * .58), (W, H * .66), (W, H), (0, H)],
          color='#2a2440', smooth=True)
lock(True)                         # alpha lock: shade inside the shape only
B(size=500, hardness=0, flow=.15, psize=False)
stroke([(W * .5, H * .62), (W * .9, H * .6)], color='#7a4a5a')
lock(False)

layer('tree')
B(size=14, taper=(0, .8))
stroke([(W * .22, H * .9), (W * .225, H * .62), (W * .21, H * .5)], color='#120e1a')
B(tip='leaf', size=22, flow=.9, spacing=.5, scatter=1.2, count=4, angle_jitter=1, size_jitter=.4, val_jitter=.2)
stroke([(W * .14, H * .5), (W * .21, H * .42), (W * .29, H * .5)], color='#1c1a2c')

adjust('grade', 'curves', points=[(0, 0), (.3, .26), (.7, .76), (1, 1)])
sample(W * .7, H * .62)
