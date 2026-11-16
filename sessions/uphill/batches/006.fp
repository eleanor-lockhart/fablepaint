; ---- porch floor: shade under the roof, doormat, chair; put the yew back in front of it
color gray.5
fpoly 203 153 240 149 262 143 275 143 242 158 190 155
color roof.3
fpoly 224 149 238 147 240 150 226 152
fatbits 205 139 w=trim.3 s=trim.4
w.....w.
w.....w.
wwwwwww.
w.....w.
wwwwwww.
w.....w.
wwwwwwww
wsssssww
w.....ww
w.....w.
w.....w.
end
color pine.1
fcircle 263 149 11
stencil only pine.1
color pine.3
fcircle 261 147 9
stencil only pine.3
color pine.5
fcircle 259 145 6
stencil only pine.1 pine.3 pine.5
brush hline 2
color pine.4
sprayrect 252 138 275 160 50
color pine.6
sprayrect 253 139 264 148 16
color pine.2
sprayrect 258 146 275 160 26
stencil off
brush pixel
; black-eyed susans the slab had covered
fatbits 253 161 y=f_yel d=earth.1
.y.
ydy
.y.
end
fatbits 263 160 y=f_yel d=earth.1
.y.
ydy
.y.
end

; ---- fill the bare soil of the long bed: foliage, a lavender drift, alyssum
stencil only earth.3
brush round 2
color leaf.5
sprayrect 40 172 122 186 110
color leaf.7
sprayrect 40 172 122 184 60
sprayrect 244 150 319 172 60
stencil only earth.3 leaf.5 leaf.7
brush pixel
color f_lilac
sprayrect 66 175 92 181 34
color f_pur_l
sprayrect 66 175 92 181 14
color f_wht
sprayrect 96 173 118 178 18
stencil off

; ---- give the spruces boughs: light on the upper left of each tier, dark beneath
stencil only pine
brush hline 3
color pine.5
draw 177 8 186 4
draw 173 20 185 15
draw 169 32 182 27
draw 164 45 178 40
draw 160 58 175 52
draw 156 71 172 65
draw 152 84 169 78
draw 149 97 166 91
draw 224 9 234 5
draw 219 22 232 17
draw 214 35 229 30
draw 209 49 225 43
draw 205 63 222 57
draw 201 77 219 71
draw 197 91 216 85
draw 194 105 212 99
brush hline 2
color pine.6
draw 174 21 180 18
draw 170 33 177 30
draw 165 46 173 43
draw 161 59 170 55
draw 157 72 166 68
draw 153 85 162 81
draw 220 23 227 20
draw 215 36 223 33
draw 210 50 219 46
draw 206 64 215 60
draw 202 78 211 74
draw 198 92 207 88
brush hline 3
color pine.0
draw 180 11 190 11
draw 176 23 192 23
draw 172 35 196 35
draw 168 48 200 48
draw 164 61 204 61
draw 160 74 208 74
draw 156 87 212 87
draw 153 100 216 100
draw 227 12 238 12
draw 222 25 242 25
draw 217 38 247 38
draw 212 52 251 52
draw 208 66 255 66
draw 204 80 259 80
draw 200 94 263 94
draw 197 108 266 108
stencil off
brush pixel
; treetops over the ridge
color leaf.11
dot 46 66 48 65 50 66 84 67 86 66 57 67 59 68 44 69
color leaf.2
dot 53 74 56 75 91 75 94 74 43 75 62 74

; ---- cast shadows
shade grass down 2
fellipse 168 192 9 2
fellipse 60 190 10 2
shade earth down 2
fellipse 293 148 5 2
fellipse 318 157 6 3
fellipse 276 152 5 2
shade off

; ---- foreground: daylilies and black-eyed susans close to the eye, bottom right
color leaf.3
fellipse 288 200 38 9
brush round 2
color leaf.5
curve 276 199 268 184 258 180
curve 284 199 280 180 270 172
curve 292 199 296 178 306 170
curve 300 199 308 184 318 180
curve 288 199 288 178 286 166
color leaf.8
curve 278 199 272 186 264 182
curve 286 199 283 182 276 174
curve 290 199 293 180 300 172
curve 298 199 304 186 312 181
curve 289 199 290 182 291 170
color leaf.12
brush pixel
curve 280 199 276 188 269 184
curve 288 199 286 184 280 176
curve 293 199 296 184 303 175
curve 301 199 306 190 314 184
color leaf.7
draw 272 177 274 190
draw 287 170 288 186
draw 303 175 300 190
draw 295 185 294 196
fatbits 268 169 o=f_org p=f_org_d y=f_yel
....o....
.o..o..o.
.oo.o.oo.
..ooyoo..
ppyyyyypp
..ppypp..
.pp.p.pp.
.p.....p.
end
fatbits 283 162 o=f_org p=f_org_d y=f_yel
....o....
.o..o..o.
.oo.o.oo.
..ooyoo..
ppyyyyypp
..ppypp..
.pp.p.pp.
.p.....p.
end
fatbits 299 167 o=f_org p=f_org_d y=f_yel
....o....
.o..o..o.
.oo.o.oo.
..ooyoo..
ppyyyyypp
..ppypp..
.pp.p.pp.
.p.....p.
end
fatbits 290 178 o=f_org p=f_org_d y=f_yel
....o....
.o..o..o.
.oo.o.oo.
..ooyoo..
ppyyyyypp
..ppypp..
.pp.p.pp.
.p.....p.
end
; buds
color f_org_d
draw 311 172 312 176
draw 262 176 263 179
color f_org
dot 311 172 262 176
; black-eyed susans in front of them
color leaf.6
draw 252 191 252 199
draw 262 196 262 199
draw 245 197 245 199
fatbits 249 186 y=f_yel e=f_yel_d d=earth.1
..y.y..
.yyyyy.
yyyddyy
.eeddye
.eeeee.
..e.e..
end
fatbits 259 191 y=f_yel e=f_yel_d d=earth.1
..y.y..
.yyyyy.
yyyddyy
.eeddye
.eeeee.
..e.e..
end
fatbits 241 193 y=f_yel e=f_yel_d d=earth.1
..y.y..
.yyyyy.
yyyddyy
.eeddye
.eeeee.
..e.e..
end
; one cabbage white over the delphiniums
color f_wht
dot 110 150 112 150
color gray.9
dot 111 151
