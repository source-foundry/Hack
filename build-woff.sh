#!/bin/sh

# ///////////////////////////////////////////////////////////////////
#
# build-woff.sh
#  A shell script that builds the Hack woff web fonts from ttf files
#  Copyright 2018 Christopher Simpkins
#  MIT License
#
#  Usage: ./build-woff.sh (--install-dependencies)
#     Arguments:
#     --install-dependencies (optional) - installs all
#       build dependencies prior to the build script execution
#
#  NOTE: If you change the source, you must build new ttf files
#        with build.sh PRIOR to execution of this script.
#        This script builds directly from previous ttf builds,
#        not source files.
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
	    echo "Usage: ./build-woff.sh (--install-dependencies)" 1>&2
	    exit 1
fi

# Optional build dependency install request with syntax `./build-web.sh --install-dependencies`
if [ "$1" = "--install-dependencies" ]
	then
		# define the current directory (Hack repository)
		CUR_DIR=$(pwd)

		if test -d "$BUILD" -o -f "$BUILD"; then
		  echo "Build directory \`$BUILD' must not exist."
		  exit 1
		fi

		mkdir "$BUILD"

		cd "$BUILD" || exit 1

		echo "#####"
		echo "Download archive."
		echo "#####"

		curl -L -O "https://github.com/bramstein/sfnt2woff-zopfli/archive/v$SFNTWOFF_VERSION.tar.gz"

		echo "#####"
		echo "Extract archives."
		echo "#####"

		tar -xzvf "v$SFNTWOFF_VERSION.tar.gz"

		cd "$SFNTWOFF" || exit 1

		echo "#####"
		echo "Build $SFNTWOFF."
		echo "#####"

		make

		# make Hack repository the current directory again following the build
		cd "$CUR_DIR" || exit 1
fi


if [ -f "$SFNTWOFF_BIN" ]; then
	echo "Beginning web font build with $SFNTWOFF"
else
	echo "Unable to locate sfnt2woff-zopfli on the path $SFNTWOFF_BIN.  Please attempt a manual install of this build dependency and then repeat your build attempt." 1>&2
	exit 1
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





