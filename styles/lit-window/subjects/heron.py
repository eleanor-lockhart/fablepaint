# subjects/heron.py: great blue heron at rest, from grid-measured landmarks on refs/photos/heron_sunnyvale.jpg.
#
# What memory got wrong and the photograph corrected:
#   - at rest the neck is FOLDED and thick, a warm grey-pink "?" sitting in front of the breast,
#     not a thin pale tube; the head rides just above the shoulders
#   - the head is a wedge that continues the line of the bill; the black eyebrow is a broad band
#     ending in two long trailing plumes
#   - the body hangs steeply like a cloak, with long pale plume lines over it and a dark tip
#   - the black shoulder patch is a vertical wedge with streaks running down from it
#   - the legs come out from under the middle of the cloak, close together; the 'knee' sits 45% down
# Source coordinates are pixels on the 430x760 gridded photo; feet at about (300, 700); bird faces left.
def heron(ox, oy, s=1.0, flip=False, pal=None, plumes=True):
    c = dict(body='#5c6c78', tip='#39434c', neck='#948b88', head='#e4e0d0', bill='#c7a04c', black=KEY,
             plume='#9aa7ad', leg='#2b2927', thigh='#74574a')
    c.update(pal or {})
    k = -1 if flip else 1
    def T(pts): return [(ox + k * (x - 300) * s, oy + (y - 700) * s) for x, y in pts]
    def sp(pts): return spline(T(pts), closed=True)
    legs = [ribbon(T(p), w=6.2 * s, taper=(0, .0), wob=.04) for p in ([(285, 532), (292, 612), (296, 700)], [(318, 566), (323, 640), (327, 694)])]
    legs += [blob(*T([(292, 612)])[0], 4.6 * s, 5.2 * s, n=7, rough=.1), blob(*T([(323, 640)])[0], 4.2 * s, 4.8 * s, n=7, rough=.1)]
    for fx, fy in ((296, 700), (327, 694)):
        legs += [ribbon(T([(fx, fy), (fx + dx, fy + dy)]), w=3.6 * s, taper=(0, .7), wob=0) for dx, dy in ((-40, 9), (-19, 16), (17, 11))]
    marks(legs, c['leg'])
    marks([sp([(250, 265), (268, 258), (292, 272), (335, 330), (372, 420), (400, 520), (408, 600), (398, 640), (372, 628), (340, 560),
               (300, 520), (262, 480), (232, 420), (210, 360), (205, 330), (225, 290)])], c['body'])
    marks([sp([(372, 505), (399, 512), (408, 600), (398, 640), (372, 628), (350, 572)])], c['tip'])
    marks([np.array(T([(279, 512), (301, 514), (305, 560), (288, 549)]))], c['thigh'])
    if plumes:
        pl = []
        for i in range(15):
            f = i / 14
            a = (262 + 44 * f, 284 + 22 * f); b = (300 + 96 * f, 468 + 120 * f)
            mid = ((a[0] + b[0]) / 2 + 9 - 14 * f, (a[1] + b[1]) / 2)
            pl.append(ribbon(T([a, mid, b]), w=2.4 * s, taper=(.1, .75), wob=0))
        marks(pl, c['plume'])
    marks([sp([(262, 198), (267, 232), (252, 262), (240, 300), (225, 345), (207, 375), (183, 345), (165, 300), (170, 258), (190, 235),
               (198, 226), (225, 228), (250, 215)])], c['neck'])
    marks([np.array(T([(222, 288), (246, 280), (245, 346), (229, 354)]))] +
          [ribbon(T(p), w=4 * s, taper=(0, .8), wob=0) for p in ([(228, 348), (241, 412)], [(219, 338), (227, 392)], [(238, 340), (252, 398)])], c['black'])
    marks([sp([(166, 190), (190, 174), (215, 167), (243, 175), (258, 198), (248, 214), (225, 226), (199, 226), (173, 207)])], c['head'])
    marks([np.array(T([(50, 215), (120, 196), (167, 185), (175, 209), (120, 212)]))], c['bill'])
    marks([ribbon(T([(172, 183), (200, 166), (232, 167), (263, 193)]), w=12 * s, taper=(.15, .25), wob=0)] +
          [ribbon(T(p), w=2.6 * s, taper=(0, .85), wob=0) for p in ([(256, 186), (286, 232), (298, 300)], [(258, 190), (300, 250), (312, 342)])] +
          [blob(*T([(182, 191)])[0], 2.7 * s, 2.7 * s, n=8, rough=.05), ribbon(T([(173, 199), (70, 212)]), w=1.3 * s, taper=(0, .5), wob=0)], c['black'])
