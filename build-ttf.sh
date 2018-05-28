#!/bin/sh

# /////////////////////////////////////////////////////////////////
#
# build-ttf.sh
#  A shell script that builds the Hack ttf fonts from UFO source
#  Copyright 2018 Christopher Simpkins
#  MIT License
#
#  Usage: ./build-ttf.sh (--system)
#     Arguments:
#     --system (optional) - use system installed build dependencies
#
# /////////////////////////////////////////////////////////////////

# default build tooling definitions
TTFAH="$HOME/ttfautohint-build/local/bin/ttfautohint"
FONTMAKE="pipenv run fontmake"
PYTHON="pipenv run python"
INSTALLFLAG=0

# test for number of arguments
if [ $# -gt 1 ]
	then
	    echo "Inappropriate arguments included in your command." 1>&2
	    echo "Usage: ./build-ttf.sh (--system)" 1>&2
	    exit 1
fi

# Optional build with system-installed build dependencies instead of pinned build process defined versions
if [ "$1" = "--system" ]
	then
		# re-define the default executables to executables that exist on PATH
		TTFAH="ttfautohint"
		FONTMAKE="fontmake"
		PYTHON="python3"

		echo "================================="
        echo "  BUILD ENVIRONMENT"
        echo "================================="
		# test re-defined system-installed build dependency paths
		if ! which "$TTFAH"; then
			echo "Unable to identify a system installed version of ttfautohint.  Please install and try again." 1>&2
			INSTALLFLAG=1
		else
			ttfautohint --version
		fi
		if ! which "$FONTMAKE"; then
			echo "Unable to identify a system installed version of fontmake.  Please install and try again." 1>&2
			INSTALLFLAG=1
		else
			"$FONTMAKE" --version
		fi
		if ! which "$PYTHON"; then
			echo "Unable to identify a Python 3 installation.  Please install and try again." 1>&2
			INSTALLFLAG=1
		else
			"$PYTHON" --version
		fi
		echo "================================="
        echo " "
        echo "================================="
        echo " "
fi

# ttfautohint path test for default builds
# test for local ttfautohint install using repository provided install script and defined ttfautohint version (and its dependencies)
# no tests for Python build dependencies here because they are always installed by default & tested in the pipenv virtualenv before these steps
if [ $# -eq 0 ]; then
	if ! [ -f "$TTFAH" ]; then
		echo "Unable to identify the expected local install path for ttfautohint.  Please install and try again." 1>&2
		INSTALLFLAG=1
	fi
fi

# If any of the dependency checks failed, exit the build and notify user
if [ $INSTALLFLAG -eq 1 ]; then
	    echo "Build canceled." 1>&2
	    exit 1
fi

# Desktop ttf font build

echo "Starting build..."
echo " "

# remove any existing release files from the build directory
if [ -f "build/ttf/Hack-Regular.ttf" ]; then
	rm build/ttf/Hack-Regular.ttf
fi

if [ -f "build/ttf/Hack-Italic.ttf" ]; then
	rm build/ttf/Hack-Italic.ttf
fi

if [ -f "build/ttf/Hack-Bold.ttf" ]; then
	rm build/ttf/Hack-Bold.ttf
fi

if [ -f "build/ttf/Hack-BoldItalic.ttf" ]; then
	rm build/ttf/Hack-BoldItalic.ttf
fi

# remove master_ttf directory if a previous build failed + exited early and it was not cleaned up

if [ -d "master_ttf" ]; then
	rm -rf master_ttf
fi

# build regular set

if ! $FONTMAKE -u "source/Hack-Regular.ufo" -o ttf
	then
	    echo "Unable to build the Hack-Regular variant set.  Build canceled." 1>&2
	    exit 1
fi

# build bold set
if ! $FONTMAKE -u "source/Hack-Bold.ufo" -o ttf
	then
	    echo "Unable to build the Hack-Bold variant set.  Build canceled." 1>&2
	    exit 1
fi

# build italic set
if ! $FONTMAKE -u "source/Hack-Italic.ufo" -o ttf
	then
	    echo "Unable to build the Hack-Italic variant set.  Build canceled." 1>&2
	    exit 1
fi

# build bold italic set

if ! $FONTMAKE -u "source/Hack-BoldItalic.ufo" -o ttf
	then
	    echo "Unable to build the Hack-BoldItalic variant set.  Build canceled." 1>&2
	    exit 1
fi

# Desktop ttf font post build fixes

# DSIG table fix with adapted fontbakery Python script
echo " "
echo "Attempting DSIG table fixes with fontbakery..."
echo " "
if ! $PYTHON postbuild_processing/fixes/fix-dsig.py master_ttf/*.ttf
	then
	    echo "Unable to complete DSIG table fixes on the release files"
	    exit 1
fi

# fstype value fix with adapted fontbakery Python script
echo " "
echo "Attempting fstype fixes with fontbakery..."
echo " "
if ! $PYTHON postbuild_processing/fixes/fix-fstype.py master_ttf/*.ttf
	then
	    echo "Unable to complete fstype fixes on the release files"
	    exit 1
fi

# Desktop ttf font hinting

echo " "
echo "Attempting ttfautohint hinting..."
echo " "
# make a temporary directory for the hinted files
mkdir master_ttf/hinted

# Hack-Regular.ttf
if ! "$TTFAH" -l 6 -r 50 -x 10 -H 181 -D latn -f latn -w G -W -t -X "" -I -m "postbuild_processing/tt-hinting/Hack-Regular-TA.txt" "master_ttf/Hack-Regular.ttf" "master_ttf/hinted/Hack-Regular.ttf"
	then
	    echo "Unable to execute ttfautohint on the Hack-Regular variant set.  Build canceled." 1>&2
	    exit 1
fi
echo "master_ttf/Hack-Regular.ttf - successful hinting with ttfautohint"

# Hack-Bold.ttf
if ! "$TTFAH" -l 6 -r 50 -x 10 -H 260 -D latn -f latn -w G -W -t -X "" -I -m "postbuild_processing/tt-hinting/Hack-Bold-TA.txt" "master_ttf/Hack-Bold.ttf" "master_ttf/hinted/Hack-Bold.ttf"
	then
	    echo "Unable to execute ttfautohint on the Hack-Bold variant set.  Build canceled." 1>&2
	    exit 1
fi
echo "master_ttf/Hack-Bold.ttf - successful hinting with ttfautohint"

# Hack-Italic.ttf
if ! "$TTFAH" -l 6 -r 50 -x 10 -H 145 -D latn -f latn -w G -W -t -X "" -I -m "postbuild_processing/tt-hinting/Hack-Italic-TA.txt" "master_ttf/Hack-Italic.ttf" "master_ttf/hinted/Hack-Italic.ttf"
	then
	    echo "Unable to execute ttfautohint on the Hack-Italic variant set.  Build canceled." 1>&2
	    exit 1
fi
echo "master_ttf/Hack-Italic.ttf - successful hinting with ttfautohint"

# Hack-BoldItalic.ttf
if ! "$TTFAH" -l 6 -r 50 -x 10 -H 265 -D latn -f latn -w G -W -t -X "" -I -m "postbuild_processing/tt-hinting/Hack-BoldItalic-TA.txt" "master_ttf/Hack-BoldItalic.ttf" "master_ttf/hinted/Hack-BoldItalic.ttf"
	then
	    echo "Unable to execute ttfautohint on the Hack-BoldItalic variant set.  Build canceled." 1>&2
	    exit 1
fi
echo "master_ttf/Hack-BoldItalic.ttf - successful hinting with ttfautohint"
echo " "

# Move release files to build directory
echo " "

# create directory if it does not exist
# (occurs with git + empty directories)
if ! [ -d build/ttf ]; then
	mkdir build/ttf
fi

mv master_ttf/hinted/Hack-Regular.ttf build/ttf/Hack-Regular.ttf
echo "Regular ttf build path: build/ttf/Hack-Regular.ttf"
mv master_ttf/hinted/Hack-Italic.ttf build/ttf/Hack-Italic.ttf
echo "Italic ttf build path: build/ttf/Hack-Italic.ttf"
mv master_ttf/hinted/Hack-Bold.ttf build/ttf/Hack-Bold.ttf
echo "Bold ttf build path: build/ttf/Hack-Bold.ttf"
mv master_ttf/hinted/Hack-BoldItalic.ttf build/ttf/Hack-BoldItalic.ttf
echo "Bold Italic ttf build path: build/ttf/Hack-BoldItalic.ttf"

# Remove master_ttf directory
rm -rf master_ttf
