; ---------------- the planet: one radial gradient through all four colours
range ball white cyan magenta black
ink gradient ball 160 78 236 150 radial bayer
fellipse 190 105 62 51.7
ink solid
; cloud bands: nudge pixels one step darker along the range; they stop short of the night side
shade ball up 1
brush round 4
curve 136 78 178 84 220 83
brush round 3
curve 148 63 180 68 212 67
brush round 4
curve 141 133 176 139 212 138
brush round 2
curve 154 145 180 149 206 148
; the rings' shadow across the globe
brush round 3
curve 129 108 184 115 238 112
; one pale zone on the day side
shade ball down 1
brush round 2
curve 137 92 168 97 200 99
shade off
brush pixel
; near half of the rings goes back on, in front
stamp 66 105
; the globe's own shadow falling across the far rings
color black
fpoly 249 85 258 85 264 90 266 97 262 104 252 104
