#!/bin/sh

# ///////////////////////////////////////////////////////////////////
#
# build-woff2.sh
#  A shell script that builds the Hack woff2 web fonts from ttf files
#  Copyright 2018 Christopher Simpkins
#  MIT License
#
#  Usage: ./build-woff2.sh (--install-dependencies)
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

# The woff2 git clone directory.
BUILD="$HOME"
INST="$HOME/woff2"

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
	    echo "Usage: ./build-woff2.sh (--install-dependencies)" 1>&2
	    exit 1
fi

# Optional build dependency install request with syntax `./build-web.sh --install-dependencies`
if [ "$1" = "--install-dependencies" ]
	then
		# define the current directory (Hack repository)
		CUR_DIR=$(pwd)

		if test -d "$INST" -o -f "$INST"; then
		  echo "Build directory \`$INST' must not exist."
		  exit 1
		fi

		cd "$BUILD" || exit 1

		echo "#####"
		echo "git clone woff2 project"
		echo "#####"

		# clone the Source Foundry fork of the woff2 repo
		#   contains fix for OS X build bug - https://github.com/google/woff2/issues/73
		#   recursive flag to clone the brotli submodule within the woff2 repo
		git clone --recursive https://github.com/source-foundry/woff2.git

		cd "$INST" || exit 1

		echo "#####"
		echo "Build woff2"
		echo "#####"

		make clean all

		# make Hack repository the current directory again following the build
		cd "$CUR_DIR" || exit 1
fi


if [ -f "$WOFF2_BIN" ]; then
	echo "Beginning web font build with $WOFF2_BIN"
else
	echo "Unable to locate woff2_compress on path $WOFF2_BIN. Please attempt a manual install of this build dependency and then repeat your build attempt." 1>&2
	exit 1
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





