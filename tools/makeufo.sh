# ------------------------------------------------------------------
#
#  makeufo.sh
#  Copyright 2015 Christopher Simpkins
#  MIT license
#
# ------------------------------------------------------------------

# DESCRIPTION
# Creates UFO font source files from FontLab Studio .vfb source files
# Executable: vfb2ufo (http://blog.fontlab.com/font-utility/vfb2ufo/)

# PostScript Source Files
vfb2ufo -fo -ttx -64 -p ../source/ufo ../source/vfb/Hack-Regular-PS.vfb
vfb2ufo -fo -ttx -64 -p ../source/ufo ../source/vfb/Hack-Bold-PS.vfb
vfb2ufo -fo -ttx -64 -p ../source/ufo ../source/vfb/Hack-Italic-PS.vfb
vfb2ufo -fo -ttx -64 -p ../source/ufo ../source/vfb/Hack-BoldItalic-PS.vfb

# TrueType Source Files
vfb2ufo -fo -ttx -64 -p ../source/ufo ../source/vfb/Hack-Regular-TT.vfb
vfb2ufo -fo -ttx -64 -p ../source/ufo ../source/vfb/Hack-Bold-TT.vfb
vfb2ufo -fo -ttx -64 -p ../source/ufo ../source/vfb/Hack-Italic-TT.vfb
vfb2ufo -fo -ttx -64 -p ../source/ufo ../source/vfb/Hack-BoldItalic-TT.vfb


