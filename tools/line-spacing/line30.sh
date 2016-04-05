#!/bin/sh

# ////////////////////////////////////////////////////////////
#
# line30.sh
#  A shell script that modifies all .otf and .ttf fonts in the
#  working directory to 30% UPM line spacing
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

# modify all .ttf and .otf files with 30% UPM line spacing
font-line percent 30 *.ttf *.otf
