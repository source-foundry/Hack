#!/bin/sh

# ////////////////////////////////////////////////////////////
#
# line15.sh
#  A shell script that modifies all .otf and .ttf fonts to
#  15% UPM line spacing
#  Copyright 2016 Christopher Simpkins
#  MIT License
#
# ////////////////////////////////////////////////////////////

# Check for font-line application
which font-line

# if not present install it
if [[ $? -ne 0 ]]; then
	pip install font-line
fi

# modify all .ttf and .otf files with 15% UPM line spacing
font-line percent 15 *.ttf *.otf
