#!/bin/sh

HACK_VERSION="v2_019"
HACK_BUILD_DIR="../../build"


# Make build directory the current working directory
cd "$HACK_BUILD_DIR"

# Build ttf file archive
tar c --exclude=.DS_Store --exclude=./.DS_Store --exclude=./*/.DS_Store -C ttf . | xz --extreme -9 --force > "archives/Hack_${HACK_VERSION}-ttf.tar.xz"

# Build otf file archive
tar c --exclude=.DS_Store --exclude=./.DS_Store --exclude=./*/.DS_Store -C otf . | xz --extreme -9 --force  > "archives/Hack_${HACK_VERSION}-otf.tar.xz"

# Build web font file archive
tar c --exclude=.DS_Store --exclude=./.DS_Store --exclude=./*/.DS_Store -C webfonts . | xz --extreme -9 --force > "archives/Hack_${HACK_VERSION}-webfonts.tar.xz"
