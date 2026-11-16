; HOUSE PALETTE -- shared by every picture of the house, so the colours agree.
; Every range runs dark -> light. Entries 224..255 are left free for each picture.
; ---- sky and clouds
pal 16 16 32 56
pal 31 50 58 63
ramp 16 31 sky
pal 32 34 40 52
pal 39 63 63 63
ramp 32 39 cloud
; ---- cedar shakes on the walls: plum shadow -> red-brown -> warm sunlit
pal 40 6 2 5
pal 46 20 7 7
ramp 40 46
pal 51 33 14 10
ramp 46 51
pal 55 50 28 17
ramp 51 55
range shake 40..55
; ---- asphalt roof shingles: plum -> brick red -> sun-bleached salmon
pal 56 12 3 7
pal 60 26 9 11
ramp 56 60
pal 64 39 17 16
ramp 60 64
pal 67 55 35 29
ramp 64 67
range roof 56..67
; ---- white paint (window sashes, doors): blue shadow -> white
pal 68 22 24 34
pal 75 63 63 60
ramp 68 75 trim
; ---- warm wood (oak trim, floors, cabinets, furniture)
pal 76 8 4 2
pal 84 36 20 8
ramp 76 84
pal 91 58 42 22
ramp 84 91
range wood 76..91
; ---- dark wood (paneling, fascia boards)
pal 92 4 2 2
pal 99 28 15 10
ramp 92 99 darkwood
; ---- broadleaf foliage: blue-black -> green -> yellow-green
pal 100 2 7 8
pal 106 10 26 10
ramp 100 106
pal 111 26 44 12
ramp 106 111
pal 115 50 60 24
ramp 111 115
range leaf 100..115
; ---- conifer and juniper
pal 116 2 7 9
pal 119 8 24 19
ramp 116 119
pal 123 36 52 38
ramp 119 123
range pine 116..123
; ---- lawn
pal 124 5 16 9
pal 129 20 40 12
ramp 124 129
pal 133 42 56 20
ramp 129 133
pal 135 54 62 34
ramp 133 135
range grass 124..135
; ---- earth, stone, bark
pal 136 6 4 3
pal 142 28 22 16
ramp 136 142
pal 147 52 48 40
ramp 142 147
range earth 136..147
; ---- neutral greys
pal 148 3 3 4
pal 163 60 60 60
ramp 148 163 gray
; ---- window glass
pal 164 4 8 12
pal 171 40 52 58
ramp 164 171 glass
; ---- flowers (single colours, dark / plain / light)
pal 172 36 4 6 f_red_d
pal 173 58 10 10 f_red
pal 174 63 30 26 f_red_l
pal 175 48 16 30 f_pink_d
pal 176 62 32 44 f_pink
pal 177 63 48 54 f_pink_l
pal 178 34 6 30 f_mag_d
pal 179 54 14 46 f_mag
pal 180 50 22 4 f_org_d
pal 181 63 36 8 f_org
pal 182 52 42 6 f_yel_d
pal 183 63 58 14 f_yel
pal 184 63 62 38 f_yel_l
pal 185 20 8 34 f_pur_d
pal 186 36 18 52 f_pur
pal 187 50 36 62 f_pur_l
pal 188 8 14 40 f_blu_d
pal 189 20 32 58 f_blu
pal 190 38 50 63 f_blu_l
pal 191 44 46 52 f_wht_d
pal 192 63 63 63 f_wht
pal 193 60 56 44 f_cream
pal 194 62 46 34 f_peach
pal 195 52 44 60 f_lilac
; ---- weathered fence boards
pal 196 8 6 5
pal 203 42 34 27
ramp 196 203 fence
; ---- interior painted walls: shadow -> white
pal 204 26 28 36
pal 211 62 62 60
ramp 204 211 wall
; ---- fawn
pal 212 16 9 5
pal 217 52 36 22
ramp 212 217 fawn
; ---- brick
pal 218 18 6 4
pal 223 50 24 16
ramp 218 223 brick
