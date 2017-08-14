#!/bin/bash

# /////////////////////////////////////////////////////////////////
#
# build.sh
#  A shell script that builds the Hack fonts from UFO source
#  Copyright 2017 Christopher Simpkins
#  MIT License
#
#  Usage: ./build.sh (--install-dependencies)
#     Arguments:
#     --install-dependencies (optional) - installs all
#       build dependencies prior to the build script execution
#
# /////////////////////////////////////////////////////////////////


if [ $# -gt 1 ]
	then
	    echo "Inappropriate arguments included in your command." 1>&2
	    echo "Usage: ./build.sh (--install-dependencies)" 1>&2
	    exit 1
elif [ "$1" = "--install-dependencies" ]
	then
		# fontmake
		pip install fontmake
		# fontTools
		pip install fonttools
		# ttfautohint v1.6 (must be pinned to v1.6 and above)
		curl -L https://sourceforge.net/projects/freetype/files/ttfautohint/1.6/ttfautohint-1.6.tar.gz/download -o ttfautohint.tar.gz
		tar -xvzf ttfautohint.tar.gz
		ttfautohint-1.6/configure
		sudo ttfautohint-1.6/make && sudo ttfautohint-1.6/make install
		if [ -f "ttfautohint-1.6.tar.gz" ]
			then
			    rm ttfautohint-1.6.tar.gz
		fi
		if [ -d "ttfautohint-1.6"]
			then
			    rm -rf ttfautohint-1.6
		fi

		# confirm installs
		installflag = 0
		which fontmake
		if [ $? -ne 0 ]
			then
			    echo "Unable to install fontmake with 'pip install fontmake'.  Please attempt manual install and repeat build without the --install-dependencies flag." 1>&2
			    $installflag = 1
		fi

		python -c "import fontTools"
		if [ $? -ne 0 ]
			then
			    echo "Unable to install fontTools with 'pip install fonttools'.  Please attempt manual install and repeat build without the --install-dependencies flag." 1>&2
			    $installflag = 1
		fi

		which ttfautohint
		if [ $? -ne 0 ]
			then
			    echo "Unable to install ttfautohint from source.  Please attempt manual install and repeat build without the --install-dependencies flag." 1>&2
			    $installflag = 1
		fi

		# if any of the dependency installs failed, exit and do not attempt build
		if [ $installflag -eq 1 ]
			then
			    echo "Build canceled." 1>&2
			    exit 1
	    fi
fi

# Desktop ttf font build

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

# build regular set
fontmake -u "source/Hack-Regular.ufo" -o ttf
if [ $? -ne 0 ]
	then
	    echo "Unable to build the Hack-Regular variant set.  Build canceled." 1>&2
	    exit 1
fi

# build bold set
fontmake -u "source/Hack-Bold.ufo" -o ttf
if [ $? -ne 0 ]
	then
	    echo "Unable to build the Hack-Bold variant set.  Build canceled." 1>&2
	    exit 1
fi

# build italic set
fontmake -u "source/Hack-Italic.ufo" -o ttf
if [ $? -ne 0 ]
	then
	    echo "Unable to build the Hack-Italic variant set.  Build canceled." 1>&2
	    exit 1
fi

# build bold italic set
fontmake -u "source/Hack-BoldItalic.ufo" -o ttf
if [ $? -ne 0 ]
	then
	    echo "Unable to build the Hack-BoldItalic variant set.  Build canceled." 1>&2
	    exit 1
fi


# Desktop ttf font hinting

# make a temporary directory for the hinted files
mkdir master_ttf/hinted

# Hack-Regular.ttf
ttfautohint -l 6 -r 50 -x 10 -H 181 -D latn -f latn -w G -W -t -X "" -I -R "master_ttf/Hack-Regular.ttf" -m "postbuild_processing/tt-hinting/Hack-Regular-TA.txt" "master_ttf/Hack-Regular.ttf" "master_ttf/hinted/Hack-Regular.ttf"
if [ $? -ne 0 ]
	then
	    echo "Unable to execute ttfautohint on the Hack-Regular variant set.  Build canceled." 1>&2
	    exit 1
fi

# Hack-Bold.ttf
ttfautohint -l 6 -r 50 -x 10 -H 260 -D latn -f latn -w G -W -t -X "" -I -R "master_ttf/Hack-Regular.ttf" -m "postbuild_processing/tt-hinting/Hack-Bold-TA.txt" "master_ttf/Hack-Bold.ttf" "master_ttf/hinted/Hack-Bold.ttf"
if [ $? -ne 0 ]
	then
	    echo "Unable to execute ttfautohint on the Hack-Bold variant set.  Build canceled." 1>&2
	    exit 1
fi

# Hack-Italic.ttf
ttfautohint -l 6 -r 50 -x 10 -H 145 -D latn -f latn -w G -W -t -X "" -I -R "master_ttf/Hack-Regular.ttf" -m "postbuild_processing/tt-hinting/Hack-Italic-TA.txt" "master_ttf/Hack-Italic.ttf" "master_ttf/hinted/Hack-Italic.ttf"
if [ $? -ne 0 ]
	then
	    echo "Unable to execute ttfautohint on the Hack-Italic variant set.  Build canceled." 1>&2
	    exit 1
fi

# Hack-BoldItalic.ttf
ttfautohint -l 6 -r 50 -x 10 -H 265 -D latn -f latn -w G -W -t -X "" -I -R "master_ttf/Hack-Regular.ttf" -m "postbuild_processing/tt-hinting/Hack-BoldItalic-TA.txt" "master_ttf/Hack-BoldItalic.ttf" "master_ttf/hinted/Hack-BoldItalic.ttf"
if [ $? -ne 0 ]
	then
	    echo "Unable to execute ttfautohint on the Hack-BoldItalic variant set.  Build canceled." 1>&2
	    exit 1
fi


# Desktop ttf font post build fixes
# TODO dsig table fix
# TODO fstype integer fix


# Move release files to build directory
mv master_ttf/hinted/Hack-Regular.ttf build/ttf/Hack-Regular.ttf
echo "Hack-Regular.ttf was moved to release directory on path build/ttf/Hack-Regular.ttf"
mv master_ttf/hinted/Hack-Italic.ttf build/ttf/Hack-Italic.ttf
echo "Hack-Italic.ttf was moved to release directory on path build/ttf/Hack-Italic.ttf"
mv master_ttf/hinted/Hack-Bold.ttf build/ttf/Hack-Bold.ttf
echo "Hack-Bold.ttf was moved to release directory on path build/ttf/Hack-Bold.ttf"
mv master_ttf/hinted/Hack-BoldItalic.ttf build/ttf/Hack-BoldItalic.ttf
echo "Hack-BoldItalic.ttf was moved to release directory on path build/ttf/Hack-BoldItalic.ttf"

# Remove master_ttf directory
rm -rf master_ttf
