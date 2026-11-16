# coyote.py: a coyote stopped and looking, from grid-measured landmarks on transfer/refs/coyote_portland.jpg
# (grid_coyote.jpg, 695 x 900; feet-centre at about (300, 830); 592 px from paws to withers = 0.60 m).
# The animal stands three-quarter on with the head turned square to the camera, so in flat silhouette it reads
# the same whether it looks at us or away up the line. That is why it is drawn as a silhouette only.
# What memory had wrong and the photograph corrected:
#   - the ears are huge: each is a quarter of the head-and-ears width, and they stand 0.2 m above the withers
#   - the legs are long and thin, more than half the standing height, and the near foreleg is planted well forward
#   - the body in three-quarter view is short, barely wider than the legs are long
#   - the tail hangs straight down behind the hind legs, it does not stream out
#   - the neck ruff makes the head sit in a collar wider than the skull
COY = [(375, 38), (405, 62), (432, 90), (462, 100), (500, 104), (545, 85), (585, 60), (610, 48), (600, 95), (585, 135), (570, 168), (578, 215), (572, 265),
       (555, 300), (562, 335), (545, 400), (532, 450), (520, 505), (505, 560), (508, 650), (520, 740), (530, 800), (540, 845), (520, 860), (488, 855),
       (478, 800), (462, 720), (450, 640), (432, 560), (425, 525), (385, 528), (345, 535), (340, 560), (335, 640), (325, 720), (318, 790), (322, 818),
       (290, 822), (268, 815), (275, 740), (280, 650), (275, 575), (255, 552), (215, 548), (190, 560), (200, 620), (215, 700), (232, 770), (248, 800),
       (235, 812), (205, 808), (195, 760), (180, 690), (165, 620), (150, 585), (158, 640), (150, 690), (132, 650), (125, 610), (122, 640), (118, 700),
       (112, 760), (118, 795), (95, 800), (72, 790), (78, 740), (85, 680), (95, 630), (88, 590), (80, 540), (76, 470), (80, 390), (95, 310), (130, 265),
       (200, 240), (290, 234), (345, 238), (350, 215), (362, 175), (378, 150), (372, 95)]
COY_RIM = [[(373, 100), (376, 42), (404, 64), (431, 92)], [(546, 87), (585, 62), (608, 51), (599, 96), (585, 136)], [(133, 266), (200, 242), (290, 236), (343, 240)]]
def coyote(ox, oy, k, color, rim=None, flip=False):
    """Feet-centre at (ox, oy); k = screen pixels per photo pixel (0.6 m of height on screen / 592)."""
    f = -1 if flip else 1
    def Tr(pts): return np.array([(ox + f * (x - 300) * k, oy + (y - 830) * k) for x, y in pts])
    marks([Tr(COY)], color)
    if rim:
        marks([ribbon(Tr(p), w=max(1.6, 20 * k), taper=(.2, .2), wob=0, smooth=False) for p in COY_RIM], rim)
