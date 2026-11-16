exec(open('../styles/lit-window/kit.py').read())
exec(open('../styles/lit-window/subjects/heron.py').read())
exec(open('../styles/lit-window/subjects/ferry.py').read())
X0, Y0, X1, Y1 = 80, 70, 1200, 1730
HZ = 502
# the block list, light to dark
PAL = dict(paper=PAPER, lamp='#ecd596', lamp2='#c9a35c', pale='#a8b3a6', mid='#5d717b', deep='#2b3f50',
           night='#121a24', pile='#1c1917', pile2='#2d2925', slate='#3a4650')
def U(a, b): return (X0 + a * (X1 - X0), Y0 + b * (Y1 - Y0))
