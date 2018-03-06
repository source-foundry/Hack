#!/bin/sh

# ////////////////////////////////////////////////////////////////////
#
# archiver.sh
#  A shell script that packages .zip, tar.gz, and tar.xz font archives
#  Copyright 2018 Christopher Simpkins
#  MIT License
#
#  Usage: ./archiver.sh
#
# ////////////////////////////////////////////////////////////////////

HACK_VERSION="v3.003"
HACK_ARCHIVES_DIR="../../../Hack-archives"
HACK_BUILD_DIR="../../build"


# Make build directory the current working directory
cd "$HACK_BUILD_DIR" || exit 1

# Cleanup Hack-archives directory if present
if [ -d "$HACK_ARCHIVES_DIR" ]; then
	rm -rf "$HACK_ARCHIVES_DIR"
fi

# Make the archive directory
mkdir "$HACK_ARCHIVES_DIR"

# Build ttf zip archive
zip -r "${HACK_ARCHIVES_DIR}/Hack-${HACK_VERSION}-ttf.zip" ttf -x "*.DS_Store"

# Build web font zip archive
zip -r "${HACK_ARCHIVES_DIR}/Hack-${HACK_VERSION}-webfonts.zip" web -x "*.DS_Store"

# Build ttf tar.gz archive
tar -c --exclude=".DS_Store" --exclude="./.DS_Store" --exclude="./*/.DS_Store" -vzf "${HACK_ARCHIVES_DIR}/Hack-${HACK_VERSION}-ttf.tar.gz" ttf

# Build web font tar.gz archive
tar -c --exclude=".DS_Store" --exclude="./.DS_Store" --exclude="./*/.DS_Store" -vzf "${HACK_ARCHIVES_DIR}/Hack-${HACK_VERSION}-webfonts.tar.gz" web

# Build ttf tar.xz archive
tar -c --exclude=".DS_Store" --exclude="./.DS_Store" --exclude="./*/.DS_Store" -C ttf . | xz --extreme -9 --force > "${HACK_ARCHIVES_DIR}/Hack-${HACK_VERSION}-ttf.tar.xz"

# Build web font tar.xz archive
tar -c --exclude=".DS_Store" --exclude="./.DS_Store" --exclude="./*/.DS_Store" -C web . | xz --extreme -9 --force > "${HACK_ARCHIVES_DIR}/Hack-${HACK_VERSION}-webfonts.tar.xz"
