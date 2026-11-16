title "THEDESK.PIC"
; ---------------- wall: navy checker, brightening toward where the monitor will glow
color blue black
ink dither 8 opaque
frect 0 0 319 139
ink dither 10 opaque
fellipse 160 84 114 82
ink dither 12 opaque
fellipse 160 84 100 72
ink dither 14 opaque
fellipse 160 84 86 62
ink solid
fellipse 160 84 70 50

; ---------------- window
color white
frect 16 16 86 98
color lgray
draw 86 16 86 98
draw 16 98 86 98
range night black blue
ink gradient night 0 10 0 112 bayer
frect 19 19 83 95
ink solid
color black
frect 19 86 26 95
frect 27 80 34 95
frect 35 89 42 95
frect 43 83 49 95
frect 52 87 59 95
frect 60 76 67 95
frect 68 84 75 95
frect 76 90 83 95
draw 63 70 63 76
color lred
dot 63 70
color yellow
dot 21 89 24 92 29 83 32 86 29 90 32 93 45 86 47 91 54 90 57 93 62 79 65 82 62 86 65 90 62 93 70 87 73 91 78 93 38 92
color white
dot 24 24 38 30 30 44 44 22 22 60 40 66 58 62 74 52 80 26 56 40 78 70 34 54
color lgray
dot 28 34 46 48 60 28 70 64 26 72 76 40
fatbits 64 26 m=yellow w=white
...ww.
....ww
....wm
....wm
w..wwm
.wwwm.
..mm..
end
color white
frect 50 19 52 95
frect 19 56 83 57
color lgray
draw 52 19 52 95
draw 19 57 83 57
color white
frect 12 99 90 101
color lgray
draw 12 102 90 102
color black
draw 14 103 90 103

; ---------------- bookshelf
color brown
frect 230 60 314 63
color yellow
draw 230 60 314 60
color black
draw 232 64 314 64
color dgray
draw 240 64 240 70 246 64
draw 304 64 304 70 298 64
color red
frect 234 34 239 59
color lred
draw 234 34 234 59
color yellow
frect 235 38 239 39
draw 235 54 239 54
color green
frect 240 38 243 59
color lgreen
draw 240 38 240 59
color white
dot 242 42 242 44 242 46
color lblue
frect 244 32 250 59
color white
frect 245 36 249 40
draw 244 32 244 59
color blue
draw 250 32 250 59
color yellow
frect 251 40 254 59
color brown
draw 254 40 254 59
frect 251 44 253 45
color magenta
frect 255 35 261 59
color lmagenta
draw 255 35 255 59
color white
frect 256 39 260 40
draw 256 55 260 55
frect 262 37 265 59
color lgray
draw 265 37 265 59
color red
frect 262 42 264 44
color cyan
frect 266 33 272 59
color lcyan
draw 266 33 266 59
color black
frect 267 37 271 38
frect 267 52 271 53
color lred
fpoly 274 59 280 59 287 39 281 37
color white
draw 275 57 282 39
color red
draw 280 59 287 39
; a certain cube
color black
frect 293 50 305 59
color red
frect 294 51 296 52
color white
frect 298 51 300 52
color lgreen
frect 302 51 304 52
color yellow
frect 294 54 296 55
color lblue
frect 298 54 300 55
color lred
frect 302 54 304 55
color lgreen
frect 294 57 296 58
color yellow
frect 298 57 300 58
color white
frect 302 57 304 58

; ---------------- desk
color brown
frect 0 140 319 171
ink dither 4
color yellow
stencil only brown
fellipse 286 158 58 20
ink dither 8
fellipse 288 158 40 13
stencil off
color black
brush hline 14
sprayrect 0 143 319 169 16
color yellow
brush hline 10
sprayrect 0 143 230 169 10
ink solid
brush pixel
color yellow
draw 0 171 319 171
color black
draw 0 140 319 140
ink dither 8 opaque
color brown black
frect 0 172 319 199
ink solid
color black
rect 20 176 140 196
rect 180 176 300 196
color yellow
frect 76 185 84 186
frect 236 185 244 186
color white
dot 76 185 236 185
