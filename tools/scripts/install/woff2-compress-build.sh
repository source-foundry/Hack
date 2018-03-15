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

# clone the Source Foundry fork of the woff2 repo
#   contains fix for OS X build bug - https://github.com/google/woff2/issues/73
#   recursive flag to clone the brotli submodule within the woff2 repo
git clone --recursive https://github.com/source-foundry/woff2.git

cd "$INST" || exit 1

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
