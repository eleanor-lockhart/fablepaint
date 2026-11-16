"""Study 2: the same mannequin, feet planted. The stance foot is fixed to the ground and rolls heel, flat,
ball; the pelvis rides over it; legs are solved from the feet by inverse kinematics."""
import json
import numpy as np
from backlot import core, draw, comp, anim, screen, figure as fg

OUT = 'out/cast/s02'
fig = fg.Figure()
wk = fg.Walk(fig)
cycle = wk.pose
rep = fg.gait_report(fig, cycle)
print(json.dumps({k: round(v, 4) for k, v in rep.items()}))

W, H, S, OX, OY = 300, 470, 400, 140, 440
def cell(g, joints=True):
    img = core.canvas(W, H, '#e9e2cf')
    img = draw.paint(img, draw.rect(W, H, 0, OY + 3, W, H), '#b9b29c')
    return fg.draw_figure(img, fig, cycle(g), S, (OX, OY), joints=joints)

N = 12                                                     # poses per stride: a one-second stride shot on twos
screen.sheet([cell(i / N) for i in range(N)], 'styles/paperlight/cast/studies/s02_planted_walk.jpg', [f'pose {i}  phase {i / N:.2f}' for i in range(N)], cols=6, cell_w=210)
pat = anim.render(lambda i: cell((i % N) / N, joints=False), N, OUT + '/frames', workers=6)
anim.encode(pat, 'styles/paperlight/cast/studies/s02_planted_walk.mp4', fps=12, loops=4, crf=20)
core.save(OUT + '/arcs.png', fg.arcs(fig, cycle, 420, (160, 450), 640, 480, travel=rep['stride']))
