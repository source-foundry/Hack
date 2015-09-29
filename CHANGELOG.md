# Version 2.015 (release build)

ttf, otf, webfont builds

Changes vs. release v2.013:

- new vertical metrics = decreased line spacing height - Issues #28, #32, #39, #41, #95, #103
- adjusted vertical position of the colon to a higher position, improves alignment with other punctuation glyphs (U+003A) - Issue #66
- changed vertical position of the dash (U+002D) so that regular and oblique, bold and bold oblique are properly aligned - Issue #107
- updated hinting algorithm for bold set (improved point position over stem of lowercase j/i for some text sizes) - Issue #84
- underscore (U+005F) centered, increased width, increased height & aligned vertical position closer to baseline - Issues #97, #98, #100, 103,
- increased vertical position of dieresis mark on lowercase u dieresis (U+00FC) - Issue #61
- increased vertical position of dieresis mark on lowercase i dieresis (U+00EF)
- increased vertical position of dieresis mark on lowercase e dieresis (U+00EB)
- decreased vertical position of the asterisk (U+002A) - Issue #34
- new design for ascii tilde - broader curves, taller glyph with goal to improve appearance at small text sizes where it tended to render like a dash (U+007E) - Issue #37
- new ttf build autohinting script (./postbuild_processing/tt-hinting/autohint.sh)
- new ttf build autohinting Control Instructions File - bold set (./postbuild_processing/tt-hinting/Hack-Bold-TA.txt)
- new ttf build release script (./postbuild_processing/tt-hinting/release.sh)
- new web font release script (./postbuild_processing/webfonts/releasewebfonts.sh)
- new vfb to UFO source file conversion script (./tools/makeufo.sh)
- new UFO source file types - includes separate source files for TrueType (`*-TT.ufo`) and PostScript (`*-PS.ufo`) releases
- source file path changes: now includes separate `ufo` and `vfb` directories under the `./source` repository directory
- Hack Open Font license updated to version 2.0.  The license changes better define the Hack project as a derivative project of the Bitstream Vera Sans Mono typeface project and are intended to make the license more consistent with the Bitstream Vera libre, open source license under which Hack is co-licensed.  There are no new restrictions on use of the fonts with these license changes.  Embedding permissions are made explicit in this version of the Hack Open Font license.


# Version 2.014 (development build)

- ttf only build for testing
- updated hinting algorithm for bold set (corrected incorrect point position of lowercase j/i at some sizes) - Issue #84
- adjusted vertical metrics - Issues #28, #32, #39, #41, #95, #103
- centered, increased width, & adjusted vertical position of underscore - Issues #97, #98, #100, 103,
- increased vertical position of dieresis mark on lowercase u dieresis (U+00FC) - Issue #61
- increased vertical position of dieresis mark on lowercase i dieresis (U+00EF)
- increased vertical position of dieresis mark on lowercase e dieresis (U+00EB)
- decreased vertical position of the asterisk (U+002A) - Issue #34
- new design for ascii tilde (U+007E) - Issue #37


# Version 2.013 (release build)

ttf, otf, webfont builds

Changes vs. release v2.010

- Fixed missing middle dot glyph (U+00B7), adjusted width of U+00B7 em box to address spacing issues in editors that highlight empty spaces (Issues #27 & 46)
- Powerline glyph alignment and size adjustments (Issue #33)
- Fixed name tables to address:
	- incorrect oblique rendering with Java type renderers on OS X (Issue #26)
	- incorrect italic + bold + bold oblique rendering in some syntax highlighters (Issues #42, #50, #60)
	- backslash character took inappropriate vertical alignment because of incorrect slant angle in some editors (Issue #67)
- Changed oblique and bold oblique font names to "Hack Italic" and "Hack Bold Italic" to address Windows listings
- Changed oblique and bold oblique webfont names to "hack-italic-webfont.[xxx]" and "hack-bolditalic-webfont.[xxx]"
- Changed oblique and bold oblique basic Latin + Latin-1 webfont subsets to the names "hack-italic-latin-webfont.[xxx]" and "hack-bolditalic-latin-webfont.[xxx]"
- Changed license name from "Modified SIL Open Font License" to "Hack Open Font License" to comply with SIL regulations for SIL Open Font License modifications
- Removed all license references to SIL to comply with SIL regulations for modifications of the SIL Open Font License
- Removed SIL Open Font License preamble from the Hack Open Font License to comply with SIL regulations for modifications of the SIL Open Font License
- Removed the following statement from Hack Open Font License condition #3: "This restriction only applies to the primary font name as presented to the users." to address a reserved font name conflict with the Bitstream Vera license
- Modified the build directory structure for the Hack web fonts
- Added Hack webfont CSS files to the build directory

# Version 2.012 (development build)

- ttf only build for testing
- Powerline glyph alignment and size adjustments (Issue #33)
- Fixed name tables to address:
	- incorrect oblique rendering with Java type renderers on OS X (Issue #26)
	- incorrect italic + bold + bold oblique rendering in some syntax highlighters (Issues #42, #50, #60)
	- backslash character took inappropriate vertical alignment because of incorrect slant angle in some editors (Issue #67)

# Version 2.011 (development build)

- ttf only build for testing
- fixed missing middle dot glyph (U+00B7), adjusted width of U+00B7 em box to address spacing issues in editors that highlight empty spaces (Issues 27 & 46)


# Version 2.010

### New Glyphs

- New glyphs for Revised Western European (ISO-8859-15, Latin-9) character set (shapes from DejaVu Sans Mono typeface)
- New glyphs for Central European (ISO-8859-2, Latin-2) character set (shapes from DejaVu Sans Mono typeface)
- New glyphs for South European (ISO-8859-3, Latin-3) character set (shapes from DejaVu Sans Mono typeface)
- New glyphs for Vietnamese character set (shapes from DejaVu Sans Mono typeface)
- New glyphs for Pan African Latin character set (shapes from DejaVu Sans Mono typeface)
- New glyphs for Cyrillic (ISO-8859-5) character set (shapes from DejaVu Sans Mono typeface)
- New glyphs for Greek (ISO-8859-7) character set (shapes from DejaVu Sans Mono typeface)
- New glyphs for Armenian character set (shapes from DejaVu Sans Mono typeface)
- New glyphs for Georgian character set (shapes from DejaVu Sans Mono typeface)
- New punctuation glyphs
- New Powerline glyphs
- New number glyphs
- New scientific inferior numerals
- New superscript numerals
- New subscript numerals
- New symbol glyphs
- New **dotlessi**
- New **iacute**
- New **icircumflex**
- New **idieresis**
- New **igrave**
- New **imacron**
- New **iogonek**
- New **itilde**
- New **uppercase upsilon**
- New **uppercase upsilon tonos**
- New uni0069
- New uni0457
- New uni0458


### Modified Glyphs

##### Latin Character Set

- Modified **uppercase Q** - added flared tail and modified tail angle
- Modified **uppercase F** - central arm lowered to fill open gap at the base
- Modified **lowercase a** - added curved tail/spur
- Modified **lowercase b** - decreased width of terminal, opened angle
- Modified **lowercase d** - decreased width of terminal, opened angle
- Modified **lowercase g** - decreased width of terminal, opened angle
- Modified **lowercase i** - rounded corners of the dot, oriented dot position left of center relative to vertical stem, adjusted vertical position of the horizontal stem to x-height, lengthened the vertical stem to slightly overshoot baseline with the curved tail, decreased width of horizontal stem
- Modified **lowercase j** - rounded corners of the dot, oriented dot position left of center relative to vertical stem
- Modified **lowercase l** - lengthened the vertical stem to overshoot the baseline with the curved tail
- Modified **lowercase m** - decreased width of terminal, opened angle
- Modified **lowercase n** - decreased width of terminal, opened angle
- Modified **lowercase p** - decreased width of terminal, opened angle
- Modified **lowercase q** - decreased width of terminal, opened angle
- Modified **lowercase r** - decreased width of terminal, opened angle
- Modified **lowercase t** - added angle to the upper terminal, increased length of the vertical stem to allow the curved tail to slightly overshoot the baseline
- Modified **lowercase y** - modified curves
- Modified **0** - modified width and length of central oval fill, improved symmetry of the oval fill in all sets
- Modified **2** - rounded the upper left corner of the base, decreased width of the spine of the hook
- Modified **Abreve** - modified curves
- Modified **Aogonek** - modified curve, decreased the width of the tail to meet typeface metrics
- Modified **Eogonek** - modified tail curve
- Modified **Iogonek** - modified tail curve
- Modified **Itilde** - modified tilde curve
- Modified **Ohorn** - modified horn curve
- Modified **Oslash** - modified curves
- Modified **Oslashacute** - modified curves
- Modified **Otilde** - modified tilde curve
- Modified **Racute** - modified bowl and leg curves
- Modified **Rcaron** - modiifed bowl and leg curves
- Modified **Rcommaaccent** - modified bowl and leg curves
- Modified **Scommaaccent** - modified curves
- Modified **Tcommaaccent** - modified comma accent curves
- Modified **Ucircumflex** - modified curves
- Modified **Udieresis** - modified curves
- Modified **Ugrave** - modified curves
- Modified **Uhorn** - modified curves
- Modified **Uhungarumlaut** - modified curves
- Modified **Umacron** - modified curves
- Modified **Uogonek** - modified curves
- Modified **Uring** - modified curves
- Modified **Utilde** - modified curves
- Modified **agrave** - decreased width of terminal, opened angle in regular and bold sets
- Modified **aacute** - decreased width of terminal, opened angle in regular and bold sets
- Modified **abreve** - decreased width of upper terminal to create an angled stem
- Modified **acircumflex** - decreased width of terminal, opened angle
- Modified **atilde** - decreased width of terminal, opened angle
- Modified **adieresis** - decreased width of terminal, opened angle
- Modified **amacron** - decreased width of upper terminal to create an angled stem
- Modified **aring** - decreased width of terminal, opened angle
- Modified **dcroat** - decreased width of terminal, opened angle
- Modified **dcaron** - decreased width of lower terminal to create angled stem
- Modified **ecaron** - modified curves
- Modified **ecircumflex** - modified curves
- Modified **edieresis** - modified curves
- Modified **egrave** - modified curves
- Modified **emacron** - modified curves
- Modified **eogonek** - modified curves
- Modified **gbreve** - modified curves of bowl and tail
- Modified **gcaron** - modified curves of bowl and tail, decreased width of upper terminal to create angled stem
- Modified **gcommaaccent** - modified curves of bowl and tail, decreased width of upper terminal to create angled stem
- Modified **gdotaccent** - modified curves of bowl and tail, decreased width of upper terminal to create angled stem
- Modified **hbar** - adjusted curves
- Modified **dotlessi** - decreased width of horizontal stem
- Modified **iacute** - decreased width of horizontal stem
- Modified **icircumflex** - decreased width of horizontal stem
- Modified **idieresis** - decreased width of horizontal stem
- Modified **igrave** - decreased width of horizontal stem
- Modified **imacron** - decreased width of horizontal stem
- Modified **iogonek** - decreased width of horizontal stem
- Modified **itilde** -decreased width of horizontal stem
- Modified **nacute** - adjusted curves
- Modified **ncaron** - adjusted curves
- Modified **ncommaaccent** - adjusted curves
- Modified **eng** - adjusted curves, decreased the upper terminal width to create an angled stem
- Modified **nacute** - decreased width of upper terminal to create angled stem
- Modified **ncaron** - decreased width of upper terminal to create angled stem
- Modified **ncommaaccent** - decreased width of upper terminal to create angled stem
- Modified **ntilde** - adjusted curves
- Modified **ohorn** - adjusted curves
- Modified **ohungarumlaut** - adjusted curves
- Modified **omacron** - adjusted curves
- Modified **oslash** - adjusted curves
- Modified **oslashacute** - adjusted curves
- Modified **otilde** - adjusted curves
- Modified **racute** - adjusted curves, decreased width of upper terminal to create angled stem
- Modified **rcaron** - adjusted curves, decreased width of upper terminal to create angled stem
- Modified **rcommaaccent** - adjusted curves, decreased width of upper terminal to create angled stem
- Modified **sacute** - adjusted curves
- Modified **scedila** - adjusted curves
- Modified **scommaaccent** - adjusted curves
- Modified **lowercase t** - decreased length of the left terminal to angle the horizontal stem
- Modified **tbar** - decreased length of the left terminal to angle the horizontal stem
- Modified **tcaron** - decreased length of the left terminal to angle the horizontal stem
- Modified **tcommaaccent** - adjusted curves, decreased length of the left terminal to angle the horizontal stem
- Modified **uhorn** - adjusted curves, decreased width of lower terminal to create angled stem
- Modified **uhungarumlaut** - adjusted curves, decreased width of lower terminal to create angled stem
- Modified **umacron** - adjusted curves, decreased width of lower terminal to create angled stem
- Modified **uogonek** - adjusted curves, decreased width of lower terminal to create angled stem
- Modified **uring** - adjusted curves, decreased width of lower terminal to create angled stem
- Modified **utilde** - adjusted curves, decreased width of lower terminal to create angled stem
- Modified **yacute** - adjusted curves
- Modified **ycircumflex** - adjusted curves
- Modified **ydieresis** - adjusted curves
- Modified **ygrave** - adjusted curves
- Modified **zdotaccent** - rounded corners of dot
- Modified **gbreve** - decreased width of terminal, opened angle in regular and bold sets
- Modified **ntilde** - decreased width of terminal, opened angle in regular and bold sets
- Modified **ugrave** - decreased width of terminal, opened angle in regular and bold sets
- Modified **uacute** - decreased width of terminal, opened angle in regular and bold sets
- Modified **ucircumflex** - decreased width of terminal, opened angle in regular and bold sets
- Modified **udieresis** - decreased width of terminal, opened angle in regular and bold sets
- Modified **exclamdown** - rounded corners of the dot
- Modified **dieresis** - rounded corners
- Modified **questionmarkdown** - rounded corners of the dot
- Modified **ordfeminine** - decreased width of lower terminal on the a character to create angled stem
- Modified **Adieresis** - rounded corners of dieresis component of glyph
- Modified **Edieresis** - rounded corners of dieresis component of glyph
- Modified **Idieresis** - rounded corners of dieresis component of glyph
- Modified **Odieresis** - rounded corners of dieresis component of glyph
- Modified **Udieresis** - rounded corners of dieresis component of glyph
- Modified **Ydieresis** - rounded corners of dieresis component of glyph
- Modified **adieresis** - rounded corners of dieresis component of glyph
- Modified **edieresis** - rounded corners of dieresis component of glyph
- Modified **idieresis** - rounded corners of dieresis component of glyph
- Modified **odieresis** - rounded corners of dieresis component of glyph
- Modified **udieresis** - rounded corners of dieresis component of glyph
- Modified **ydieresis** - rounded corners of dieresis component of glyph
- Modified **Idotaccent** - rounded corners of the dot
- Modified **dotaccent** - rounded corners of the dot
- Modified **ellipsis** - rounded corners of the dots
- Modified **periodcentered** - rounded corners of the dot


##### Greek Character Set

- Modified **upsilondieresistonos** - adjusted vertical position to properly position on the baseline
- Modified **iotadieresistonos** - adjusted vertical position to properly position on the baseline
- Modified **eth** - altered curve of the neck
- Modified **uppercase eta** - modified the curves
- Modified **uppercase theta** - modified the curves
- Modified **uppercase omicron** - modified the curves
- Modified **uppercase rho** - modified the curves
- Modified **uppercase psi** - modified the curves
- Modified **uppercase upsilon** - new glyph style (change from Latin Y shape)
- Modified **uppercase omega** - modified the curves
- Modified **uppercase alphatonos** - adjusted right and left sidebearings, corrected position of the tonos symbol
- Modified **uppercase epsilontonos** - adjusted right and left sidebearings, corrected position of the tonos symbol
- Modified **uppercase etatonos** - adjusted right and left sidebearings, corrected position of the tonos symbol
- Modified **uppercase iotatonos** - adjusted right and left sidebearings, corrected position of the tonos symbol
- Modified **uppercase omicrontonos** - adjusted right and left sidebearings, corrected position of the tonos symbol
- Modified **uppercase upsilontonos** - adjusted right and left sidebearings, corrected position of the tonos symbol
- Modified **uppercase omegatonos** - adjusted right and left sidebearings, corrected position of the tonos symbol
- Modified **uppercase iotadieresis** - rounded the dieresis points
- Modified **uppercase upsilondieresis** - new upsilon shape, rounded the dieresis points
- Modified **lowercase alpha** - adjusted curves
- Modified **lowercase beta** - adjusted curves
- Modified **lowercase gamma** - adjusted curves
- Modified **lowercase delta** - adjusted curves
- Modified **lowercase epsilon** - adjusted curves
- Modified **lowercase zeta** - adjusted curves
- Modified **lowercase eta** - decreased width of the top terminal to create angled stem, adjusted curves
- Modified **lowercase theta** - adjusted curves
- Modified **lowercase iota** - adjusted curves
- Modified **lowercase lambda** - adjusted curves
- Modified **lowercase mu** - adjusted curves
- Modified **lowercase nu** - adjusted curves
- Modified **lowercase xi** - adjusted curves
- Modified **lowercase omicron** - adjusted curves
- Modified **lowercase pi** - adjusted curves
- Modified **lowercase rho** - adjusted curves
- Modified **lowercase sigmafinal** - adjusted curves
- Modified **lowercase sigma** - adjusted curves
- Modified **lowercase tau** - adjusted curves
- Modified **lowercase upsilon** - adjusted curves
- Modified **lowercase phi** - adjusted curves
- Modified **lowercase chi** - adjusted curves
- Modified **lowercase psi** - adjusted curves
- Modified **lowercase omega** - adjusted curves
- Modified **lowercase iotatonos** - adjusted curves
- Modified **lowercase iotadieresis** - rounded points of the dieresis, adjusted curves
- Modified **iotadieresistonos** - rounded corners of points of dieresis mark, appropriately positioned tonos mark, adjusted curves
- Modified **lowercase upsilontonos** - adjusted curves
- Modified **lowercase upsilondieresis** - rounded points of dieresis mark, adjusted curves
- Modified **upsilondieresistonos** - rounded corners of points of dieresis mark, appropriately positioned tonos mark, adjusted curves
- Modified **lowercase omicrontonos** - adjusted curves
- Modified **lowercase omegatonos** - adjusted curves
- Modified **lowercase alphatonos** - adjusted curves
- Modified **lowercase epsilontonos** - adjusted curves
- Modified **lowercase etatonos** - decreased width of top terminal to create angled stem, adjusted curves


##### Cyrillic Character Set

- Modified curves in uni0411, uni0412, uni0401, uni0417, uni041B, uni041E, uni0420, uni0421, uni0423, uni040E, uni0424, uni0427, uni042F, uni042C, uni042A, uni042B, uni0409, uni040A, uni0405, uni0404, uni042D, uni0408, uni040B, uni042E, uni0402, uni0462, uni0472, uni0494, uni0498, uni04AA, uni04BA, uni04CB, uni04D0, uni04D2, uni04D6, uni04D8, uni04DA, uni04DC, uni04DE, uni04E0, uni04E4, uni04E6, uni04E8, uni04EA, uni04EC, uni04EE, uni04F0, uni04F2, uni04F4, uni04F8, uni0510, uni051A, uni0430, uni0431, uni0432, uni0434, uni0435, uni0450, uni0451, uni0437, uni0439, uni043B, uni043E, uni0440, uni0441, uni0443, uni045E, uni0444, uni0447, uni044F, uni044C, uni044A, uni044B, uni0459, uni045A, uni0455, uni0454, uni044D, uni0456, uni0457, uni0458, uni045B, uni044E, uni0452, uni0463, uni0473, uni0499, uni04AB, uni04BB, uni04CC, uni04D1, uni04D3, uni04D7, uni04D9, uni04DB, uni04DD, uni04DF, uni04E1, uni04E5, uni04E7, uni04E9, uni04EB, uni04ED, uni04EF, uni04F1, uni04F3, uni04F5, uni04F9, uni0511, uni051B, uni04D5
- Rounded corners of points of dieresis marks in uni0401, uni0407, uni04D2, uni04DA, uni04DC, uni04DE, uni04E4, uni04E6, uni04EA, uni04EC, uni04F0, uni04F4, uni04F8, uni0451, uni0457, uni04D3, uni04DB, uni04DD, uni04DF, uni04E5, uni04E7, uni04EB, uni04ED, uni04F1, uni04F5, uni04F9
- Rounded corners of dots in uni0456, uni0458
- Modified **lowercase i** glyphs (uni0456, uni0457) so that they are consistent with the shape of the Hack Latin lowercase i
- Modified **uni0430** - decreased width of lower terminal to create angle
- Modified **uni0440** - decreased width of upper terminal to create angle
- Modified **uni04D1** - decreased width of lower terminal to create angle
- Modified **uni04D3** - decreased width of lower terminal to create angle
- Modified **uni051B** - decreased width of upper terminal to create angle
- Numerous metrics changes to better align the Cyrillic glyphs in a fixed width format

##### Armenian Character Set

- Modified curves in uni0531, uni0532, uni0533, uni0534, uni0535, uni0536, uni0538, uni0539, uni053A, uni053B, uni053D, uni053E, uni053F, uni0540, uni0541, uni0542, uni0543, uni0544, uni0545, uni0546, uni0547, uni0548, uni0549, uni054A, uni054B, uni054C, uni054D, uni054E, uni054F, uni0550, uni0551, uni0553, uni0554, uni0555, uni0556, uni0561, uni0562, uni0563, uni0564, uni0565, uni0566, uni0568, uni0569, uni056A, uni056B, uni056D, uni056E, uni056F, uni0570, uni0571, uni0572, uni0573, uni0574, uni0575, uni0576, uni0577, uni0578, uni0579, uni057A, uni057B, uni057C, uni057D, uni057E, uni057F, uni0580, uni0581, uni0583, uni0584, uni0585, uni0586, uni0587
- Modified **uni0563** - decreased width of the upper terminal to create angle
- Modified **uni0564** - decreased width of the upper terminal to create angle
- Modified **uni0566** - decreased width of the upper terminal to create angle
- Modified **uni0568** - decreased width of the upper terminal to create angle
- Modified **uni0569** - decreased width of the upper terminal to create angle
- Modified **uni0572** - decreased width of the upper terminal to create angle
- Modified **uni0573** - decreased width of the upper terminal to create angle
- Modified **uni0574** - decreased width of the upper terminal to create angle
- Modified **uni0576** - decreased width of the upper terminal to create angle
- Modified **uni0578** - decreased width of the upper terminal to create angle
- Modified **uni057C** - decreased width of the upper terminal to create angle
- Modified **uni057D** - decreased width of the upper terminal to create angle
- Modified **uni0580** - decreased width of the upper terminal to create angle
- Modified **uni0581** - decreased width of the upper terminal to create angle
- Modified **uni0584** - decreased width of the upper terminal to create angle


##### Georgian Character Set

- Modified curves in uni10D0, uni10D1, uni10D2, uni10D3, uni10D4, uni10D5, uni10D6, uni10D7, uni10D8, uni10D9, uni10DA, uni10DB, uni10DC, uni10DD, uni10DE, uni10DF, uni10E0, uni10E1, uni10E2, uni10E3, uni10E4, uni10E5, uni10E6, uni10E7, uni10E8, uni10E9, uni10EA, uni10EB, uni10EC, uni10ED, uni10EE, uni10EF, uni10F0, uni10F1, uni10F2, uni10F3, uni10F4, uni10F5, uni10F6, uni10F7, uni10F8, uni10F9, uni10FA, uni10FC, uni055C, uni055E
- Rounded corners of points in uni10FB, uni0589


##### Punctuation Character Set

- Modified curves in uni2047, questiondown, uni203D, uni203F, uni2048, uni2049, uni204B, uni2E18, uni2E1F, uni2E2E, uni2E18.case, questiondown.case, uni208E, uni207E, uni2768, uni2769, uni276B, uni27C5, uni27C6, uni2987, uni2988, uni055C, uni055E, uni061F, H18533, circle, uni25EF, uni25D0, uni25D1, uni25D2, uni25D3, uni25D6, uni25D7, uni25D4, uni25D5, uni25F4, uni25F5, uni25F6, uni25F7, uni25CD, uni25C9, uni25CE, openbullet, invbullet, invcircle, uni25DA, uni25DB, uni25E0, uni25E1, uni25DC, uni25DD, uni25DE, uni25DF, ampersand, copyright, registered, section, degree
- Modified **dong** - decreased width of the lower terminal to create an angled stem
- Modified **uni20A5** - decreased width of the upper terminal to create an angled stem
- Modified **uni225D** - decreased width of the lower terminal on the d character to create an angled stem
- Modified **uni225E** - decreased width of the upper terminal to create an angled stem


##### Symbol Character Set

- Modified curves in cent, colonmonetary, dong, euro, florin, lira, peseta, sterling, uni0E3F, uni20A0, uni20A2, uni20A5, uni20A8, uni20AA, uni20AF, uni20B0, uni20B1, uni20B2, uni20B4, uni20B5, uni20B9, approxequal, asciitilde, circlemultiply, circleplus, congruent, element, emptyset, infinity, integral, integralbt, integraltp, intersection, notelement, notsubset, partialdiff, percent, perthousand, propersubset, propersuperset, proportional, reflexsubset, reflexsuperset, similar, suchthat, therefore, uni2031, uni2126, uni2201, uni220A, uni220C, uni220D, uni2218, uni221B, uni222C, uni222D, uni2235, uni2236, uni2237, uni2238, uni2239, uni223A, uni223B, uni223D, uni2241, uni2242, uni2243, uni2244, uni2246, uni2247, uni2249, uni224A, uni224B, uni224C, uni224E, uni224F, uni2250, uni2251, uni2252, uni2253, uni2254, uni2255, uni2256, uni2257, uni2258, uni225D, uni225E, uni225F, uni2272, uni2273, uni2274, uni2275, uni227C, uni227D, uni227E, uni227F, uni2285, uni2288, uni2289, uni228B, uni228D, uni2296, uni2298, uni2299, uni229A, uni229B, uni229C, uni229D, uni22B8, uni22CD, uni22D0, uni22D1, uni22DE, uni22DF, uni22E0, uni22E1, uni22E6, uni22E7, uni22E8, uni22E9, uni22EF, uni23A8, uni23AC, uni27DC, uni2A00, uni2A6A, uni2A6B, union, uni219C, uni219D, uni21AD, uni21A9, uni21AA, uni21AB, uni21AC, uni21B6, uni21B7, uni21BA, uni21BB, uni21F4, H18533, circle, uni25EF, uni25D0, uni25D1, uni25D2, uni25D3, uni25D6, uni25D7, uni25D4, uni25D5, uni25F4, uni25F5, uni25F6, uni25F7, uni25CD, uni25C9, uni25CE, openbullet, invbullet, invcircle, uni25DA, uni25DB, uni25E0, uni25E1, uni25DC, uni25DD, uni25DE, uni25DF, at, ampersand, copyright, registered, section, degree, uni0606, uni03F6

### Metrics Changes

- Changed line gap / typo line gap to 275 units
- Modified **uppercase P** - increased right sidebearing to equal sidebearing of uppercase O glyph
- Modified **uppercase Z** - changed to right = left sidebearing (shifts orientation to left) for regular, bold, oblique sets
- Modified **uppercase Z** - reduced left sidebearing for bold oblique set, not necessary to make this equal as with above sets
- Modified **lowercase a** - reduced left sidebearing
- Modified **lowercase c** - reduced left sidebearing
- Modified **lowercase e** - increased left sidebearing
- Modified **lowercase g** - increased left sidebearing
- Modified **lowercase i** - increased left sidebearing
- Modified **lowercase j** - increased left sidebearing
- Modified **lowercase k** - reduced left sidebearing
- Modified **lowercase r** - reduced left sidebearing
- Modified **3** - increased left sidebearing
- Modified **Zacute** - centered glyph (reduced left sidebearing, increased right sidebearing)
- Modified **Zcaron** - centered glyph (reduced left sidebearing, increased right sidebearing)
- Modified **Zdotaccent** - centered glyph (reduced left sidebearing, increased right sidebearing)
- Modified **aacute** - increased left sidebearing
- Modified **abreve** - increased left sidebearing
- Modified **acircumflex** - increased left sidebearing
- Modified **adieresis** - increased left sidebearing
- Modified **agrave** - increased left sidebearing
- Modified **amacron** - increased left sidebearing
- Modified **aogonek** - increased left sidebearing
- Modified **aring** - increased left sidebearing
- Modified **atilde** - increased left sidebearing
- Modified **kcommaaccent** - decreased left sidebearing
- Modified **racute** - decreased left sidebearing
- Modified **rcaron** - decreased left sidebearing
- Modified **rcommaaccent** - decreased left sidebearing
- Mofified **Mu** - increased left sidebearing
- Modified **Zeta** - reduced left sidebearing to center the glyph
- Modified **Rho** - reduced left sidebearing
- Modified **Phi** - increased left sidebearing
- Modified **left guillemet** - increased right sidebearing
- Modified **right guillemet** - increased left sidebearing
- Modified **left brace** - increased right sidebearing
- Modified **right brace** - increased left sidebearing
- Modified **left bracket** - increased right sidebearing
- Modified **right bracket** - increased left sidebearing
- Modified **left parenthesis** - increased right sidebearing
- Modified **right parenthesis** - increased left sidebearing
- Adjusted spacing on all diacritic marks in the regular, bold, oblique, and bold oblique set

### True Type Instructions / PostScript Hinting

- New TrueType instructions / PostScript hinting across the entire glyph set

### Removed

- Removed **fi** and **fl** ligatures. Spacing issues that require these ligatures are not present in this monospaced typeface


# Version 1.3

### Modified Glyphs

- Curve adjustments & curve smoothing across all glyphs in the font collection
- hinting improvements

### Build Files

- New binary build system - should result in improved cross-platform compatibility for font binaries


# Version 1.2

### Modified Glyphs

- Modified **lowercase i** glyph. Removed serif and added curved tail
- Modified **hyphen** glyph. Widened
- Modified **zero** glyph. Adjusted alignment and shape of the oval fill
- Modified **left parenthesis** glyph. Increased right sidebearing length
- Modified **right parenthesis** glyph. Increased left sidebearing length

### Source

- Converted to UFO formatted source


# Version 1.0.1

- Modified the SIL license to permit dual licensing with the Bitstream Vera license.  This modification removed the stipulation that multiple licenses are not possible (preamble and section #5) and was intended to create the new Reserved Font Name Hack for this typeface modification and preserve the right (for myself and others) to define Reserved Font Names for all future fonts derived from this typeface.  There are no other modifications to either license under which this font is released.
- This release did not introduce changes to the glyphs included in the typeface


# Version 1.0.0
- Branched Bitstream Vera Sans Mono 1.10 release

## Changes

### New Glyphs

- New **exclamation point** glyph. Circular full stop point, tapered line, increased weight relative to other characters.
- New **asterisk** glyph.  Glyph shape from Source Code Pro.  Modified vertical position of the glyph to orient closer to the ascender.
- New **period** glyph.  Circular full stop point, modified from square glyph.
- New **comma** glyph.  Rounded comma shape from Source Code Pro, modified from square glyph.
- New **colon** glyph. Circular colon points, modified from square points.
- New **semicolon** glyph. Circular point and rounded comma shape from Source Code Pro, increased vertical spacing between the shapes


### Modified Glyphs
- Modified **percent** glyph.  Increased line length and added vertical line ends.
- Modified **zero** glyph.  Changed circular fill to oval fill.
- Modified **left square bracket** glyph. Increased height of the glyph.
- Modified **right square bracket** glyph. Increased height of the glyph.
- Modified **left curly bracket** glyph.  Modified vertical position, increased length of the horizontal stem, decreased left sidebearing
- Modified **right curly bracket** glyph. Modified vertical position, increased length of the horizontal stem, decreased right sidebearing
- Modified **question mark** glyph.  Changed square full stop point to circular full stop point.
- Modified **hyphen** glyph. Raised vertical alignment to center `->` character combinations.

### Font Styles
- **Regular** - includes all changes indicated above
- **Regular Oblique** - includes all changes indicated above
- **Bold** - includes all changes indicated above
- **Bold Oblique** - includes all changes indicated above


