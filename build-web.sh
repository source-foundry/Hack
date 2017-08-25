#!/bin/sh

# /////////////////////////////////////////////////////////////////
#
# build-web.sh
#  A shell script that builds the Hack web fonts from ttf files
#  Copyright 2017 Christopher Simpkins
#  MIT License
#
#  Usage: ./build-web.sh (--install-dependencies)
#     Arguments:
#     --install-dependencies (optional) - installs all
#       build dependencies prior to the build script execution
#
#  NOTE: If you change the source, you must build new ttf files
#        with build.sh PRIOR to execution of this script
#
# /////////////////////////////////////////////////////////////////

# The build directory.
BUILD="$HOME/sfnt2woff-zopfli-build"

# sfnt2woff-zopfli version
SFNTWOFF_VERSION="1.1.0"
SFNTWOFF="sfnt2woff-zopfli-$SFNTWOFF_VERSION"

# Path to sfnt2woff-zopfli executable
SFNTWOFF_BIN="$BUILD/$SFNTWOFF/sfnt2woff-zopfli"

# test for number of arguments
if [ $# -gt 1 ]
	then
	    echo "Inappropriate arguments included in your command." 1>&2
	    echo "Usage: ./build-web.sh (--install-dependencies)" 1>&2
	    exit 1
fi

# Optional build dependency install request with syntax `./build-web.sh --install-dependencies`
if [ "$1" = "--install-dependencies" ]
	then
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
fi


if [ -f "$SFNTWOFF_BIN" ]; then
	echo "Beginning web font build with $SFNTWOFF"
else
	echo "Unable to locate sfnt2woff-zopfli." 1>&2
	exit 1
fi

# TODO : implement woff build from ttf build files
# TODO : move woff files to appropriate build directory
# TODO : cleanup pulled tar.gz archive file



