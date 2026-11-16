; ---------------- clouds: bright rim first (offset toward the sun), dark body, then lighter bellies
stencil protect suncore sunrim moon
; cloud A, upper right -- rim pushed down-left
color cloud.7
fellipse 248 68 62 5
fellipse 226 65 30 4
fellipse 273 64 34 5
fellipse 203 70 30 3
fellipse 298 69 26 4
fellipse 178 72 16 2
color cloud.1
fellipse 250 66 62 5
fellipse 228 63 30 4
fellipse 275 62 34 5
fellipse 205 68 30 3
fellipse 300 67 26 4
fellipse 180 70 16 2
; cloud B, left -- rim pushed down-right
color cloud.7
fellipse 52 86 46 4
fellipse 32 83 22 3
fellipse 74 84 20 3
fellipse 97 88 18 2
fellipse 10 88 14 2
color cloud.1
fellipse 50 84 46 4
fellipse 30 81 22 3
fellipse 72 82 20 3
fellipse 95 86 18 2
fellipse 8 86 14 2
; cloud D, high thin wisp
color cloud.6
fellipse 134 52 26 2
fellipse 117 54 14 1
fellipse 154 54 12 1
color cloud.1
fellipse 135 50 26 2
fellipse 118 52 14 1
fellipse 155 52 12 1
; cloud C, low streaks on the right
color cloud.7
fellipse 213 103 40 2
fellipse 248 100 26 2
fellipse 178 106 18 1
fellipse 288 105 24 2
color cloud.2
fellipse 215 101 40 2
fellipse 250 98 26 2
fellipse 180 104 18 1
fellipse 290 103 24 2
; bellies: mid tone two pixels below the top edge, rose four below
stencil only cloud.1 cloud.2
color cloud.3
fellipse 250 68 62 5
fellipse 228 65 30 4
fellipse 275 64 34 5
fellipse 205 70 30 3
fellipse 300 69 26 4
fellipse 50 86 46 4
fellipse 30 83 22 3
fellipse 72 84 20 3
fellipse 95 88 18 2
fellipse 135 52 26 2
fellipse 215 103 40 2
fellipse 250 100 26 2
fellipse 290 105 24 2
stencil only cloud.3
color cloud.5
fellipse 249 71 60 5
fellipse 227 68 28 4
fellipse 274 67 32 5
fellipse 51 89 44 4
fellipse 31 86 20 3
fellipse 73 87 18 3
ink dither 8
color cloud.4
fellipse 249 69 60 5
fellipse 274 65 32 5
fellipse 227 66 28 4
fellipse 51 87 44 4
ink solid
stencil off
; streaks crossing the glow, dark against the bright sky
stencil protect suncore sunrim
color cloud.5
fellipse 36 108 30 1
fellipse 160 113 24 1
color cloud.6
fellipse 60 115 18 0
fellipse 140 119 16 0
color cloud.7
draw 8 110 62 110
draw 138 115 182 115
stencil off

; ---------------- the beam (drawn before the tower so the tower covers its root)
shade sky up 1
ink dither 8
fpoly 232 51 0 26 0 50 232 54
fpoly 240 51 319 40 319 58 240 54
ink solid
fpoly 232 52 0 34 0 42 232 53
fpoly 240 52 319 46 319 52 240 53
ink dither 8
fpoly 232 51 130 40 130 52 232 54
shade off
ink solid

; ---------------- sea
ink gradient sea 0 199 0 128 bayer
frect 0 128 319 199
ink solid
