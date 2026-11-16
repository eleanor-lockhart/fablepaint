# subjects/orca.py: a breaching orca, from grid-measured landmarks on refs/photos/orca_srkw_breach.jpg
# (a Southern Resident breaching side-on, head up and to the right, about 37 degrees above level).
#
# What the photograph corrected in my earlier (remembered) orca:
#   - it is STOCKY: greatest depth is about a quarter of the visible length, and it stays deep
#     almost to the head; I had drawn a slender torpedo
#   - the head is blunt and rounded, the lower jaw white right up to the tip
#   - the pectoral flipper is a broad paddle hanging from the white chest, half as long as the head-to-fin distance
#   - the white comes up the flank in a lobe behind the dorsal fin; the eye patch is a slanted oval
#   - the dorsal fin sits well back, at about the middle of the visible body
# Source coordinates are grid units on the photo (x unit 73.2 px, y unit 50.3 px). The whale rises out
# of the water at about (2.8, 7.6). `rot` turns it further upright (degrees), `flip` makes it head left.
def orca(ox, oy, s=1.0, flip=False, rot=0.0, pal=None, jaw=14.0):
    c = dict(black='#0d1013', white='#e9e2cf', saddle='#3a4650', mouth='#3b171a', tooth='#e9e2cf')
    c.update(pal or {})
    bx, by = 2.8 * 73.2, 7.6 * 50.3
    ca, sa = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    def T(pts):
        out = []
        for ux, uy in pts:
            dx, dy = ux * 73.2 - bx, uy * 50.3 - by
            x_, y_ = dx * ca + dy * sa, -dx * sa + dy * ca
            out.append((ox + (-x_ if flip else x_) * s, oy + y_ * s))
        return out
    def J(pts, pivot=(7.1, 2.6)):                 # swing the lower jaw open about the corner of the mouth
        a = math.radians(jaw); out = []
        for ux, uy in pts:
            dx, dy = (ux - pivot[0]) * 73.2, (uy - pivot[1]) * 50.3
            out.append((pivot[0] + (dx * math.cos(a) - dy * math.sin(a)) / 73.2, pivot[1] + (dx * math.sin(a) + dy * math.cos(a)) / 50.3))
        return out
    back = [(8.1, 1.7), (7.95, 1.45), (7.5, 1.38), (6.9, 1.6), (6.2, 2.05), (5.5, 2.6), (4.6, 3.4), (4.05, 4.2), (3.6, 5.0), (3.15, 6.0), (2.85, 7.0), (2.7, 7.7)]
    belly = [(3.0, 7.8), (3.6, 7.3), (4.3, 6.7), (5.2, 5.9), (6.0, 5.15), (6.6, 4.5), (7.1, 3.7)]
    lowjaw = J([(7.1, 3.7), (7.6, 2.9), (7.95, 2.25), (8.12, 1.95), (7.6, 2.2)])
    marks([spline(T(back + belly + lowjaw[:4] + [(7.1, 2.6), (7.7, 2.05)]), closed=True)], c['black'])
    marks([spline(T([(4.7, 3.3), (4.2, 3.18), (3.5, 3.33), (3.72, 3.75), (4.0, 4.3), (4.4, 3.9)]), closed=True)], c['black'])     # dorsal fin
    # white: lower jaw, throat, chest, belly, and the lobe that climbs the flank
    white = lowjaw[3:4] + lowjaw[4:5] + [(7.1, 2.62), (6.75, 3.3), (6.45, 4.0), (6.0, 4.6), (5.3, 5.25), (4.6, 5.68), (3.95, 5.8), (3.4, 6.2), (3.3, 6.6),
             (3.5, 6.95), (3.2, 7.5), (3.0, 7.8), (3.6, 7.3), (4.3, 6.7), (5.2, 5.9), (6.0, 5.15), (6.6, 4.5), (7.1, 3.7)] + lowjaw[1:3]
    marks([np.array(T(white))], c['white'])
    marks([spline(T([(6.45, 1.86), (6.75, 1.66), (7.2, 1.62), (7.4, 1.74), (7.1, 1.9), (6.7, 1.98)]), closed=True)], c['white'])     # eye patch
    if c.get('saddle'):
        marks([spline(T([(3.95, 4.5), (3.75, 4.75), (3.4, 5.5), (3.55, 5.45), (3.9, 4.85)]), closed=True)], c['saddle'])            # saddle patch
    # mouth: dark gape, a row of teeth on each jaw
    gape = [(8.08, 1.78), (7.1, 2.6)] + lowjaw[3:4]
    marks([np.array(T(gape))], c['mouth'])
    teeth = []
    for t in np.linspace(.12, .8, 8):
        ux, uy = 8.08 + (7.1 - 8.08) * t, 1.78 + (2.6 - 1.78) * t
        teeth.append(np.array(T([(ux - .035, uy - .02), (ux + .035, uy + .04), (ux - .05, uy + .14)])))
        lx, ly = lowjaw[3][0] + (7.1 - lowjaw[3][0]) * t, lowjaw[3][1] + (2.6 - lowjaw[3][1]) * t
        teeth.append(np.array(T([(lx - .04, ly - .02), (lx + .04, ly + .03), (lx + .0, ly - .13)])))
    marks(teeth, c['tooth'])
    # flipper: a broad black paddle hanging from the chest
    marks([spline(T([(6.75, 4.1), (7.35, 4.6), (7.6, 5.6), (7.4, 6.6), (6.9, 6.5), (6.65, 5.6), (6.55, 4.8)]), closed=True)], c['black'])
    return dict(snout=T([(8.1, 1.7)])[0], eye=T([(7.25, 2.05)])[0], fluke=T([(2.8, 7.6)])[0], fliptip=T([(7.3, 6.6)])[0],
                chin=T(lowjaw[3:4])[0], backmid=T([(4.6, 3.4)])[0], T=T)
