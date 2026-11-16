; close the pinholes along the fascia
color darkwood.3
fpoly 30 126 201 116 201 118 31 128
color roof.9
draw 30 125 201 115
color shake.1
draw 33 129 201 119
; porch slab is concrete, not dirt
color gray.6
fpoly 186 155 242 160 277 143 262 141 240 149 203 153
color gray.11
draw 186 156 242 161
draw 187 157 242 162
color gray.8
fpoly 196 159 232 162 232 164 196 161
color gray.5
draw 196 162 232 165

; ================= bed along the wall =================
; hollyhocks, left of the big window
fatbits 42 146 s=leaf.7 g=leaf.10 b=f_pink c=f_pink_d l=leaf.5
..g..
..g..
..sb.
..sc.
bbs..
bcs..
..sbb
..sbc
bbs..
bcs..
..sbb
..sbc
bbs..
bcs..
..sbb
..sbc
bbs..
bcs..
..s..
.lsl.
llsll
lllll
end
fatbits 47 140 s=leaf.7 g=leaf.10 b=f_wht c=f_cream l=leaf.6
..g..
..g..
..sb.
..sc.
bbs..
bcs..
..sbb
..sbc
bbs..
bcs..
..sbb
..sbc
bbs..
bcs..
..sbb
..sbc
bbs..
bcs..
..sbb
..sbc
bbs..
bcs..
..s..
..s..
.lsl.
llsll
lllll
end
fatbits 52 144 s=leaf.7 g=leaf.10 b=f_red c=f_red_d l=leaf.5
..g..
..g..
..sb.
..sc.
bbs..
bcs..
..sbb
..sbc
bbs..
bcs..
..sbb
..sbc
bbs..
bcs..
..sbb
..sbc
bbs..
bcs..
..s..
..s..
.lsl.
llsll
lllll
end
fatbits 57 138 s=leaf.7 g=leaf.10 b=f_pink_l c=f_pink l=leaf.6
..g..
..g..
..sb.
..sc.
bbs..
bcs..
..sbb
..sbc
bbs..
bcs..
..sbb
..sbc
bbs..
bcs..
..sbb
..sbc
bbs..
bcs..
..sbb
..sbc
bbs..
bcs..
..sbb
..sbc
..s..
..s..
.lsl.
llsll
lllll
end
fatbits 62 147 s=leaf.7 g=leaf.10 b=f_mag c=f_mag_d l=leaf.5
..g..
..g..
..sb.
..sc.
bbs..
bcs..
..sbb
..sbc
bbs..
bcs..
..sbb
..sbc
bbs..
bcs..
..s..
..s..
.lsl.
llsll
lllll
end
; phlox under the window
color leaf.4
fcircle 78 171 9
color leaf.7
stencil only leaf.4
fcircle 77 170 7
stencil only leaf.4 leaf.7
brush round 2
color f_mag
spray 78 167 8 16
color f_pink
spray 77 166 7 14
brush pixel
color f_pink_l
spray 76 165 6 10
stencil off
; rose bush
color leaf.3
fcircle 103 167 11
color leaf.6
stencil only leaf.3
fcircle 102 166 9
stencil off
color leaf.9
dot 97 160 100 158 104 159 95 164 108 162 99 164
color f_red
frect 96 162 97 163
frect 101 158 102 159
frect 107 160 108 161
frect 111 165 112 166
frect 99 168 100 169
frect 105 170 106 171
frect 110 171 111 172
frect 94 170 95 171
frect 103 164 104 165
color f_red_l
dot 96 162 101 158 107 160 111 165 99 168 105 170 103 164
color f_red_d
dot 97 163 102 159 108 161 112 166 100 169 106 171
; delphiniums
fatbits 116 147 t=f_blu_l b=f_blu d=f_blu_d s=leaf.7 l=leaf.6
.t.
.t.
tbt
bbd
bbd
tbd
bbd
bbb
dbd
bbd
.s.
.s.
lsl
lll
end
fatbits 120 143 t=f_pur_l b=f_pur d=f_pur_d s=leaf.7 l=leaf.6
.t.
.t.
tbt
bbd
bbd
tbd
bbd
bbb
dbd
bbd
bbd
tbd
.s.
.s.
.s.
lsl
lll
end
fatbits 124 146 t=f_blu_l b=f_blu d=f_blu_d s=leaf.7 l=leaf.6
.t.
.t.
tbt
bbd
bbd
tbd
bbd
bbb
dbd
bbd
.s.
.s.
lsl
lll
end
fatbits 128 150 t=f_pur_l b=f_pur d=f_pur_d s=leaf.7 l=leaf.6
.t.
tbt
bbd
tbd
bbd
bbb
dbd
.s.
.s.
lsl
lll
end
; daylilies
color leaf.6
curve 146 169 139 161 133 164
curve 147 169 155 162 160 164
curve 146 169 143 160 141 157
color leaf.9
curve 146 169 140 159 135 161
curve 146 169 142 158 139 154
curve 146 169 146 158 147 152
curve 147 169 151 158 154 155
curve 147 169 154 160 159 161
color leaf.11
curve 145 169 143 161 142 158
curve 148 169 150 161 152 158
color f_org
frect 134 159 135 160
frect 138 152 139 153
frect 146 149 147 150
frect 154 153 155 154
frect 158 159 159 160
frect 142 156 143 157
frect 150 158 151 159
color f_yel
dot 134 159 138 152 146 149 154 153 158 159 142 156 150 158
color f_org_d
dot 135 160 139 153 147 150 155 154 159 160
; daisies by the porch
color leaf.4
fcircle 174 161 7
color leaf.7
stencil only leaf.4
fcircle 173 160 6
stencil off
fatbits 167 155 w=f_wht y=f_yel
.w.
wyw
.w.
end
fatbits 172 152 w=f_wht y=f_yel
.w.
wyw
.w.
end
fatbits 177 155 w=f_wht y=f_yel
.w.
wyw
.w.
end
fatbits 170 159 w=f_wht y=f_yel
.w.
wyw
.w.
end
fatbits 176 160 w=f_wht y=f_yel
.w.
wyw
.w.
end
fatbits 180 157 w=f_wht y=f_yel
.w.
wyw
.w.
end
; hostas along the front
color leaf.3
fellipse 128 171 6 2
fellipse 139 170 6 2
fellipse 150 168 6 2
fellipse 161 167 6 2
color leaf.11
fellipse 128 170 5 2
fellipse 139 169 5 2
fellipse 150 167 5 2
fellipse 161 166 5 2
color leaf.13
draw 125 169 129 168
draw 136 168 140 167
draw 147 166 151 165
draw 158 165 162 164
color f_cream
dot 124 170 132 170 135 169 143 169 146 167 154 167 157 166 165 166
color f_lilac
dot 128 166 128 165 139 165 139 164 150 163 161 162 161 161
; marigold edging
color leaf.6
brush round 2
draw 44 185 62 183 92 179 118 174
color f_org
dot 44 184 52 183 60 182 68 181 76 180 84 179 92 178 100 176 108 175 116 173
color f_yel
dot 48 184 56 183 64 182 72 181 80 180 88 179 96 177 104 176 112 174
brush pixel
color f_org_d
dot 45 185 53 184 61 183 69 182 77 181 85 180 93 179 101 177 109 176

; ================= right-hand bed =================
color leaf.4
fellipse 268 165 18 5
color leaf.7
fellipse 266 164 15 3
color leaf.9
dot 252 163 258 162 266 161 274 162 281 163 262 164 270 165
fatbits 253 161 y=f_yel d=earth.1
.y.
ydy
.y.
end
fatbits 258 164 y=f_yel d=earth.1
.y.
ydy
.y.
end
fatbits 263 160 y=f_yel d=earth.1
.y.
ydy
.y.
end
fatbits 268 165 y=f_yel d=earth.1
.y.
ydy
.y.
end
fatbits 273 161 y=f_yel d=earth.1
.y.
ydy
.y.
end
fatbits 278 165 y=f_yel d=earth.1
.y.
ydy
.y.
end
fatbits 283 162 y=f_yel d=earth.1
.y.
ydy
.y.
end
fatbits 261 167 y=f_yel_d d=earth.1
.y.
ydy
.y.
end
fatbits 271 168 y=f_yel_d d=earth.1
.y.
ydy
.y.
end
fatbits 248 164 y=f_yel d=earth.1
.y.
ydy
.y.
end
; coneflowers at the far right
color leaf.7
draw 291 162 291 168
draw 296 165 296 170
draw 301 166 301 170
draw 307 165 307 169
draw 312 166 312 169
draw 317 164 317 168
color f_pur
frect 290 160 292 161
frect 300 164 302 165
frect 311 164 313 165
color f_lilac
frect 295 163 297 164
frect 306 163 308 164
frect 316 162 318 163
color earth.1
dot 291 160 296 163 301 164 307 163 312 164 317 162
; geranium in a pot on the slab, watering can by the step
fatbits 231 151 r=f_red g=leaf.8 p=brick.3 q=brick.1
.rgr.g
ggrgrg
.gggg.
.pppq.
.pppq.
..pq..
end
fatbits 221 160 g=gray.11 h=gray.7 s=gray.9 d=gray.6
..hhh...
.h...h.s
.gggd.s.
.gggds..
.gggd...
.gggd...
end

; ================= island bed =================
stencil only earth.3
brush round 2
color leaf.5
spray 122 188 40 150
color leaf.7
spray 120 187 36 70
stencil off
brush pixel
; salvia
color leaf.6
draw 90 185 90 189
draw 93 184 93 189
draw 96 184 96 190
draw 99 185 99 190
color f_pur
draw 90 179 90 184
draw 93 177 93 183
draw 96 178 96 183
draw 99 180 99 184
color f_pur_l
dot 90 179 93 177 96 178 99 180
; bee balm
color leaf.7
draw 105 177 105 188
draw 108 175 108 189
draw 111 176 111 189
draw 114 174 114 189
draw 117 177 117 188
color f_red
frect 104 175 106 176
frect 107 173 109 174
frect 110 174 112 175
frect 113 172 115 173
frect 116 175 118 176
color f_red_l
dot 105 175 108 173 111 174 114 172 117 175
; coreopsis
color leaf.8
fcircle 127 186 6
color f_yel
dot 123 183 126 182 129 183 131 185 124 186 128 186 126 188 130 188 122 188
color f_yel_l
dot 126 182 129 183 124 186
; daisies
color leaf.6
fcircle 153 187 6
fatbits 148 183 w=f_wht y=f_yel
.w.
wyw
.w.
end
fatbits 153 181 w=f_wht y=f_yel
.w.
wyw
.w.
end
fatbits 157 184 w=f_wht y=f_yel
.w.
wyw
.w.
end
fatbits 151 187 w=f_wht y=f_yel
.w.
wyw
.w.
end
fatbits 156 188 w=f_wht y=f_yel
.w.
wyw
.w.
end
; pinks along the near edge
color f_pink
dot 92 193 100 194 108 195 116 195 124 195 132 195 140 195 148 194
color f_wht
dot 96 194 104 195 112 195 120 195 128 195 136 195 144 194 152 193
color f_pink_l
dot 93 193 101 194 109 195 117 195 125 195 133 195 141 195
; post and birdhouse
color fence.3
draw 140 159 140 187
color fence.6
draw 139 159 139 187
fatbits 135 150 r=roof.3 w=wood.11 v=wood.7 d=earth.0 p=wood.5 h=roof.6
....h....
...hrr...
..hrrrr..
.hrrrrrr.
.wwwwwvv.
.wwwdwvv.
.wwwwwvv.
.wwwpwvv.
.wwwwwvv.
end

; ================= left corner =================
color leaf.4
fellipse 16 187 17 5
color leaf.7
fellipse 14 186 14 3
stencil only leaf.4 leaf.7
brush round 2
color f_pink_l
spray 14 186 15 14
color f_wht
spray 16 186 15 10
color f_red_l
spray 12 186 14 10
brush pixel
color f_peach
spray 15 186 15 12
stencil off
