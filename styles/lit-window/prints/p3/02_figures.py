exec(open('../styles/lit-window/prints/p3/common.py').read())
window(X0, Y0, X1, Y1)
mx, my, mr = MOON
# ---- bigger moon (the first was too small to hold the machine)
use('moon'); clear()
a = np.linspace(0, 2 * np.pi, 100)
marks([np.c_[mx + mr * np.cos(a), my + mr * np.sin(a)]], PAPERW)
marks([spline(blob(mx - 44, my - 52, 36, 22, n=8, rough=.3), closed=True), spline(blob(mx + 54, my - 36, 20, 30, n=8, rough=.3), closed=True), spline(blob(mx - 62, my + 24, 20, 26, n=8, rough=.3), closed=True)], '#dcd6c4')
# ---- the machine: far off, knee-deep, a flat silhouette against the moon. Units: its own height.
block('mech')
HM, cx, wl = 292, mx, HZ + 7
def M(pts): return np.array([(cx + u * HM, wl - v * HM) for u, v in pts])
MECH = '#13101b'
parts = [
    [(-.115, -.01), (-.12, .15), (-.142, .19), (-.115, .235), (-.10, .37), (-.02, .37), (-.045, .235), (-.052, .19), (-.06, .15), (-.062, -.01)],     # left leg
    [(.03, -.01), (.035, .15), (.028, .19), (.045, .235), (.02, .37), (.10, .37), (.115, .235), (.138, .19), (.115, .15), (.108, -.01)],             # right leg
    [(-.10, .37), (.10, .37), (.082, .43), (.0, .465), (-.082, .43)],                                                                              # pelvis
    [(-.05, .43), (.05, .43), (.042, .55), (-.042, .55)],                                                                                          # waist: very narrow
    [(-.042, .54), (.042, .54), (.165, .60), (.205, .70), (.155, .765), (.05, .785), (-.05, .785), (-.155, .765), (-.205, .70), (-.165, .60)],     # chest
    [(-.195, .70), (-.238, .72), (-.258, 1.02), (-.222, 1.045), (-.188, .765)],                                                                    # shoulder pylons
    [(.195, .70), (.238, .72), (.266, 1.03), (.23, 1.055), (.188, .765)],
    [(-.035, .775), (-.01, .895), (.05, .93), (.105, .905), (.15, .835), (.128, .80), (.118, .765), (.07, .768)],                                   # head, hunched and turned
    [(.065, .915), (.20, 1.005), (.10, .895)],                                                                                                     # horn
    [(-.19, .72), (-.235, .60), (-.262, .47), (-.252, .33), (-.268, .26), (-.285, .18), (-.262, .21), (-.255, .165), (-.24, .215), (-.215, .33), (-.222, .47), (-.17, .60)],   # hanging arm
    [(.19, .72), (.262, .625), (.335, .525), (.375, .445), (.408, .405), (.39, .385), (.342, .42), (.29, .50), (.222, .58), (.17, .62)],           # arm reaching toward the whale
]
marks([M(p) for p in parts], MECH)
marks([ribbon(M([(-.03, .63), (-.2, .46), (-.36, .2), (-.5, -.01)]), w=2.4, taper=(0, 0), wob=.05)], MECH)                                         # the power cable
block('mechlight')
marks([M([(.385, .40), (.41, .405), (.50, .31), (.488, .30)])], '#e9c98a')                                                                         # the knife: a sliver of light
marks([M([(.075, .868), (.112, .858), (.112, .848), (.078, .856)])], EYE)                                                                          # one eye
marks(ticks(cx - .09 * HM, wl + 4, wl + 110, 26, th=2.2, jitter=.2, gap=.3) + ticks(cx + .07 * HM, wl + 4, wl + 110, 26, th=2.2, jitter=.2, gap=.3), MECH)
# ---- the pod, heading in
block('pod')
fins = [(800, 716, 1.0), (872, 760, 1.3), (968, 700, .8), (700, 804, 1.5)]
marks([np.array([(x + 13 * k, y), (x - 2 * k, y - 24 * k), (x - 6 * k, y - 22 * k), (x - 10 * k, y)]) for x, y, k in fins], BLACK)
marks([lens(x - 34 * k, y + 2, 70 * k, 2.6 * k) for x, y, k in fins] + [lens(x - 10 * k, y + 7 * k, 90 * k, 2.2 * k) for x, y, k in fins], PALE)
# ---- the whale
block('whale')
w = orca(950, 1575, s=1.6, flip=True, rot=20.6, pal=dict(black=BLACK, white=PALE, saddle='#2c3944', tooth=PAPERW))
print({k: [round(v) for v in w[k]] for k in ('snout', 'chin', 'fliptip', 'backmid')})
