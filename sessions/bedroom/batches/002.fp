title "BEDROOM.LBM"
pal 224 28 28 28
pal 227 59 59 55
ramp 224 227 plat
pal 228 22 28 40
pal 233 57 60 63
ramp 228 233 bwall
pal 234 63 63 54 glow
clear black
; ---------------- shell: back wall square-on, left wall running away, vanishing point 195,58
ink gradient bwall 40 0 330 0 bayer
frect 72 0 319 160
ink solid
color bwall.4
fpoly 0 0 72 0 72 160 24 199 0 199
shade bwall down 1
ink dither 8
frect 60 0 72 160
frect 72 0 80 160
ink solid
frect 70 0 73 160
shade off
; floor: dark painted boards
color darkwood.2
fpoly 72 160 319 160 319 199 24 199
color darkwood.1
draw 80 160 36 199
draw 100 160 64 199
draw 120 160 91 199
draw 140 160 119 199
draw 160 160 147 199
draw 180 160 174 199
draw 200 160 202 199
draw 220 160 230 199
draw 240 160 257 199
draw 260 160 285 199
draw 280 160 312 199
draw 300 160 319 178
shade darkwood up 1
ink dither 8
fpoly 150 160 300 160 319 172 319 199 120 199
ink dither 4
fpoly 190 160 280 160 319 185 319 199 200 199
shade off
ink solid
; baseboards
color darkwood.1
frect 72 152 319 160
fpoly 72 152 72 160 24 199 10 199
color darkwood.4
draw 72 152 319 152
draw 72 152 10 199

; ---------------- window, blinds two-thirds down
color wood.7
frect 252 24 316 104
color wood.9
draw 252 24 316 24
draw 252 24 252 104
color wood.5
draw 316 25 316 104
frect 257 29 311 99
; outside
color leaf.9
frect 258 30 310 98
color sky.14
frect 258 78 310 84
color leaf.11
fcircle 268 86 7
fcircle 284 84 9
fcircle 300 88 8
color leaf.7
frect 258 92 310 98
color leaf.13
dot 264 84 270 82 282 80 288 82 298 85 304 86
color grass.9
frect 258 95 310 98
; slats
color wood.12
frect 258 30 310 76
color wood.8
draw 258 32 310 32
draw 258 35 310 35
draw 258 38 310 38
draw 258 41 310 41
draw 258 44 310 44
draw 258 47 310 47
draw 258 50 310 50
draw 258 53 310 53
draw 258 56 310 56
draw 258 59 310 59
draw 258 62 310 62
draw 258 65 310 65
draw 258 68 310 68
draw 258 71 310 71
draw 258 74 310 74
color glow
draw 258 33 310 33
draw 258 39 310 39
draw 258 45 310 45
draw 258 51 310 51
draw 258 57 310 57
draw 258 63 310 63
draw 258 69 310 69
color wood.9
frect 258 75 310 77
color wood.6
draw 268 30 268 76
draw 300 30 300 76
draw 306 77 306 90
dot 306 91 306 92
; sill
color wood.9
frect 250 104 318 106
color wood.5
draw 250 107 318 107

; ---------------- shelf over the bed: books and a radio-cassette
color wood.9
frect 96 72 178 73
color wood.5
draw 96 74 178 74
draw 104 75 104 79
draw 170 75 170 79
color f_red_d
frect 100 58 103 71
color f_blu_d
frect 104 60 108 71
color leaf.6
frect 109 57 111 71
color f_yel_d
frect 112 61 116 71
color f_cream
frect 117 59 119 71
color f_pur_d
frect 120 62 124 71
color f_org_d
frect 125 58 128 71
color f_blu
frect 129 60 131 71
color f_wht_d
draw 101 60 101 62
draw 106 62 106 64
draw 114 63 114 65
draw 122 64 122 66
draw 126 60 126 62
color f_red
fpoly 132 71 136 71 140 60 136 59
color gray.5
frect 146 61 172 71
color gray.8
draw 146 61 172 61
color gray.2
fcircle 152 66 3
fcircle 166 66 3
color gray.9
dot 152 66 166 66
color gray.12
frect 157 63 161 66
color black
frect 158 64 160 65
color gray.7
dot 157 69 159 69 161 69
draw 149 60 149 57 169 57 169 60
draw 171 60 176 50

; ================= the bed: lower half of a bunk =================
color wood.6
frect 80 99 84 127
frect 203 99 207 127
color wood.8
draw 84 99 84 127
draw 207 99 207 127
color wood.10
frect 81 96 82 98
frect 204 96 205 98
color wood.7
fpoly 21 137 80 109 80 116 21 148
fpoly 21 150 80 118 80 126 21 163
color wood.9
draw 21 137 80 109
draw 21 150 80 118
color wood.4
draw 21 148 80 116
color wood.5
fpoly 207 109 213 137 213 163 207 126
color trim.5
fpoly 80 126 207 126 214 163 17 163
color f_red_d
fpoly 110 126 126 126 119 133 102 133
color leaf.7
fpoly 126 126 142 126 137 133 119 133
color f_pink_d
fpoly 142 126 158 126 154 133 137 133
color f_cream
fpoly 158 126 174 126 172 133 154 133
color f_pur
fpoly 174 126 190 126 190 133 172 133
color f_blu
fpoly 190 126 207 126 208 133 190 133
color f_cream
fpoly 102 133 119 133 111 141 92 141
color f_pur
fpoly 119 133 137 133 131 141 111 141
color f_blu
fpoly 137 133 154 133 150 141 131 141
color f_yel_d
fpoly 154 133 172 133 170 141 150 141
color f_red_d
fpoly 172 133 190 133 189 141 170 141
color leaf.7
fpoly 190 133 208 133 210 141 189 141
color f_yel_d
fpoly 92 141 111 141 101 151 79 151
color f_red_d
fpoly 111 141 131 141 123 151 101 151
color leaf.7
fpoly 131 141 150 141 145 151 123 151
color f_pink_d
fpoly 150 141 170 141 166 151 145 151
color f_cream
fpoly 170 141 189 141 188 151 166 151
color f_pur
fpoly 189 141 210 141 211 151 188 151
color f_pink_d
fpoly 79 151 101 151 88 163 63 163
color f_cream
fpoly 101 151 123 151 113 163 88 163
color f_pur
fpoly 123 151 145 151 138 163 113 163
color f_blu
fpoly 145 151 166 151 163 163 138 163
color f_yel_d
fpoly 166 151 188 151 187 163 163 163
color f_red_d
fpoly 188 151 211 151 214 163 187 163
color f_blu
frect 63 164 88 172
color f_yel_d
frect 89 164 113 172
color f_red_d
frect 114 164 138 172
color leaf.7
frect 139 164 163 172
color f_pink_d
frect 164 164 187 172
color f_cream
frect 188 164 214 172
ink dither 6
color darkwood.1
frect 63 164 214 172
ink pattern dots
color f_red
fpoly 158 126 174 126 172 133 154 133
fpoly 102 133 119 133 111 141 92 141
fpoly 170 141 189 141 188 151 166 151
fpoly 101 151 123 151 113 163 88 163
color f_wht
fpoly 190 126 207 126 208 133 190 133
fpoly 137 133 154 133 150 141 131 141
fpoly 145 151 166 151 163 163 138 163
color f_yel
fpoly 126 126 142 126 137 133 119 133
fpoly 131 141 150 141 145 151 123 151
ink solid
color trim.6
fpoly 106 126 110 126 63 163 57 163
fpoly 76 129 104 129 74 154 36 154
color trim.7
fpoly 78 130 100 130 84 141 56 141
color trim.4
fpoly 74 154 36 154 40 151 78 150
color f_blu_l
draw 84 131 50 152
draw 96 131 66 152
color wood.6
frect 21 173 209 194
color wood.8
draw 21 173 209 173
color wood.5
draw 30 178 90 178
draw 110 182 170 182
draw 60 188 120 188
draw 150 190 200 190
draw 26 185 50 185
color darkwood.0
frect 21 195 209 199
color wood.6
frect 209 121 216 199
frect 13 121 21 199
color wood.8
draw 209 121 209 199
draw 13 121 13 199
color wood.4
draw 216 121 216 199
draw 21 121 21 199
color wood.9
frect 209 119 216 120
frect 13 119 21 120
color wood.11
frect 211 115 213 118
frect 16 115 18 118
color wood.6
draw 214 116 214 118
draw 19 116 19 118
