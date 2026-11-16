title "Our House"
defpattern roofp
........
########
########
###.####
........
########
########
#######.
end
defpattern shake
########
..#.....
..#.....
..#.....
########
......#.
......#.
......#.
end
defpattern grass
........
...#....
..#.....
........
........
.......#
......#.
........
end
; ---------------- sky: a light grey, so the clouds can be white
color black white
ink dither 2 opaque
frect 0 0 511 240
; lawn
ink pattern grass opaque
frect 0 236 511 341
ink solid
; ---------------- clouds: black a pixel bigger, white on top = an outline for free
color black
fcircle 36 50 13
fcircle 60 40 19
fcircle 88 32 23
fcircle 120 40 19
fcircle 150 48 13
frect 30 46 156 59
fcircle 330 38 15
fcircle 352 30 18
fcircle 376 38 14
frect 322 36 384 47
color white
fcircle 36 50 12
fcircle 60 40 18
fcircle 88 32 22
fcircle 120 40 18
fcircle 150 48 12
frect 30 46 156 58
fcircle 330 38 14
fcircle 352 30 17
fcircle 376 38 13
frect 322 36 384 46
color black
ink dither 3
fellipse 92 53 58 5
fellipse 352 43 30 3
fellipse 110 44 12 4
fellipse 62 46 10 3
ink solid
; ---------------- trees behind the house
color black
fpoly 250 6 244 20 248 21 238 38 243 39 231 58 237 59 224 80 231 81 217 102 225 103 212 124 300 124 285 103 292 102 277 81 284 80 270 59 276 58 263 39 268 38 257 21 261 20
fpoly 306 30 300 46 304 47 294 66 299 67 288 88 294 89 283 110 290 111 280 130 340 130 328 111 334 110 322 89 328 88 317 67 322 66 311 47 315 46
color white
brush hline 3
stencil only black
sprayrect 214 20 252 124 90
sprayrect 282 44 306 130 50
brush pixel
sprayrect 214 20 300 124 80
sprayrect 282 44 340 130 50
stencil off
; far trees, left and right
color black
ink dither 10 opaque
fcircle 14 150 22
fcircle 44 162 16
fcircle 430 120 34
fcircle 480 110 40
fcircle 500 150 30
fcircle 400 150 22
ink dither 5 opaque
fcircle 8 142 12
fcircle 420 108 18
fcircle 470 92 22
ink solid
color black
circle 14 150 22
circle 44 162 16

; ================= the house =================
; long roof
ink pattern roofp opaque
fpoly 115 73 272 126 358 198 249 187
ink solid
color black
poly 115 73 272 126 358 198 249 187
draw 115 72 272 125
; gable wall, sunlit
ink pattern shake opaque
fpoly 115 82 31 178 32 288 250 248 250 192
ink solid
poly 115 82 31 178 32 288 250 248 250 192
; side wall, in shade
ink pattern shake opaque
fpoly 250 192 358 203 358 266 250 248
ink dither 6
fpoly 250 192 358 203 358 266 250 248
ink solid
draw 250 192 250 248
; rake boards and eave fascia, painted white
color white
fpoly 115 73 7 178 7 185 115 81
fpoly 115 73 249 187 249 194 115 81
fpoly 249 187 358 198 358 203 249 192
color black
poly 115 73 7 178 7 185 115 81
poly 115 73 249 187 249 194 115 81
poly 249 187 358 198 358 203 249 192
; attic vent
color white
frect 111 125 129 153
color black
rect 111 125 129 153
draw 113 129 127 129
draw 113 133 127 133
draw 113 137 127 137
draw 113 141 127 141
draw 113 145 127 145
draw 113 149 127 149
; window on the gable
color white
frect 170 190 202 220
color black
rect 170 190 202 220
frect 174 194 198 203
frect 174 207 198 216
color white
draw 178 202 186 195
draw 180 202 188 195
draw 178 215 184 209
; windows down the side wall
color white
fpoly 268 200 282 201 282 234 268 232
fpoly 298 204 310 205 310 236 298 235
fpoly 328 207 339 208 339 240 328 239
color black
poly 268 200 282 201 282 234 268 232
poly 298 204 310 205 310 236 298 235
poly 328 207 339 208 339 240 328 239
fpoly 271 204 279 205 279 215 271 214
fpoly 271 218 279 219 279 230 271 229
fpoly 301 208 307 209 307 218 301 217
fpoly 301 221 307 222 307 232 301 231
fpoly 331 211 336 212 336 221 331 220
fpoly 331 224 336 225 336 236 331 235
; door hood, door, the window beside it
color black
fpoly 50 184 86 158 122 180 122 186 86 166 50 190
color white
fpoly 60 186 86 169 112 183
color black
poly 60 186 86 169 112 183
color white
frect 55 187 58 246
frect 114 184 117 246
frect 79 194 107 246
frect 41 190 65 246
color black
rect 55 187 58 246
rect 114 184 117 246
rect 79 194 107 246
rect 41 190 65 246
frect 84 200 102 220
frect 45 194 61 216
frect 45 220 61 242
color white
draw 87 218 96 202
draw 89 218 98 202
draw 53 194 53 242
draw 47 214 52 200
color black
rect 84 226 102 241
fcircle 104 224 1

; ================= back end: one storey, flat roof, railed porch on top =================
ink pattern shake opaque
fpoly 358 172 478 170 478 190 358 190
ink solid
color white
frect 356 167 480 171
frect 360 150 476 166
color black
rect 356 167 480 171
rect 360 150 476 153
frect 360 150 363 166
frect 388 150 391 166
frect 416 150 419 166
frect 444 150 447 166
frect 473 150 476 166
ink pattern vlines4
frect 364 154 472 166
ink solid
; kitchen porch below it
ink dither 12 opaque
fpoly 358 206 478 204 478 262 358 264
ink pattern roofp opaque
fpoly 352 190 478 186 482 201 356 204
ink solid
color black
poly 352 190 478 186 482 201 356 204
color white
fpoly 356 204 482 201 482 205 356 208
color black
poly 356 204 482 201 482 205 356 208
color white
frect 367 208 371 264
frect 471 206 475 262
frect 387 212 412 261
frect 431 212 457 248
frect 354 262 484 268
color black
rect 367 208 371 264
rect 471 206 475 262
rect 387 212 412 261
rect 431 212 457 248
rect 354 262 484 268
frect 392 217 407 234
frect 435 216 453 229
frect 435 233 453 244
color white
draw 395 232 403 219
draw 439 228 446 218
color black
rect 392 240 407 256
fcircle 409 238 1
; hanging basket and a chair
draw 380 208 380 220
fcircle 380 226 7
color white
dot 376 223 380 221 384 224 378 228 383 229 376 230 381 226
draw 375 233 374 238
draw 385 233 387 239
color white
frect 418 240 428 242
color black
rect 418 228 428 242
draw 418 242 418 258
draw 428 242 428 258
draw 418 234 428 234
