#!/bin/sh

# /////////////////////////////////////////////////////////////////
#
# woff2-compress-build.sh
#  A shell script that builds the woff2_compress build dependency
#  Copyright 2018 Christopher Simpkins
#  MIT License
#
#  Usage: ./woff2-compress-build.sh
#
# /////////////////////////////////////////////////////////////////

# The woff2 git clone directory.
BUILD="$HOME"
INST="$HOME/woff2"
WOFF2_COMMIT="5e5f2cf20d5f9d3373a2d8b4905105f80646c014"

# woff2 executable path
WOFF2_BIN="$BUILD/woff2/woff2_compress"

if test -d "$INST" -o -f "$INST"; then
  echo "Build directory \`$INST' must not exist."
  exit 1
fi

cd "$BUILD" || exit 1

echo "#####"
echo "git clone woff2 project"
echo "#####"

# clone the woff2 repository
git clone --recursive https://github.com/google/woff2.git

cd "$INST" || exit 1

# checkout desired version tag
echo " "
echo "Checking out woff2 at commit $WOFF2_COMMIT"
git checkout $WOFF2_COMMIT

echo "#####"
echo "Build woff2"
echo "#####"

make clean all

if [ -f "$WOFF2_BIN" ]; then
	echo " "
	echo "woff2_compress successfully built on the path '$WOFF2_BIN'"
else
	echo "The woff2_compress build failed."
	exit 1
fi
