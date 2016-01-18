#!/bin/sh

HACK_VERSION="v2.019"
HACK_BUILD_DIR="../../build"


# Make build directory the current working directory
cd "$HACK_BUILD_DIR"

# Build ttf file archive
tar c ttf --exclude=*.DS_Store | xz --extreme -9 --force > "Hack_${HACK_VERSION}-ttf.tar.xz"

# Build otf file archive
tar c otf --exclude=*.DS_Store | xz --extreme -9 --force  > "Hack_${HACK_VERSION}-otf.tar.xz"

# Build web font file archive
tar c webfonts --exclude=*.DS_Store | xz --extreme -9 --force > "Hack_${HACK_VERSION}-webfonts.tar.xz"
