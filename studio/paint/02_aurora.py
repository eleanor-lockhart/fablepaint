exec(open('paint/common.py').read())
# First pass read as shower curtains: hard tops, hard sides, a drawn pink line. Redo them.
for n in ('aurora1', 'aurora2', 'aurora3', 'aurora_red', 'fringe'):
    delete(n)
props('aurora_glow', opacity=.6)
use('aurora_glow')
G = '#4dffa0'

def curtain(name, pts, pr, size, L1, L2, gain, seed, raysx=90):
    """Hem as a ribbon of varying brightness; one copy dragged up into ordinary rays, a second into
    the few tall ones; both broken into filaments by column noise."""
    layer(name, blend='add')
    B(size=size, hardness=.3, flow=.9, spacing=.06, psize=False, pflow=True)
    stroke(pts, color=G, pressure=pr)
    B(size=size * 2.4, hardness=0, flow=.22, spacing=.06, psize=False, pflow=True)
    stroke(pts, color=G, pressure=pr)
    duplicate(name, name + '_tall')
    smear(L2, 90, .33, gain * 1.3)
    cols = noise_field(1, 3, seed + 7, stretch=(16, .15))
    modulate(np.clip((cols - .45) * 3, 0, 1) * (.3 + .7 * noise_field(1, 4, seed + 3, stretch=(110, .4))))
    use(name)
    smear(L1, 90, .28, gain)
    modulate(.2 + .8 * noise_field(1, 5, seed, stretch=(raysx, .5)) ** 1.5)
    use(name + '_tall')
    merge_down()
    gaussian_blur(1.6)

main = [(-200, 760), (60, 700), (300, 655), (520, 640), (700, 600), (860, 615), (1000, 560), (1090, 480), (1050, 410),
        (1110, 360), (1260, 350), (1420, 385), (1600, 350), (1780, 300), (1980, 270), (2200, 215), (2420, 200), (2700, 150)]
mpr = [.2, .4, .7, .5, .9, .6, 1, 1, .7, 1, .8, .9, .6, .8, .5, .7, .4, .2]
curtain('aurora3', [(-200, 840), (100, 815), (380, 820), (640, 800), (820, 810)], [.2, .45, .3, .4, 0], 11, 420, 640, 3.5, 31, 150)
curtain('aurora2', [(700, 830), (980, 800), (1250, 790), (1500, 750), (1760, 720), (2000, 715), (2250, 680), (2500, 640), (2760, 620)],
        [0, .3, .5, .35, .6, .3, .5, .3, .1], 14, 520, 800, 4.0, 32, 130)
curtain('aurora1', main, mpr, 26, 620, 900, 6.0, 33, 90)

# crimson where the rays run out of oxygen-green: lifted, softened copy of the big curtain
duplicate('aurora1', 'aurora_red')
transform(translate=(0, -150))
gaussian_blur(35)
colorize('#ff2a6a', 1.0)
modulate(.35 + .65 * noise_field(1, 4, 40, stretch=(60, .4)))
props(opacity=.26)
# magenta hem, only on the brightest folds, thin
layer('fringe', blend='add', opacity=.6)
B(size=4.5, hardness=.2, flow=.32, spacing=.1, psize=False, pflow=True)
stroke([(x, y + 12) for x, y in main], color='#ff7ad9', pressure=[0, 0, .5, .1, .8, .2, 1, 1, .4, 1, .5, .7, .1, .5, 0, .3, 0, 0])
modulate(.3 + .7 * noise_field(1, 5, 33, stretch=(90, .5)))
gaussian_blur(1.3)
