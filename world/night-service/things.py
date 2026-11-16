"""Things of the world that are drawn once and used everywhere (house rule 12: one thing, one model).

Each is a paper cut-out: polygons in its own units, u along the way it faces, v up, feet (or waterline) at v = 0.
Put one in a place with `Set.card(name, polys, origin, heading, metres=...)`.

    NO4, NO4_M            No. 4, the Lineman. Unit = its height above the water; it is forty metres.
    NO4_EYE, NO4_CHEST    its eye and the window in its chest, same units
    heron(), HERON_M      the Notary. Unit = its height; a great blue heron stands about 1.15 m.
"""
import numpy as np
from backlot import shapes as sh

NO4_M = 40.0
NO4 = [[(-.115, -.01), (-.12, .15), (-.142, .19), (-.115, .235), (-.10, .37), (-.02, .37), (-.045, .235), (-.052, .19), (-.06, .15), (-.062, -.01)],
       [(.03, -.01), (.035, .15), (.028, .19), (.045, .235), (.02, .37), (.10, .37), (.115, .235), (.138, .19), (.115, .15), (.108, -.01)],
       [(-.10, .37), (.10, .37), (.082, .43), (.0, .465), (-.082, .43)], [(-.05, .43), (.05, .43), (.042, .55), (-.042, .55)],
       [(-.042, .54), (.042, .54), (.165, .60), (.205, .70), (.155, .765), (.05, .785), (-.05, .785), (-.155, .765), (-.205, .70), (-.165, .60)],
       [(-.195, .70), (-.238, .72), (-.258, 1.02), (-.222, 1.045), (-.188, .765)], [(.195, .70), (.238, .72), (.266, 1.03), (.23, 1.055), (.188, .765)],
       [(-.035, .775), (-.01, .895), (.05, .93), (.105, .905), (.15, .835), (.128, .80), (.118, .765), (.07, .768)], [(.065, .915), (.20, 1.005), (.10, .895)],
       [(-.19, .72), (-.235, .60), (-.262, .47), (-.252, .33), (-.268, .26), (-.285, .18), (-.262, .21), (-.255, .165), (-.24, .215), (-.215, .33), (-.222, .47), (-.17, .60)],
       [(.19, .72), (.262, .625), (.335, .525), (.375, .445), (.408, .405), (.39, .385), (.342, .42), (.29, .50), (.222, .58), (.17, .62)]]      # as first drawn for the opening (op/common.py)
NO4_EYE = [(.075, .868), (.112, .858), (.112, .848), (.078, .856)]
NO4_CHEST = [(-.028, .700), (.030, .700), (.030, .628), (-.028, .628)]
NO4_BACK = (-.03, .63)                       # where the Cable goes in

HERON_M = 1.15
def heron():
    """The heron's parts, facing +u, standing on v = 0, one unit tall. Landmarks measured for the Lit Window print."""
    sh.setup(64, 64, 1)
    T = lambda pts: np.array([(-(x - 300) / 533.0, (700 - y) / 533.0) for x, y in pts])
    body = [(250, 265), (268, 258), (292, 272), (335, 330), (372, 420), (400, 520), (408, 600), (398, 640), (372, 628), (340, 560), (300, 520), (262, 480), (232, 420), (210, 360), (205, 330), (225, 290)]
    neck = [(262, 198), (267, 232), (252, 262), (240, 300), (225, 345), (207, 375), (183, 345), (165, 300), (170, 258), (190, 235), (198, 226), (225, 228), (250, 215)]
    head = [(166, 190), (190, 174), (215, 167), (243, 175), (258, 198), (248, 214), (225, 226), (199, 226), (173, 207)]
    polys = [np.asarray(sh.spline(T(body), closed=True)), np.asarray(sh.spline(T(neck), closed=True)), np.asarray(sh.spline(T(head), closed=True)), T([(50, 215), (120, 196), (167, 185), (175, 209), (120, 212)])]
    for leg in ([(285, 532), (292, 612), (296, 700)], [(318, 566), (323, 640), (327, 694)]):
        P = T(leg); w = 7 / 533.0 / 2
        polys.append(np.array([(x - w, y) for x, y in P] + [(x + w, y) for x, y in P[::-1]]))
    return polys
