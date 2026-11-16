exec(open('../atelier/prints/p2/common.py').read())
exec(open('../atelier/subjects/lookout.py').read())
window(X0, Y0, X1, Y1)
eye = (48, -36, -8)
bx, by = U(.385, .318)
P0 = camera(eye=eye, look=(0, 0, 5), fov=35.2, centre=(bx, by))
ox, oy = P0(0, 0, 0)
P = camera(eye=eye, look=(0, 0, 5), fov=35.2, centre=(bx + (bx - ox), by + (by - oy)))     # put her feet on the knoll
block('tower')
info = lookout(P, eye, dict(timber=DARK, timber2='#2a363c', lamp=LAMP, lamp2=LAMP2, snow=S1, shade=S2))
# guy wires
marks([seg(P(3, -3, 6), P(13, -15, -1.5), w=.9, wob=0), seg(P(3, 3, 6), P(17, 12, -1.2), w=.9, wob=0), seg(P(-3, -3, 6), P(-15, -13, -1.2), w=.9, wob=0)], '#2a363c')
# smoke from the stove: someone is home
px_, py_ = info['pipe']
marks([ribbon([(px_, py_ - 2), (px_ + 6, py_ - 34), (px_ + 30, py_ - 70), (px_ + 78, py_ - 96), (px_ + 150, py_ - 108)], w=5, taper=(.05, .6), wob=.3)], '#7d8f95', opacity=.8)
# the cabin beside her, buried to the eaves
block('cabin')
marks([np.array([P(7, -2.2, .2), P(11.5, -2.2, .2), P(11.5, -2.2, 1.5), P(7, -2.2, 1.5)])], DARK)
marks([np.array([P(11.5, -2.2, .2), P(11.5, 1.8, .2), P(11.5, 1.8, 1.5), P(11.5, -.2, 2.9), P(11.5, -2.2, 1.5)])], '#2a363c')
marks([np.array([P(6.7, -2.6, 1.45), P(11.9, -2.6, 1.45), P(11.9, -.2, 3.15), P(6.7, -.2, 3.15)])], S1)
# snow heaped round the feet of the tower so the posts sink into it
block('heap')
hx, hy = info['base']
marks([wobble(np.array([(hx - 120, hy + 30), (hx - 70, hy + 4), (hx - 20, hy - 6), (hx + 40, hy - 2), (hx + 110, hy + 14), (hx + 190, hy + 20), (hx + 260, hy + 44), (hx - 120, hy + 44)]), .7, 22)], S2)
print('tower base', round(hx), round(hy), 'apex', [round(v) for v in info['apex']])
