exec(open('../styles/lit-window/kit.py').read())
exec(open('../styles/lit-window/subjects/orca.py').read())
X0, Y0, X1, Y1 = 80, 70, 1200, 1730
HZ = 585
MOON = (528, 330, 130)
# block list, light to dark
PAPERW, PALE, MIDL, MID, DEEP, NIGHT = '#e9e2cf', '#c5cfce', '#8fa3aa', '#4f6676', '#22364a', '#0f1722'
BLACK, CITY, FIRE, EYE = '#0d1013', '#17212b', '#d8823a', '#a6dc7e'
def U(a, b): return (X0 + a * (X1 - X0), Y0 + b * (Y1 - Y0))
