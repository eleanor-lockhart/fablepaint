; ---------------- calm the back wall: flat paint, two soft steps of light
stencil only bwall
color bwall.3
frect 73 0 319 151
color bwall.4
frect 228 0 319 151
ink dither 8
frect 196 0 227 151
color bwall.2
frect 73 0 96 151
ink dither 4
frect 97 0 112 151
ink solid
color bwall.1
frect 70 0 73 160
stencil off
; shadows on the wall: under the shelf, beside the far posts
shade bwall down 1
frect 98 75 176 77
frect 76 100 79 126
frect 199 100 202 126
shade off
; the quilt's drop: plain colours again, a shade line under the mattress edge
color trim.4
frect 21 164 62 172
color f_blu_d
frect 63 164 88 172
color f_yel_d
frect 89 164 113 172
color f_red_d
frect 114 164 138 172
color leaf.5
frect 139 164 163 172
color f_pink_d
frect 164 164 187 172
color f_cream
frect 188 164 208 172
ink dither 8
color darkwood.1
frect 21 164 208 165
frect 21 171 208 172
ink solid

; ================= desk under the window =================
color wood.9
fpoly 216 109 310 109 319 113 319 123 222 123
color wood.11
draw 216 109 310 109
color wood.6
fpoly 216 110 222 124 222 188 216 160
color wood.8
frect 222 124 319 188
color wood.10
draw 222 124 319 124
color wood.5
rect 226 127 318 137
color darkwood.0
frect 228 139 284 188
color wood.5
rect 287 140 319 154
rect 287 156 319 171
rect 287 173 319 188
color f_yel_d
frect 270 131 273 132
frect 301 146 303 147
frect 301 163 303 164
frect 301 180 303 181
color wood.7
draw 230 130 262 130
draw 280 133 312 133
draw 290 149 298 149
draw 306 166 316 166

; ================= Macintosh SE =================
shade bwall down 1
fpoly 224 90 233 87 233 109 224 109
shade off
color plat.1
fpoly 233 87 237 90 237 116 233 110
color plat.3
fpoly 237 90 256 90 250 87 233 87
color plat.2
frect 237 90 256 116
color plat.3
draw 237 90 256 90
draw 237 90 237 116
color plat.1
draw 256 91 256 116
draw 238 116 256 116
frect 239 92 254 103
color f_wht
frect 240 93 253 102
color plat.1
dot 240 93 253 93 240 102 253 102
; what's on the screen: a paint program, a little house
color black
dot 241 93 243 93 244 93 246 93 248 93 249 93 251 93
draw 241 94 252 94
dot 241 96 241 98 241 100 242 97 242 99
draw 243 101 252 101
dot 247 96 246 97 247 97 248 97
draw 245 98 249 98
dot 245 99 249 99 245 100 249 100 247 100
dot 252 96
; grooves, drive slot, the six-colour apple
color plat.1
draw 238 105 255 105
draw 238 112 255 112
color black
draw 248 108 254 108
dot 251 109
color leaf.11
dot 239 107 240 107
color f_yel
dot 239 108
color f_org
dot 240 108
color f_red
dot 239 109
color f_blu
dot 240 109
; shadow it throws on the desk
shade wood down 2
fpoly 228 111 237 116 256 117 250 113
shade off
; keyboard, mouse on its mat, a few disks
color plat.2
fpoly 232 119 266 119 270 122 234 122
color plat.3
draw 232 119 266 119
color plat.1
dot 235 120 237 120 239 120 241 120 243 120 245 120 247 120 249 120 251 120 253 120 255 120 257 120 259 120 261 120 263 120 265 120
dot 236 121 238 121 240 121 242 121 250 121 258 121 260 121 262 121 264 121 266 121 268 121
draw 234 123 270 123
curve 250 118 249 117 247 116
color f_blu_d
fpoly 272 118 286 118 289 122 274 122
color plat.2
frect 276 119 280 121
color plat.3
draw 276 119 280 119
color plat.1
draw 276 120 280 120
curve 278 118 268 115 257 114
color f_blu_d
frect 224 120 229 122
color gray.12
dot 225 120 226 120
color f_wht
draw 225 122 228 122
color gray.4
frect 226 115 231 117
color gray.12
dot 227 115 228 115
color f_cream
draw 227 117 230 117
; lamp, books, pencil cup
color gray.3
fellipse 297 114 6 2
color gray.5
curve 297 113 302 98 291 88
color f_red
fpoly 284 86 292 84 295 90 286 93
color f_red_l
draw 285 86 291 85
color f_red_d
draw 287 93 295 90
color f_red_d
frect 300 107 314 109
color leaf.6
frect 301 105 313 106
color f_cream
draw 300 108 313 108
color gray.9
frect 307 99 311 104
color f_yel
draw 308 94 308 98
draw 310 95 310 98
color f_pink
dot 308 93 310 94
color f_blu
draw 309 96 309 98

; ================= chair, pushed back from the desk =================
color wood.9
fpoly 249 157 286 157 289 164 246 164
color wood.6
frect 246 164 289 168
frect 246 124 249 199
frect 286 124 289 199
frect 246 124 289 129
frect 249 150 286 153
frect 255 130 256 149
frect 262 130 263 149
frect 269 130 270 149
frect 276 130 277 149
frect 249 184 286 186
color wall.6
dot 246 124 289 124
color wood.8
draw 247 125 288 125
draw 289 126 289 199
draw 256 130 256 149
draw 263 130 263 149
draw 270 130 270 149
draw 277 130 277 149
draw 249 150 286 150
color wood.4
draw 246 126 246 199
draw 246 168 289 168

; ================= rag rug, bear on the bed =================
color f_blu_d
fpoly 222 189 319 189 319 199 215 199
color f_red_d
draw 221 191 319 191
draw 219 195 319 195
color f_cream
draw 220 193 319 193
draw 217 197 319 197
color wood.6
frect 246 189 249 199
frect 286 189 289 199
color wood.8
draw 289 189 289 199
fatbits 113 114 b=fawn.3 l=fawn.5 o=black m=f_cream c=fawn.5 d=fawn.1
.bb...bb...
bllb.bllb..
bbbbbbbbb..
bbobbbobb..
bbbmmmbbd..
.bbmomdd...
..bbbbd....
.bbbbbbb...
bbbcccbbd..
bbcccccbd..
bbcccccdd..
.bb.d.bd...
bbb...bdd..
end
