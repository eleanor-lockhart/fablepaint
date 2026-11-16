; ---------------- right wall: wainscot in perspective
color darkwood.5
fpoly 254 76 319 84 319 172 254 130
color darkwood.2
draw 258 77 258 133
draw 262 77 262 135
draw 266 78 266 138
draw 312 84 312 168
draw 317 84 317 171
color darkwood.7
draw 254 75 319 83
color darkwood.6
draw 254 76 319 84
; ---------------- pantry doorway
color wood.9
fpoly 269 32 307 24 307 166 269 142
color wood.11
draw 269 32 269 142
draw 269 32 307 24
color wood.6
draw 307 25 307 166
; the room beyond: dim wall, shelves square-on
color wall.1
fpoly 272 36 304 29 304 163 272 142
color wood.3
fpoly 272 142 304 141 304 163
color darkwood.1
draw 272 141 304 141
; bare bulb and its pool of light
shade wall up 1
fcircle 289 46 12
shade wall up 1
fcircle 289 44 6
shade off
color gray.7
draw 289 31 289 39
color glow
frect 288 40 290 42
color f_yel_l
dot 289 43
; shelf boards
color wood.8
frect 272 54 304 54
frect 272 75 304 75
frect 272 96 304 96
frect 272 117 304 117
color wood.3
frect 272 55 304 55
frect 272 76 304 76
frect 272 97 304 97
frect 272 118 304 118
; top shelf: boxes and tins
color f_org_d
frect 274 45 278 53
color f_cream
frect 275 47 277 49
color gray.9
frect 280 48 284 53
color gray.12
draw 280 48 284 48
color f_blu_d
frect 296 44 301 53
color f_wht_d
frect 297 46 300 48
; second shelf: put-up jars
fatbits 273 65 l=gray.10 g=f_org h=f_peach d=f_org_d
lllll
ghggd
ghggd
gggdd
ghggd
ggggd
ggggd
ggggd
dgggd
end
fatbits 279 65 l=gray.10 g=leaf.7 h=leaf.11 d=leaf.4
lllll
ghggd
ghggd
gggdd
ghggd
ggggd
ggggd
ggggd
dgggd
end
fatbits 285 65 l=gray.10 g=f_red_d h=f_red d=shake.2
lllll
ghggd
ghggd
gggdd
ghggd
ggggd
ggggd
ggggd
dgggd
end
fatbits 291 65 l=gray.10 g=f_pur_d h=f_pur d=shake.1
lllll
ghggd
ghggd
gggdd
ghggd
ggggd
ggggd
ggggd
dgggd
end
fatbits 297 65 l=gray.10 g=f_yel_d h=f_yel d=gold.1
lllll
ghggd
ghggd
gggdd
ghggd
ggggd
ggggd
ggggd
dgggd
end
; third shelf: tins
fatbits 274 87 t=gray.11 a=f_red b=f_wht_d s=f_red_d
ttttt
aaaas
aaaas
bbbbs
bbbbs
aaaas
aaaas
aaaas
tttts
end
fatbits 280 87 t=gray.11 a=leaf.7 b=f_cream s=leaf.4
ttttt
aaaas
bbbbs
bbbbs
aaaas
aaaas
aaaas
aaaas
tttts
end
fatbits 286 87 t=gray.11 a=f_yel_d b=leaf.6 s=gold.1
ttttt
aaaas
aaaas
bbbbs
aaaas
aaaas
aaaas
aaaas
tttts
end
fatbits 292 87 t=gray.11 a=f_red b=f_wht_d s=f_red_d
ttttt
aaaas
aaaas
bbbbs
bbbbs
aaaas
aaaas
aaaas
tttts
end
fatbits 298 89 t=gray.11 a=f_blu_d b=f_wht_d s=shake.1
ttttt
aaaas
bbbbs
aaaas
aaaas
aaaas
tttts
end
; bottom shelf: flour sack, pot, sack of potatoes; broom below
color f_cream
frect 274 106 281 116
color f_wht_d
draw 274 106 281 106
color f_red_d
frect 276 110 279 112
color gray.8
frect 284 110 292 116
color gray.12
draw 283 109 293 109
color gray.5
draw 292 111 292 116
color earth.6
frect 295 105 302 116
color earth.8
draw 296 106 296 115
color earth.4
dot 298 108 300 111 297 113 301 114
color wood.10
draw 277 120 279 140
color f_yel_d
fpoly 278 136 281 136 283 141 276 141
; the hatch in the pantry floor: just its edge and its ring
color darkwood.0
draw 284 143 302 148
draw 284 143 303 143
color gray.11
dot 297 146 298 146

; ---------------- calendar between the corner and the doorway
color f_wht
fpoly 258 47 267 45 267 67 258 68
color sky.10
fpoly 258 47 267 45 267 54 258 56
color leaf.8
fpoly 258 53 267 51 267 55 258 57
color f_red
draw 258 57 267 56
color gray.9
dot 260 60 262 60 264 59 266 59 260 62 262 62 264 61 266 61 260 64 262 64 264 63 266 63 260 66 262 66 264 65
color gray.5
dot 262 46

; ---------------- crown line and ceiling light
color wall.3
draw 45 0 96 30 254 30 319 10
color wall.2
draw 97 31 253 31
draw 255 31 319 11
shade wall up 1
ink dither 8
fellipse 150 16 46 15
ink solid
fellipse 150 16 28 10
shade off
color glow
fpoly 142 23 158 23 161 10 139 10
color f_wht
fpoly 144 22 156 22 158 12 142 12
color wood.6
draw 142 23 158 23
draw 139 10 161 10
color wood.8
draw 142 23 139 10
draw 158 23 161 10

; ---------------- the yellow step stool under the phone
fatbits 166 109 y=f_yel_d Y=f_yel c=gray.11 g=gray.4 t=gray.8 d=gold.1
....yyyyyyyyyy......
...yyyyyyyyyyyy.....
...yYYYYYYYYYYy.....
...yyyyyyyyyyyy.....
....yyyyyyyyyy......
....c........c......
....c........c......
....c........c......
....c........c......
....c........c......
..yYYYYYYYYYYYYy....
.yyyyyyyyyyyyyyyy...
.dddddddddddddddd...
..c..........c......
..c..........c......
..c.tttttttt.c......
.c..gggggggg..c.....
.c............c.....
.c............c.....
.c.tttttttttt.c.....
c..gggggggggg..c....
c..............c....
c..............c....
end

; ---------------- upper cabinets on the left wall
; soffit
color wall.5
fpoly 74 2 104 26 104 31 74 11
color wall.6
frect 48 2 74 10
; fronts (turned away from the window) and the end panel (facing us)
color wood.7
fpoly 74 11 104 31 104 70 74 75
color wood.10
frect 48 11 74 75
color wood.9
draw 52 12 52 74
draw 58 12 58 74
draw 63 12 63 74
draw 69 12 69 74
color wood.11
draw 55 12 55 74
draw 66 12 66 74
color wood.5
draw 74 11 74 75
color wood.4
draw 85 18 85 74
draw 93 24 93 72
draw 99 28 99 71
draw 74 11 104 31
draw 74 75 104 70
color wood.9
draw 76 14 76 73
draw 86 20 86 72
draw 94 25 94 71
color f_yel_d
dot 83 66 91 65 97 64 102 63
color wood.3
draw 48 75 74 75
draw 48 11 74 11
