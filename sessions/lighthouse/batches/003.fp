; taper the streaks near the sun
stencil protect suncore sunrim
color cloud.5
draw 0 108 76 108
draw 126 113 194 113
stencil off

; ---------------- sea: glare line, the sun's road, wave texture
color sunrim
draw 56 128 150 128
color suncore
draw 86 128 114 128
shade sea up 2
brush hline 6
sprayrect 0 131 319 150 70
brush hline 9
sprayrect 0 150 319 175 50
brush hline 12
sprayrect 0 172 319 199 34
shade sea down 2
brush hline 8
sprayrect 0 140 319 199 60
shade off
brush hline 7
color glint.0
sprayrect 92 129 108 134 10
color glint.1
sprayrect 90 129 110 137 10
color glint.2
sprayrect 88 130 112 140 10
brush hline 5
color glint.0
sprayrect 88 135 112 150 12
color glint.3
sprayrect 84 135 116 155 14
color glint.1
sprayrect 84 140 116 160 12
color glint.5
sprayrect 82 138 118 158 10
brush hline 4
color glint.2
sprayrect 78 152 122 175 14
color glint.6
sprayrect 78 155 122 180 12
color glint.0
sprayrect 80 150 120 172 8
color glint.4
sprayrect 76 160 124 185 10
brush hline 3
color glint.7
sprayrect 70 172 130 198 14
color glint.1
sprayrect 72 176 128 198 10
color glint.3
sprayrect 70 170 130 198 12
brush pixel

; ---------------- far headland
color farland
fpoly 0 120 14 118 30 121 48 124 66 126 84 128 0 128
color farlit
draw 0 120 14 118 30 121 48 124 66 126 83 127

; ---------------- the headland: rock face on the left, grass slope on the right
color rock.2
fpoly 118 199 126 190 134 184 138 174 148 168 154 158 166 152 176 144 190 139 204 136 220 134 262 133 288 135 319 133 319 199
color grass.1
fpoly 190 139 204 136 220 134 262 133 288 135 319 133 319 199 192 199 188 188 196 176 190 162 196 150

; ---------------- lighthouse
; halo round the lantern
shade sky up 2
ink dither 8
fcircle 236 52 16
ink solid
fcircle 236 52 9
shade off
; tower, lit from the left
ink gradient tower 249 0 223 0 bayer
fpoly 225 136 229 62 243 62 247 136
stencil only tower
ink gradient stripe 249 0 223 0 bayer
frect 220 76 252 89
frect 220 104 252 117
stencil off
ink solid
color tower.7
draw 229 62 225 136
; gallery and railing
color tower.1
frect 225 59 247 61
draw 227 62 245 62
draw 225 55 247 55
dot 225 56 225 57 225 58 228 56 228 57 228 58 231 56 231 57 234 56 234 57 238 56 238 57 241 56 241 57 244 56 244 57 244 58 247 56 247 57 247 58
color tower.6
draw 225 59 227 59
dot 225 55 225 56
; lantern room
color lamp.1
frect 231 46 241 58
color lamp.0
frect 234 48 238 56
color lamp.2
draw 232 47 232 57
draw 240 47 240 57
color rock.0
draw 231 46 231 58
draw 241 46 241 58
draw 231 46 241 46
color rock.1
draw 234 47 234 54
draw 238 47 238 54
; roof and finial
color stripe.1
fpoly 229 46 232 41 236 38 240 41 243 46
color stripe.4
draw 230 45 233 41 236 38
color rock.0
draw 229 46 243 46
draw 236 32 236 37
dot 235 36 237 36
; door and lit windows
color rock.0
frect 234 125 238 136
draw 235 124 237 124
color lamp.2
frect 235 66 236 70
frect 235 94 236 98
color rock.1
draw 234 65 237 65
draw 234 93 237 93

; ---------------- keeper's cottage
ink dither 6 opaque
color tower.3 tower.2
frect 250 121 282 135
ink solid
color roofdark
fpoly 247 121 252 113 280 113 285 121
color roofmid
fpoly 248 120 252 114 262 114 258 120
color rooflit
draw 248 120 252 113 280 113
color roofdark
frect 274 107 277 113
color rooflit
draw 274 107 274 112
color lamp.1
frect 255 125 259 130
frect 271 125 275 130
color lamp.0
frect 256 126 258 129
frect 272 126 274 129
color rock.1
draw 257 125 257 130
draw 255 127 259 127
draw 273 125 273 130
draw 271 127 275 127
color roofdark
frect 263 125 267 135
color lamp.2
dot 266 130
