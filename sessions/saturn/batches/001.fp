title "SATURN.PIC"
clear black
; ---------------- rings, drawn whole on empty space
color magenta
fellipse 190 105 120 23
color white
fellipse 190 105 117 22.2
color black
fellipse 190 105 107 20.2
color cyan
fellipse 190 105 104 19.5
color white
fellipse 190 105 97 18.1
color cyan
fellipse 190 105 91 16.9
ink dither 8 opaque
color white cyan
fellipse 190 105 100 18.8
ink solid
color cyan
fellipse 190 105 93 17.3
ink dither 8 opaque
color magenta black
fellipse 190 105 86 15.9
ink solid
color black
fellipse 190 105 77 14.2
; keep the near half as a brush: it goes back on after the planet is painted
pickup 66 105 314 130 black

; ---------------- nebula and stars, only where space is still empty
stencil only black
; airbrushed, so it clumps like dust instead of sitting on a grid
color magenta
spray 30 22 44 420
spray 62 40 50 520
spray 100 58 44 380
spray 48 30 20 260
spray 134 74 30 160
color cyan
spray 92 50 30 220
spray 120 66 22 120
spray 20 14 24 120
color white
spray 56 34 14 40
color cyan
spray 284 170 46 380
spray 262 182 30 180
color magenta
spray 296 160 28 150
ink solid
color white
sprayrect 0 0 319 199 90
color cyan
sprayrect 0 0 319 199 70
color magenta
sprayrect 0 0 319 199 50
stencil off
