exec(open('paint/common.py').read())
delete('mtn_far')
delete('mtn_near')
far = [(0, 760), (90, 735), (180, 750), (260, 700), (340, 720), (430, 660), (500, 690), (590, 640), (680, 675), (770, 700),
       (860, 730), (950, 745), (1040, 770), (1130, 790), (1220, 800), (1320, 785), (1420, 760), (1500, 720), (1580, 740),
       (1660, 690), (1750, 650), (1830, 675), (1910, 630), (2000, 660), (2080, 640), (2170, 690), (2260, 670), (2350, 710),
       (2440, 700), (2560, 740)]
near = [(0, 800), (70, 770), (150, 785), (230, 730), (290, 700), (330, 640), (365, 650), (400, 585), (430, 600), (470, 548),
        (500, 515), (520, 540), (555, 530), (600, 590), (650, 600), (700, 650), (760, 665), (820, 720), (880, 740), (940, 800),
        (1020, 830), (1100, 855), (1200, 868), (1300, 872), (1400, 862), (1500, 845), (1580, 815), (1650, 790), (1700, 800),
        (1760, 740), (1800, 720), (1840, 745), (1900, 700), (1950, 705), (2000, 650), (2050, 620), (2090, 640), (2130, 590),
        (2165, 600), (2210, 560), (2240, 585), (2290, 575), (2340, 630), (2400, 645), (2460, 700), (2520, 705), (2560, 735)]

def massif(name, pts, snow, rock, seed, relief_scale, relief_depth, rock_cut, jag):
    """Silhouette -> roughened; fractal relief lit from above, clipped to it; bare rock where snow won't hold."""
    layer(name, below='haze')
    fill_poly(pts + [(W + 40, 930), (-40, 930)], color=snow)
    turbulence(jag, 16, seed=seed)
    turbulence(jag * .35, 70, seed=seed + 1)
    # snowfields a little brighter high up, where they face the sky
    lock(True)
    gradient('linear', (0, 500), (0, 900), [(0, '#ffffff', .10), (1, '#000000', .30)])
    lock(False)
    layer(name + '_rock', clip=True)
    fill(rock)
    n = noise_field(7, 6, seed + 2, stretch=(1.8, .45), ridged=True) * .6 + noise_field(22, 4, seed + 3) * .4
    mask(np.clip((n - rock_cut) * 7, 0, 1))
    layer(name + '_relief', blend='overlay', clip=True)
    clouds('#000000', '#ffffff', scale=relief_scale, octaves=7, seed=seed + 4, ridged=True)
    emboss(angle=115, depth=relief_depth)
    gaussian_blur(.8)

massif('mtn_far', far, '#1e4a52', '#0e2630', 50, 14, 1.2, .50, 12)
massif('mtn_near', near, '#1d4f4b', '#050c12', 60, 9, 2.2, .47, 18)
