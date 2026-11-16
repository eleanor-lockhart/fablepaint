; ---------------- backsplash wall (old wallpaper, a faint dotted print)
color wall.2
fpoly 89 70 89 93 48 113 48 75
ink pattern dots
color gold.3
fpoly 89 70 89 93 48 113 48 75
ink solid
; ---------------- counter top: cream laminate with gold flecks, aluminium edge
color lam.2
fpoly 89 92 121 92 17 200 0 200 0 137
stencil only lam.2
color gold.3
sprayrect 0 92 121 199 240
color lam.1
sprayrect 0 92 121 199 200
color lam.3
sprayrect 0 92 121 199 160
stencil off
; ---------------- lower cabinets: flat plywood doors
color wood.8
fpoly 121 94 121 139 97 200 18 200
shade wood up 1
brush vline 5
stencil only wood.8
sprayrect 18 94 121 199 90
shade wood down 1
sprayrect 18 94 121 199 90
stencil off
shade off
brush pixel
color darkwood.0
fpoly 121 134 121 139 97 200 93 200
color wood.4
draw 121 100 59 181 45 200
draw 118 96 118 133
draw 109 105 109 157
draw 101 114 101 177
draw 88 127 88 199
draw 67 149 67 199
draw 43 174 43 199
color wood.10
draw 102 114 102 176
draw 89 128 89 199
draw 68 150 68 199
draw 44 175 44 199
color gray.12
draw 121 93 17 200
color gray.7
draw 121 94 18 200
color f_yel_d
frect 104 110 105 111
frect 103 124 104 125
frect 91 138 92 139
frect 71 162 72 163
frect 48 184 49 185
frect 96 121 97 122
frect 81 141 82 142
frect 60 168 61 169
color f_yel_l
dot 104 110 103 124 91 138 71 162 48 184 96 121 81 141 60 168

; ---------------- the range
color almond.3
fpoly 84 95 118 95 109 104 65 104
color almond.2
fpoly 84 84 84 95 65 104 65 90
color gray.4
draw 83 87 66 94
draw 83 88 66 95
color gray.12
dot 80 88 76 90 72 91 68 93
color f_wht
dot 78 86 78 87
color almond.1
fpoly 118 96 118 145 109 169 109 105
color gray.3
fpoly 117 110 117 128 110 142 110 119
color gray.6
draw 117 133 110 150
color gray.13
draw 117 103 110 111
color gray.7
draw 117 104 110 112
ink dither 8 opaque
color f_red f_wht
fpoly 116 105 112 109 112 124 116 119
ink solid
; burners
color gray.2
fellipse 91 97 4 1
fellipse 106 97 4 1
fellipse 100 102 5 1
color gray.11
draw 87 96 95 96
draw 102 96 110 96
draw 95 101 105 101
color gray.9
draw 65 104 109 104
; kettle on the near back burner
color gray.2
fellipse 83 102 5 1
color avo.2
fellipse 82 98 5 4
color avo.3
draw 79 96 81 95
color avo.1
draw 84 101 86 99
color black
curve 78 95 82 90 86 95
dot 82 93
color avo.2
draw 87 97 90 95
; ---------------- hood
color almond.3
frect 65 73 97 79
color almond.2
fpoly 109 70 109 76 97 80 97 73
color gray.12
draw 65 80 97 80
draw 97 80 109 76
color gray.6
draw 65 73 97 73

; ---------------- things on the counter
; canisters
color f_org_d
frect 61 92 67 104
frect 54 97 59 107
frect 49 101 53 109
color f_cream
frect 61 96 67 98
frect 54 100 59 102
frect 49 104 53 105
color darkwood.3
frect 61 91 67 92
frect 54 96 59 97
frect 49 100 53 101
color f_org
draw 61 93 61 104
draw 54 98 54 107
draw 49 102 49 109
; toaster
color gray.12
frect 84 100 96 108
color gray.15
draw 84 100 96 100
draw 85 102 85 106
color gray.7
frect 94 101 96 108
color black
draw 87 100 93 100
frect 84 109 96 109
dot 97 104
; cookie jar by the fridge
color earth.6
fellipse 103 88 4 4
color earth.8
draw 100 86 101 85
color earth.4
frect 101 83 105 84
dot 103 82
; paper towels under the cabinet, potholder on the end panel
color trim.7
frect 68 77 80 82
color trim.4
draw 68 82 80 82
color gray.8
dot 67 79 81 79
ink dither 8 opaque
color f_red f_wht
frect 57 50 63 57
ink solid
color f_red_d
rect 57 50 63 57
color gray.9
dot 60 48 60 49
