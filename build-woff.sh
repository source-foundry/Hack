#!/bin/sh

# ///////////////////////////////////////////////////////////////////
#
# build-woff.sh
#  A shell script that builds the Hack woff web fonts from ttf files
#  Copyright 2018 Christopher Simpkins
#  MIT License
#
#  Usage: ./build-woff.sh (--system)
#     Arguments:
#     --system (optional) - build with a system installed version
#                           of build dependencies
#
#  NOTE: If you modify the source, you must build new ttf files
#        PRIOR to execution of this script. This script builds
#        directly from previous ttf builds, not source files.
#
# ///////////////////////////////////////////////////////////////////

# The sfnt2woff-zopfli build directory.
BUILD="$HOME/sfnt2woff-zopfli-build"

# sfnt2woff-zopfli version
SFNTWOFF_VERSION="1.1.0"
SFNTWOFF="sfnt2woff-zopfli-$SFNTWOFF_VERSION"

# Path to sfnt2woff-zopfli executable
SFNTWOFF_BIN="$BUILD/$SFNTWOFF/sfnt2woff-zopfli"
ZOPFLI_ITERATIONS="3"

# The font build directory paths and file paths for the woff builds
TTF_BUILD="build/ttf"
WOFF_BUILD="build/web/fonts"
REGULAR_TTF="Hack-Regular.ttf"
REGULAR_PRE="Hack-Regular.woff"
REGULAR_WOFF="hack-regular.woff"
BOLD_TTF="Hack-Bold.ttf"
BOLD_PRE="Hack-Bold.woff"
BOLD_WOFF="hack-bold.woff"
ITALIC_TTF="Hack-Italic.ttf"
ITALIC_PRE="Hack-Italic.woff"
ITALIC_WOFF="hack-italic.woff"
BOLDITALIC_TTF="Hack-BoldItalic.ttf"
BOLDITALIC_PRE="Hack-BoldItalic.woff"
BOLDITALIC_WOFF="hack-bolditalic.woff"

# test for number of arguments
if [ $# -gt 1 ]
	then
	    echo "Inappropriate arguments included in your command." 1>&2
	    echo "Usage: ./build-woff.sh (--system)" 1>&2
	    exit 1
fi

# determine if system installed executable on PATH is requested for build
# then test for presence of the sfnt2woff-zopfli build dependency based upon where it should be located
if [ "$1" = "--system" ]; then
	SFNTWOFF_BIN="sfnt2woff-zopfli"
	if ! which $SFNTWOFF_BIN; then
		echo "Unable to identify sfnt2woff-zopfli executable on system PATH.  Please install and try again." 1>&2
		exit 1
	else
		# display version of installed sfnt2woff-zopfli
		echo "Beginning web font build with $SFNTWOFF_BIN"
	fi
else
	if [ -f "$SFNTWOFF_BIN" ]; then
		echo "Beginning web font build with $SFNTWOFF_BIN"
	else
		echo "Unable to locate sfnt2woff-zopfli on the path $SFNTWOFF_BIN.  Please install this build dependency and then repeat your build attempt." 1>&2
	    exit 1
	fi

fi

# Build woff files from ttf files
# regular set
if ! "$SFNTWOFF_BIN" -n $ZOPFLI_ITERATIONS "$TTF_BUILD/$REGULAR_TTF"; then
	echo "Failed to build $REGULAR_WOFF from $REGULAR_TTF." 1>&2
	exit 1
else
	echo "Regular woff set successfully built from $REGULAR_TTF"
fi

# bold set
if ! "$SFNTWOFF_BIN" -n $ZOPFLI_ITERATIONS "$TTF_BUILD/$BOLD_TTF"; then
	echo "Failed to build $BOLD_WOFF from $BOLD_TTF" 1>&2
	exit 1
else
	echo "Bold woff set successfully built from $BOLD_TTF"
fi

# italic set
if ! "$SFNTWOFF_BIN" -n $ZOPFLI_ITERATIONS "$TTF_BUILD/$ITALIC_TTF"; then
	echo "Failed to build $BOLD_WOFF from $ITALIC_TTF" 1>&2
	exit 1
else
	echo "Italic woff set successfully built from $ITALIC_TTF"
fi

# bold italic set
if ! "$SFNTWOFF_BIN" -n $ZOPFLI_ITERATIONS "$TTF_BUILD/$BOLDITALIC_TTF"; then
	echo "Failed to build $BOLDITALIC_WOFF from $BOLDITALIC_TTF" 1>&2
	exit 1
else
	echo "Bold Italic woff set successfully built from $BOLDITALIC_TTF"
fi

echo "Moving woff files to build directory..."

# create directory if it does not exist
# (occurs with git + empty directories)
if ! [ -d "$WOFF_BUILD" ]; then
	mkdir $WOFF_BUILD
fi

# move woff files to appropriate build directory
mv "$TTF_BUILD/$REGULAR_PRE" "$WOFF_BUILD/$REGULAR_WOFF"
mv "$TTF_BUILD/$BOLD_PRE" "$WOFF_BUILD/$BOLD_WOFF"
mv "$TTF_BUILD/$ITALIC_PRE" "$WOFF_BUILD/$ITALIC_WOFF"
mv "$TTF_BUILD/$BOLDITALIC_PRE" "$WOFF_BUILD/$BOLDITALIC_WOFF"

echo " "

if [ -f "$WOFF_BUILD/$REGULAR_WOFF" ]; then
	echo "Regular woff build path: $WOFF_BUILD/$REGULAR_WOFF"
fi

if [ -f "$WOFF_BUILD/$BOLD_WOFF" ]; then
	echo "Bold woff build path: $WOFF_BUILD/$BOLD_WOFF"
fi

if [ -f "$WOFF_BUILD/$ITALIC_WOFF" ]; then
	echo "Italic woff build path: $WOFF_BUILD/$ITALIC_WOFF"
fi

if [ -f "$WOFF_BUILD/$BOLDITALIC_WOFF" ]; then
	echo "Bold Italic woff build path: $WOFF_BUILD/$BOLDITALIC_WOFF"
fi
