exec(open('../styles/lit-window/kit.py').read())
X0, Y0, X1, Y1 = 80, 70, 1200, 1730
# block list, light to dark
S1, S2, S3 = '#ece7d8', '#b7c3c5', '#8c9fa6'          # snow: paper, shade, deep shade
SKY0, SKY1, SKY2 = '#17232d', '#2d404c', '#62757b'    # sky top, middle, at the ridge
FAR, DARK, DARK2 = '#3c5058', '#141a1d', '#27353c'    # far trees, near timber and fir, second fir
LAMP, LAMP2 = '#ecd596', '#d2a257'
def U(a, b): return (X0 + a * (X1 - X0), Y0 + b * (Y1 - Y0))
def Us(pts): return np.array([U(a, b) for a, b in pts])
TRACK = [(.66, 1.02), (.54, .87), (.33, .75), (.25, .65), (.35, .56), (.47, .475), (.43, .40), (.385, .338)]
