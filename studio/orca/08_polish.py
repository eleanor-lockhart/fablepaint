exec(open('orca/common.py').read())
# the flipper's rim light made it a tyre: drop it, leave one soft sheen
delete('flipper_rim'); delete('flip_gloss')
use('flipper')
lock(True)
B(size=80, hardness=0, flow=.10, psize=False)
stroke([(1250, 790), (1320, 860), (1350, 940)], color='#56648c')
lock(False)
# the foam under the breach was one flat disc: break it open and lay real froth over it
use('splash')
B(tip='stipple', size=120, flow=.9, spacing=.3, angle_jitter=1, scatter=.5, size_jitter=.4, roundness=.45, psize=False, blend='erase')
for y_ in (1300, 1332, 1366):
    stroke([(130, y_), (440, y_ + 10), (760, y_)], color='#000000')
B(tip='stipple', size=70, flow=.8, spacing=.25, angle_jitter=1, scatter=.5, size_jitter=.5, roundness=.4, psize=False)
for y_, w_ in ((1296, 250), (1322, 310), (1352, 340), (1384, 300)):
    stroke([(440 - w_, y_), (440, y_ + 8), (440 + w_, y_)], color='#e4ecff')
