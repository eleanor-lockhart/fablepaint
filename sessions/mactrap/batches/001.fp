title "The Trap Door"
; ---------------- pantry walls
color black white
ink dither 3 opaque
frect 120 0 392 170
ink dither 6 opaque
fpoly 0 0 120 0 120 170 0 241
ink dither 5 opaque
fpoly 392 0 512 0 512 241 392 170
ink solid
; ---------------- board floor
color white
fpoly 120 170 392 170 512 241 512 341 0 341 0 241
color black
draw 120 0 120 170
draw 392 0 392 170
draw 120 170 392 170
draw 120 170 0 241
draw 392 170 512 241
draw 143 170 0 271
draw 165 170 0 316
draw 188 170 43 341
draw 211 170 114 341
draw 233 170 185 341
draw 256 170 256 341
draw 279 170 327 341
draw 301 170 398 341
draw 324 170 469 341
draw 347 170 512 316
draw 369 170 512 271
; grain and nail heads
brush hline 5
sprayrect 0 172 511 341 150
brush pixel
dot 150 178 172 178 196 178 220 178 244 178 268 178 292 178 316 178 340 178 362 178
dot 96 310 136 310 180 310 228 310 284 310 336 310 384 310 428 310
; soft shadow toward the walls
ink dither 4
fpoly 120 170 392 170 400 176 112 176
fpoly 120 170 0 241 0 262 126 176
fpoly 392 170 512 241 512 262 386 176
ink solid

; ---------------- the hole
fpoly 184 210 328 210 381 298 131 298
; far side: the thickness of the floor and a joist
color white
fpoly 186 211 326 211 325 220 187 220
color black
draw 186 216 326 216
; frame round the opening
poly 182 208 330 208 384 300 128 300
; ---------------- steps going down, each one dimmer
color white
frect 150 284 362 290
color black
rect 150 284 362 290
color white black
ink dither 13 opaque
frect 168 270 344 275
ink dither 9 opaque
frect 182 258 330 262
ink dither 5 opaque
frect 194 248 318 251
ink dither 3 opaque
frect 204 240 308 242
ink dither 1 opaque
frect 212 234 300 235
; stringers fading down
ink dither 10
draw 148 296 176 268
draw 364 296 336 268
ink dither 5
draw 176 268 198 246
draw 336 268 314 246
ink dither 2
draw 198 246 214 230
draw 314 246 298 230
; what the cellar gives back: a smear of bulb-light on the floor, the steel post
ink dither 2
fellipse 256 226 44 5
ink dither 3
frect 236 221 239 232
ink solid

; ---------------- the hatch, swung up on its hinges and leaning on the shelves
color black white
ink dither 7 opaque
fpoly 184 210 328 210 323 45 189 45
ink solid
color black
poly 184 210 328 210 323 45 189 45
draw 213 210 216 45
draw 242 210 243 45
draw 270 210 269 45
draw 299 210 296 45
; battens and brace on its underside
color white
ink dither 14 opaque
color white black
fpoly 188 70 324 70 324 84 188 84
fpoly 185 170 327 170 327 184 185 184
fpoly 190 170 202 170 322 84 310 84
ink solid
color black
poly 188 70 324 70 324 84 188 84
poly 185 170 327 170 327 184 185 184
draw 190 170 310 84
draw 202 170 322 84
dot 200 77 229 77 256 77 283 77 310 77 200 177 229 177 256 177 283 177 312 177
dot 201 77 230 77 257 77 284 77 311 77 201 177 230 177 257 177 284 177 313 177
; strap hinges
frect 204 203 226 212
frect 286 203 308 212
color white
dot 209 207 215 207 221 207 291 207 297 207 303 207
; its thickness along the top edge
color white
fpoly 189 45 323 45 321 40 191 40
color black
poly 189 45 323 45 321 40 191 40
