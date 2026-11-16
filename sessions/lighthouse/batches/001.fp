title "LIGHTHSE.LBM"
; ---------------- palette: every range runs dark -> light
pal 16 2 3 14
pal 27 10 6 26
ramp 16 27
pal 34 26 9 30
ramp 27 34
pal 39 44 14 26
ramp 34 39
pal 43 58 26 14
ramp 39 43
pal 47 63 54 28
ramp 43 47
range sky 16..47
pal 48 3 4 13
pal 54 10 8 26
ramp 48 54
pal 59 30 14 30
ramp 54 59
pal 63 52 32 26
ramp 59 63
range sea 48..63
pal 64 4 2 8
pal 67 14 7 14
ramp 64 67
pal 71 48 25 17
ramp 67 71
range rock 64..71
pal 72 11 9 21
pal 75 28 22 33
ramp 72 75
pal 79 63 53 40
ramp 75 79
range tower 72..79
pal 80 16 2 8
pal 85 60 16 10
ramp 80 85
range stripe 80..85
pal 86 12 6 21
pal 89 32 12 27
ramp 86 89
pal 93 63 38 22
ramp 89 93
range cloud 86..93
pal 94 63 63 52 suncore
pal 95 63 58 36 sunrim
pal 96 63 62 48
pal 97 63 54 30
pal 98 62 42 20
pal 99 54 30 22
pal 100 44 22 26
pal 101 54 30 22
pal 102 62 42 20
pal 103 63 54 30
range glint 96..103
cycle glint 2
pal 104 63 63 54
pal 105 63 59 38
pal 106 63 50 22
pal 107 58 38 14
range lamp 104..107
pal 108 3 6 6
pal 111 9 17 9
ramp 108 111
pal 113 34 32 10
ramp 111 113
range grass 108..113
pal 114 60 60 63
pal 115 40 42 56
pal 116 24 26 44
pal 117 40 42 56
range twinkle 114..117
cycle twinkle 5
pal 118 14 5 9 roofdark
pal 119 30 10 11 roofmid
pal 120 50 20 14 rooflit
pal 121 27 13 29 farland
pal 122 36 17 30 farlit
pal 123 58 46 44 foam
pal 124 42 32 40 foamdim
pal 125 62 60 52 moon

; ---------------- sky
ink gradient sky 0 0 0 127 bayer
frect 0 0 319 127
; glow around where the sun will sit
shade sky up 2
ink dither 8
fellipse 100 128 110 40
ink solid
fellipse 100 128 84 30
ink dither 8
fellipse 100 128 62 22
ink solid
fellipse 100 128 44 16
shade sky up 3
ink dither 8
fellipse 100 127 30 11
shade off
ink solid
; stars, only where the sky is still dark
stencil only 16..23
color twinkle.2
sprayrect 0 0 319 44 60
color twinkle.1
sprayrect 0 0 319 40 40
color twinkle.0
sprayrect 0 0 319 34 22
stencil off
; crescent moon, lit limb toward the sun
fatbits 46 22 m=moon
.....mm..
......mm.
.......mm
.......mm
m......mm
m.....mmm
.mm.mmmm.
..mmmmm..
end
; sun
color sunrim
fcircle 100 126 13
color suncore
fcircle 100 126 11
