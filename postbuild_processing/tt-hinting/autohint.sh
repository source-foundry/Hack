# ------------------------------------------------------------------
#
#  autohint.sh
#  Copyright 2015 Christopher Simpkins
#  MIT license
#
# ------------------------------------------------------------------

# DESCRIPTION
# Applies hints to the Hack ttf font builds with ttfautohint
# Executable: ttfautohint (http://www.freetype.org/ttfautohint/doc/ttfautohint.html)


# Hack-Regular.ttf
ttfautohint -l 4 -r 80 -G 350 -x 0 -H 181 -D latn -f latn -w G -W -t -X "" -I "../prehinted_builds/Hack-Regular.ttf" "../posthinted_builds/Hack-Regular.ttf"
echo "Hack-Regular.ttf hinted and moved to ../posthinted_builds/Hack-Regular.ttf"

# Hack-Bold.ttf
ttfautohint -l 4 -r 80 -G 350 -x 0 -H 260 -D latn -f latn -w G -W -t -X "" -I -m "Hack-Bold-TA.txt" "../prehinted_builds/Hack-Bold.ttf" "../posthinted_builds/Hack-Bold.ttf"
echo "Hack-Bold.ttf hinted and moved to ../posthinted_builds/Hack-Bold.ttf"

# Hack-Italic.ttf
ttfautohint -l 4 -r 80 -G 350 -x 0 -H 145 -D latn -f latn -w G -W -t -X "" -I "../prehinted_builds/Hack-Italic.ttf" "../posthinted_builds/Hack-Italic.ttf"
echo "Hack-Italic.ttf hinted and moved to ../posthinted_builds/Hack-Italic.ttf"

# Hack-BoldItalic.ttf
ttfautohint -l 4 -r 80 -G 350 -x 0 -H 265 -D latn -f latn -w G -W -t -X "" -I "../prehinted_builds/Hack-BoldItalic.ttf" "../posthinted_builds/Hack-BoldItalic.ttf"
echo "Hack-BoldItalic.ttf hinted and moved to ../posthinted_builds/Hack-BoldItalic.ttf"
