title "KITCHEN.LBM"
pal 224 22 15 5
pal 227 48 38 13
ramp 224 227
pal 229 61 53 27
ramp 227 229
range gold 224..229
pal 230 38 33 22
pal 233 62 59 48
ramp 230 233 lam
pal 234 13 17 6
pal 237 48 52 26
ramp 234 237 avo
pal 238 63 63 54 glow
pal 239 56 60 63 daylight
pal 240 30 28 26
pal 243 62 60 54
ramp 240 243 almond
clear black
; ---------------- the shell, one-point perspective, vanishing point 150,62
range ceil wall.4 wall.5 wall.6
ink gradient ceil 150 30 150 0 bayer
fpoly 45 0 96 30 254 30 319 10 319 0
ink solid
color wall.6
frect 96 30 254 130
color wall.3
fpoly 45 0 96 30 96 130 40 200 0 200 0 0
color wall.7
fpoly 254 30 319 10 319 172 254 130
; ---------------- parquet floor (done first: nothing else on screen is in the wood range yet)
color wood.5
fpoly 96 130 254 130 319 172 319 199 40 200
shade wood up 1
fpoly 150 62 40 200 68 200
fpoly 150 62 96 200 123 200
fpoly 150 62 151 200 178 200
fpoly 150 62 206 200 234 200
fpoly 150 62 261 200 289 200
fpoly 150 62 316 200 344 200
shade wood down 1
frect 0 135 319 140
frect 0 149 319 156
frect 0 168 319 180
frect 0 198 319 199
shade wood up 1
brush hline 3
sprayrect 40 130 319 199 220
shade wood down 1
brush vline 3
sprayrect 40 130 319 199 160
shade off
brush pixel
stencil only wood
color wood.2
draw 96 130 40 200
draw 110 130 68 200
draw 123 130 96 200
draw 137 130 123 200
draw 150 130 151 200
draw 164 130 178 200
draw 178 130 206 200
draw 191 130 234 200
draw 205 130 261 200
draw 218 130 289 200
draw 232 130 316 200
draw 246 130 319 182
draw 0 135 319 135
draw 0 141 319 141
draw 0 148 319 148
draw 0 157 319 157
draw 0 168 319 168
draw 0 181 319 181
draw 0 198 319 198
stencil off

; ---------------- far wall: wainscot, chair rail
color darkwood.3
frect 96 76 254 130
color darkwood.1
draw 166 78 166 129
draw 171 78 171 129
draw 176 78 176 129
draw 181 78 181 129
draw 186 78 186 129
draw 238 78 238 129
draw 243 78 243 129
draw 248 78 248 129
draw 253 78 253 129
color darkwood.6
draw 96 75 254 75
color darkwood.5
draw 96 76 254 76
draw 96 126 254 126
; ---------------- back door
color wood.9
frect 191 37 235 130
color wood.11
draw 191 37 191 130
draw 191 37 235 37
color wood.6
draw 235 38 235 130
color trim.5
frect 194 40 232 130
; the garden through the nine panes
color sky.13
frect 198 50 228 62
color leaf.5
frect 198 60 228 66
color leaf.8
frect 198 65 228 77
color fence.4
frect 198 70 228 73
color fence.2
draw 198 74 228 74
color leaf.10
fcircle 203 62 4
fcircle 214 60 5
fcircle 225 63 4
color leaf.7
fcircle 209 64 3
fcircle 220 65 3
color leaf.6
frect 198 75 228 79
color grass.8
frect 198 80 228 92
color grass.9
frect 198 86 228 92
color f_pink
dot 200 77 204 78 210 76 222 77 226 78 201 81 213 80
color f_yel
dot 202 79 207 77 216 78 224 80 219 76
color f_red
dot 205 80 211 78 221 79 227 76
color f_wht
dot 199 79 208 80 215 77 223 78
; muntins
color trim.6
frect 207 50 208 92
frect 218 50 219 92
frect 198 63 228 64
frect 198 78 228 79
color trim.3
rect 197 49 229 93
; gingham valance
ink dither 8 opaque
color f_red f_wht
frect 198 50 228 55
ink solid
color f_red
frect 198 56 199 56
frect 202 56 204 56
frect 207 56 209 56
frect 212 56 214 56
frect 217 56 219 56
frect 222 56 224 56
frect 227 56 228 56
color gray.9
draw 196 49 230 49
; lower panels, knob, bolt
color trim.3
rect 198 98 211 124
rect 215 98 228 124
color trim.7
draw 199 123 210 123 210 99
draw 216 123 227 123 227 99
color f_yel_d
frect 229 96 230 97
color f_yel_l
dot 229 96
color gray.11
dot 229 90 230 90
color darkwood.0
draw 192 130 234 130
; light switch
color trim.7
frect 241 66 243 71
color gray.6
dot 242 68

; ---------------- refrigerator, harvest gold
color gold.3
frect 124 56 162 139
color wall.6
dot 124 56 162 56
color gold.4
frect 125 58 129 138
color gold.5
draw 126 60 126 136
ink dither 8
color gold.2
frect 151 57 156 138
ink solid
frect 157 57 161 138
color gold.0
draw 124 80 162 80
color gold.1
draw 124 81 162 81
draw 162 57 162 139
color gray.3
frect 125 136 161 139
color gray.6
draw 126 137 160 137
color gray.13
frect 154 66 155 77
frect 154 84 155 102
color gray.7
draw 156 66 156 77
draw 156 84 156 102
color wood.7
draw 154 69 154 75
draw 154 87 154 99
color gray.12
draw 129 60 135 60
; what's stuck to it
color f_wht
frect 130 88 142 98
color sky.8
draw 131 89 141 89
color f_yel
dot 140 90 139 90 140 91 141 91
color shake.9
frect 133 93 138 96
color roof.6
fpoly 132 93 135 90 139 93
color grass.6
draw 131 97 141 97
color f_red
dot 136 87 137 87
color f_cream
frect 145 103 154 113
color leaf.8
draw 150 108 150 112
color f_pink
dot 149 106 151 106 150 105 150 107
color f_yel
dot 150 106
color f_blu
dot 149 103 150 103
color trim.7
frect 133 62 137 73
color gray.8
draw 134 64 136 64
draw 134 66 136 66
draw 134 68 135 68
draw 134 70 136 70
color f_red
dot 131 120 139 125
color f_yel
dot 134 121
color leaf.10
dot 137 120
color f_blu
dot 140 121 133 124
color f_org
dot 143 120
color f_pur
dot 146 122
; on top of it
color f_yel
frect 128 42 134 55
color f_yel_d
draw 134 42 134 55
color f_red
frect 129 45 133 48
color f_blu_l
frect 135 45 140 55
color f_wht
frect 136 47 139 50
color f_blu
draw 140 45 140 55
color f_org
frect 141 40 148 55
color f_org_d
draw 148 40 148 55
color f_cream
frect 142 43 147 46
color wood.9
frect 150 49 160 55
color wood.6
draw 150 51 160 51
draw 150 53 160 53
dot 152 50 155 50 158 50 153 52 156 52 159 52 152 54 155 54 158 54
color wood.11
draw 150 49 160 49

; ---------------- clock and telephone in the gap
color trim.7
fcircle 176 45 6
color darkwood.3
circle 176 45 6
color black
draw 176 45 176 41
draw 176 45 179 46
color f_red
dot 176 45
fatbits 171 58 c=f_cream h=lam.1 d=gray.6 w=f_wht s=lam.0
.ccccccccc.
ccccccccccc
chhcccccccc
chhcddddccc
chhcdwwdccc
chhcdwwdccc
chhcddddccc
chhcccccccc
chhcccccccc
chhcccccccc
chhccsssccc
.ccccccccc.
end
color lam.0
draw 171 70 182 70
ink dither 8
color lam.2
curve 173 70 169 98 172 118
curve 172 118 176 124 178 112
curve 178 112 180 92 177 72
ink solid
