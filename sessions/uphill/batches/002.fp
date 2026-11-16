title "UPHILL.LBM"
; extra colours for this picture: far hills in haze
pal 224 30 42 50 haze1
pal 225 24 37 44 haze2
pal 226 17 31 34 haze3
pal 227 12 25 24 haze4
; ---------------- sky
ink gradient sky 0 0 0 122 bayer
frect 0 0 319 125
ink solid
; ---------------- cumulus: shadow mass first, then the lit tops pushed up and left
color cloud.3
fcircle 30 44 16
fcircle 52 38 20
fcircle 78 44 17
fcircle 100 50 12
fcircle 12 52 12
fcircle 120 54 9
frect 4 48 124 58
fcircle 262 34 13
fcircle 282 30 16
fcircle 302 36 13
frect 252 34 312 42
fcircle 140 20 8
fcircle 152 17 10
fcircle 166 21 7
color cloud.2
frect 6 57 122 59
frect 254 42 310 43
stencil only cloud.3
color cloud.5
fcircle 28 41 15
fcircle 50 34 19
fcircle 76 40 16
fcircle 98 47 11
fcircle 10 49 11
fcircle 118 52 8
fcircle 260 31 12
fcircle 280 27 15
fcircle 300 33 12
fcircle 139 18 7
fcircle 151 15 9
fcircle 165 19 6
stencil only cloud.5
color cloud.7
fcircle 26 37 12
fcircle 47 29 16
fcircle 73 36 12
fcircle 95 44 8
fcircle 9 46 8
fcircle 278 23 12
fcircle 258 28 9
fcircle 298 30 9
fcircle 150 13 7
ink dither 8
color cloud.6
fcircle 30 43 14
fcircle 52 36 18
fcircle 78 42 14
fcircle 281 28 13
stencil only cloud.3
ink dither 8
color cloud.4
frect 0 46 130 52
frect 250 30 315 36
stencil off
ink solid
; ---------------- far hills, hazier with distance
color haze1
fpoly 236 125 250 104 268 99 290 101 306 96 319 97 319 125
color haze2
fpoly 262 125 276 108 296 104 319 106 319 125
ink dither 6
color haze3
fpoly 262 125 276 110 296 106 319 108 319 125
ink solid
color haze3
fpoly 284 125 296 113 319 111 319 125
ink dither 8
color haze4
fpoly 284 125 296 115 319 113 319 125
ink solid
; treetops beyond the roof on the left
color leaf.5
fcircle 50 70 7
fcircle 60 71 6
fcircle 88 71 7
fcircle 40 73 5
color leaf.8
fcircle 48 68 4
fcircle 86 69 4
fcircle 58 69 3
color leaf.3
fcircle 54 73 4
fcircle 92 73 4
; ---------------- the two big spruces
color pine.1
fpoly 181 0 176 8 180 9 172 20 177 21 168 32 173 33 163 45 169 46 159 58 165 59 155 71 161 72 151 84 158 85 148 97 154 98 146 112 222 112 214 98 220 97 210 85 217 84 207 72 213 71 203 59 209 58 199 46 205 45 195 33 200 32 191 21 196 20 188 9 192 8 187 0
fpoly 229 0 223 9 227 10 218 22 223 23 213 35 219 36 208 49 215 50 204 63 211 64 200 77 207 78 196 91 203 92 193 105 199 106 195 112 272 112 266 106 271 105 262 92 268 91 258 78 264 77 254 64 260 63 250 50 256 49 246 36 251 35 241 23 246 22 237 10 241 9 235 0
stencil only pine.1
color pine.0
brush hline 4
sprayrect 186 4 222 112 150
sprayrect 236 4 272 112 170
color pine.2
brush hline 3
sprayrect 148 0 190 112 190
sprayrect 196 0 240 112 210
color pine.3
sprayrect 150 6 182 112 120
sprayrect 198 6 230 112 130
brush hline 2
color pine.4
sprayrect 152 20 178 112 60
sprayrect 200 20 226 112 70
color pine.5
sprayrect 154 40 172 110 22
sprayrect 202 40 220 110 26
stencil off
brush pixel
