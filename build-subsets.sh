#!/bin/sh

# //////////////////////////////////////////////////////////////////////
#
# build-subsets.sh
#  A shell script that builds the Hack web font subsets from UFO source
#  Copyright 2018 Christopher Simpkins
#  MIT License
#
#  Usage: ./build-subsets.sh
#
#  NOTE: must install build dependencies in:
#        1) build-ttf.sh
#        2) build-woff.sh
#        3) build-woff2.sh
#       before you execute this script.  You can do this with:
#
#
#       $ ./build-ttf.sh --install-dependencies
#       $ ./build-woff.sh --install-dependencies
#       $ ./build-woff2.sh --install-dependencies
#
# //////////////////////////////////////////////////////////////////////

# ttfautohint local install path from Werner Lemberg's ttfautohint-build.sh install script
#   - This is revised to ttfautohint on the user's PATH if this local install is not identified
#     then the identified ttfautohint is used to execute hinting.  Versions of ttfautohint < 1.6 exit with status
#     code 1 due to use of -R option
#   - The intent is to support use of ttfautohint installed on a user's PATH (e.g. they've previously installed it)
TTFAH="$HOME/ttfautohint-build/local/bin/ttfautohint"

# The sfnt2woff-zopfli build directory.
SFNTWOFF_BUILD="$HOME/sfnt2woff-zopfli-build"

# sfnt2woff-zopfli version
SFNTWOFF_VERSION="1.1.0"
SFNTWOFF="sfnt2woff-zopfli-$SFNTWOFF_VERSION"

# Path to sfnt2woff-zopfli executable
SFNTWOFF_BIN="$SFNTWOFF_BUILD/$SFNTWOFF/sfnt2woff-zopfli"
ZOPFLI_ITERATIONS="3"

# The woff2 git clone directory.
WOFF2_BUILD="$HOME"
# woff2 executable path
WOFF2_BIN="$WOFF2_BUILD/woff2/woff2_compress"

# temporary source directory for subset source files
TEMP_SOURCE="source/temp"

# The font build directory paths and file paths for the woff builds
TTF_BUILD="master_ttf"

REGULAR_TTF="Hack-Regular.ttf"
REGULAR_WOFF_PRE="Hack-Regular.woff"
REGULAR_WOFF="hack-regular-subset.woff"
REGULAR_WOFF2_PRE="Hack-Regular.woff2"
REGULAR_WOFF2="hack-regular-subset.woff2"

BOLD_TTF="Hack-Bold.ttf"
BOLD_WOFF_PRE="Hack-Bold.woff"
BOLD_WOFF="hack-bold-subset.woff"
BOLD_WOFF2_PRE="Hack-Bold.woff2"
BOLD_WOFF2="hack-bold-subset.woff2"

ITALIC_TTF="Hack-Italic.ttf"
ITALIC_WOFF_PRE="Hack-Italic.woff"
ITALIC_WOFF="hack-italic-subset.woff"
ITALIC_WOFF2_PRE="Hack-Italic.woff2"
ITALIC_WOFF2="hack-italic-subset.woff2"

BOLDITALIC_TTF="Hack-BoldItalic.ttf"
BOLDITALIC_WOFF_PRE="Hack-BoldItalic.woff"
BOLDITALIC_WOFF="hack-bolditalic-subset.woff"
BOLDITALIC_WOFF2_PRE="Hack-BoldItalic.woff2"
BOLDITALIC_WOFF2="hack-bolditalic-subset.woff2"

# release directory path for web fonts
WEB_BUILD="build/web/fonts"

# test for number of arguments
if [ $# -gt 0 ]
	then
	    echo "Inappropriate arguments included in your command." 1>&2
	    echo "Usage: ./build-subsets.sh" 1>&2
	    exit 1
fi

# ////////////////////////////////////////
#
#
#  Confirm that dependencies are installed
#
#
# ////////////////////////////////////////

INSTALLFLAG=0

echo "Confirming that build dependencies are installed..."
echo " "

# fontmake installed
if ! which fontmake
	then
	    echo "fontmake was not found.  Please install all build dependencies with 'make build-with-dependencies', then attempt your build again." 1>&2
	    INSTALLFLAG=1
fi

# fontTools python library can be imported
if ! python -c "import fontTools"
	then
	    echo "The fontTools library was not found.  Please install all build dependencies with 'make build-with-dependencies', then attempt your build again." 1>&2
	    INSTALLFLAG=1
else
	echo "fontTools Python library identified"
fi

# ttfautohint installed
#   - tests for install to local path from ttfautohint-build.sh script
#   - if not found on this path, tests for install on system PATH - if found, revises TTFAH to the string "ttfautohint" for execution of instruction sets
if ! [ -f "$TTFAH" ]
	then
	    if ! which ttfautohint
	    	then
	            echo "ttfautohint was not found.  Please install all build dependencies with 'make build-with-dependencies', then attempt your build again." 1>&2
	            INSTALLFLAG=1
	    else
	    	TTFAH="ttfautohint"  # revise TTFAH variable to ttfautohint installed on the user's PATH for excecution of hints below
	    	echo "ttfautohint executable identified"
	    fi
	else
		echo "ttfautohint executable identified"
fi

# sfntwoff-zopfli installed
if ! [ -f "$SFNTWOFF_BIN" ]
	then
	    echo "sfnt2woff-zopfli was not found on the path $SFNTWOFF_BIN.  Please install all build dependencies with 'make build-with-dependencies', then attempt your build again." 1>&2
	    INSTALLFLAG=1
else
	echo "sfnt2woff-zopfli executable identified"
fi

# woff2 installed
if ! [ -f "$WOFF2_BIN" ]
	then
	    echo "woff2_compress was not found on the path $WOFF2_BIN.  Please install all build dependencies with 'make build-with-dependencies', then attempt your build again." 1>&2
	    INSTALLFLAG=1
else
	echo "woff2_compress executable identified"
fi

# if any of the dependency installs failed, exit and do not attempt build, notify user
if [ $INSTALLFLAG -eq 1 ]
	then
	    echo "Build canceled." 1>&2
	    exit 1
fi

# ////////////////////////////////////////////////
#
#
#  Create temporary source files with lib.plist
#    replacements that include subset definitions
#
#
# ////////////////////////////////////////////////

# cleanup any previously created temp directory that was not removed
if ! [ -d "$TEMP_SOURCE" ]; then
	rm -rf $TEMP_SOURCE
fi

# create temp directory for subset source files
mkdir $TEMP_SOURCE

# copy source to temporary directory
cp -r source/Hack-Regular.ufo $TEMP_SOURCE/Hack-Regular.ufo
cp -r source/Hack-Italic.ufo $TEMP_SOURCE/Hack-Italic.ufo
cp -r source/Hack-Bold.ufo $TEMP_SOURCE/Hack-Bold.ufo
cp -r source/Hack-BoldItalic.ufo $TEMP_SOURCE/Hack-BoldItalic.ufo

# copy lib.plist files with subset definitions to temporary source directories
cp source/subset-lib/lib-regular.plist $TEMP_SOURCE/Hack-Regular.ufo/lib.plist
cp source/subset-lib/lib-italic.plist $TEMP_SOURCE/Hack-Italic.ufo/lib.plist
cp source/subset-lib/lib-bold.plist $TEMP_SOURCE/Hack-Bold.ufo/lib.plist
cp source/subset-lib/lib-bolditalic.plist $TEMP_SOURCE/Hack-BoldItalic.ufo/lib.plist

# /////////////////////////////////////////////
#
#
#  Begin subset ttf font build from UFO source
#
#
# /////////////////////////////////////////////

echo "Starting web font subset build..."
echo " "

# remove master_ttf directory if a previous build failed + exited early and it was not cleaned up
if [ -d "master_ttf" ]; then
	rm -rf master_ttf
fi

# build regular subset

if ! fontmake --subset -u "$TEMP_SOURCE/Hack-Regular.ufo" -o ttf
	then
	    echo "Unable to build the Hack-Regular variant subset.  Build canceled." 1>&2
	    exit 1
fi

# build bold subset
if ! fontmake --subset -u "$TEMP_SOURCE/Hack-Bold.ufo" -o ttf
	then
	    echo "Unable to build the Hack-Bold variant subset.  Build canceled." 1>&2
	    exit 1
fi

# build italic subset
if ! fontmake --subset -u "$TEMP_SOURCE/Hack-Italic.ufo" -o ttf
	then
	    echo "Unable to build the Hack-Italic variant subset.  Build canceled." 1>&2
	    exit 1
fi

# build bold italic subset

if ! fontmake --subset -u "$TEMP_SOURCE/Hack-BoldItalic.ufo" -o ttf
	then
	    echo "Unable to build the Hack-BoldItalic variant subset.  Build canceled." 1>&2
	    exit 1
fi


# /////////////////////////////////////////////
#
#
#  Post build fixes
#
#
# /////////////////////////////////////////////

# DSIG table fix with adapted fontbakery Python script
echo " "
echo "Attempting DSIG table fixes with fontbakery..."
echo " "
if ! python postbuild_processing/fixes/fix-dsig.py master_ttf/*.ttf
	then
	    echo "Unable to complete DSIG table fixes on the release files"
	    exit 1
fi

# fstype value fix with adapted fontbakery Python script
echo " "
echo "Attempting fstype fixes with fontbakery..."
echo " "
if ! python postbuild_processing/fixes/fix-fstype.py master_ttf/*.ttf
	then
	    echo "Unable to complete fstype fixes on the release files"
	    exit 1
fi

# /////////////////////////////////////////////
#
#
#  Hinting of ttf subsets
#
#
# /////////////////////////////////////////////

echo " "
echo "Attempting ttfautohint hinting..."
echo " "
# make a temporary directory for the hinted files
mkdir master_ttf/hinted

# Hack-Regular.ttf
if ! "$TTFAH" -l 6 -r 50 -x 10 -H 181 -D latn -f latn -w G -W -t -X "" -I -R "master_ttf/Hack-Regular.ttf" -m "postbuild_processing/tt-hinting/Hack-Regular-TA.txt" "master_ttf/Hack-Regular.ttf" "master_ttf/hinted/Hack-Regular.ttf"
	then
	    echo "Unable to execute ttfautohint on the Hack-Regular variant subset.  Build canceled." 1>&2
	    exit 1
fi
echo "master_ttf/Hack-Regular.ttf subset - successful hinting with ttfautohint"

# Hack-Bold.ttf
if ! "$TTFAH" -l 6 -r 50 -x 10 -H 260 -D latn -f latn -w G -W -t -X "" -I -R "master_ttf/Hack-Regular.ttf" -m "postbuild_processing/tt-hinting/Hack-Bold-TA.txt" "master_ttf/Hack-Bold.ttf" "master_ttf/hinted/Hack-Bold.ttf"
	then
	    echo "Unable to execute ttfautohint on the Hack-Bold variant subset.  Build canceled." 1>&2
	    exit 1
fi
echo "master_ttf/Hack-Bold.ttf subset - successful hinting with ttfautohint"

# Hack-Italic.ttf
if ! "$TTFAH" -l 6 -r 50 -x 10 -H 145 -D latn -f latn -w G -W -t -X "" -I -R "master_ttf/Hack-Regular.ttf" -m "postbuild_processing/tt-hinting/Hack-Italic-TA.txt" "master_ttf/Hack-Italic.ttf" "master_ttf/hinted/Hack-Italic.ttf"
	then
	    echo "Unable to execute ttfautohint on the Hack-Italic variant subset.  Build canceled." 1>&2
	    exit 1
fi
echo "master_ttf/Hack-Italic.ttf subset - successful hinting with ttfautohint"

# Hack-BoldItalic.ttf
if ! "$TTFAH" -l 6 -r 50 -x 10 -H 265 -D latn -f latn -w G -W -t -X "" -I -R "master_ttf/Hack-Regular.ttf" -m "postbuild_processing/tt-hinting/Hack-BoldItalic-TA.txt" "master_ttf/Hack-BoldItalic.ttf" "master_ttf/hinted/Hack-BoldItalic.ttf"
	then
	    echo "Unable to execute ttfautohint on the Hack-BoldItalic variant subset.  Build canceled." 1>&2
	    exit 1
fi
echo "master_ttf/Hack-BoldItalic.ttf subset - successful hinting with ttfautohint"
echo " "

# /////////////////////////////////////////////
#
#
#  Build woff subsets
#
#
# /////////////////////////////////////////////

# regular set
if ! "$SFNTWOFF_BIN" -n $ZOPFLI_ITERATIONS "$TTF_BUILD/$REGULAR_TTF"; then
	echo "Failed to build $REGULAR_WOFF from $REGULAR_TTF." 1>&2
	exit 1
else
	echo "Regular woff subset successfully built from $REGULAR_TTF"
fi

# bold set
if ! "$SFNTWOFF_BIN" -n $ZOPFLI_ITERATIONS "$TTF_BUILD/$BOLD_TTF"; then
	echo "Failed to build $BOLD_WOFF from $BOLD_TTF" 1>&2
	exit 1
else
	echo "Bold woff subset successfully built from $BOLD_TTF"
fi

# italic set
if ! "$SFNTWOFF_BIN" -n $ZOPFLI_ITERATIONS "$TTF_BUILD/$ITALIC_TTF"; then
	echo "Failed to build $BOLD_WOFF from $ITALIC_TTF" 1>&2
	exit 1
else
	echo "Italic woff subset successfully built from $ITALIC_TTF"
fi

# bold italic set
if ! "$SFNTWOFF_BIN" -n $ZOPFLI_ITERATIONS "$TTF_BUILD/$BOLDITALIC_TTF"; then
	echo "Failed to build $BOLDITALIC_WOFF from $BOLDITALIC_TTF" 1>&2
	exit 1
else
	echo "Bold Italic woff subset successfully built from $BOLDITALIC_TTF"
fi

# /////////////////////////////////////////////
#
#
#  Build woff2 subsets
#
#
# /////////////////////////////////////////////

echo " "

# regular set
if ! "$WOFF2_BIN" "$TTF_BUILD/$REGULAR_TTF"; then
	echo "Failed to build woff2 subset from $REGULAR_TTF." 1>&2
	exit 1
else
	echo "Regular woff2 font subset successfully built from $REGULAR_TTF"
fi

# bold set
if ! "$WOFF2_BIN" "$TTF_BUILD/$BOLD_TTF"; then
	echo "Failed to build woff2 subset from $BOLD_TTF" 1>&2
	exit 1
else
	echo "Bold woff2 subset successfully built from $BOLD_TTF"
fi

# italic set
if ! "$WOFF2_BIN" "$TTF_BUILD/$ITALIC_TTF"; then
	echo "Failed to build woff2 subset from $ITALIC_TTF" 1>&2
	exit 1
else
	echo "Italic woff2 subset successfully built from $ITALIC_TTF"
fi

# bold italic set
if ! "$WOFF2_BIN" "$TTF_BUILD/$BOLDITALIC_TTF"; then
	echo "Failed to build woff2 subset from $BOLDITALIC_TTF" 1>&2
	exit 1
else
	echo "Bold Italic woff2 subset successfully built from $BOLDITALIC_TTF"
fi


# //////////////////////////////////////////////
#
#
#  Move web font subset files to build directory
#
#
# //////////////////////////////////////////////

# create the build directory if it does not exist
if ! [ -d "$WEB_BUILD" ]; then
	mkdir $WEB_BUILD
fi

echo " "
echo "Moving woff files to build directory..."

# move woff files to appropriate build directory
mv "$TTF_BUILD/$REGULAR_WOFF_PRE" "$WEB_BUILD/$REGULAR_WOFF"
mv "$TTF_BUILD/$BOLD_WOFF_PRE" "$WEB_BUILD/$BOLD_WOFF"
mv "$TTF_BUILD/$ITALIC_WOFF_PRE" "$WEB_BUILD/$ITALIC_WOFF"
mv "$TTF_BUILD/$BOLDITALIC_WOFF_PRE" "$WEB_BUILD/$BOLDITALIC_WOFF"

if [ -f "$WEB_BUILD/$REGULAR_WOFF" ]; then
	echo "Regular woff build path: $WEB_BUILD/$REGULAR_WOFF"
fi

if [ -f "$WEB_BUILD/$BOLD_WOFF" ]; then
	echo "Bold woff build path: $WEB_BUILD/$BOLD_WOFF"
fi

if [ -f "$WEB_BUILD/$ITALIC_WOFF" ]; then
	echo "Italic woff build path: $WEB_BUILD/$ITALIC_WOFF"
fi

if [ -f "$WEB_BUILD/$BOLDITALIC_WOFF" ]; then
	echo "Bold Italic woff build path: $WEB_BUILD/$BOLDITALIC_WOFF"
fi

echo "Moving woff2 files to build directory..."

# move woff files to appropriate build directory
mv "$TTF_BUILD/$REGULAR_WOFF2_PRE" "$WEB_BUILD/$REGULAR_WOFF2"
mv "$TTF_BUILD/$BOLD_WOFF2_PRE" "$WEB_BUILD/$BOLD_WOFF2"
mv "$TTF_BUILD/$ITALIC_WOFF2_PRE" "$WEB_BUILD/$ITALIC_WOFF2"
mv "$TTF_BUILD/$BOLDITALIC_WOFF2_PRE" "$WEB_BUILD/$BOLDITALIC_WOFF2"

if [ -f "$WEB_BUILD/$REGULAR_WOFF2" ]; then
	echo "Regular woff2 subset build path: $WEB_BUILD/$REGULAR_WOFF2"
fi

if [ -f "$WEB_BUILD/$BOLD_WOFF2" ]; then
	echo "Bold woff2 subset build path: $WEB_BUILD/$BOLD_WOFF2"
fi

if [ -f "$WEB_BUILD/$ITALIC_WOFF2" ]; then
	echo "Italic woff2 subset build path: $WEB_BUILD/$ITALIC_WOFF2"
fi

if [ -f "$WEB_BUILD/$BOLDITALIC_WOFF2" ]; then
	echo "Bold Italic woff2 subset build path: $WEB_BUILD/$BOLDITALIC_WOFF2"
fi

# //////////////////////////////////////////////
#
#
#  Cleanup temp directory
#
#
# //////////////////////////////////////////////

rm -rf master_ttf
rm -rf "$TEMP_SOURCE"

