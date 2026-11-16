; ---------------- wall under the window: same wallpaper
color wall.2
fpoly 48 104 48 113 0 137 0 121
ink pattern dots
color gold.3
fpoly 48 104 48 113 0 137 0 121
ink solid
; ---------------- window over the sink
color wood.9
fpoly 46 19 46 105 2 121 2 3
color wood.11
draw 46 19 2 3
draw 46 19 46 105
color wood.6
draw 2 4 2 121
; daylight outside: sky, then the trees down the hill
color sky.14
fpoly 43 24 43 62 6 62 6 10
color leaf.9
fpoly 43 62 43 100 6 114 6 62
color daylight
fpoly 43 24 43 40 6 34 6 10
color leaf.7
fpoly 43 52 43 62 6 62 6 46
color leaf.10
fcircle 36 52 5
fcircle 24 49 6
fcircle 12 47 5
color leaf.12
fcircle 34 50 3
fcircle 22 46 3
color leaf.6
fpoly 43 78 43 100 6 114 6 84
color leaf.11
dot 38 68 30 70 22 72 14 74 34 74 26 77 18 80 10 82
; sashes
color wood.9
fpoly 43 60 43 64 6 64 6 60
fpoly 26 17 23 17 23 108 26 107
color wood.11
draw 43 60 6 60
color wood.6
draw 43 64 6 64
; gingham valance and cafe curtain
ink dither 8 opaque
color f_red f_wht
fpoly 43 24 43 33 6 22 6 10
fpoly 43 66 43 100 6 114 6 66
ink solid
color f_red_d
draw 43 34 6 23
draw 43 66 6 66
draw 36 67 36 102
draw 28 67 28 105
draw 19 67 19 109
draw 11 67 11 112
color f_wht
draw 39 67 39 101
draw 32 67 32 103
draw 23 67 23 107
draw 15 67 15 110
color gray.9
draw 43 65 6 65
; sill and what lives on it
color wood.11
fpoly 47 103 47 105 0 123 0 120
color wood.6
draw 47 106 0 124
fatbits 28 100 g=leaf.8 l=leaf.11 f=f_pur p=brick.3 q=brick.1
.lf.fl.
lgfglgl
.ggggg.
..ppq..
..ppq..
end
color f_blu_l
frect 13 108 15 115
color f_wht
draw 13 109 13 114
color f_blu
dot 14 107

; ---------------- sink: white enamel, chrome rim
color gray.12
fpoly 43 118 86 118 58 146 -3 146
color gray.7
draw 86 118 58 146
color trim.5
fpoly 45 120 84 120 74 128 27 128
fpoly 24 131 72 131 57 143 0 143
color trim.3
fpoly 45 120 84 120 82 122 43 122
fpoly 24 131 72 131 70 133 21 133
color trim.4
fpoly 45 120 43 122 29 128 27 128
fpoly 24 131 21 133 3 143 0 143
color trim.7
draw 50 126 70 126
draw 14 141 50 141
color gray.6
fellipse 60 125 3 1
fellipse 36 138 4 1
color gray.11
dot 60 125 36 138
; a pot left to soak in the far basin
color gray.8
fellipse 50 124 6 2
color gray.11
ellipse 50 124 6 2
color sky.10
fellipse 50 124 4 1
color black
draw 56 124 62 122
; faucet
color gray.6
brush round 2
curve 23 127 24 113 40 116
draw 40 116 41 120
color gray.12
brush pixel
curve 22 126 23 112 39 115
draw 39 115 40 119
color gray.15
curve 22 122 24 113 34 113
color gray.11
frect 18 125 28 127
frect 11 123 14 126
frect 31 122 34 125
color gray.15
dot 11 123 31 122 19 125
color gray.6
draw 10 127 14 127
draw 30 126 34 126
draw 12 121 12 122
draw 32 120 32 121
color gray.13
draw 10 121 14 121
draw 30 120 34 120

; ---------------- dish rack in the near corner
color f_yel_d
fpoly 0 152 40 148 52 170 30 199 0 199
color f_yel
draw 0 152 40 148
color trim.6
fellipse 9 162 5 10
color trim.3
ellipse 9 162 5 10
color trim.6
fellipse 15 164 5 10
color f_blu
ellipse 15 164 5 10
color trim.6
fellipse 21 166 5 10
color trim.3
ellipse 21 166 5 10
color trim.7
fellipse 27 168 5 10
color f_blu
ellipse 27 168 5 10
color trim.5
fellipse 27 168 3 6
color gray.9
draw 0 170 34 178 46 172
draw 0 177 34 186 48 178
draw 34 178 34 190
draw 46 172 48 180
draw 6 172 6 180
draw 13 174 13 182
draw 20 176 20 184
draw 27 177 27 186
color gray.13
draw 0 169 34 177 46 171
; a mug and a glass at the end of it
color f_blu_d
frect 37 160 43 168
color f_blu
draw 37 160 37 168
color f_blu_l
draw 38 160 42 160
color f_blu_d
draw 44 162 45 163 44 166
; washing-up liquid and a sponge
color leaf.9
frect 67 124 70 136
color leaf.12
draw 67 125 67 135
color f_wht
frect 68 121 69 123
color f_yel
frect 62 147 69 149
color leaf.7
draw 62 150 69 150

; ---------------- light
; sun through the window lands on the counter and the floor
shade lam up 1
fpoly 44 136 80 124 66 160 30 190
shade wood up 2
fpoly 128 158 186 148 214 168 146 184
shade wood down 2
fpoly 155 153 160 152 184 176 178 177
fpoly 137 170 200 158 201 160 138 172
shade wood up 1
ink dither 8
fpoly 124 156 190 145 220 168 146 188
; daylight from the back door washing down the floor
fpoly 194 131 232 131 248 162 188 162
ink solid
fpoly 199 131 229 131 234 144 196 144
; shadows: beside the fridge, under the stool, along the cabinets' toe
shade wood down 1
fpoly 162 131 170 131 176 141 162 141
fpoly 168 131 186 131 190 136 168 136
ink dither 8
fpoly 121 139 127 139 104 200 97 200
shade off
ink solid
