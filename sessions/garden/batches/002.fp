title "GARDEN.LBM"
pal 224 20 30 40 shed_d
pal 225 29 42 52 shed
pal 226 40 53 60 shed_l
defpattern board8
#.......
#.......
#.......
#.......
#.......
#.......
#.......
#.......
end
; ---------------- the woods beyond the fence
color leaf.2
frect 0 0 319 70
color sky.13
brush round 2
sprayrect 0 0 319 22 60
brush pixel
; trunks standing in the gloom
color earth.3
frect 148 0 152 62
frect 198 0 201 62
frect 234 0 239 62
frect 278 0 281 62
frect 306 0 309 62
color earth.5
draw 148 0 148 62
draw 198 0 198 62
draw 234 0 234 62
draw 278 0 278 62
draw 306 0 306 62
; foliage in layers, each lit from the upper left
color leaf.4
fcircle 20 20 22
fcircle 120 12 24
fcircle 176 28 20
fcircle 222 14 22
fcircle 262 32 20
fcircle 300 16 22
fcircle 60 40 18
fcircle 140 46 16
fcircle 210 46 16
fcircle 290 48 16
color leaf.6
fcircle 16 16 16
fcircle 116 8 18
fcircle 172 24 14
fcircle 218 10 16
fcircle 258 28 14
fcircle 296 12 16
fcircle 56 36 12
fcircle 136 42 11
fcircle 206 42 11
fcircle 286 44 11
color leaf.8
fcircle 12 12 10
fcircle 112 5 11
fcircle 168 20 8
fcircle 214 6 10
fcircle 254 24 8
fcircle 292 8 10
fcircle 52 32 7
fcircle 132 38 6
fcircle 202 38 6
fcircle 282 40 6
stencil only leaf
brush round 2
color leaf.10
sprayrect 0 0 319 50 220
color leaf.12
brush pixel
sprayrect 0 0 319 44 160
color leaf.3
brush round 2
sprayrect 0 10 319 68 200
color leaf.1
sprayrect 0 30 319 70 120
stencil off
brush pixel

; ---------------- the board fence
color fence.3
frect 0 58 319 112
ink pattern board8
color fence.1
frect 0 58 319 112
ink solid
stencil only fence.3
shade fence up 1
brush vline 30
sprayrect 0 58 319 112 40
shade fence down 1
sprayrect 0 58 319 112 34
shade off
stencil off
brush pixel
; rails
color fence.5
frect 0 68 319 70
frect 0 96 319 98
color fence.1
draw 0 71 319 71
draw 0 99 319 99
color fence.6
draw 0 68 319 68
draw 0 96 319 96
; sun and leaf-shadow moving on the boards
shade fence up 2
fcircle 110 80 9
fcircle 126 88 6
fcircle 170 76 8
fcircle 240 84 10
fcircle 258 76 5
fcircle 300 90 8
fcircle 196 92 5
shade fence up 1
ink dither 8
fcircle 114 82 13
fcircle 172 78 12
fcircle 242 86 14
fcircle 300 90 12
ink solid
shade fence down 1
fcircle 140 66 8
fcircle 210 64 9
fcircle 280 66 8
fcircle 150 104 7
fcircle 224 102 6
shade off
color leaf.1
draw 0 58 319 58

; ---------------- the big tree
color earth.3
fpoly 60 0 84 0 86 96 92 116 54 116 60 96
color earth.1
draw 66 0 67 60 65 112
draw 74 0 75 50 76 112
draw 80 0 81 70 84 112
color earth.6
draw 61 0 61 96
draw 62 20 63 90
draw 70 10 70 40
draw 71 60 71 100
color earth.8
draw 62 30 62 70
color earth.3
brush round 4
curve 82 30 104 18 124 0
brush pixel
color earth.6
curve 82 28 104 16 122 0
; its own leaves, hanging into the top of the picture
color leaf.5
fcircle 36 6 14
fcircle 96 4 12
fcircle 70 2 10
color leaf.8
fcircle 33 3 9
fcircle 93 1 8
color leaf.11
dot 28 2 34 6 40 1 90 3 96 6 30 9 100 2
color leaf.3
dot 40 14 46 10 86 12 104 10 74 9

; ---------------- lawn in broken sun
range lawn grass.5 grass.6 grass.7
ink gradient lawn 0 112 0 199 bayer
frect 0 112 319 199
ink solid
shade grass down 1
fellipse 60 150 50 9
fellipse 180 140 60 7
fellipse 280 176 50 10
fellipse 120 186 60 8
fellipse 250 128 40 5
shade grass up 1
fellipse 140 162 44 6
fellipse 230 190 46 7
fellipse 40 180 34 6
fellipse 290 148 26 5
shade grass up 2
fellipse 150 164 22 3
fellipse 236 192 24 3
fellipse 34 182 16 3
shade off
stencil only grass
brush vline 2
color grass.9
sprayrect 0 116 319 199 380
color grass.4
sprayrect 0 116 319 199 300
brush pixel
color grass.10
sprayrect 0 150 319 199 140
stencil off
