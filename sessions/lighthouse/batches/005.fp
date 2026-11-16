; stronger beam near the lamp
shade sky up 1
fpoly 232 51 150 43 150 52 232 54
fpoly 240 51 319 43 319 55 240 54
ink dither 8
fpoly 232 50 90 34 90 50 232 55
shade off
ink solid
; flare off the lens
color lamp.1
draw 227 52 230 52
draw 242 52 245 52
color lamp.2
dot 226 52 246 52 236 44 236 43
; chimney smoke drifting off
color tower.3
dot 276 105 277 103 277 102 279 100 280 99 282 97 283 97 285 95 288 94
color tower.2
dot 276 104 278 101 281 98 284 96 286 95 290 93
; streaks inside the big clouds
stencil only cloud.5
color cloud.4
brush hline 9
dot 222 67 240 69 262 66 282 68 300 70 60 88 34 86 78 87
color cloud.6
brush hline 6
dot 232 71 268 71 294 72 44 90 70 90
brush pixel
stencil off
; signed, as one did
color sea.5
text 3 192 "FABLE 5.2" tiny
