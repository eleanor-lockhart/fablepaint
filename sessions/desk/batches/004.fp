; cat fixes: lose the whiskers that landed on its own back, separate head from body
ink dither 8 opaque
color yellow brown
draw 165 29 160 28
draw 165 31 160 32
ink solid
color brown
curve 169 21 166 27 169 33
draw 170 34 181 34

; ---------------- keyboard
ink dither 8
color black
frect 96 170 230 170
ink solid
color lgray
fpoly 100 156 220 156 226 167 94 167
color dgray
frect 94 168 226 169
color white
draw 100 156 220 156
fpoly 103 158 217 158 221 165 99 165
color lgray
draw 100 160 220 160
draw 98 163 222 163
ink pattern vlines4
frect 99 158 221 159
frect 99 161 221 162
frect 99 164 139 165
frect 181 164 221 165
ink solid
frect 114 158 116 165
frect 196 158 198 165

; ---------------- mouse
ink dither 8
color black
fellipse 248 164 6 3
ink solid
color lgray
fellipse 245 161 5 4
color white
draw 241 159 243 158 246 158
color dgray
draw 245 157 245 160
draw 241 161 249 161
curve 245 156 240 151 229 153

; ---------------- coffee
ink dither 8
color black
fellipse 55 152 9 2
ink solid
color red
brush round 2
ellipse 56 144 4 4
brush pixel
frect 58 136 72 151
fellipse 65 151 7 2
color lred
frect 59 137 61 150
ink dither 8
color black
frect 69 137 72 152
ink solid
color lred
fellipse 65 136 7 2
color black
fellipse 65 136 5 1
color brown
draw 61 136 66 136
color white
spline 63 131 61 126 64 121 62 116
color lgray
spline 68 130 70 125 67 120 69 113
dot 65 112 66 110

; ---------------- cactus
ink dither 8
color black
fellipse 26 158 10 2
ink dither 8 opaque
color lred brown
fpoly 22 147 38 147 36 158 24 158
ink solid
color lred
frect 21 144 39 146
color brown
draw 36 148 35 158
draw 21 147 39 147
color green
fellipse 30 132 6 12
fellipse 39 131 2 4
draw 36 134 39 134
draw 36 135 39 135
color lgreen
draw 27 124 27 142
draw 31 121 31 143
dot 39 128 39 130 39 132
color yellow
dot 25 127 25 133 25 139 29 124 29 130 29 136 33 126 33 132 33 138 35 129 35 136 41 129
color lmagenta
dot 29 119 30 118 31 119 30 120
color white
dot 30 119

; ---------------- floppies under the lamp
color dgray
frect 270 160 287 169
color black
frect 271 161 286 168
color white
frect 273 165 284 167
color red
draw 274 166 282 166
color blue
frect 257 156 274 165
color lblue
draw 257 156 274 156
draw 257 156 257 165
color lgray
frect 262 157 269 159
color dgray
frect 265 157 266 158
color white
frect 259 161 272 164
color blue
draw 260 162 269 162
draw 260 163 266 163

; ---------------- banker's lamp and its light
stencil only black
color blue
fpoly 280 119 312 119 319 132 319 139 262 139
stencil off
ink dither 4
color lblue
fpoly 284 119 308 119 316 139 272 139
ink solid
color brown
fellipse 296 151 11 3
color yellow
draw 287 150 291 149 298 149
frect 295 120 296 149
color brown
draw 297 120 297 149
color green
fellipse 296 113 19 6
color blue
frect 276 118 316 120
color yellow
draw 280 118 312 118
color white
draw 286 118 306 118
ink dither 8
color lgreen
fellipse 290 110 11 2
ink solid
color white
draw 284 109 288 108
color yellow
frect 276 112 277 115
frect 315 112 316 115
dot 308 120 308 122 308 124 308 126
color white
dot 308 127

; ---------------- memo pinned to the wall
color brown
frect 212 79 224 90
color yellow
frect 211 78 223 89
color brown
draw 213 82 221 82
draw 213 84 219 84
draw 213 86 220 86
color lred
dot 217 78 217 79

; signed
color yellow
text 4 193 "FABLE 5.2" tiny
