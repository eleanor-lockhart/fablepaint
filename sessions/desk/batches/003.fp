; ---------------- ginger cat loafing on the monitor
; tail first, draped down the left bezel
ink dither 8 opaque
color yellow brown
brush round 4
spline 139 37 131 39 125 45 122 55 123 65 121 73 124 79
brush pixel
ink solid
color brown
draw 123 48 126 48
draw 120 53 123 53
draw 120 58 123 58
draw 121 63 124 63
draw 120 68 123 68
draw 119 73 122 73
color white
frect 122 77 125 80
dot 121 78 121 79
; body
ink dither 8 opaque
color yellow brown
fellipse 158 32 23 11
ink solid
stencil only yellow
color brown
frect 135 40 181 43
stencil only brown
color yellow
frect 142 21 174 23
stencil off
; tabby stripes over the back
color brown
brush round 2
curve 142 27 141 31 143 36
curve 148 24 147 29 149 35
curve 154 23 153 28 155 34
curve 160 23 159 28 161 34
brush pixel
; one paw hanging over the bezel
ink dither 8 opaque
color yellow brown
frect 161 42 165 46
ink solid
color white
frect 161 47 165 49
color lgray
dot 163 49 161 49 165 49
color brown
draw 160 42 160 47
draw 166 42 166 47
; head
ink dither 8 opaque
color yellow brown
fellipse 176 27 10 8
fpoly 168 22 170 13 175 19
fpoly 178 19 183 13 185 22
ink solid
color lred
dot 171 17 171 18 172 18 182 17 182 18 181 18
color brown
draw 174 20 174 23
draw 176 19 176 23
draw 178 20 178 23
draw 167 26 169 26
draw 183 26 185 26
color white
fellipse 176 32 4 2
color black
draw 171 27 172 28 173 28 174 27
draw 178 27 179 28 180 28 181 27
dot 174 32 175 33 176 32 177 33 178 32
color lred
draw 175 30 177 30
dot 176 31
color white
draw 165 29 160 28
draw 165 31 160 32
draw 187 29 192 28
draw 187 31 192 32
; a little shadow where it sits
color dgray
draw 131 43 135 43
draw 182 43 187 43
