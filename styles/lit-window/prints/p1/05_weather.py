exec(open('../styles/lit-window/prints/p1/common.py').read())
window(X0, Y0, X1, Y1)
# ---- rain: ruled, from the south-west. Dark hairlines where the picture is light, pale where it is dark.
block('rain_dark')
marks(rain(X0, Y0, X1, Y1, n=80, angle=106, w=1.0, length=(.25, .8), spread=1.2), '#0b1016', opacity=.55)
block('rain_pale')
marks(rain(X0, Y0, X1, Y1, n=120, angle=106, w=.9, length=(.2, .7), spread=1.2), '#93a3a6', opacity=.26)
# ---- rings where drops land, growing toward us
block('rings', below='rain_dark')
rr = []
for _ in range(46):
    f = rng.uniform(.12, 1) ** .8
    y = HZ + (Y1 - HZ) * f; x = rng.uniform(410, X1 - 10)
    rx = 3 + 24 * f * rng.uniform(.6, 1.2)
    rr.append(ring(x, y, rx, w=.9 + .6 * f))
    if rng.uniform() < .4:
        rr.append(ring(x, y, rx * .5, w=.8 + .4 * f))
marks(rr, '#6e828a', opacity=.75)
finish(X0, Y0, X1, Y1, tooth=.3)
seal(X1 - 66, Y1 - 66, 36)
block('title')
text(X0 + 2, Y1 + 30, 'Last boat, rain', size=30, font='Liberation Serif', color='#4b4438', anchor='la')
text(X1 - 2, Y1 + 34, 'Fable', size=24, font='Liberation Serif', color='#4b4438', anchor='ra')
