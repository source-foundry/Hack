#!/bin/sh

# ////////////////////////////////////////////////////////////
#
# line10.sh
#  A shell script that modifies all .otf and .ttf fonts in the
#  working directory to 10% UPM line spacing
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

# modify all .ttf and .otf files with 10% UPM line spacing
font-line percent 10 *.ttf *.otf
