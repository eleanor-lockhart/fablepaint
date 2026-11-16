RESET = dict(tip='round', size=20, hardness=.8, opacity=1, flow=1, spacing=.1, angle=0, roundness=1, follow=False,
             scatter=0, count=1, size_jitter=0, angle_jitter=0, flow_jitter=0, hue_jitter=0, sat_jitter=0,
             val_jitter=0, psize=True, pflow=False, taper=(0, 0), blend='normal', mix=0, grain=0, smooth=True)
def B(**kw):
    brush(**{**RESET, **kw})
HZ = 880                      # far waterline
MOON = (1330, 420, 230)
FULL = [(0, 0), (2560, 0), (2560, 1440), (0, 1440)]
def edge_light(base, name, colour, dx, dy, strength=1.0, blur=1.2):
    """Rim light: a clipped 'add' layer lit only where the shape's edge faces (dx, dy)."""
    a = px(base)[..., 3]
    rim = np.clip(a - np.roll(np.roll(a, -dy, 0), -dx, 1), 0, 1)
    use(base)
    layer(name, blend='add', clip=True)
    fill(colour)
    modulate(rim * strength)
    gaussian_blur(blur)
