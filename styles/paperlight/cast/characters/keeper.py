"""The Keeper. Keeps the light on the headland. Sixty-odd, thick-set, a short coat, a flat cap, a beard,
heavy boots. He walks as if the ground might be wet: short stride, feet barely lifted, leaning into it,
hands doing very little. Everything here is numbers on the common rig (backlot.figure)."""
import sys, math
from pathlib import Path
import numpy as np
from backlot import core, draw, anim, screen, figure as fg

HEAD = [(-.045, -.022), (-.056, .030), (-.060, .058), (-.040, .084), (-.004, .094), (.034, .084), (.050, .066), (.074, .060), (.074, .053), (.050, .050),
        (.048, .040), (.052, .032), (.075, .010), (.054, .003), (.058, -.006), (.066, -.022), (.060, -.052), (.036, -.068), (.010, -.052), (-.012, -.036), (-.035, -.026)]
        # a round flat cap with a short peak, a nose, a beard that juts
COAT = [(0.0, -.060), (.10, -.058), (.20, -.066), (.28, -.058), (.33, -.030), (.33, .030), (.285, .070), (.17, .080), (.08, .076), (0.0, .072),
        (-.10, .076), (-.135, .062), (-.135, -.056), (-.08, -.066)]                                                 # trunk and coat skirt in one piece

def extras(fig, J, pose):
    """Coat hem that swings a little behind the legs, and a collar."""
    sw = .012 * math.sin(math.radians(pose.get('hipN', 0) - pose.get('hipF', 0)) / 2)
    hem = fig.on_trunk(J, [(.02, .074), (-.06, .078), (-.150, .066 + sw), (-.150, -.060 + sw), (-.06, -.068), (.02, -.060)])
    collar = fig.on_trunk(J, [(.300, -.040), (.345, -.030), (.352, .034), (.300, .052)])
    return [('hem', hem, 2), ('collar', collar, 0)]

def make():
    fig = fg.Figure(build=dict(hip=.058, knee=.040, calf=.043, ankle=.029, chest=.072, shoulder=.036, elbow=.030, wrist=.022, neck=.031, head=1.18),
                    seg=dict(thigh=.236, shank=.236, hand=.100, foot_fwd=.118, foot_back=.050), head_profile=HEAD, trunk_profile=COAT, extras=extras)
    walk = fg.Walk(fig, stride=.64, stance=.66, strike_pitch=12, toeoff_pitch=-30, lift=.034, lean=9.0, arm=.45, elbow=18.0,
                   stance_knee=((0, 8), (.14, 20), (.40, 10), (.50, 12)))
    return fig, walk

if __name__ == '__main__':
    HERE = Path(__file__).resolve().parent
    fig, walk = make()
    print({k: round(v, 3) for k, v in fg.gait_report(fig, walk.pose).items()})
    W, H, S, OY = 320, 470, 400, 440
    def cell(pose, joints=False):
        img = core.canvas(W, H, '#e9e2cf'); img = draw.paint(img, draw.rect(W, H, 0, OY + 3, W, H), '#b9b29c')
        return fg.draw_figure(img, fig, pose, S, (150, OY), colours=('#4a4f58', '#20242a', '#20242a'), joints=joints)
    stand = dict(shN=-4, shF=6, elN=14, elF=18, lean=5)
    cells = [cell(stand, True), cell(walk.pose(0.0)), cell(walk.pose(.10)), cell(walk.pose(.30)), cell(walk.pose(.42))]
    screen.sheet(cells, str(HERE / 'keeper_sheet.jpg'), ['The Keeper: standing, joints shown', 'walk: contact', 'down', 'passing', 'up'], cols=5, cell_w=250)
    # the walk on moving ground: marks pass under him at the speed his stride implies, so a sliding foot would show
    N, WW = 14, 560
    def frame(i):
        g = i / N
        img = core.canvas(WW, H, '#e9e2cf'); img = draw.paint(img, draw.rect(WW, H, 0, OY + 3, WW, H), '#b9b29c')
        step = walk.stride * S / 4
        for k in range(-2, 12):
            x = (k * step - (g * walk.stride * S)) % (step * 10) - step
            img = draw.paint(img, draw.rect(WW, H, x, OY + 3, x + 3, OY + 14), '#8f8874')
        return fg.draw_figure(img, fig, walk.pose(g), S, (WW / 2 - 20, OY), colours=('#4a4f58', '#20242a', '#20242a'))
    pat = anim.render(frame, N, 'out/cast/keeper/frames', workers=6)
    anim.encode(pat, str(HERE / 'keeper_walk.mp4'), fps=12, loops=4, crf=20)
