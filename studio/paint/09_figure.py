exec(open('paint/common.py').read())
# the shore lip was stacked above the figure and ran straight across their coat
move('shore', above='snow_ridges')
props('cracks', opacity=.18)
use('cracks'); gaussian_blur(1.1)
# the pair on the shore looked like toys: redraw with real proportions, head tipped back, hands in pockets
use('figure'); clear()
x, y = 1560, 1236
ink = '#04070a'
fill_ellipse(x - 26, y + 3, 64, 6, color='#040b10', opacity=.5, feather=5)
for sx in (-1, 1):
    fill_poly([(x + sx * 4, y), (x + sx * 6, y - 7), (x + sx * 17, y - 7), (x + sx * 18, y)], color=ink)
    fill_poly([(x + sx * 5, y - 6), (x + sx * 3, y - 58), (x + sx * 17, y - 58), (x + sx * 15, y - 6)], color=ink)
    fill_poly([(x + sx * 18, y - 100), (x + sx * 26, y - 84), (x + sx * 25, y - 64), (x + sx * 19, y - 60), (x + sx * 17, y - 80)], color=ink, smooth=True)
fill_poly([(x - 19, y - 50), (x - 21, y - 80), (x - 19, y - 98), (x - 12, y - 106), (x + 12, y - 106), (x + 19, y - 98),
           (x + 21, y - 80), (x + 19, y - 50)], color=ink, smooth=True)
fill_ellipse(x, y - 113, 10.5, 11.5, color=ink)
fill_ellipse(x, y - 110, 12.5, 8, color=ink)                      # the ruff of the hood
dx = x - 66
fill_poly([(dx - 14, y), (dx - 16, y - 18), (dx - 10, y - 34), (dx - 2, y - 42), (dx + 6, y - 40), (dx + 11, y - 28),
           (dx + 12, y - 10), (dx + 16, y)], color=ink, smooth=True)
fill_poly([(dx + 5, y - 26), (dx + 11, y - 26), (dx + 14, y), (dx + 7, y)], color=ink)
fill_ellipse(dx + 4, y - 50, 8.5, 7.5, angle=-25, color=ink)
fill_poly([(dx + 8, y - 56), (dx + 22, y - 64), (dx + 24, y - 59), (dx + 12, y - 48)], color=ink, smooth=True)
fill_poly([(dx - 3, y - 53), (dx - 6, y - 65), (dx + 2, y - 58)], color=ink)
fill_poly([(dx + 3, y - 57), (dx + 3, y - 68), (dx + 9, y - 59)], color=ink)
B(size=4.5, hardness=.6, spacing=.15, taper=(0, .7))
stroke([(dx - 13, y - 3), (dx - 28, y - 1), (dx - 35, y - 9)], color=ink)
# only a thread of the sky's colour on what faces it
B(size=1.7, hardness=.4, flow=.45, spacing=.15, taper=(.3, .4))
for pts in ([(x - 8, y - 123), (x, y - 125.5), (x + 8, y - 123)], [(x - 17, y - 102), (x - 22, y - 92)], [(x + 17, y - 102), (x + 22, y - 92)],
            [(dx - 3, y - 56), (dx + 6, y - 58), (dx + 20, y - 64)], [(dx - 14, y - 26), (dx - 8, y - 37), (dx - 1, y - 42)]):
    stroke(pts, color='#4fb898')
