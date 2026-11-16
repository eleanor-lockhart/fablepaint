"""The cast of NIGHT SERVICE as paper figures on the common rig (backlot.figure).
Each character is: a build, a head cut in profile, a trunk (coat), costume and props, a height, a standing
pose, and the colour of the window in the chest. cast() returns them all by name."""
import sys, math
from pathlib import Path
import numpy as np
from backlot import figure as fg
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'styles/paperlight/cast/characters'))
import keeper as _keeper

def rect(c, w, h):
    return np.array([(c[0] - w / 2, c[1] + h / 2), (c[0] + w / 2, c[1] + h / 2), (c[0] + w / 2, c[1] - h / 2), (c[0] - w / 2, c[1] - h / 2)])

# ---------------------------------------------------------------- Marisol, the Lookout
MARISOL_HEAD = [(-.034, -.028), (-.048, .000), (-.070, .026), (-.092, .052), (-.096, .086), (-.076, .114), (-.044, .120), (-.020, .106), (-.002, .098), (.036, .084),
                (.048, .058), (.046, .044), (.062, .024), (.050, .014), (.054, .002), (.050, -.010), (.044, -.030), (.020, -.040), (-.010, -.030)]
PARKA = [(0, -.052), (.10, -.054), (.20, -.062), (.28, -.060), (.325, -.050), (.345, -.030), (.33, .022), (.275, .058), (.17, .062), (.08, .056), (0, .052),
         (-.045, .048), (-.058, 0), (-.045, -.048)]
def marisol_extras(fig, J, pose):
    return [('binoculars', fig.on_head(J, [(.046, .062), (.112, .068), (.116, .034), (.050, .028)]), 3)]

# ---------------------------------------------------------------- Dee, the Deckhand
DEE_HEAD = [(-.034, -.028), (-.050, .000), (-.058, .040), (-.050, .082), (-.020, .104), (.016, .100), (.044, .078), (.056, .056), (.047, .050), (.046, .040),
            (.064, .021), (.050, .012), (.055, .001), (.049, -.011), (.046, -.031), (.022, -.041), (-.008, -.030)]
def dee_extras(fig, J, pose):
    hi = '#c9cf98'
    out = [('stripe1', fig.on_trunk(J, [(.165, -.054), (.165, .063), (.148, .063), (.148, -.054)]), 0, hi),
           ('stripe2', fig.on_trunk(J, [(.085, -.050), (.085, .056), (.068, .056), (.068, -.050)]), 0, hi),
           ('cigarette', fig.on_head(J, [(.054, -.001), (.094, -.010), (.094, -.017), (.054, -.008)]), 3, '#d8d4c4'),
           ('lit_ember', fig.on_head(J, [(.092, -.006), (.104, -.008), (.104, -.019), (.092, -.019)]), 3, '#ff7a2a')]
    return out

# ---------------------------------------------------------------- Red, the Signal Maintainer
RED_HEAD = [(-.034, -.028), (-.050, .000), (-.052, .040), (-.080, .046), (-.078, .055), (-.056, .060), (-.046, .092), (-.010, .110), (.030, .100), (.052, .066),
            (.090, .058), (.090, .049), (.050, .046), (.066, .022), (.051, .012), (.054, .000), (.049, -.012), (.047, -.032), (.022, -.041), (-.008, -.030)]
RAINCOAT = [(0, -.056), (.10, -.054), (.20, -.062), (.28, -.056), (.33, -.028), (.33, .026), (.28, .062), (.17, .066), (.08, .062), (0, .060), (-.12, .066),
            (-.225, .072), (-.225, -.066), (-.10, -.060)]
def red_extras(fig, J, pose):
    h = J['handN']
    return [('hem', fig.on_trunk(J, [(.02, .062), (-.225, .074), (-.225, -.068), (.02, -.058)]), 2),
            ('lantern_bail', rect((h[0], h[1] - .020), .006, .040), 3),
            ('lantern', np.array([(h[0] - .020, h[1] - .036), (h[0] + .020, h[1] - .036), (h[0] + .026, h[1] - .046), (h[0] + .024, h[1] - .104), (h[0] - .024, h[1] - .104), (h[0] - .026, h[1] - .046)]), 3),
            ('lit_lantern', rect((h[0], h[1] - .074), .028, .040), 3, '#ff3b24')]

# ---------------------------------------------------------------- Vesper Lang, Director of Continuity
LANG_HEAD = [(-.028, -.032), (-.060, -.030), (-.066, .030), (-.054, .078), (-.016, .101), (.028, .095), (.051, .068), (.054, .046), (.046, .040), (.069, .022),
             (.050, .012), (.053, .001), (.048, -.011), (.048, -.034), (.024, -.042), (.004, -.034)]
LONGCOAT = [(0, -.048), (.10, -.046), (.20, -.054), (.28, -.050), (.33, -.026), (.33, .024), (.28, .054), (.17, .056), (.08, .050), (0, .050), (-.16, .058),
            (-.31, .066), (-.31, -.060), (-.14, -.054)]
def lang_extras(fig, J, pose):
    h = J['handN']
    return [('hem', fig.on_trunk(J, [(.02, .050), (-.31, .068), (-.31, -.062), (.02, -.050)]), 2),
            ('sash', fig.on_trunk(J, [(.315, -.030), (.315, -.008), (.060, .054), (.035, .050)]), 0, '#c9cf98'),
            ('tablet', np.array([(h[0] - .012, h[1] + .064), (h[0] + .040, h[1] + .050), (h[0] + .024, h[1] - .030), (h[0] - .028, h[1] - .016)]), 3),
            ('lit_tablet', np.array([(h[0] - .006, h[1] + .054), (h[0] + .033, h[1] + .044), (h[0] + .020, h[1] - .020), (h[0] - .019, h[1] - .010)]), 3, '#dbeeff')]

# ---------------------------------------------------------------- a Passenger
HAT_HEAD = [(-.034, -.028), (-.050, .000), (-.052, .044), (-.086, .050), (-.086, .058), (-.050, .062), (-.044, .106), (.030, .106), (.040, .062), (.092, .058),
            (.092, .050), (.050, .046), (.066, .022), (.051, .012), (.054, .000), (.049, -.012), (.047, -.032), (.022, -.041), (-.008, -.030)]
def passenger_extras(fig, J, pose):
    h = J['handF']
    return [('case_handle', rect((h[0], h[1] - .012), .030, .010), -1), ('suitcase', rect((h[0], h[1] - .075), .150, .110), -1)]

def cast():
    """name -> dict(fig, pose, height, window, colours, title, role)"""
    kf, _ = _keeper.make()
    C = {}
    C['keeper'] = dict(fig=kf, height=.95, window='#ffb347', title='ORRIN', role='the Keeper',
                       pose=dict(lean=8, shN=-22, elN=34, shF=-16, elF=30, hipN=3, hipF=-4, kneeN=6, kneeF=4))
    C['red'] = dict(fig=fg.Figure(build=dict(hip=.052, chest=.060, shoulder=.028, ankle=.024, head=1.08), head_profile=RED_HEAD, trunk_profile=RAINCOAT, extras=red_extras),
                    height=.99, window='#ff5a3c', title='RED', role='the Signal Maintainer',
                    pose=dict(lean=1, shN=14, elN=10, shF=-6, elF=10, hipN=2, hipF=-3))
    C['dee'] = dict(fig=fg.Figure(build=dict(hip=.055, knee=.035, calf=.037, ankle=.025, chest=.064, shoulder=.030, elbow=.024, wrist=.017, head=1.12), head_profile=DEE_HEAD, extras=dee_extras),
                    height=.92, window='#ff9a3c', title='DEE', role='the Deckhand',
                    pose=dict(lean=-3, head=4, shN=-10, elN=42, shF=-4, elF=36, hipN=-4, kneeN=2, hipF=20, kneeF=26, ankleF=4))
    C['marisol'] = dict(fig=fg.Figure(build=dict(hip=.051, knee=.031, calf=.033, ankle=.021, chest=.055, shoulder=.025, elbow=.020, wrist=.015, neck=.021, head=1.12),
                                      head_profile=MARISOL_HEAD, trunk_profile=PARKA, extras=marisol_extras),
                        height=.92, window='#ffe08a', title='MARISOL', role='the Lookout',
                        pose=dict(lean=-4, head=-9, shN=55, elN=150, wrN=0, shF=50, elF=152, wrF=0, hipN=5, hipF=-6, kneeF=3))
    C['passenger'] = dict(fig=fg.Figure(head_profile=HAT_HEAD, extras=passenger_extras), height=.94, window='#fff6cf', title='A PASSENGER', role='thinks there has been a mistake',
                          colours=('#8f9794', '#b9c0bb', '#b9c0bb'), edge='#dfe4de',
                          pose=dict(lean=5, shN=-6, elN=12, shF=4, elF=8, hipN=8, hipF=-8, kneeF=6))
    C['lang'] = dict(fig=fg.Figure(build=dict(hip=.046, knee=.029, calf=.031, ankle=.018, chest=.053, shoulder=.023, elbow=.019, wrist=.014, neck=.020, head=1.05),
                                   seg=dict(thigh=.255, shank=.255), head_profile=LANG_HEAD, trunk_profile=LONGCOAT, extras=lang_extras),
                     height=1.02, window='#dbeeff', title='VESPER LANG', role='Director of Continuity',
                     pose=dict(lean=0, shN=34, elN=86, wrN=-20, shF=-10, elF=24, hipN=2, hipF=-2))
    return C
