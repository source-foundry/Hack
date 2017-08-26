#!/bin/sh
# shellcheck disable=SC2103
#
# This script builds a stand-alone binary for the command line version of
# ttfautohint, downloading any necessary libraries.
#
# Version 2017-Aug-17.
# Written by Werner Lemberg <wl@gnu.org>.
# To the extent possible under law, the person who associated CC0 with this work
# has waived all copyright and related or neighboring rights to this work.

#
# User configuration.
#

# The build directory.
BUILD="$HOME/ttfautohint-build"

# The library versions.
FREETYPE_VERSION="2.8"
HARFBUZZ_VERSION="1.4.8"
TTFAUTOHINT_VERSION="1.6"

# Necessary patches (lists of at most 10 URLs each separated by whitespace,
# to be applied in order).
FREETYPE_PATCHES="\
  http://git.savannah.gnu.org/cgit/freetype/freetype2.git/patch/?id=c9a9cf59 \
  http://git.savannah.gnu.org/cgit/freetype/freetype2.git/patch/?id=c8829e4b \
"
HARFBUZZ_PATCHES=""
TTFAUTOHINT_PATCHES=""


#
# Nothing to configure below this comment.
#

FREETYPE="freetype-$FREETYPE_VERSION"
HARFBUZZ="harfbuzz-$HARFBUZZ_VERSION"
TTFAUTOHINT="ttfautohint-$TTFAUTOHINT_VERSION"

if test -d "$BUILD" -o -f "$BUILD"; then
  echo "Build directory \`$BUILD' must not exist."
  exit 1
fi

INST="$BUILD/local"

mkdir "$BUILD"
mkdir "$INST"

cd "$BUILD" || exit 1


echo "#####"
echo "Download all necessary archives and patches."
echo "#####"

curl -L -O "http://download.savannah.gnu.org/releases/freetype/$FREETYPE.tar.gz"
curl -O "https://www.freedesktop.org/software/harfbuzz/release/$HARFBUZZ.tar.bz2"
curl -L -O "http://download.savannah.gnu.org/releases/freetype/$TTFAUTOHINT.tar.gz"

count=0
for i in $FREETYPE_PATCHES
do
  curl -o ft-patch-$count.diff $i
  count=$($count + 1)
done

count=0
for i in $HARFBUZZ_PATCHES
do
  curl -o hb-patch-$count.diff $i
  count=$($count + 1)
done

count=0
for i in $TTFAUTOHINT_PATCHES
do
  curl -o ta-patch-$count.diff $i
  count=$($count + 1)
done


# Our environment variables.
TA_CPPFLAGS="-I$INST/include"
TA_CFLAGS="-g -O2"
TA_CXXFLAGS="-g -O2"
TA_LDFLAGS="-L$INST/lib"


echo "#####"
echo "Extract archives."
echo "#####"

tar -xzvf "$FREETYPE.tar.gz"
tar -xjvf "$HARFBUZZ.tar.bz2"
tar -xzvf "$TTFAUTOHINT.tar.gz"


echo "#####"
echo "Apply patches."
echo "#####"

cd "$FREETYPE" || exit 1
for i in ../ft-patch-*.diff
do
  test -f "$i" || continue
  patch --forward \
        --strip=1 \
        --reject-file=- \
        < "$i"
done
cd ..

cd "$HARFBUZZ" || exit 1
for i in ../hb-patch-*.diff
do
  test -f "$i" || continue
  patch --forward \
        --strip=1 \
        --reject-file=- \
        < "$i"
done
cd ..

cd "$TTFAUTOHINT" || exit 1
for i in ../ta-patch-*.diff
do
  test -f "$i" || continue
  patch --forward \
        --strip=1 \
        --reject-file=- \
        < "$i"
done
cd ..


echo "#####"
echo "$FREETYPE"
echo "#####"

cd "$FREETYPE" || exit 1

./configure \
  --without-bzip2 \
  --without-png \
  --without-zlib \
  --without-harfbuzz \
  --prefix="$INST" \
  --enable-static \
  --disable-shared \
  CFLAGS="$TA_CPPFLAGS $TA_CFLAGS" \
  CXXFLAGS="$TA_CPPFLAGS $TA_CXXFLAGS" \
  LDFLAGS="$TA_LDFLAGS"
make
make install
cd ..


echo "#####"
echo "$HARFBUZZ"
echo "#####"

cd "$HARFBUZZ" || exit 1

./configure \
  --disable-dependency-tracking \
  --disable-gtk-doc-html \
  --with-glib=no \
  --with-cairo=no \
  --with-fontconfig=no \
  --with-icu=no \
  --prefix="$INST" \
  --enable-static \
  --disable-shared \
  CFLAGS="$TA_CPPFLAGS $TA_CFLAGS" \
  CXXFLAGS="$TA_CPPFLAGS $TA_CXXFLAGS" \
  LDFLAGS="$TA_LDFLAGS" \
  PKG_CONFIG=true \
  FREETYPE_CFLAGS="-I$INST/include/freetype2" \
  FREETYPE_LIBS="-L$INST/lib -lfreetype"
make
make install
cd ..


echo "#####"
echo "$TTFAUTOHINT"
echo "#####"

cd "$TTFAUTOHINT" || exit 1

./configure \
  --disable-dependency-tracking \
  --without-qt \
  --without-doc \
  --prefix="$INST" \
  --enable-static \
  --disable-shared \
  --with-freetype-config="$INST/bin/freetype-config" \
  CFLAGS="$TA_CPPFLAGS $TA_CFLAGS" \
  CXXFLAGS="$TA_CPPFLAGS $TA_CXXFLAGS" \
  LDFLAGS="$TA_LDFLAGS" \
  PKG_CONFIG=true \
  HARFBUZZ_CFLAGS="-I$INST/include/harfbuzz" \
  HARFBUZZ_LIBS="-L$INST/lib -lharfbuzz"
make LDFLAGS="$TA_LDFLAGS -all-static"
make install-strip
cd ..


echo "#####"
echo "binary: $INST/bin/ttfautohint"
echo "#####"

# eof
