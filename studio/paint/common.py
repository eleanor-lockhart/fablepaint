# shared by every batch of the aurora painting
BASE = dict(tip='round', size=20, hardness=.8, opacity=1, flow=1, spacing=.1, angle=0, roundness=1, follow=False,
            scatter=0, count=1, size_jitter=0, angle_jitter=0, flow_jitter=0, hue_jitter=0, sat_jitter=0,
            val_jitter=0, psize=True, pflow=False, taper=(0, 0), blend='normal', mix=0, grain=0, smooth=True)
def B(**kw):
    brush(**{**BASE, **kw})
HORIZON = 900
LAKE = [(0, 905), (1880, 905), (1930, 930), (1960, 980), (1900, 1050), (1700, 1130), (1300, 1195), (700, 1180), (0, 1140)]
LAND = [(1880, 905), (2600, 905), (2600, 1480), (-40, 1480), (-40, 1140), (0, 1140), (700, 1180), (1300, 1195), (1700, 1130),
        (1900, 1050), (1960, 980), (1930, 930)]
FULL = [(0, 0), (2560, 0), (2560, 1440), (0, 1440)]
GROUND = [(2560 * .25, 905), (2560 * .75, 905), (2560 * 1.9, 1330), (-2560 * .9, 1330)]   # full-canvas texture laid on the ground plane
