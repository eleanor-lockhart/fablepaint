defpattern tabs
#.......
#.......
#.......
........
....#...
....#...
....#...
........
end
; lawn base under everything
color grass.5
frect 0 124 319 199

; ================= back block: one storey, flat roof =================
color shake.5
fpoly 277 101 319 98 319 139 277 142
color shake.11
fpoly 196 106 277 101 277 142 203 154 196 150
color shake.7
draw 196 109 277 104
draw 196 113 277 107
draw 196 116 277 110
draw 196 119 277 113
draw 196 122 277 116
draw 196 126 277 119
draw 196 129 277 122
draw 196 132 277 124
draw 196 136 277 127
draw 196 139 277 130
draw 196 142 277 133
draw 196 145 277 136
draw 196 149 277 139
color shake.3
draw 277 104 319 101
draw 277 107 319 104
draw 277 110 319 107
draw 277 113 319 110
draw 277 116 319 113
draw 277 119 319 116
draw 277 122 319 119
draw 277 124 319 121
draw 277 127 319 124
draw 277 130 319 127
draw 277 133 319 130
draw 277 136 319 133
draw 277 139 319 136
brush vline 2
stencil only shake.11
color shake.12
sprayrect 196 100 277 154 130
color shake.10
sprayrect 196 100 277 154 110
stencil only shake.5
color shake.6
sprayrect 277 98 319 142 70
color shake.4
sprayrect 277 98 319 142 60
stencil off
brush pixel
; windows on the shaded wall
color trim.3
fpoly 289 121 296 120 296 139 289 140
fpoly 302 120 309 119 309 137 302 138
color glass.1
frect 290 122 295 138
frect 303 121 308 136
color glass.4
draw 291 128 294 123
draw 304 127 307 122
color trim.3
draw 290 130 295 130
draw 303 128 308 128
color trim.5
draw 288 140 297 139
draw 301 138 310 137
; parapet cap of the flat roof
color darkwood.3
draw 196 106 277 101 319 98
color darkwood.5
draw 195 105 277 100 319 97
color darkwood.7
draw 195 104 277 99
; railing of the roof porch, set back on the far half
color fence.6
draw 204 95 262 91
color fence.4
draw 204 96 262 92
ink pattern vlines
color fence.4
fpoly 205 97 261 93 261 99 205 103
ink solid
color fence.6
frect 204 94 205 103
frect 218 93 219 102
frect 233 92 234 101
frect 247 91 248 100
frect 261 90 262 99
color fence.7
draw 204 94 204 102
draw 218 93 218 101
draw 233 92 233 100
draw 247 91 247 99
draw 261 90 261 98

; ================= main wall =================
color shake.9
fpoly 36 128 201 118 201 154 36 172
color shake.5
draw 36 131 201 121
draw 36 135 201 124
draw 36 138 201 126
draw 36 142 201 129
draw 36 145 201 132
draw 36 148 201 135
draw 36 152 201 137
draw 36 155 201 140
draw 36 158 201 143
draw 36 162 201 146
draw 36 165 201 148
draw 36 169 201 151
stencil only shake.9
brush vline 2
color shake.10
sprayrect 36 118 201 172 380
color shake.8
sprayrect 36 118 201 172 300
color shake.7
ink pattern tabs
fpoly 36 128 201 118 201 154 36 172
ink solid
brush pixel
color shake.11
sprayrect 36 118 201 172 120
stencil off
; shadow thrown by the eave
shade shake down 3
fpoly 36 128 201 118 201 123 36 134
shade shake down 1
ink dither 8
fpoly 36 134 201 123 201 125 36 136
ink solid
shade off

; ================= front gable, seen edge-on at the left =================
color shake.12
fpoly 0 88 10 72 30 126 36 128 36 172 0 172
color shake.8
draw 14 83 0 85
draw 15 86 0 88
draw 16 89 0 91
draw 17 92 0 94
draw 18 95 0 97
draw 20 98 0 100
draw 21 101 0 103
draw 22 104 0 106
draw 23 107 0 109
draw 27 115 0 116
draw 29 119 0 120
draw 30 123 0 123
draw 33 127 0 127
draw 36 131 0 130
draw 36 135 0 134
draw 36 138 0 137
draw 36 142 0 141
draw 36 145 0 144
draw 36 148 0 147
; attic vent
fatbits 9 95 d=darkwood.2 l=darkwood.6
ddddd
dllld
ddddd
dllld
ddddd
dllld
ddddd
end
; door hood
color roof.8
fpoly 0 108 13 111 17 123 0 121
color roof.6
draw 0 112 14 115
draw 0 116 15 119
color roof.10
draw 0 108 13 111
color darkwood.4
draw 0 122 17 124
draw 0 123 17 125
frect 15 125 16 142
color darkwood.6
draw 15 125 15 142
; windows on the gable
color trim.7
frect 2 127 11 141
frect 24 128 31 142
color glass.2
frect 4 129 9 134
frect 4 136 9 139
frect 26 130 29 135
frect 26 137 29 140
color glass.5
draw 5 133 8 130
draw 27 134 28 131

; ================= main roof =================
color roof.7
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
stencil only roof.7
ink pattern tabs
color roof.6
fpoly 10 72 170 78 201 116 30 126
ink solid
brush hline 2
color roof.8
sprayrect 10 72 201 126 300
color roof.6
sprayrect 10 72 201 126 200
stencil off
brush pixel
shade roof up 1
ink dither 6
fpoly 10 72 170 78 178 88 15 86
shade roof down 1
ink dither 5
fpoly 26 114 194 108 201 116 30 126
shade off
ink solid
; ridge cap, rakes, eave
color roof.10
draw 10 72 170 78
color roof.9
draw 10 73 170 79
color darkwood.4
brush round 2
draw 172 79 202 116
color darkwood.5
draw 10 73 30 126
draw 10 72 0 88
brush pixel
color roof.10
draw 30 125 201 115
color darkwood.3
draw 30 126 201 116
draw 31 127 201 117
; roof vents and pipes
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

; ================= windows on the main wall =================
color trim.6
fpoly 70 129 86 128 86 158 70 159
fpoly 123 125 134 124 134 140 123 141
fpoly 165 121 177 120 177 145 165 146
color glass.2
fpoly 72 131 84 130 84 142 72 143
fpoly 125 127 132 126 132 131 125 132
fpoly 167 123 175 122 175 132 167 133
color glass.1
fpoly 72 145 84 144 84 156 72 157
fpoly 125 134 132 133 132 138 125 139
fpoly 167 135 175 134 175 143 167 144
color glass.5
draw 74 141 79 132
draw 75 141 80 132
draw 168 131 172 124
draw 126 131 129 127
ink dither 8
color trim.4
frect 72 131 75 157
frect 82 131 84 157
frect 167 123 168 144
frect 174 123 175 144
ink solid
color trim.7
draw 69 160 87 159
draw 122 142 135 141
draw 164 147 178 146
color shake.3
draw 70 161 87 160
draw 123 143 135 142
draw 165 148 178 147
shade trim down 2
fpoly 70 128 86 127 86 131 70 133
fpoly 123 124 134 123 134 126 123 127
fpoly 165 120 177 119 177 123 165 124
shade off

; ================= porch =================
shade shake down 6
fpoly 183 119 242 128 276 112 277 142 240 150 203 154 190 156 183 150
shade off
; floor slab and step
color earth.6
fpoly 186 155 242 160 277 143 262 141 240 149 203 153
color earth.10
draw 186 156 242 161
color earth.7
fpoly 196 159 232 162 232 164 196 161
; door
color trim.4
fpoly 223 126 238 124 238 146 223 148
color glass.1
fpoly 225 128 236 127 236 136 225 137
color glass.3
draw 227 135 231 128
color trim.2
draw 225 139 236 138 236 144 225 146 225 139
color shake.0
draw 222 126 222 148
draw 239 124 239 146
color f_yel_d
dot 235 139
; window
color trim.4
fpoly 250 124 264 122 264 145 250 147
color glass.1
fpoly 252 126 262 125 262 134 252 135
color glass.0
fpoly 252 137 262 136 262 143 252 145
color glass.3
draw 254 133 258 126
; posts
color darkwood.3
frect 215 123 216 150
color darkwood.5
frect 186 120 187 156
color darkwood.7
draw 186 120 186 156
; porch roof
color roof.8
fpoly 180 117 229 106 276 111 242 126
color roof.6
draw 219 108 269 114
draw 209 110 262 117
draw 200 113 256 120
draw 190 115 249 123
color roof.10
draw 180 117 229 106
color darkwood.4
draw 180 118 242 127
draw 180 119 242 128
color darkwood.2
draw 242 127 276 112
draw 242 128 276 113
color darkwood.5
frect 241 129 243 160
color wood.8
draw 241 129 241 160
; hanging basket
color gray.6
draw 197 121 197 128
color leaf.5
fcircle 197 132 4
color leaf.10
dot 195 130 197 129 199 131 196 133
color f_pink
dot 194 132 198 130 200 133 196 135
color f_red
dot 196 131 199 134
color leaf.8
dot 194 136 195 138 199 137 200 139 197 137
