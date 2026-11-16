exec(open('paint/common.py').read())
# ---------------- night sky: near-black overhead, a breath of teal toward the horizon
use('Background')
gradient('linear', (0, 0), (0, HORIZON), [(0, '#02040b'), (.5, '#050f24'), (.85, '#0a2030'), (1, '#12303a')])

# ---------------- the Milky Way, faint, climbing out of the left
yy, xx = np.mgrid[:H, :W].astype(np.float32)
th = math.radians(62)
dist = (xx - 520) * math.sin(th) + (yy - 430) * math.cos(th)
band = np.exp(-(dist / 190) ** 2)
mw = band * (.3 + .7 * noise_field(7, 5, 21)) * (1 - .75 * noise_field(11, 5, 22, ridged=True) * band)
mw *= np.clip((880 - yy) / 300, 0, 1)
layer('milkyway', blend='add')
fill('#93a8d6')
modulate(mw * .16)

# ---------------- stars: thousands of faint ones, fewer bright, thicker along the band
layer('stars', blend='add')
dens = .3 + 3 * mw
dens[HORIZON:] = 0
B(size=1.6, hardness=.6, flow=.9, flow_jitter=.85, size_jitter=.5, psize=False)
scatter(11000, density=dens, color='#cfdcff')
B(size=2.6, hardness=.7, flow=.9, flow_jitter=.6, size_jitter=.4, psize=False)
scatter(1500, density=dens, color='#e8eeff')
scatter(400, density=dens, color='#ffd9b8')
P = np.stack([rng.uniform(0, W, 70), rng.uniform(0, 860, 70)], 1)
B(size=4.5, hardness=.8, size_jitter=.3, psize=False)
dabs(P, color='#ffffff')
B(size=22, hardness=0, flow=.18, psize=False)
dabs(P, color='#9fc0ff')
B(tip='star', size=46, flow=.5, psize=False, size_jitter=.4)
dabs(P[:9], color='#dfe8ff')

# ---------------- the aurora
G = '#4dffa0'
def curtain(name, pts, pr, size, length, gain, seed, raysx=90):
    """Lay the bright lower hem as a ribbon, drag it upward into rays, then break it into filaments."""
    layer(name, blend='add')
    B(size=size, hardness=.25, flow=.9, spacing=.06, psize=False, pflow=True)
    stroke(pts, color=G, pressure=pr)
    B(size=size * 2.6, hardness=0, flow=.25, spacing=.06, psize=False, pflow=True)
    stroke(pts, color=G, pressure=pr)
    smear(length, 90, .45, gain)
    modulate(.18 + .82 * noise_field(1, 5, seed, stretch=(raysx, .5)) ** 1.6)
    gaussian_blur(1.4)
    perspective([(0, 0), (W, 0), (W, H), (0, H)], [(W * .07, 0), (W * .93, 0), (W, H), (0, H)])

# diffuse glow behind everything
layer('aurora_glow', blend='add')
B(size=420, hardness=0, flow=.05, spacing=.08, psize=False)
main = [(60, 700), (300, 640), (560, 600), (800, 610), (980, 560), (1100, 470), (1040, 400), (1160, 360),
        (1420, 380), (1700, 330), (2000, 250), (2300, 200), (2600, 180)]
stroke(main, color='#1e8f6a')
stroke([(900, 800), (1500, 740), (2100, 690), (2600, 630)], color='#1e8f6a')
gaussian_blur(90)

curtain('aurora3', [(-50, 820), (200, 800), (500, 810), (760, 790)], [.3, .5, .4, .2], 14, 200, 5.0, 31, 140)
curtain('aurora2', [(900, 800), (1200, 770), (1500, 740), (1800, 700), (2100, 690), (2400, 640), (2600, 630)],
        [.2, .5, .7, .5, .6, .4, .3], 18, 280, 6.0, 32, 120)
curtain('aurora1', main, [.35, .6, .8, .7, 1, 1, .8, 1, .85, .7, .8, .6, .4], 26, 460, 8.0, 33, 90)

# crimson at altitude: a copy of the big curtain lifted, softened and recoloured
duplicate('aurora1', 'aurora_red')
transform(translate=(0, -190))
gaussian_blur(45)
colorize('#ff2a6a', 1.0)
props(opacity=.32)
# and the magenta hem nitrogen puts on the brightest folds
layer('fringe', blend='add')
B(size=10, hardness=.1, flow=.5, spacing=.08, psize=False, pflow=True)
stroke([(x, y + 9) for x, y in main], color='#ff5fd0', pressure=[.1, .3, .7, .5, 1, 1, .7, 1, .7, .4, .5, .3, .1])
gaussian_blur(2.5)
perspective([(0, 0), (W, 0), (W, H), (0, H)], [(W * .07, 0), (W * .93, 0), (W, H), (0, H)])
