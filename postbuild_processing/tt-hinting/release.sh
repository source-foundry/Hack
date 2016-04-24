# ------------------------------------------------------------------
#
#  release.sh
#  Copyright 2016 Christopher Simpkins
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

# Moves release otf build files (after hinting) to the build/otf path of the repository
cp ../posthinted_builds/Hack-Regular.otf ../../build/otf/Hack-Regular.otf
echo "moved hinted version of Hack-Regular.otf to ../../build/otf/Hack-Regular.otf"
cp ../posthinted_builds/Hack-Bold.otf ../../build/otf/Hack-Bold.otf
echo "moved hinted version of Hack-Bold.otf to ../../build/otf/Hack-Bold.otf"
cp ../posthinted_builds/Hack-Italic.otf ../../build/otf/Hack-Italic.otf
echo "moved hinted version of Hack-Italic.otf to ../../build/otf/Hack-Italic.otf"
cp ../posthinted_builds/Hack-BoldItalic.otf ../../build/otf/Hack-BoldItalic.otf
echo "moved hinted version of Hack-BoldItalic.otf to ../../build/otf/Hack-BoldItalic.otf"
