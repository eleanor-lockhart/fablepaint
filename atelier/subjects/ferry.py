# subjects/ferry.py: a Washington State Ferries Jumbo Mark II (Tacoma / Wenatchee / Puyallup),
# built as a box model from photographs (see refs/photos/ferry_*.jpg) and drawn through kit.camera().
# World units are metres: x along the 140 m hull, y across the 27 m beam, z up from the waterline.
#
# What memory got wrong and the photographs corrected:
#   - she is long and LOW (about 10:1), and nearly all white: the dark hull is a thin strip at the water
#   - three rows of openings: two rows of rounded car-deck ports, then one near-continuous window band
#   - the upper decks stop short of the ends and the ends are rounded, with the car-deck mouth open
#   - wide, low pilot houses with green roofs set back from each end, a tall mast beside each
#   - one stack amidships: white foot, green band, black louvred top
#   - at night the pilot houses are dark; she reads as bands of light with no hull under them
def _plan(L, B, straight, tip, n=9):
    """Rounded-ended plan (convex, counter-clockwise): straight sides out to +-straight,
    then quarter-elliptical noses that end in a flat tip of half-width `tip` at x = +-L."""
    nose = [(straight + (L - straight) * math.sin(math.pi / 2 * k / n), tip + (B - tip) * math.cos(math.pi / 2 * k / n)) for k in range(n + 1)]
    out = [(x, -y) for x, y in nose]                    # along the -y side toward the bow tip
    out += [(x, y) for x, y in nose[::-1]]              # round the bow and back along +y
    out += [(-x, y) for x, y in nose]                   # along +y toward the stern tip
    out += [(-x, -y) for x, y in nose[::-1]]            # round the stern
    return out

def ferry(P, eye, night=True, side=1, pal=None):
    """Draw the ferry on the current layer stack. `side` = +1 if the camera is on the +y side.
    Returns dict of useful screen points (waterline run for reflections, light positions)."""
    c = dict(white='#55666f', white2='#44545d', hull='#12181b', green='#1f4a3c', dark='#101417', stackblk='#15181b',
             lamp='#ecd596', lamp2='#d9b56e', lamp3='#a9925a', roof='#1d4034', key=KEY, nav_g='#7fd9a0', nav_w='#f1ead2') if night else \
        dict(white='#d8d8cc', white2='#b9bfba', hull='#1c2422', green='#2f6a55', dark='#2a3236', stackblk='#23272a',
             lamp='#39464e', lamp2='#39464e', lamp3='#39464e', roof='#2f6a55', key=KEY, nav_g='#2f6a55', nav_w='#d8d8cc')
    c.update(pal or {})
    hull = _plan(70, 13.7, 46, 5.0)
    upper = _plan(60, 13.7, 42, 7.5)
    S = 13.7 * side
    def wall(plan, z0, z1, col, only=None):
        marks(extrude(P, plan, z0, z1, eye, only=only), col)
    def row(z0, z1, xa, xb, pitch, wd, col, y=S, r=.0):
        q = []
        for x in np.arange(xa, xb, pitch):
            q.append(np.array([P(x, y, z0), P(x + wd, y, z0), P(x + wd, y, z1), P(x, y, z1)]))
        marks(q, col)
    # hull and sides, bottom to top
    wall(hull, 0, 1.3, c['hull']); wall(hull, 1.3, 2.1, c['green']); wall(hull, 2.1, 8.6, c['white'])
    wall(hull, 2.9, 7.6, c['dark'], only=lambda m: abs(m[1]) < 9.6 and abs(m[0]) > 60)          # car-deck mouths
    wall(upper, 8.6, 13.5, c['white'])
    wall(upper, 8.6, 13.5, c['white2'], only=lambda m: abs(m[0]) > 44)                          # the rounded ends turn away
    wall(hull, 2.1, 8.6, c['white2'], only=lambda m: abs(m[0]) > 50 and abs(m[1]) >= 9.6)
    # openings
    row(3.4, 5.3, -44, 44, 6.4, 4.2, c['lamp3'])
    row(6.3, 7.7, -45, 45, 4.9, 3.3, c['lamp2'])
    row(9.9, 11.7, -41.5, 41.5, 2.3, 1.75, c['lamp'])
    # sun deck: rail, solarium, stack
    wall(boxplan(-28, 28, -8, 8), 13.5, 16.2, c['white'])
    row(14.2, 15.6, -26, 26, 3.4, 2.5, c['lamp'], y=8 * side)
    wall(boxplan(-4.5, 4.5, -3.2, 3.2), 16.2, 19.4, c['white'])
    wall(boxplan(-4.5, 4.5, -3.2, 3.2), 17.0, 18.0, c['green'])
    wall(boxplan(-4.2, 4.2, -3.0, 3.0), 19.4, 23.6, c['stackblk'])
    # pilot houses and masts at both ends
    lights = []
    for sx in (-1, 1):
        xa, xb = sorted((sx * 46, sx * 56))
        wall(boxplan(xa, xb, -5.5, 5.5), 13.5, 16.4, c['white'])
        wall(boxplan(xa - .5, xb + .5, -7.5, 7.5), 16.4, 18.8, c['white'])
        wall(boxplan(xa - .5, xb + .5, -7.5, 7.5), 17.2, 18.4, c['dark'])
        wall(boxplan(xa - 1, xb + 1, -8.2, 8.2), 18.8, 19.5, c['roof'])
        mx = sx * 40
        marks([seg(P(mx, 0, 16.2), P(mx, 0, 28.5), w=1.6, wob=0), seg(P(mx, -2.6, 25), P(mx, 2.6, 25), w=1.1, wob=0),
               seg(P(mx - 1.6, 0, 22), P(mx + 1.6, 0, 22), w=1.4, wob=0), seg(P(mx - 2.2, 0, 16.2), P(mx, 0, 24), w=1.0, wob=0)], c['white'] if night else c['key'])
        lights.append(P(mx, 0, 28.5))
    rail = [seg(P(x, S, 14.7), P(x + 6, S, 14.7), w=.9, wob=0) for x in np.arange(-42, 42, 6)]
    marks(rail, c['white'])
    return dict(mast_lights=lights, side_light=P(48, S * .6, 17.0), waterline=[P(x, S, 0) for x in np.arange(-46, 47, 4)],
                rows=[(P(x, S, 10.8), 'lamp') for x in np.arange(-41, 42, 2.3)], pal=c)
