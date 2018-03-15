#!/bin/sh

# ///////////////////////////////////////////////////////////////////
#
# build-woff2.sh
#  A shell script that builds the Hack woff2 web fonts from ttf files
#  Copyright 2018 Christopher Simpkins
#  MIT License
#
#  Usage: ./build-woff2.sh (--system)
#     Arguments:
#     --system (optional) - use build dependencies installed on PATH
#
#  NOTE: If you change the source, you must build new ttf files
#        PRIOR to the execution of this script. This script builds
#        directly from previous ttf builds, not source files.
#
# ///////////////////////////////////////////////////////////////////

# The woff2 git clone directory.
BUILD="$HOME"

# woff2 executable path
WOFF2_BIN="$BUILD/woff2/woff2_compress"


# The font build directory paths and file paths for the woff builds
TTF_BUILD="build/ttf"
WOFF_BUILD="build/web/fonts"
REGULAR_TTF="Hack-Regular.ttf"
REGULAR_PRE="Hack-Regular.woff2"
REGULAR_WOFF="hack-regular.woff2"
BOLD_TTF="Hack-Bold.ttf"
BOLD_PRE="Hack-Bold.woff2"
BOLD_WOFF="hack-bold.woff2"
ITALIC_TTF="Hack-Italic.ttf"
ITALIC_PRE="Hack-Italic.woff2"
ITALIC_WOFF="hack-italic.woff2"
BOLDITALIC_TTF="Hack-BoldItalic.ttf"
BOLDITALIC_PRE="Hack-BoldItalic.woff2"
BOLDITALIC_WOFF="hack-bolditalic.woff2"

# test for number of arguments
if [ $# -gt 1 ]
	then
	    echo "Inappropriate arguments included in your command." 1>&2
	    echo "Usage: ./build-woff2.sh (--system)" 1>&2
	    exit 1
fi

# determine if system installed executable on PATH is requested for build
# then test for presence of the woff2_compress build dependency based upon where it should be located
if [ "$1" = "--system" ]; then
	WOFF2_BIN="woff2_compress"
	if ! which $WOFF2_BIN; then
		echo "Unable to identify woff2_compress executable on system PATH.  Please install and try again." 1>&2
		exit 1
	else
		# display version of installed woff2_compress
		echo "Beginning web font build with $WOFF2_BIN"
	fi
fi

# test for woff2_compress executable with default build approach
if [ $# -eq 0 ]; then
	if [ -f "$WOFF2_BIN" ]; then
		echo "Beginning web font build with $WOFF2_BIN"
	else
		echo "Unable to locate woff2_compress on path $WOFF2_BIN. Please attempt a manual install of this build dependency and then repeat your build attempt." 1>&2
		exit 1
	fi
fi

# Build woff2 files from ttf files
# regular set
if ! "$WOFF2_BIN" "$TTF_BUILD/$REGULAR_TTF"; then
	echo "Failed to build woff2 from $REGULAR_TTF." 1>&2
	exit 1
else
	echo "Regular woff2 font set successfully built from $REGULAR_TTF"
fi

# bold set
if ! "$WOFF2_BIN" "$TTF_BUILD/$BOLD_TTF"; then
	echo "Failed to build woff2 from $BOLD_TTF" 1>&2
	exit 1
else
	echo "Bold woff2 set successfully built from $BOLD_TTF"
fi

# italic set
if ! "$WOFF2_BIN" "$TTF_BUILD/$ITALIC_TTF"; then
	echo "Failed to build woff2 from $ITALIC_TTF" 1>&2
	exit 1
else
	echo "Italic woff2 set successfully built from $ITALIC_TTF"
fi

# bold italic set
if ! "$WOFF2_BIN" "$TTF_BUILD/$BOLDITALIC_TTF"; then
	echo "Failed to build woff2 from $BOLDITALIC_TTF" 1>&2
	exit 1
else
	echo "Bold Italic woff2 set successfully built from $BOLDITALIC_TTF"
fi

echo "Moving woff2 files to build directory..."

# create directory if it does not exist
# (occurs with git + empty directories)
if ! [ -d "$WOFF_BUILD" ]; then
	mkdir $WOFF_BUILD
fi

# move woff2 files to appropriate build directory
mv "$TTF_BUILD/$REGULAR_PRE" "$WOFF_BUILD/$REGULAR_WOFF"
mv "$TTF_BUILD/$BOLD_PRE" "$WOFF_BUILD/$BOLD_WOFF"
mv "$TTF_BUILD/$ITALIC_PRE" "$WOFF_BUILD/$ITALIC_WOFF"
mv "$TTF_BUILD/$BOLDITALIC_PRE" "$WOFF_BUILD/$BOLDITALIC_WOFF"

echo " "

if [ -f "$WOFF_BUILD/$REGULAR_WOFF" ]; then
	echo "Regular woff2 build path: $WOFF_BUILD/$REGULAR_WOFF"
fi

if [ -f "$WOFF_BUILD/$BOLD_WOFF" ]; then
	echo "Bold woff2 build path: $WOFF_BUILD/$BOLD_WOFF"
fi

if [ -f "$WOFF_BUILD/$ITALIC_WOFF" ]; then
	echo "Italic woff2 build path: $WOFF_BUILD/$ITALIC_WOFF"
fi

if [ -f "$WOFF_BUILD/$BOLDITALIC_WOFF" ]; then
	echo "Bold Italic woff2 build path: $WOFF_BUILD/$BOLDITALIC_WOFF"
fi





