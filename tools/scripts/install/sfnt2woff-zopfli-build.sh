#!/bin/sh

# /////////////////////////////////////////////////////////////////
#
# sfnt2woff-zopfli-build.sh
#  A shell script that builds the sfnt2woff-zopfli build dependency
#  Copyright 2018 Christopher Simpkins
#  MIT License
#
#  Usage: ./sfnt2woff-zopfli-build.sh
#
# /////////////////////////////////////////////////////////////////

# The sfnt2woff-zopfli build directory.
BUILD="$HOME/sfnt2woff-zopfli-build"

# sfnt2woff-zopfli version
SFNTWOFF_VERSION="1.1.0"
SFNTWOFF="sfnt2woff-zopfli-$SFNTWOFF_VERSION"

# Path to sfnt2woff-zopfli executable
SFNTWOFF_BIN="$BUILD/$SFNTWOFF/sfnt2woff-zopfli"

if test -d "$BUILD" -o -f "$BUILD"; then
  echo "Build directory '$BUILD' must not exist."
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

if [ -f "$SFNTWOFF_BIN" ]; then
	echo "sfnt2woff-zopfli successfully built on the path '$SFNTWOFF_BIN'"
else
	echo "The sfnt2woff-zopfli build failed."
	exit 1
fi
