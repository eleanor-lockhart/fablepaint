; ---------------- rock face: backlit, so shadow mass + rim light on the profile
stencil only rock.2
ink dither 5
color rock.3
fpoly 122 199 134 186 142 176 152 170 160 158 172 152 184 144 192 142 194 152 188 164 194 176 186 188 190 199
ink dither 8
color rock.4
fpoly 176 148 188 143 190 152 184 160 176 160
fpoly 156 162 168 156 172 164 166 174 156 174
fpoly 140 180 150 173 154 182 148 192 138 194
fpoly 126 194 134 188 138 196 134 199 124 199
ink solid
stencil off
; cracks, with a lit lip on their right
color rock.0
draw 176 144 178 156 175 170 178 184 175 199
draw 154 158 157 172 153 186 156 199
draw 138 174 140 186 137 199
draw 166 152 168 160
draw 190 139 193 150 188 162 193 176 186 188 189 199
draw 163 176 166 188 163 199
draw 146 184 148 199
color rock.4
draw 179 157 177 170 180 183
draw 158 173 155 186
draw 141 187 139 198
; rim light: risers warm, treads hot
color rock.5
brush round 2
draw 118 199 126 190 134 184 138 174 148 168 154 158 166 152 176 144 190 139
brush pixel
color rock.6
draw 119 198 126 190 134 184 138 174 148 168 154 158 166 152 176 144 190 139
color rock.7
draw 127 189 133 184
draw 139 173 147 168
draw 155 157 165 152
draw 177 143 189 139
; boulders in the surf and a little foam
color rock.2
fellipse 108 197 9 4
fellipse 92 199 6 2
color rock.6
draw 100 196 104 193 110 193
draw 87 198 91 197
color foamdim
brush hline 4
dot 96 195 114 199 82 199 122 196
color foam
brush hline 3
dot 99 198 118 198 104 199 88 196
brush pixel

; ---------------- grass slope
stencil only grass.1
ink dither 6
color grass.2
frect 190 133 319 160
ink dither 3
frect 190 160 319 199
ink solid
color grass.0
brush vline 3
sprayrect 196 150 319 199 260
color grass.2
brush vline 2
sprayrect 196 140 319 199 240
color grass.3
sprayrect 194 136 319 150 70
sprayrect 196 150 319 199 60
stencil off
brush pixel
; rim-lit turf along the brow
color grass.4
draw 190 139 204 136 220 134 224 134
draw 284 135 288 135 319 133
color grass.5
draw 192 138 204 135 218 133
dot 196 136 201 134 207 133 213 132 290 133 297 132 305 132 312 131 316 131
color grass.4
dot 194 136 199 135 204 134 210 133 216 132 222 132 287 133 294 133 301 132 309 131
; path from the door, winding to the foreground
ink dither 10 opaque
color rock.4 rock.3
fpoly 234 137 239 137 243 143 254 150 264 162 272 178 290 199 256 199 252 178 250 164 244 152 236 144
ink solid
color rock.5
draw 234 137 236 144 244 152 250 164 252 178 256 199
color rock.1
draw 240 138 244 143 255 150 265 162 273 178 291 199
; warm spill under the cottage windows
ink dither 6
color lamp.3
frect 254 136 260 138
frect 270 136 276 138
ink solid
; fence along the cliff edge
color rock.0
draw 194 133 194 138
draw 201 132 201 137
draw 208 131 208 136
draw 215 130 215 135
draw 221 129 221 134
draw 194 134 201 133 208 132 215 131 221 130
color rock.6
dot 194 133 201 132 208 131 215 130 221 129
; foreground grasses and poppies
color grass.3
curve 300 199 298 186 302 174
curve 306 199 308 184 304 170
curve 312 199 314 188 318 178
curve 292 199 290 190 286 182
curve 316 199 312 186 310 176
curve 228 199 226 190 229 182
curve 236 199 238 190 234 184
curve 220 199 217 192 214 188
color grass.4
curve 303 199 304 188 308 178
curve 296 199 294 188 296 178
curve 232 199 232 190 236 180
curve 310 199 310 192 314 184
color grass.5
dot 302 174 304 170 308 178 236 180 286 182
color stripe.5
frect 296 176 297 177
frect 317 177 318 178
frect 228 181 229 182
color stripe.3
dot 297 178 318 179 229 183

; ---------------- sailboat on the horizon, three gulls
fatbits 159 119 s=rock.1 h=rock.0
....s....
....s....
...ss....
...sss...
..ssss...
..sssss..
.ssssss..
....s....
.hhhhhhh.
..hhhhh..
end
color sea.9
draw 161 130 166 130
dot 163 132 164 132
fatbits 148 70 b=rock.1
bb...bb
..b.b..
...b...
end
fatbits 166 63 b=rock.1
b...b
.b.b.
..b..
end
fatbits 134 60 b=rock.1
bb..bb
..bb..
end

; ---------------- a better crescent
ink gradient sky 0 0 0 127 bayer
frect 43 20 57 31
ink solid
fatbits 45 22 m=moon
..........
........m.
........mm
.......mmm
.......mmm
m.....mmmm
.mmmmmmmm.
...mmmm...
end
