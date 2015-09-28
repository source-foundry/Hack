# ------------------------------------------------------------------
#
#  release.sh
#  Copyright 2015 Christopher Simpkins
#  MIT license
#
# ------------------------------------------------------------------

# DESCRIPTION
# Moves release ttf build files (after hinting) to the build/ttf path of the repository

cp ../posthinted_builds/Hack-Regular.ttf ../../build/ttf/Hack-Regular.ttf
echo "moved hinted version of Hack-Regular.ttf to ../../build/ttf/Hack-Regular.ttf"
cp ../posthinted_builds/Hack-Bold.ttf ../../build/ttf/Hack-Bold.ttf
echo "moved hinted version of Hack-Bold.ttf to ../../build/ttf/Hack-Bold.ttf"
cp ../posthinted_builds/Hack-Italic.ttf ../../build/ttf/Hack-Italic.ttf
echo "moved hinted version of Hack-Italic.ttf to ../../build/ttf/Hack-Italic.ttf"
cp ../posthinted_builds/Hack-BoldItalic.ttf ../../build/ttf/Hack-BoldItalic.ttf
echo "moved hinted version of Hack-BoldItalic.ttf to ../../build/ttf/Hack-BoldItalic.ttf"
