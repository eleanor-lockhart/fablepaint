; the roof read as clay tile: calm the reds in the palette, then relay it as worn asphalt
pal 60 26 9 11
ramp 56 60
pal 64 39 17 16
ramp 60 64
pal 67 55 35 29
ramp 64 67
defpattern tabs2
........
#.......
#.......
........
........
....#...
....#...
........
end
color roof.6
fpoly 10 72 170 78 201 116 30 126
color roof.5
draw 11 76 172 81
draw 13 80 174 83
draw 14 84 177 86
draw 16 87 179 89
draw 17 91 181 92
draw 19 95 183 94
draw 20 99 186 97
draw 21 103 188 100
draw 23 107 190 102
draw 24 111 192 105
draw 26 114 194 108
draw 27 118 197 111
draw 29 122 199 113
stencil only roof.6
ink pattern tabs2
fpoly 10 72 170 78 201 116 30 126
ink solid
brush hline 2
color roof.7
sprayrect 10 72 201 126 240
color roof.5
sprayrect 10 72 201 126 110
stencil off
brush pixel
shade roof up 1
ink dither 7
fpoly 10 72 170 78 180 90 16 88
ink dither 3
fpoly 16 88 180 90 190 102 22 104
shade roof down 1
ink dither 5
fpoly 26 114 194 108 201 116 30 126
; rain streaks below the vents
ink dither 8
brush vline 5
dot 49 82 49 90 116 84 116 92 163 86 100 90 100 98 142 86
shade off
ink solid
brush pixel
color roof.10
draw 10 72 170 78
color roof.8
draw 10 73 170 79
color darkwood.4
brush round 2
draw 172 79 202 116
color darkwood.5
draw 10 73 30 126
draw 10 72 0 88
brush pixel
color roof.9
draw 30 125 201 115
color darkwood.3
draw 30 126 201 116
draw 31 127 201 117
color shake.1
draw 32 128 201 118
draw 35 129 201 119
fatbits 47 75 a=roof.2 b=roof.10 c=roof.0
bbb.
aac.
.ccc
end
fatbits 114 77 a=roof.2 b=roof.10 c=roof.0
bbb.
aac.
.ccc
end
fatbits 161 79 a=roof.2 b=roof.10 c=roof.0
bbb.
aac.
.ccc
end
fatbits 99 79 p=gray.9 h=gray.13 s=roof.2
.h.
.p.
.p.
sps
.ss
end
fatbits 141 78 p=gray.9 h=gray.13 s=roof.2
.h.
.p.
sps
.ss
end
; windows: plain glass with curtains drawn to the sides, not a screen of checks
color glass.2
fpoly 72 131 84 130 84 142 72 143
fpoly 167 123 175 122 175 132 167 133
color glass.1
fpoly 72 145 84 144 84 156 72 157
fpoly 167 135 175 134 175 143 167 144
color glass.5
draw 76 141 81 132
draw 169 131 172 125
color glass.4
draw 77 141 82 132
color trim.3
frect 72 131 73 142
frect 72 145 73 156
frect 83 131 84 142
frect 83 145 84 156
frect 167 124 167 132
frect 167 135 167 143
frect 175 123 175 132
frect 175 135 175 143

; ================= lawn =================
range lawn grass.5 grass.6 grass.7 grass.8
ink gradient lawn 0 150 0 199 bayer
stencil only grass.5
frect 0 124 319 199
stencil off
ink solid
; mowing stripes fanning toward the house
shade grass up 1
fpoly 120 124 -60 199 -20 199
fpoly 120 124 20 199 60 199
fpoly 120 124 100 199 140 199
fpoly 120 124 180 199 220 199
fpoly 120 124 260 199 300 199
fpoly 120 124 340 199 380 199
shade off
; blades
stencil only grass
brush vline 2
color grass.9
sprayrect 0 150 319 199 420
color grass.4
sprayrect 0 150 319 199 300
brush pixel
color grass.10
sprayrect 0 165 319 199 160
stencil off

; ================= beds, path, shrubs =================
color earth.3
fpoly 38 172 184 155 187 159 178 165 152 169 122 173 92 179 62 183 40 186
fpoly 244 161 262 150 277 143 319 138 319 168 296 172 270 171 250 167
fellipse 122 188 42 8
fpoly 0 172 38 172 40 186 30 193 0 195
color earth.2
brush pixel
sprayrect 0 150 319 196 0
; edging stones
color earth.7
draw 187 160 178 166 152 170 122 174 92 180 62 184 40 187 30 194 0 196
draw 244 162 250 168 270 172 296 173 319 169
ellipse 122 188 42 8
color earth.10
dot 184 162 176 167 168 168 160 169 150 170 142 171 132 173 124 174 114 176 106 177 98 179 88 181 80 181 72 182 64 184 54 185 46 186 36 190 26 194 16 195 6 196
dot 246 164 252 169 260 171 268 172 276 172 284 173 292 173 300 172 308 171 316 170
dot 82 186 86 183 94 181 104 180 114 180 124 180 134 180 144 181 152 183 160 186 163 190 158 193 150 195 140 196 128 196 116 196 104 196 94 195 86 193 81 190
; stepping stones
color earth.6
fellipse 206 168 6 2
fellipse 215 173 6 2
fellipse 212 179 7 3
fellipse 204 184 7 3
fellipse 209 191 8 3
fellipse 200 197 9 3
color earth.9
fellipse 205 167 6 2
fellipse 214 172 6 2
fellipse 211 178 7 2
fellipse 203 183 7 3
fellipse 208 190 8 3
fellipse 199 196 9 3
color earth.11
draw 201 166 206 165
draw 210 171 215 170
draw 206 177 212 176
draw 198 182 204 181
draw 202 188 209 188
draw 192 195 200 194
; clipped evergreens: left corner globe, right-hand mounds, a little cone
color pine.1
fcircle 20 159 20
fcircle 263 149 11
color pine.3
stencil only pine.1
fcircle 18 157 18
fcircle 261 147 9
stencil only pine.3
color pine.5
fcircle 14 153 12
fcircle 259 145 6
stencil only pine.1 pine.3 pine.5
brush hline 2
color pine.4
sprayrect 0 140 42 176 120
sprayrect 252 138 275 160 50
color pine.6
sprayrect 0 140 22 158 40
sprayrect 253 139 264 148 16
color pine.2
sprayrect 10 150 42 176 60
sprayrect 258 146 275 160 26
stencil off
brush pixel
color leaf.3
fcircle 303 151 13
fcircle 47 172 8
color leaf.6
stencil only leaf.3
fcircle 301 149 11
fcircle 46 171 7
stencil only leaf.6
color leaf.9
fcircle 298 146 7
fcircle 44 169 4
stencil only leaf.3 leaf.6 leaf.9
color leaf.11
sprayrect 290 139 304 150 26
sprayrect 40 165 47 171 10
color leaf.5
sprayrect 296 146 316 162 40
sprayrect 43 168 55 179 16
stencil off
color pine.2
fpoly 284 125 291 147 277 147
color pine.4
fpoly 284 126 284 147 278 147
color pine.6
draw 283 128 279 144
color pine.0
draw 285 130 290 146
