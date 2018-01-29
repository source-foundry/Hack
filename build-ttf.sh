#!/bin/sh

# /////////////////////////////////////////////////////////////////
#
# build-ttf.sh
#  A shell script that builds the Hack ttf fonts from UFO source
#  Copyright 2018 Christopher Simpkins
#  MIT License
#
#  Usage: ./build-ttf.sh (--install-dependencies)
#     Arguments:
#     --install-dependencies (optional) - installs all
#       build dependencies prior to the build script execution
#
# /////////////////////////////////////////////////////////////////

# ttfautohint local install path from Werner Lemberg's ttfautohint-build.sh install script
#   - This is revised to ttfautohint on the user's PATH if this local install is not identified
#     then the identified ttfautohint is used to execute hinting.  Versions of ttfautohint < 1.6 exit with status
#     code 1 due to use of -R option
#   - The intent is to support use of ttfautohint installed on a user's PATH (e.g. they've previously installed it)
TTFAH="$HOME/ttfautohint-build/local/bin/ttfautohint"

# test for number of arguments
if [ $# -gt 1 ]
	then
	    echo "Inappropriate arguments included in your command." 1>&2
	    echo "Usage: ./build-ttf.sh (--install-dependencies)" 1>&2
	    exit 1
fi

# Optional build dependency install request with syntax `./build.sh --install-dependencies`
if [ "$1" = "--install-dependencies" ]
	then
		# fontmake
		pip install --upgrade fontmake
		# fontTools (installed with fontmake at this time. leave this as dependency check as python scripts for fixes require it should fontTools eliminate dep)
		pip install --upgrade fonttools
		# ttfautohint v1.6 (must be pinned to v1.6 and above for Hack instruction sets)
        tools/scripts/install/ttfautohint-build.sh

fi

# confirm executable installs and library imports for build dependencies
INSTALLFLAG=0

echo "Confirming that build dependencies are installed..."
echo " "
# fontmake installed
if ! which fontmake
	then
	    echo "Unable to install fontmake with 'pip install fontmake'.  Please attempt a manual install of this build dependency and then repeat your build attempt." 1>&2
	    INSTALLFLAG=1
fi
# fontTools python library can be imported
if ! python -c "import fontTools"
	then
	    echo "Unable to install fontTools with 'pip install fonttools'.  Please attempt a manual install of this build dependency and then repeat your build attempt." 1>&2
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
	            echo "Unable to install ttfautohint from source.  Please attempt a manual install of this build dependency and then repeat your build attempt." 1>&2
	            INSTALLFLAG=1
	    else
	    	TTFAH="ttfautohint"  # revise TTFAH variable to ttfautohint installed on the user's PATH for excecution of hints below
	    fi
fi
# if any of the dependency installs failed, exit and do not attempt build, notify user
if [ $INSTALLFLAG -eq 1 ]
	then
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

if ! fontmake -u "source/Hack-Regular.ufo" -o ttf
	then
	    echo "Unable to build the Hack-Regular variant set.  Build canceled." 1>&2
	    exit 1
fi

# build bold set
if ! fontmake -u "source/Hack-Bold.ufo" -o ttf
	then
	    echo "Unable to build the Hack-Bold variant set.  Build canceled." 1>&2
	    exit 1
fi

# build italic set
if ! fontmake -u "source/Hack-Italic.ufo" -o ttf
	then
	    echo "Unable to build the Hack-Italic variant set.  Build canceled." 1>&2
	    exit 1
fi

# build bold italic set

if ! fontmake -u "source/Hack-BoldItalic.ufo" -o ttf
	then
	    echo "Unable to build the Hack-BoldItalic variant set.  Build canceled." 1>&2
	    exit 1
fi

# Desktop ttf font post build fixes

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
