# Copyright 2013 Google, Inc. All Rights Reserved.
#
# Google Author(s): Behdad Esfahbod

# subset.py file from Just van Rossom's fonttools project
#
# Copyright 1999-2004
# by Just van Rossum, Letterror, The Netherlands.
# The full text of the license is available at https://github.com/behdad/fonttools/blob/master/LICENSE.txt

from __future__ import print_function, division, absolute_import
from fontTools.misc.py23 import *
from fontTools import ttLib
from fontTools.ttLib.tables import otTables
from fontTools.misc import psCharStrings
import sys
import struct
import time
import array

__usage__ = "pyftsubset font-file [glyph...] [--option=value]..."

__doc__="""\
pyftsubset -- OpenType font subsetter and optimizer

  pyftsubset is an OpenType font subsetter and optimizer, based on fontTools.
  It accepts any TT- or CFF-flavored OpenType (.otf or .ttf) or WOFF (.woff)
  font file. The subsetted glyph set is based on the specified glyphs
  or characters, and specified OpenType layout features.

  The tool also performs some size-reducing optimizations, aimed for using
  subset fonts as webfonts.  Individual optimizations can be enabled or
  disabled, and are enabled by default when they are safe.

Usage:
  """+__usage__+"""

  At least one glyph or one of --gids, --gids-file, --glyphs, --glyphs-file,
  --text, --text-file, --unicodes, or --unicodes-file, must be specified.

Arguments:
  font-file
    The input font file.
  glyph
    Specify one or more glyph identifiers to include in the subset. Must be
    PS glyph names, or the special string '*' to keep the entire glyph set.

Initial glyph set specification:
  These options populate the initial glyph set. Same option can appear
  multiple times, and the results are accummulated.
  --gids=<NNN>[,<NNN>...]
      Specify comma/whitespace-separated list of glyph IDs or ranges as
      decimal numbers.  For example, --gids=10-12,14 adds glyphs with
      numbers 10, 11, 12, and 14.
  --gids-file=<path>
      Like --gids but reads from a file. Anything after a '#' on any line
      is ignored as comments.
  --glyphs=<glyphname>[,<glyphname>...]
      Specify comma/whitespace-separated PS glyph names to add to the subset.
      Note that only PS glyph names are accepted, not gidNNN, U+XXXX, etc
      that are accepted on the command line.  The special string '*' wil keep
      the entire glyph set.
  --glyphs-file=<path>
      Like --glyphs but reads from a file. Anything after a '#' on any line
      is ignored as comments.
  --text=<text>
      Specify characters to include in the subset, as UTF-8 string.
  --text-file=<path>
      Like --text but reads from a file. Newline character are not added to
      the subset.
  --unicodes=<XXXX>[,<XXXX>...]
      Specify comma/whitespace-separated list of Unicode codepoints or
      ranges as hex numbers, optionally prefixed with 'U+', 'u', etc.
      For example, --unicodes=41-5a,61-7a adds ASCII letters, so does
      the more verbose --unicodes=U+0041-005A,U+0061-007A.
      The special strings '*' will choose all Unicode characters mapped
      by the font.
  --unicodes-file=<path>
      Like --unicodes, but reads from a file. Anything after a '#' on any
      line in the file is ignored as comments.
  --ignore-missing-glyphs
      Do not fail if some requested glyphs or gids are not available in
      the font.
  --no-ignore-missing-glyphs
      Stop and fail if some requested glyphs or gids are not available
      in the font. [default]
  --ignore-missing-unicodes [default]
      Do not fail if some requested Unicode characters (including those
      indirectly specified using --text or --text-file) are not available
      in the font.
  --no-ignore-missing-unicodes
      Stop and fail if some requested Unicode characters are not available
      in the font.
      Note the default discrepancy between ignoring missing glyphs versus
      unicodes.  This is for historical reasons and in the future
      --no-ignore-missing-unicodes might become default.

Other options:
  For the other options listed below, to see the current value of the option,
  pass a value of '?' to it, with or without a '='.
  Examples:
    $ pyftsubset --glyph-names?
    Current setting for 'glyph-names' is: False
    $ ./pyftsubset --name-IDs=?
    Current setting for 'name-IDs' is: [1, 2]
    $ ./pyftsubset --hinting? --no-hinting --hinting?
    Current setting for 'hinting' is: True
    Current setting for 'hinting' is: False

Output options:
  --output-file=<path>
      The output font file. If not specified, the subsetted font
      will be saved in as font-file.subset.
  --flavor=<type>
      Specify flavor of output font file. May be 'woff' or 'woff2'.
      Note that WOFF2 requires the Brotli Python extension, available
      at https://github.com/google/brotli

Glyph set expansion:
  These options control how additional glyphs are added to the subset.
  --notdef-glyph
      Add the '.notdef' glyph to the subset (ie, keep it). [default]
  --no-notdef-glyph
      Drop the '.notdef' glyph unless specified in the glyph set. This
      saves a few bytes, but is not possible for Postscript-flavored
      fonts, as those require '.notdef'. For TrueType-flavored fonts,
      this works fine as long as no unsupported glyphs are requested
      from the font.
  --notdef-outline
      Keep the outline of '.notdef' glyph. The '.notdef' glyph outline is
      used when glyphs not supported by the font are to be shown. It is not
      needed otherwise.
  --no-notdef-outline
      When including a '.notdef' glyph, remove its outline. This saves
      a few bytes. [default]
  --recommended-glyphs
      Add glyphs 0, 1, 2, and 3 to the subset, as recommended for
      TrueType-flavored fonts: '.notdef', 'NULL' or '.null', 'CR', 'space'.
      Some legacy software might require this, but no modern system does.
  --no-recommended-glyphs
      Do not add glyphs 0, 1, 2, and 3 to the subset, unless specified in
      glyph set. [default]
  --layout-features[+|-]=<feature>[,<feature>...]
      Specify (=), add to (+=) or exclude from (-=) the comma-separated
      set of OpenType layout feature tags that will be preserved.
      Glyph variants used by the preserved features are added to the
      specified subset glyph set. By default, 'calt', 'ccmp', 'clig', 'curs',
      'kern', 'liga', 'locl', 'mark', 'mkmk', 'rclt', 'rlig' and all features
      required for script shaping are preserved. To see the full list, try
      '--layout-features=?'. Use '*' to keep all features.
      Multiple --layout-features options can be provided if necessary.
      Examples:
        --layout-features+=onum,pnum,ss01
            * Keep the default set of features and 'onum', 'pnum', 'ss01'.
        --layout-features-='mark','mkmk'
            * Keep the default set of features but drop 'mark' and 'mkmk'.
        --layout-features='kern'
            * Only keep the 'kern' feature, drop all others.
        --layout-features=''
            * Drop all features.
        --layout-features='*'
            * Keep all features.
        --layout-features+=aalt --layout-features-=vrt2
            * Keep default set of features plus 'aalt', but drop 'vrt2'.

Hinting options:
  --hinting
      Keep hinting [default]
  --no-hinting
      Drop glyph-specific hinting and font-wide hinting tables, as well
      as remove hinting-related bits and pieces from other tables (eg. GPOS).
      See --hinting-tables for list of tables that are dropped by default.
      Instructions and hints are stripped from 'glyf' and 'CFF ' tables
      respectively. This produces (sometimes up to 30%) smaller fonts that
      are suitable for extremely high-resolution systems, like high-end
      mobile devices and retina displays.
      XXX Note: Currently there is a known bug in 'CFF ' hint stripping that
      might make the font unusable as a webfont as they will be rejected by
      OpenType Sanitizer used in common browsers. For more information see:
      https://github.com/behdad/fonttools/issues/144
      The --desubroutinize options works around that bug.

Optimization options:
  --desubroutinize
      Remove CFF use of subroutinizes.  Subroutinization is a way to make CFF
      fonts smaller.  For small subsets however, desubroutinizing might make
      the font smaller.  It has even been reported that desubroutinized CFF
      fonts compress better (produce smaller output) WOFF and WOFF2 fonts.
      Also see note under --no-hinting.
  --no-desubroutinize [default]
      Leave CFF subroutinizes as is, only throw away unused subroutinizes.

Font table options:
  --drop-tables[+|-]=<table>[,<table>...]
      Specify (=), add to (+=) or exclude from (-=) the comma-separated
      set of tables that will be be dropped.
      By default, the following tables are dropped:
      'BASE', 'JSTF', 'DSIG', 'EBDT', 'EBLC', 'EBSC', 'SVG ', 'PCLT', 'LTSH'
      and Graphite tables: 'Feat', 'Glat', 'Gloc', 'Silf', 'Sill'
      and color tables: 'CBLC', 'CBDT', 'sbix', 'COLR', 'CPAL'.
      The tool will attempt to subset the remaining tables.
      Examples:
        --drop-tables-='SVG '
            * Drop the default set of tables but keep 'SVG '.
        --drop-tables+=GSUB
            * Drop the default set of tables and 'GSUB'.
        --drop-tables=DSIG
            * Only drop the 'DSIG' table, keep all others.
        --drop-tables=
            * Keep all tables.
  --no-subset-tables+=<table>[,<table>...]
      Add to the set of tables that will not be subsetted.
      By default, the following tables are included in this list, as
      they do not need subsetting (ignore the fact that 'loca' is listed
      here): 'gasp', 'head', 'hhea', 'maxp', 'vhea', 'OS/2', 'loca',
      'name', 'cvt ', 'fpgm', 'prep', 'VMDX', and 'DSIG'. Tables that the tool
      does not know how to subset and are not specified here will be dropped
      from the font.
      Example:
         --no-subset-tables+=FFTM
            * Keep 'FFTM' table in the font by preventing subsetting.
  --hinting-tables[-]=<table>[,<table>...]
      Specify (=), add to (+=) or exclude from (-=) the list of font-wide
      hinting tables that will be dropped if --no-hinting is specified,
      Examples:
        --hinting-tables-='VDMX'
            * Drop font-wide hinting tables except 'VDMX'.
        --hinting-tables=''
            * Keep all font-wide hinting tables (but strip hints from glyphs).
  --legacy-kern
      Keep TrueType 'kern' table even when OpenType 'GPOS' is available.
  --no-legacy-kern
      Drop TrueType 'kern' table if OpenType 'GPOS' is available. [default]

Font naming options:
  These options control what is retained in the 'name' table. For numerical
  codes, see: http://www.microsoft.com/typography/otspec/name.htm
  --name-IDs[+|-]=<nameID>[,<nameID>...]
      Specify (=), add to (+=) or exclude from (-=) the set of 'name' table
      entry nameIDs that will be preserved. By default only nameID 1 (Family)
      and nameID 2 (Style) are preserved. Use '*' to keep all entries.
      Examples:
        --name-IDs+=0,4,6
            * Also keep Copyright, Full name and PostScript name entry.
        --name-IDs=''
            * Drop all 'name' table entries.
        --name-IDs='*'
            * keep all 'name' table entries
  --name-legacy
      Keep legacy (non-Unicode) 'name' table entries (0.x, 1.x etc.).
      XXX Note: This might be needed for some fonts that have no Unicode name
      entires for English. See: https://github.com/behdad/fonttools/issues/146
  --no-name-legacy
      Drop legacy (non-Unicode) 'name' table entries [default]
  --name-languages[+|-]=<langID>[,<langID>]
      Specify (=), add to (+=) or exclude from (-=) the set of 'name' table
      langIDs that will be preserved. By default only records with langID
      0x0409 (English) are preserved. Use '*' to keep all langIDs.
  --obfuscate-names
      Make the font unusable as a system font by replacing name IDs 1, 2, 3, 4,
      and 6 with dummy strings (it is still fully functional as webfont).

Glyph naming and encoding options:
  --glyph-names
      Keep PS glyph names in TT-flavored fonts. In general glyph names are
      not needed for correct use of the font. However, some PDF generators
      and PDF viewers might rely on glyph names to extract Unicode text
      from PDF documents.
  --no-glyph-names
      Drop PS glyph names in TT-flavored fonts, by using 'post' table
      version 3.0. [default]
  --legacy-cmap
      Keep the legacy 'cmap' subtables (0.x, 1.x, 4.x etc.).
  --no-legacy-cmap
      Drop the legacy 'cmap' subtables. [default]
  --symbol-cmap
      Keep the 3.0 symbol 'cmap'.
  --no-symbol-cmap
      Drop the 3.0 symbol 'cmap'. [default]

Other font-specific options:
  --recalc-bounds
      Recalculate font bounding boxes.
  --no-recalc-bounds
      Keep original font bounding boxes. This is faster and still safe
      for all practical purposes. [default]
  --recalc-timestamp
      Set font 'modified' timestamp to current time.
  --no-recalc-timestamp
      Do not modify font 'modified' timestamp. [default]
  --canonical-order
      Order tables as recommended in the OpenType standard. This is not
      required by the standard, nor by any known implementation.
  --no-canonical-order
      Keep original order of font tables. This is faster. [default]

Application options:
  --verbose
      Display verbose information of the subsetting process.
  --timing
      Display detailed timing information of the subsetting process.
  --xml
      Display the TTX XML representation of subsetted font.

Example:
  Produce a subset containing the characters ' !"#$%' without performing
  size-reducing optimizations:

  $ pyftsubset font.ttf --unicodes="U+0020-0025" \\
    --layout-features='*' --glyph-names --symbol-cmap --legacy-cmap \\
    --notdef-glyph --notdef-outline --recommended-glyphs \\
    --name-IDs='*' --name-legacy --name-languages='*'
"""


def _add_method(*clazzes):
    """Returns a decorator function that adds a new method to one or
    more classes."""
    def wrapper(method):
        for clazz in clazzes:
            assert clazz.__name__ != 'DefaultTable', \
                    'Oops, table class not found.'
            assert not hasattr(clazz, method.__name__), \
                    "Oops, class '%s' has method '%s'." % (clazz.__name__,
                                                           method.__name__)
            setattr(clazz, method.__name__, method)
        return None
    return wrapper

def _uniq_sort(l):
    return sorted(set(l))

def _set_update(s, *others):
    # Jython's set.update only takes one other argument.
    # Emulate real set.update...
    for other in others:
        s.update(other)

def _dict_subset(d, glyphs):
	return {g:d[g] for g in glyphs}


@_add_method(otTables.Coverage)
def intersect(self, glyphs):
    """Returns ascending list of matching coverage values."""
    return [i for i,g in enumerate(self.glyphs) if g in glyphs]

@_add_method(otTables.Coverage)
def intersect_glyphs(self, glyphs):
    """Returns set of intersecting glyphs."""
    return set(g for g in self.glyphs if g in glyphs)

@_add_method(otTables.Coverage)
def subset(self, glyphs):
    """Returns ascending list of remaining coverage values."""
    indices = self.intersect(glyphs)
    self.glyphs = [g for g in self.glyphs if g in glyphs]
    return indices

@_add_method(otTables.Coverage)
def remap(self, coverage_map):
    """Remaps coverage."""
    self.glyphs = [self.glyphs[i] for i in coverage_map]

@_add_method(otTables.ClassDef)
def intersect(self, glyphs):
    """Returns ascending list of matching class values."""
    return _uniq_sort(
         ([0] if any(g not in self.classDefs for g in glyphs) else []) +
            [v for g,v in self.classDefs.items() if g in glyphs])

@_add_method(otTables.ClassDef)
def intersect_class(self, glyphs, klass):
    """Returns set of glyphs matching class."""
    if klass == 0:
        return set(g for g in glyphs if g not in self.classDefs)
    return set(g for g,v in self.classDefs.items()
                            if v == klass and g in glyphs)

@_add_method(otTables.ClassDef)
def subset(self, glyphs, remap=False):
    """Returns ascending list of remaining classes."""
    self.classDefs = {g:v for g,v in self.classDefs.items() if g in glyphs}
    # Note: while class 0 has the special meaning of "not matched",
    # if no glyph will ever /not match/, we can optimize class 0 out too.
    indices = _uniq_sort(
         ([0] if any(g not in self.classDefs for g in glyphs) else []) +
            list(self.classDefs.values()))
    if remap:
        self.remap(indices)
    return indices

@_add_method(otTables.ClassDef)
def remap(self, class_map):
    """Remaps classes."""
    self.classDefs = {g:class_map.index(v) for g,v in self.classDefs.items()}

@_add_method(otTables.SingleSubst)
def closure_glyphs(self, s, cur_glyphs):
    s.glyphs.update(v for g,v in self.mapping.items() if g in cur_glyphs)

@_add_method(otTables.SingleSubst)
def subset_glyphs(self, s):
    self.mapping = {g:v for g,v in self.mapping.items()
                    if g in s.glyphs and v in s.glyphs}
    return bool(self.mapping)

@_add_method(otTables.MultipleSubst)
def closure_glyphs(self, s, cur_glyphs):
    indices = self.Coverage.intersect(cur_glyphs)
    _set_update(s.glyphs, *(self.Sequence[i].Substitute for i in indices))

@_add_method(otTables.MultipleSubst)
def subset_glyphs(self, s):
    indices = self.Coverage.subset(s.glyphs)
    self.Sequence = [self.Sequence[i] for i in indices]
    # Now drop rules generating glyphs we don't want
    indices = [i for i,seq in enumerate(self.Sequence)
               if all(sub in s.glyphs for sub in seq.Substitute)]
    self.Sequence = [self.Sequence[i] for i in indices]
    self.Coverage.remap(indices)
    self.SequenceCount = len(self.Sequence)
    return bool(self.SequenceCount)

@_add_method(otTables.AlternateSubst)
def closure_glyphs(self, s, cur_glyphs):
    _set_update(s.glyphs, *(vlist for g,vlist in self.alternates.items()
                            if g in cur_glyphs))

@_add_method(otTables.AlternateSubst)
def subset_glyphs(self, s):
    self.alternates = {g:vlist
                       for g,vlist in self.alternates.items()
                       if g in s.glyphs and
                       all(v in s.glyphs for v in vlist)}
    return bool(self.alternates)

@_add_method(otTables.LigatureSubst)
def closure_glyphs(self, s, cur_glyphs):
    _set_update(s.glyphs, *([seq.LigGlyph for seq in seqs
                             if all(c in s.glyphs for c in seq.Component)]
                            for g,seqs in self.ligatures.items()
                            if g in cur_glyphs))

@_add_method(otTables.LigatureSubst)
def subset_glyphs(self, s):
    self.ligatures = {g:v for g,v in self.ligatures.items()
                      if g in s.glyphs}
    self.ligatures = {g:[seq for seq in seqs
                             if seq.LigGlyph in s.glyphs and
                                all(c in s.glyphs for c in seq.Component)]
                      for g,seqs in self.ligatures.items()}
    self.ligatures = {g:v for g,v in self.ligatures.items() if v}
    return bool(self.ligatures)

@_add_method(otTables.ReverseChainSingleSubst)
def closure_glyphs(self, s, cur_glyphs):
    if self.Format == 1:
        indices = self.Coverage.intersect(cur_glyphs)
        if(not indices or
           not all(c.intersect(s.glyphs)
                   for c in self.LookAheadCoverage + self.BacktrackCoverage)):
            return
        s.glyphs.update(self.Substitute[i] for i in indices)
    else:
        assert 0, "unknown format: %s" % self.Format

@_add_method(otTables.ReverseChainSingleSubst)
def subset_glyphs(self, s):
    if self.Format == 1:
        indices = self.Coverage.subset(s.glyphs)
        self.Substitute = [self.Substitute[i] for i in indices]
        # Now drop rules generating glyphs we don't want
        indices = [i for i,sub in enumerate(self.Substitute)
                 if sub in s.glyphs]
        self.Substitute = [self.Substitute[i] for i in indices]
        self.Coverage.remap(indices)
        self.GlyphCount = len(self.Substitute)
        return bool(self.GlyphCount and
                    all(c.subset(s.glyphs)
                        for c in self.LookAheadCoverage+self.BacktrackCoverage))
    else:
        assert 0, "unknown format: %s" % self.Format

@_add_method(otTables.SinglePos)
def subset_glyphs(self, s):
    if self.Format == 1:
        return len(self.Coverage.subset(s.glyphs))
    elif self.Format == 2:
        indices = self.Coverage.subset(s.glyphs)
        self.Value = [self.Value[i] for i in indices]
        self.ValueCount = len(self.Value)
        return bool(self.ValueCount)
    else:
        assert 0, "unknown format: %s" % self.Format

@_add_method(otTables.SinglePos)
def prune_post_subset(self, options):
    if not options.hinting:
        # Drop device tables
        self.ValueFormat &= ~0x00F0
    return True

@_add_method(otTables.PairPos)
def subset_glyphs(self, s):
    if self.Format == 1:
        indices = self.Coverage.subset(s.glyphs)
        self.PairSet = [self.PairSet[i] for i in indices]
        for p in self.PairSet:
            p.PairValueRecord = [r for r in p.PairValueRecord
                                 if r.SecondGlyph in s.glyphs]
            p.PairValueCount = len(p.PairValueRecord)
        # Remove empty pairsets
        indices = [i for i,p in enumerate(self.PairSet) if p.PairValueCount]
        self.Coverage.remap(indices)
        self.PairSet = [self.PairSet[i] for i in indices]
        self.PairSetCount = len(self.PairSet)
        return bool(self.PairSetCount)
    elif self.Format == 2:
        class1_map = self.ClassDef1.subset(s.glyphs, remap=True)
        class2_map = self.ClassDef2.subset(s.glyphs, remap=True)
        self.Class1Record = [self.Class1Record[i] for i in class1_map]
        for c in self.Class1Record:
            c.Class2Record = [c.Class2Record[i] for i in class2_map]
        self.Class1Count = len(class1_map)
        self.Class2Count = len(class2_map)
        return bool(self.Class1Count and
                    self.Class2Count and
                    self.Coverage.subset(s.glyphs))
    else:
        assert 0, "unknown format: %s" % self.Format

@_add_method(otTables.PairPos)
def prune_post_subset(self, options):
    if not options.hinting:
        # Drop device tables
        self.ValueFormat1 &= ~0x00F0
        self.ValueFormat2 &= ~0x00F0
    return True

@_add_method(otTables.CursivePos)
def subset_glyphs(self, s):
    if self.Format == 1:
        indices = self.Coverage.subset(s.glyphs)
        self.EntryExitRecord = [self.EntryExitRecord[i] for i in indices]
        self.EntryExitCount = len(self.EntryExitRecord)
        return bool(self.EntryExitCount)
    else:
        assert 0, "unknown format: %s" % self.Format

@_add_method(otTables.Anchor)
def prune_hints(self):
    # Drop device tables / contour anchor point
    self.ensureDecompiled()
    self.Format = 1

@_add_method(otTables.CursivePos)
def prune_post_subset(self, options):
    if not options.hinting:
        for rec in self.EntryExitRecord:
            if rec.EntryAnchor: rec.EntryAnchor.prune_hints()
            if rec.ExitAnchor: rec.ExitAnchor.prune_hints()
    return True

@_add_method(otTables.MarkBasePos)
def subset_glyphs(self, s):
    if self.Format == 1:
        mark_indices = self.MarkCoverage.subset(s.glyphs)
        self.MarkArray.MarkRecord = [self.MarkArray.MarkRecord[i]
                                     for i in mark_indices]
        self.MarkArray.MarkCount = len(self.MarkArray.MarkRecord)
        base_indices = self.BaseCoverage.subset(s.glyphs)
        self.BaseArray.BaseRecord = [self.BaseArray.BaseRecord[i]
                                     for i in base_indices]
        self.BaseArray.BaseCount = len(self.BaseArray.BaseRecord)
        # Prune empty classes
        class_indices = _uniq_sort(v.Class for v in self.MarkArray.MarkRecord)
        self.ClassCount = len(class_indices)
        for m in self.MarkArray.MarkRecord:
            m.Class = class_indices.index(m.Class)
        for b in self.BaseArray.BaseRecord:
            b.BaseAnchor = [b.BaseAnchor[i] for i in class_indices]
        return bool(self.ClassCount and
                    self.MarkArray.MarkCount and
                    self.BaseArray.BaseCount)
    else:
        assert 0, "unknown format: %s" % self.Format

@_add_method(otTables.MarkBasePos)
def prune_post_subset(self, options):
        if not options.hinting:
            for m in self.MarkArray.MarkRecord:
                if m.MarkAnchor:
                    m.MarkAnchor.prune_hints()
            for b in self.BaseArray.BaseRecord:
                for a in b.BaseAnchor:
                    if a:
                        a.prune_hints()
        return True

@_add_method(otTables.MarkLigPos)
def subset_glyphs(self, s):
    if self.Format == 1:
        mark_indices = self.MarkCoverage.subset(s.glyphs)
        self.MarkArray.MarkRecord = [self.MarkArray.MarkRecord[i]
                                     for i in mark_indices]
        self.MarkArray.MarkCount = len(self.MarkArray.MarkRecord)
        ligature_indices = self.LigatureCoverage.subset(s.glyphs)
        self.LigatureArray.LigatureAttach = [self.LigatureArray.LigatureAttach[i]
                                             for i in ligature_indices]
        self.LigatureArray.LigatureCount = len(self.LigatureArray.LigatureAttach)
        # Prune empty classes
        class_indices = _uniq_sort(v.Class for v in self.MarkArray.MarkRecord)
        self.ClassCount = len(class_indices)
        for m in self.MarkArray.MarkRecord:
            m.Class = class_indices.index(m.Class)
        for l in self.LigatureArray.LigatureAttach:
            for c in l.ComponentRecord:
                c.LigatureAnchor = [c.LigatureAnchor[i] for i in class_indices]
        return bool(self.ClassCount and
                    self.MarkArray.MarkCount and
                    self.LigatureArray.LigatureCount)
    else:
        assert 0, "unknown format: %s" % self.Format

@_add_method(otTables.MarkLigPos)
def prune_post_subset(self, options):
        if not options.hinting:
            for m in self.MarkArray.MarkRecord:
                if m.MarkAnchor:
                    m.MarkAnchor.prune_hints()
            for l in self.LigatureArray.LigatureAttach:
                for c in l.ComponentRecord:
                    for a in c.LigatureAnchor:
                        if a:
                            a.prune_hints()
        return True

@_add_method(otTables.MarkMarkPos)
def subset_glyphs(self, s):
    if self.Format == 1:
        mark1_indices = self.Mark1Coverage.subset(s.glyphs)
        self.Mark1Array.MarkRecord = [self.Mark1Array.MarkRecord[i]
                                      for i in mark1_indices]
        self.Mark1Array.MarkCount = len(self.Mark1Array.MarkRecord)
        mark2_indices = self.Mark2Coverage.subset(s.glyphs)
        self.Mark2Array.Mark2Record = [self.Mark2Array.Mark2Record[i]
                                       for i in mark2_indices]
        self.Mark2Array.MarkCount = len(self.Mark2Array.Mark2Record)
        # Prune empty classes
        class_indices = _uniq_sort(v.Class for v in self.Mark1Array.MarkRecord)
        self.ClassCount = len(class_indices)
        for m in self.Mark1Array.MarkRecord:
            m.Class = class_indices.index(m.Class)
        for b in self.Mark2Array.Mark2Record:
            b.Mark2Anchor = [b.Mark2Anchor[i] for i in class_indices]
        return bool(self.ClassCount and
                    self.Mark1Array.MarkCount and
                    self.Mark2Array.MarkCount)
    else:
        assert 0, "unknown format: %s" % self.Format

@_add_method(otTables.MarkMarkPos)
def prune_post_subset(self, options):
        if not options.hinting:
            # Drop device tables or contour anchor point
            for m in self.Mark1Array.MarkRecord:
                if m.MarkAnchor:
                    m.MarkAnchor.prune_hints()
            for b in self.Mark2Array.Mark2Record:
                for m in b.Mark2Anchor:
                    if m:
                        m.prune_hints()
        return True

@_add_method(otTables.SingleSubst,
             otTables.MultipleSubst,
             otTables.AlternateSubst,
             otTables.LigatureSubst,
             otTables.ReverseChainSingleSubst,
             otTables.SinglePos,
             otTables.PairPos,
             otTables.CursivePos,
             otTables.MarkBasePos,
             otTables.MarkLigPos,
             otTables.MarkMarkPos)
def subset_lookups(self, lookup_indices):
    pass

@_add_method(otTables.SingleSubst,
             otTables.MultipleSubst,
             otTables.AlternateSubst,
             otTables.LigatureSubst,
             otTables.ReverseChainSingleSubst,
             otTables.SinglePos,
             otTables.PairPos,
             otTables.CursivePos,
             otTables.MarkBasePos,
             otTables.MarkLigPos,
             otTables.MarkMarkPos)
def collect_lookups(self):
    return []

@_add_method(otTables.SingleSubst,
             otTables.MultipleSubst,
             otTables.AlternateSubst,
             otTables.LigatureSubst,
             otTables.ReverseChainSingleSubst,
             otTables.ContextSubst,
             otTables.ChainContextSubst,
             otTables.ContextPos,
             otTables.ChainContextPos)
def prune_post_subset(self, options):
    return True

@_add_method(otTables.SingleSubst,
             otTables.AlternateSubst,
             otTables.ReverseChainSingleSubst)
def may_have_non_1to1(self):
    return False

@_add_method(otTables.MultipleSubst,
             otTables.LigatureSubst,
             otTables.ContextSubst,
             otTables.ChainContextSubst)
def may_have_non_1to1(self):
    return True

@_add_method(otTables.ContextSubst,
             otTables.ChainContextSubst,
             otTables.ContextPos,
             otTables.ChainContextPos)
def __subset_classify_context(self):

    class ContextHelper(object):
        def __init__(self, klass, Format):
            if klass.__name__.endswith('Subst'):
                Typ = 'Sub'
                Type = 'Subst'
            else:
                Typ = 'Pos'
                Type = 'Pos'
            if klass.__name__.startswith('Chain'):
                Chain = 'Chain'
            else:
                Chain = ''
            ChainTyp = Chain+Typ

            self.Typ = Typ
            self.Type = Type
            self.Chain = Chain
            self.ChainTyp = ChainTyp

            self.LookupRecord = Type+'LookupRecord'

            if Format == 1:
                Coverage = lambda r: r.Coverage
                ChainCoverage = lambda r: r.Coverage
                ContextData = lambda r:(None,)
                ChainContextData = lambda r:(None, None, None)
                RuleData = lambda r:(r.Input,)
                ChainRuleData = lambda r:(r.Backtrack, r.Input, r.LookAhead)
                SetRuleData = None
                ChainSetRuleData = None
            elif Format == 2:
                Coverage = lambda r: r.Coverage
                ChainCoverage = lambda r: r.Coverage
                ContextData = lambda r:(r.ClassDef,)
                ChainContextData = lambda r:(r.BacktrackClassDef,
                                             r.InputClassDef,
                                             r.LookAheadClassDef)
                RuleData = lambda r:(r.Class,)
                ChainRuleData = lambda r:(r.Backtrack, r.Input, r.LookAhead)
                def SetRuleData(r, d):(r.Class,) = d
                def ChainSetRuleData(r, d):(r.Backtrack, r.Input, r.LookAhead) = d
            elif Format == 3:
                Coverage = lambda r: r.Coverage[0]
                ChainCoverage = lambda r: r.InputCoverage[0]
                ContextData = None
                ChainContextData = None
                RuleData = lambda r: r.Coverage
                ChainRuleData = lambda r:(r.BacktrackCoverage +
                                          r.InputCoverage +
                                          r.LookAheadCoverage)
                SetRuleData = None
                ChainSetRuleData = None
            else:
                assert 0, "unknown format: %s" % Format

            if Chain:
                self.Coverage = ChainCoverage
                self.ContextData = ChainContextData
                self.RuleData = ChainRuleData
                self.SetRuleData = ChainSetRuleData
            else:
                self.Coverage = Coverage
                self.ContextData = ContextData
                self.RuleData = RuleData
                self.SetRuleData = SetRuleData

            if Format == 1:
                self.Rule = ChainTyp+'Rule'
                self.RuleCount = ChainTyp+'RuleCount'
                self.RuleSet = ChainTyp+'RuleSet'
                self.RuleSetCount = ChainTyp+'RuleSetCount'
                self.Intersect = lambda glyphs, c, r: [r] if r in glyphs else []
            elif Format == 2:
                self.Rule = ChainTyp+'ClassRule'
                self.RuleCount = ChainTyp+'ClassRuleCount'
                self.RuleSet = ChainTyp+'ClassSet'
                self.RuleSetCount = ChainTyp+'ClassSetCount'
                self.Intersect = lambda glyphs, c, r: (c.intersect_class(glyphs, r) if c
                                                                                             else (set(glyphs) if r == 0 else set()))

                self.ClassDef = 'InputClassDef' if Chain else 'ClassDef'
                self.ClassDefIndex = 1 if Chain else 0
                self.Input = 'Input' if Chain else 'Class'

    if self.Format not in [1, 2, 3]:
        return None    # Don't shoot the messenger; let it go
    if not hasattr(self.__class__, "__ContextHelpers"):
        self.__class__.__ContextHelpers = {}
    if self.Format not in self.__class__.__ContextHelpers:
        helper = ContextHelper(self.__class__, self.Format)
        self.__class__.__ContextHelpers[self.Format] = helper
    return self.__class__.__ContextHelpers[self.Format]

@_add_method(otTables.ContextSubst,
             otTables.ChainContextSubst)
def closure_glyphs(self, s, cur_glyphs):
    c = self.__subset_classify_context()

    indices = c.Coverage(self).intersect(cur_glyphs)
    if not indices:
        return []
    cur_glyphs = c.Coverage(self).intersect_glyphs(cur_glyphs)

    if self.Format == 1:
        ContextData = c.ContextData(self)
        rss = getattr(self, c.RuleSet)
        rssCount = getattr(self, c.RuleSetCount)
        for i in indices:
            if i >= rssCount or not rss[i]: continue
            for r in getattr(rss[i], c.Rule):
                if not r: continue
                if not all(all(c.Intersect(s.glyphs, cd, k) for k in klist)
                           for cd,klist in zip(ContextData, c.RuleData(r))):
                    continue
                chaos = set()
                for ll in getattr(r, c.LookupRecord):
                    if not ll: continue
                    seqi = ll.SequenceIndex
                    if seqi in chaos:
                        # TODO Can we improve this?
                        pos_glyphs = None
                    else:
                        if seqi == 0:
                            pos_glyphs = frozenset([c.Coverage(self).glyphs[i]])
                        else:
                            pos_glyphs = frozenset([r.Input[seqi - 1]])
                    lookup = s.table.LookupList.Lookup[ll.LookupListIndex]
                    chaos.add(seqi)
                    if lookup.may_have_non_1to1():
                        chaos.update(range(seqi, len(r.Input)+2))
                    lookup.closure_glyphs(s, cur_glyphs=pos_glyphs)
    elif self.Format == 2:
        ClassDef = getattr(self, c.ClassDef)
        indices = ClassDef.intersect(cur_glyphs)
        ContextData = c.ContextData(self)
        rss = getattr(self, c.RuleSet)
        rssCount = getattr(self, c.RuleSetCount)
        for i in indices:
            if i >= rssCount or not rss[i]: continue
            for r in getattr(rss[i], c.Rule):
                if not r: continue
                if not all(all(c.Intersect(s.glyphs, cd, k) for k in klist)
                           for cd,klist in zip(ContextData, c.RuleData(r))):
                    continue
                chaos = set()
                for ll in getattr(r, c.LookupRecord):
                    if not ll: continue
                    seqi = ll.SequenceIndex
                    if seqi in chaos:
                        # TODO Can we improve this?
                        pos_glyphs = None
                    else:
                        if seqi == 0:
                            pos_glyphs = frozenset(ClassDef.intersect_class(cur_glyphs, i))
                        else:
                            pos_glyphs = frozenset(ClassDef.intersect_class(s.glyphs, getattr(r, c.Input)[seqi - 1]))
                    lookup = s.table.LookupList.Lookup[ll.LookupListIndex]
                    chaos.add(seqi)
                    if lookup.may_have_non_1to1():
                        chaos.update(range(seqi, len(getattr(r, c.Input))+2))
                    lookup.closure_glyphs(s, cur_glyphs=pos_glyphs)
    elif self.Format == 3:
        if not all(x.intersect(s.glyphs) for x in c.RuleData(self)):
            return []
        r = self
        chaos = set()
        for ll in getattr(r, c.LookupRecord):
            if not ll: continue
            seqi = ll.SequenceIndex
            if seqi in chaos:
                # TODO Can we improve this?
                pos_glyphs = None
            else:
                if seqi == 0:
                    pos_glyphs = frozenset(cur_glyphs)
                else:
                    pos_glyphs = frozenset(r.InputCoverage[seqi].intersect_glyphs(s.glyphs))
            lookup = s.table.LookupList.Lookup[ll.LookupListIndex]
            chaos.add(seqi)
            if lookup.may_have_non_1to1():
                chaos.update(range(seqi, len(r.InputCoverage)+1))
            lookup.closure_glyphs(s, cur_glyphs=pos_glyphs)
    else:
        assert 0, "unknown format: %s" % self.Format

@_add_method(otTables.ContextSubst,
             otTables.ContextPos,
             otTables.ChainContextSubst,
             otTables.ChainContextPos)
def subset_glyphs(self, s):
    c = self.__subset_classify_context()

    if self.Format == 1:
        indices = self.Coverage.subset(s.glyphs)
        rss = getattr(self, c.RuleSet)
        rssCount = getattr(self, c.RuleSetCount)
        rss = [rss[i] for i in indices if i < rssCount]
        for rs in rss:
            if not rs: continue
            ss = getattr(rs, c.Rule)
            ss = [r for r in ss
                  if r and all(all(g in s.glyphs for g in glist)
                               for glist in c.RuleData(r))]
            setattr(rs, c.Rule, ss)
            setattr(rs, c.RuleCount, len(ss))
        # Prune empty rulesets
        indices = [i for i,rs in enumerate(rss) if rs and getattr(rs, c.Rule)]
        self.Coverage.remap(indices)
        rss = [rss[i] for i in indices]
        setattr(self, c.RuleSet, rss)
        setattr(self, c.RuleSetCount, len(rss))
        return bool(rss)
    elif self.Format == 2:
        if not self.Coverage.subset(s.glyphs):
            return False
        ContextData = c.ContextData(self)
        klass_maps = [x.subset(s.glyphs, remap=True) if x else None for x in ContextData]

        # Keep rulesets for class numbers that survived.
        indices = klass_maps[c.ClassDefIndex]
        rss = getattr(self, c.RuleSet)
        rssCount = getattr(self, c.RuleSetCount)
        rss = [rss[i] for i in indices if i < rssCount]
        del rssCount
        # Delete, but not renumber, unreachable rulesets.
        indices = getattr(self, c.ClassDef).intersect(self.Coverage.glyphs)
        rss = [rss if i in indices else None for i,rss in enumerate(rss)]

        for rs in rss:
            if not rs: continue
            ss = getattr(rs, c.Rule)
            ss = [r for r in ss
                  if r and all(all(k in klass_map for k in klist)
                               for klass_map,klist in zip(klass_maps, c.RuleData(r)))]
            setattr(rs, c.Rule, ss)
            setattr(rs, c.RuleCount, len(ss))

            # Remap rule classes
            for r in ss:
                c.SetRuleData(r, [[klass_map.index(k) for k in klist]
                                  for klass_map,klist in zip(klass_maps, c.RuleData(r))])

        # Prune empty rulesets
        rss = [rs if rs and getattr(rs, c.Rule) else None for rs in rss]
        while rss and rss[-1] is None:
            del rss[-1]
        setattr(self, c.RuleSet, rss)
        setattr(self, c.RuleSetCount, len(rss))

        # TODO: We can do a second round of remapping class values based
        # on classes that are actually used in at least one rule.    Right
        # now we subset classes to c.glyphs only.    Or better, rewrite
        # the above to do that.

        return bool(rss)
    elif self.Format == 3:
        return all(x.subset(s.glyphs) for x in c.RuleData(self))
    else:
        assert 0, "unknown format: %s" % self.Format

@_add_method(otTables.ContextSubst,
             otTables.ChainContextSubst,
             otTables.ContextPos,
             otTables.ChainContextPos)
def subset_lookups(self, lookup_indices):
    c = self.__subset_classify_context()

    if self.Format in [1, 2]:
        for rs in getattr(self, c.RuleSet):
            if not rs: continue
            for r in getattr(rs, c.Rule):
                if not r: continue
                setattr(r, c.LookupRecord,
                        [ll for ll in getattr(r, c.LookupRecord)
                         if ll and ll.LookupListIndex in lookup_indices])
                for ll in getattr(r, c.LookupRecord):
                    if not ll: continue
                    ll.LookupListIndex = lookup_indices.index(ll.LookupListIndex)
    elif self.Format == 3:
        setattr(self, c.LookupRecord,
                [ll for ll in getattr(self, c.LookupRecord)
                 if ll and ll.LookupListIndex in lookup_indices])
        for ll in getattr(self, c.LookupRecord):
            if not ll: continue
            ll.LookupListIndex = lookup_indices.index(ll.LookupListIndex)
    else:
        assert 0, "unknown format: %s" % self.Format

@_add_method(otTables.ContextSubst,
             otTables.ChainContextSubst,
             otTables.ContextPos,
             otTables.ChainContextPos)
def collect_lookups(self):
    c = self.__subset_classify_context()

    if self.Format in [1, 2]:
        return [ll.LookupListIndex
            for rs in getattr(self, c.RuleSet) if rs
            for r in getattr(rs, c.Rule) if r
            for ll in getattr(r, c.LookupRecord) if ll]
    elif self.Format == 3:
        return [ll.LookupListIndex
            for ll in getattr(self, c.LookupRecord) if ll]
    else:
        assert 0, "unknown format: %s" % self.Format

@_add_method(otTables.ExtensionSubst)
def closure_glyphs(self, s, cur_glyphs):
    if self.Format == 1:
        self.ExtSubTable.closure_glyphs(s, cur_glyphs)
    else:
        assert 0, "unknown format: %s" % self.Format

@_add_method(otTables.ExtensionSubst)
def may_have_non_1to1(self):
    if self.Format == 1:
        return self.ExtSubTable.may_have_non_1to1()
    else:
        assert 0, "unknown format: %s" % self.Format

@_add_method(otTables.ExtensionSubst,
             otTables.ExtensionPos)
def subset_glyphs(self, s):
    if self.Format == 1:
        return self.ExtSubTable.subset_glyphs(s)
    else:
        assert 0, "unknown format: %s" % self.Format

@_add_method(otTables.ExtensionSubst,
             otTables.ExtensionPos)
def prune_post_subset(self, options):
    if self.Format == 1:
        return self.ExtSubTable.prune_post_subset(options)
    else:
        assert 0, "unknown format: %s" % self.Format

@_add_method(otTables.ExtensionSubst,
             otTables.ExtensionPos)
def subset_lookups(self, lookup_indices):
    if self.Format == 1:
        return self.ExtSubTable.subset_lookups(lookup_indices)
    else:
        assert 0, "unknown format: %s" % self.Format

@_add_method(otTables.ExtensionSubst,
             otTables.ExtensionPos)
def collect_lookups(self):
    if self.Format == 1:
        return self.ExtSubTable.collect_lookups()
    else:
        assert 0, "unknown format: %s" % self.Format

@_add_method(otTables.Lookup)
def closure_glyphs(self, s, cur_glyphs=None):
    if cur_glyphs is None:
        cur_glyphs = frozenset(s.glyphs)

    # Memoize
    if (id(self), cur_glyphs) in s._doneLookups:
        return
    s._doneLookups.add((id(self), cur_glyphs))

    if self in s._activeLookups:
        raise Exception("Circular loop in lookup recursion")
    s._activeLookups.append(self)
    for st in self.SubTable:
        if not st: continue
        st.closure_glyphs(s, cur_glyphs)
    assert(s._activeLookups[-1] == self)
    del s._activeLookups[-1]

@_add_method(otTables.Lookup)
def subset_glyphs(self, s):
    self.SubTable = [st for st in self.SubTable if st and st.subset_glyphs(s)]
    self.SubTableCount = len(self.SubTable)
    return bool(self.SubTableCount)

@_add_method(otTables.Lookup)
def prune_post_subset(self, options):
    ret = False
    for st in self.SubTable:
        if not st: continue
        if st.prune_post_subset(options): ret = True
    return ret

@_add_method(otTables.Lookup)
def subset_lookups(self, lookup_indices):
    for s in self.SubTable:
        s.subset_lookups(lookup_indices)

@_add_method(otTables.Lookup)
def collect_lookups(self):
    return _uniq_sort(sum((st.collect_lookups() for st in self.SubTable
                           if st), []))

@_add_method(otTables.Lookup)
def may_have_non_1to1(self):
    return any(st.may_have_non_1to1() for st in self.SubTable if st)

@_add_method(otTables.LookupList)
def subset_glyphs(self, s):
    """Returns the indices of nonempty lookups."""
    return [i for i,l in enumerate(self.Lookup) if l and l.subset_glyphs(s)]

@_add_method(otTables.LookupList)
def prune_post_subset(self, options):
    ret = False
    for l in self.Lookup:
        if not l: continue
        if l.prune_post_subset(options): ret = True
    return ret

@_add_method(otTables.LookupList)
def subset_lookups(self, lookup_indices):
    self.ensureDecompiled()
    self.Lookup = [self.Lookup[i] for i in lookup_indices
                   if i < self.LookupCount]
    self.LookupCount = len(self.Lookup)
    for l in self.Lookup:
        l.subset_lookups(lookup_indices)

@_add_method(otTables.LookupList)
def neuter_lookups(self, lookup_indices):
    """Sets lookups not in lookup_indices to None."""
    self.ensureDecompiled()
    self.Lookup = [l if i in lookup_indices else None for i,l in enumerate(self.Lookup)]

@_add_method(otTables.LookupList)
def closure_lookups(self, lookup_indices):
    lookup_indices = _uniq_sort(lookup_indices)
    recurse = lookup_indices
    while True:
        recurse_lookups = sum((self.Lookup[i].collect_lookups()
                               for i in recurse if i < self.LookupCount), [])
        recurse_lookups = [l for l in recurse_lookups
                           if l not in lookup_indices and l < self.LookupCount]
        if not recurse_lookups:
            return _uniq_sort(lookup_indices)
        recurse_lookups = _uniq_sort(recurse_lookups)
        lookup_indices.extend(recurse_lookups)
        recurse = recurse_lookups

@_add_method(otTables.Feature)
def subset_lookups(self, lookup_indices):
    self.LookupListIndex = [l for l in self.LookupListIndex
                            if l in lookup_indices]
    # Now map them.
    self.LookupListIndex = [lookup_indices.index(l)
                            for l in self.LookupListIndex]
    self.LookupCount = len(self.LookupListIndex)
    return self.LookupCount or self.FeatureParams

@_add_method(otTables.Feature)
def collect_lookups(self):
    return self.LookupListIndex[:]

@_add_method(otTables.FeatureList)
def subset_lookups(self, lookup_indices):
    """Returns the indices of nonempty features."""
    # Note: Never ever drop feature 'pref', even if it's empty.
    # HarfBuzz chooses shaper for Khmer based on presence of this
    # feature.    See thread at:
    # http://lists.freedesktop.org/archives/harfbuzz/2012-November/002660.html
    feature_indices = [i for i,f in enumerate(self.FeatureRecord)
                       if (f.Feature.subset_lookups(lookup_indices) or
                           f.FeatureTag == 'pref')]
    self.subset_features(feature_indices)
    return feature_indices

@_add_method(otTables.FeatureList)
def collect_lookups(self, feature_indices):
    return _uniq_sort(sum((self.FeatureRecord[i].Feature.collect_lookups()
                           for i in feature_indices
                           if i < self.FeatureCount), []))

@_add_method(otTables.FeatureList)
def subset_features(self, feature_indices):
    self.ensureDecompiled()
    self.FeatureRecord = [self.FeatureRecord[i] for i in feature_indices]
    self.FeatureCount = len(self.FeatureRecord)
    return bool(self.FeatureCount)

@_add_method(otTables.DefaultLangSys,
             otTables.LangSys)
def subset_features(self, feature_indices):
    if self.ReqFeatureIndex in feature_indices:
        self.ReqFeatureIndex = feature_indices.index(self.ReqFeatureIndex)
    else:
        self.ReqFeatureIndex = 65535
    self.FeatureIndex = [f for f in self.FeatureIndex if f in feature_indices]
    # Now map them.
    self.FeatureIndex = [feature_indices.index(f) for f in self.FeatureIndex
                         if f in feature_indices]
    self.FeatureCount = len(self.FeatureIndex)
    return bool(self.FeatureCount or self.ReqFeatureIndex != 65535)

@_add_method(otTables.DefaultLangSys,
             otTables.LangSys)
def collect_features(self):
    feature_indices = self.FeatureIndex[:]
    if self.ReqFeatureIndex != 65535:
        feature_indices.append(self.ReqFeatureIndex)
    return _uniq_sort(feature_indices)

@_add_method(otTables.Script)
def subset_features(self, feature_indices):
    if(self.DefaultLangSys and
       not self.DefaultLangSys.subset_features(feature_indices)):
        self.DefaultLangSys = None
    self.LangSysRecord = [l for l in self.LangSysRecord
                          if l.LangSys.subset_features(feature_indices)]
    self.LangSysCount = len(self.LangSysRecord)
    return bool(self.LangSysCount or self.DefaultLangSys)

@_add_method(otTables.Script)
def collect_features(self):
    feature_indices = [l.LangSys.collect_features() for l in self.LangSysRecord]
    if self.DefaultLangSys:
        feature_indices.append(self.DefaultLangSys.collect_features())
    return _uniq_sort(sum(feature_indices, []))

@_add_method(otTables.ScriptList)
def subset_features(self, feature_indices):
    self.ScriptRecord = [s for s in self.ScriptRecord
                         if s.Script.subset_features(feature_indices)]
    self.ScriptCount = len(self.ScriptRecord)
    return bool(self.ScriptCount)

@_add_method(otTables.ScriptList)
def collect_features(self):
    return _uniq_sort(sum((s.Script.collect_features()
                           for s in self.ScriptRecord), []))

@_add_method(ttLib.getTableClass('GSUB'))
def closure_glyphs(self, s):
    s.table = self.table
    if self.table.ScriptList:
        feature_indices = self.table.ScriptList.collect_features()
    else:
        feature_indices = []
    if self.table.FeatureList:
        lookup_indices = self.table.FeatureList.collect_lookups(feature_indices)
    else:
        lookup_indices = []
    if self.table.LookupList:
        while True:
            orig_glyphs = frozenset(s.glyphs)
            s._activeLookups = []
            s._doneLookups = set()
            for i in lookup_indices:
                if i >= self.table.LookupList.LookupCount: continue
                if not self.table.LookupList.Lookup[i]: continue
                self.table.LookupList.Lookup[i].closure_glyphs(s)
            del s._activeLookups, s._doneLookups
            if orig_glyphs == s.glyphs:
                break
    del s.table

@_add_method(ttLib.getTableClass('GSUB'),
             ttLib.getTableClass('GPOS'))
def subset_glyphs(self, s):
    s.glyphs = s.glyphs_gsubed
    if self.table.LookupList:
        lookup_indices = self.table.LookupList.subset_glyphs(s)
    else:
        lookup_indices = []
    self.subset_lookups(lookup_indices)
    return True

@_add_method(ttLib.getTableClass('GSUB'),
             ttLib.getTableClass('GPOS'))
def subset_lookups(self, lookup_indices):
    """Retains specified lookups, then removes empty features, language
    systems, and scripts."""
    if self.table.LookupList:
        self.table.LookupList.subset_lookups(lookup_indices)
    if self.table.FeatureList:
        feature_indices = self.table.FeatureList.subset_lookups(lookup_indices)
    else:
        feature_indices = []
    if self.table.ScriptList:
        self.table.ScriptList.subset_features(feature_indices)

@_add_method(ttLib.getTableClass('GSUB'),
             ttLib.getTableClass('GPOS'))
def neuter_lookups(self, lookup_indices):
    """Sets lookups not in lookup_indices to None."""
    if self.table.LookupList:
        self.table.LookupList.neuter_lookups(lookup_indices)

@_add_method(ttLib.getTableClass('GSUB'),
             ttLib.getTableClass('GPOS'))
def prune_lookups(self, remap=True):
    """Remove (default) or neuter unreferenced lookups"""
    if self.table.ScriptList:
        feature_indices = self.table.ScriptList.collect_features()
    else:
        feature_indices = []
    if self.table.FeatureList:
        lookup_indices = self.table.FeatureList.collect_lookups(feature_indices)
    else:
        lookup_indices = []
    if self.table.LookupList:
        lookup_indices = self.table.LookupList.closure_lookups(lookup_indices)
    else:
        lookup_indices = []
    if remap:
        self.subset_lookups(lookup_indices)
    else:
        self.neuter_lookups(lookup_indices)

@_add_method(ttLib.getTableClass('GSUB'),
                         ttLib.getTableClass('GPOS'))
def subset_feature_tags(self, feature_tags):
    if self.table.FeatureList:
        feature_indices = \
            [i for i,f in enumerate(self.table.FeatureList.FeatureRecord)
             if f.FeatureTag in feature_tags]
        self.table.FeatureList.subset_features(feature_indices)
    else:
        feature_indices = []
    if self.table.ScriptList:
        self.table.ScriptList.subset_features(feature_indices)

@_add_method(ttLib.getTableClass('GSUB'),
             ttLib.getTableClass('GPOS'))
def prune_features(self):
    """Remove unreferenced features"""
    if self.table.ScriptList:
        feature_indices = self.table.ScriptList.collect_features()
    else:
        feature_indices = []
    if self.table.FeatureList:
        self.table.FeatureList.subset_features(feature_indices)
    if self.table.ScriptList:
        self.table.ScriptList.subset_features(feature_indices)

@_add_method(ttLib.getTableClass('GSUB'),
             ttLib.getTableClass('GPOS'))
def prune_pre_subset(self, options):
    # Drop undesired features
    if '*' not in options.layout_features:
        self.subset_feature_tags(options.layout_features)
    # Neuter unreferenced lookups
    self.prune_lookups(remap=False)
    return True

@_add_method(ttLib.getTableClass('GSUB'),
             ttLib.getTableClass('GPOS'))
def remove_redundant_langsys(self):
    table = self.table
    if not table.ScriptList or not table.FeatureList:
        return

    features = table.FeatureList.FeatureRecord

    for s in table.ScriptList.ScriptRecord:
        d = s.Script.DefaultLangSys
        if not d:
            continue
        for lr in s.Script.LangSysRecord[:]:
            l = lr.LangSys
            # Compare d and l
            if len(d.FeatureIndex) != len(l.FeatureIndex):
                continue
            if (d.ReqFeatureIndex == 65535) != (l.ReqFeatureIndex == 65535):
                continue

            if d.ReqFeatureIndex != 65535:
                if features[d.ReqFeatureIndex] != features[l.ReqFeatureIndex]:
                    continue

            for i in range(len(d.FeatureIndex)):
                if features[d.FeatureIndex[i]] != features[l.FeatureIndex[i]]:
                    break
            else:
                # LangSys and default are equal; delete LangSys
                s.Script.LangSysRecord.remove(lr)

@_add_method(ttLib.getTableClass('GSUB'),
             ttLib.getTableClass('GPOS'))
def prune_post_subset(self, options):
    table = self.table

    self.prune_lookups() # XXX Is this actually needed?!

    if table.LookupList:
        table.LookupList.prune_post_subset(options)
        # XXX Next two lines disabled because OTS is stupid and
        # doesn't like NULL offsets here.
        #if not table.LookupList.Lookup:
        #    table.LookupList = None

    if not table.LookupList:
        table.FeatureList = None

    if table.FeatureList:
        self.remove_redundant_langsys()
        # Remove unreferenced features
        self.prune_features()

    # XXX Next two lines disabled because OTS is stupid and
    # doesn't like NULL offsets here.
    #if table.FeatureList and not table.FeatureList.FeatureRecord:
    #    table.FeatureList = None

    # Never drop scripts themselves as them just being available
    # holds semantic significance.
    # XXX Next two lines disabled because OTS is stupid and
    # doesn't like NULL offsets here.
    #if table.ScriptList and not table.ScriptList.ScriptRecord:
    #    table.ScriptList = None

    return True

@_add_method(ttLib.getTableClass('GDEF'))
def subset_glyphs(self, s):
    glyphs = s.glyphs_gsubed
    table = self.table
    if table.LigCaretList:
        indices = table.LigCaretList.Coverage.subset(glyphs)
        table.LigCaretList.LigGlyph = [table.LigCaretList.LigGlyph[i]
                                       for i in indices]
        table.LigCaretList.LigGlyphCount = len(table.LigCaretList.LigGlyph)
    if table.MarkAttachClassDef:
        table.MarkAttachClassDef.classDefs = \
            {g:v for g,v in table.MarkAttachClassDef.classDefs.items()
             if g in glyphs}
    if table.GlyphClassDef:
        table.GlyphClassDef.classDefs = \
            {g:v for g,v in table.GlyphClassDef.classDefs.items()
             if g in glyphs}
    if table.AttachList:
        indices = table.AttachList.Coverage.subset(glyphs)
        GlyphCount = table.AttachList.GlyphCount
        table.AttachList.AttachPoint = [table.AttachList.AttachPoint[i]
                                        for i in indices
                                        if i < GlyphCount]
        table.AttachList.GlyphCount = len(table.AttachList.AttachPoint)
    if hasattr(table, "MarkGlyphSetsDef") and table.MarkGlyphSetsDef:
        for coverage in table.MarkGlyphSetsDef.Coverage:
            coverage.subset(glyphs)
        # TODO: The following is disabled. If enabling, we need to go fixup all
        # lookups that use MarkFilteringSet and map their set.
        # indices = table.MarkGlyphSetsDef.Coverage = \
        #   [c for c in table.MarkGlyphSetsDef.Coverage if c.glyphs]
    return True

@_add_method(ttLib.getTableClass('GDEF'))
def prune_post_subset(self, options):
    table = self.table
    # XXX check these against OTS
    if table.LigCaretList and not table.LigCaretList.LigGlyphCount:
        table.LigCaretList = None
    if table.MarkAttachClassDef and not table.MarkAttachClassDef.classDefs:
        table.MarkAttachClassDef = None
    if table.GlyphClassDef and not table.GlyphClassDef.classDefs:
        table.GlyphClassDef = None
    if table.AttachList and not table.AttachList.GlyphCount:
        table.AttachList = None
    if (hasattr(table, "MarkGlyphSetsDef") and
        table.MarkGlyphSetsDef and
        not table.MarkGlyphSetsDef.Coverage):
        table.MarkGlyphSetsDef = None
        if table.Version == 0x00010002/0x10000:
            table.Version = 1.0
    return bool(table.LigCaretList or
                table.MarkAttachClassDef or
                table.GlyphClassDef or
                table.AttachList or
                (table.Version >= 0x00010002/0x10000 and table.MarkGlyphSetsDef))

@_add_method(ttLib.getTableClass('kern'))
def prune_pre_subset(self, options):
    # Prune unknown kern table types
    self.kernTables = [t for t in self.kernTables if hasattr(t, 'kernTable')]
    return bool(self.kernTables)

@_add_method(ttLib.getTableClass('kern'))
def subset_glyphs(self, s):
    glyphs = s.glyphs_gsubed
    for t in self.kernTables:
        t.kernTable = {(a,b):v for (a,b),v in t.kernTable.items()
                                           if a in glyphs and b in glyphs}
    self.kernTables = [t for t in self.kernTables if t.kernTable]
    return bool(self.kernTables)

@_add_method(ttLib.getTableClass('vmtx'))
def subset_glyphs(self, s):
    self.metrics = _dict_subset(self.metrics, s.glyphs)
    return bool(self.metrics)

@_add_method(ttLib.getTableClass('hmtx'))
def subset_glyphs(self, s):
    self.metrics = _dict_subset(self.metrics, s.glyphs)
    return True # Required table

@_add_method(ttLib.getTableClass('hdmx'))
def subset_glyphs(self, s):
    self.hdmx = {sz:_dict_subset(l, s.glyphs) for sz,l in self.hdmx.items()}
    return bool(self.hdmx)

@_add_method(ttLib.getTableClass('VORG'))
def subset_glyphs(self, s):
    self.VOriginRecords = {g:v for g,v in self.VOriginRecords.items()
                               if g in s.glyphs}
    self.numVertOriginYMetrics = len(self.VOriginRecords)
    return True    # Never drop; has default metrics

@_add_method(ttLib.getTableClass('post'))
def prune_pre_subset(self, options):
    if not options.glyph_names:
        self.formatType = 3.0
    return True # Required table

@_add_method(ttLib.getTableClass('post'))
def subset_glyphs(self, s):
    self.extraNames = []    # This seems to do it
    return True # Required table

@_add_method(ttLib.getTableModule('glyf').Glyph)
def remapComponentsFast(self, indices):
    if not self.data or struct.unpack(">h", self.data[:2])[0] >= 0:
        return    # Not composite
    data = array.array("B", self.data)
    i = 10
    more = 1
    while more:
        flags =(data[i] << 8) | data[i+1]
        glyphID =(data[i+2] << 8) | data[i+3]
        # Remap
        glyphID = indices.index(glyphID)
        data[i+2] = glyphID >> 8
        data[i+3] = glyphID & 0xFF
        i += 4
        flags = int(flags)

        if flags & 0x0001: i += 4    # ARG_1_AND_2_ARE_WORDS
        else: i += 2
        if flags & 0x0008: i += 2    # WE_HAVE_A_SCALE
        elif flags & 0x0040: i += 4    # WE_HAVE_AN_X_AND_Y_SCALE
        elif flags & 0x0080: i += 8    # WE_HAVE_A_TWO_BY_TWO
        more = flags & 0x0020    # MORE_COMPONENTS

    self.data = data.tostring()

@_add_method(ttLib.getTableClass('glyf'))
def closure_glyphs(self, s):
    decompose = s.glyphs
    while True:
        components = set()
        for g in decompose:
            if g not in self.glyphs:
                continue
            gl = self.glyphs[g]
            for c in gl.getComponentNames(self):
                if c not in s.glyphs:
                    components.add(c)
        components = set(c for c in components if c not in s.glyphs)
        if not components:
            break
        decompose = components
        s.glyphs.update(components)

@_add_method(ttLib.getTableClass('glyf'))
def prune_pre_subset(self, options):
    if options.notdef_glyph and not options.notdef_outline:
        g = self[self.glyphOrder[0]]
        # Yay, easy!
        g.__dict__.clear()
        g.data = ""
    return True

@_add_method(ttLib.getTableClass('glyf'))
def subset_glyphs(self, s):
    self.glyphs = _dict_subset(self.glyphs, s.glyphs)
    indices = [i for i,g in enumerate(self.glyphOrder) if g in s.glyphs]
    for v in self.glyphs.values():
        if hasattr(v, "data"):
            v.remapComponentsFast(indices)
        else:
            pass    # No need
    self.glyphOrder = [g for g in self.glyphOrder if g in s.glyphs]
    # Don't drop empty 'glyf' tables, otherwise 'loca' doesn't get subset.
    return True

@_add_method(ttLib.getTableClass('glyf'))
def prune_post_subset(self, options):
    remove_hinting = not options.hinting
    for v in self.glyphs.values():
        v.trim(remove_hinting=remove_hinting)
    return True

@_add_method(ttLib.getTableClass('CFF '))
def prune_pre_subset(self, options):
    cff = self.cff
    # CFF table must have one font only
    cff.fontNames = cff.fontNames[:1]

    if options.notdef_glyph and not options.notdef_outline:
        for fontname in cff.keys():
            font = cff[fontname]
            c,_ = font.CharStrings.getItemAndSelector('.notdef')
            # XXX we should preserve the glyph width
            c.bytecode = '\x0e' # endchar
            c.program = None

    return True # bool(cff.fontNames)

@_add_method(ttLib.getTableClass('CFF '))
def subset_glyphs(self, s):
    cff = self.cff
    for fontname in cff.keys():
        font = cff[fontname]
        cs = font.CharStrings

        # Load all glyphs
        for g in font.charset:
            if g not in s.glyphs: continue
            c,sel = cs.getItemAndSelector(g)

        if cs.charStringsAreIndexed:
            indices = [i for i,g in enumerate(font.charset) if g in s.glyphs]
            csi = cs.charStringsIndex
            csi.items = [csi.items[i] for i in indices]
            del csi.file, csi.offsets
            if hasattr(font, "FDSelect"):
                sel = font.FDSelect
                # XXX We want to set sel.format to None, such that the
                # most compact format is selected. However, OTS was
                # broken and couldn't parse a FDSelect format 0 that
                # happened before CharStrings. As such, always force
                # format 3 until we fix cffLib to always generate
                # FDSelect after CharStrings.
                # https://github.com/khaledhosny/ots/pull/31
                #sel.format = None
                sel.format = 3
                sel.gidArray = [sel.gidArray[i] for i in indices]
            cs.charStrings = {g:indices.index(v)
                              for g,v in cs.charStrings.items()
                              if g in s.glyphs}
        else:
            cs.charStrings = {g:v
                              for g,v in cs.charStrings.items()
                              if g in s.glyphs}
        font.charset = [g for g in font.charset if g in s.glyphs]
        font.numGlyphs = len(font.charset)

    return True # any(cff[fontname].numGlyphs for fontname in cff.keys())

@_add_method(psCharStrings.T2CharString)
def subset_subroutines(self, subrs, gsubrs):
    p = self.program
    assert len(p)
    for i in range(1, len(p)):
        if p[i] == 'callsubr':
            assert isinstance(p[i-1], int)
            p[i-1] = subrs._used.index(p[i-1] + subrs._old_bias) - subrs._new_bias
        elif p[i] == 'callgsubr':
            assert isinstance(p[i-1], int)
            p[i-1] = gsubrs._used.index(p[i-1] + gsubrs._old_bias) - gsubrs._new_bias

@_add_method(psCharStrings.T2CharString)
def drop_hints(self):
    hints = self._hints

    if hints.has_hint:
        self.program = self.program[hints.last_hint:]
        if hasattr(self, 'width'):
            # Insert width back if needed
            if self.width != self.private.defaultWidthX:
                self.program.insert(0, self.width - self.private.nominalWidthX)

    if hints.has_hintmask:
        i = 0
        p = self.program
        while i < len(p):
            if p[i] in ['hintmask', 'cntrmask']:
                assert i + 1 <= len(p)
                del p[i:i+2]
                continue
            i += 1

    # TODO: we currently don't drop calls to "empty" subroutines.

    assert len(self.program)

    del self._hints

class _MarkingT2Decompiler(psCharStrings.SimpleT2Decompiler):

    def __init__(self, localSubrs, globalSubrs):
        psCharStrings.SimpleT2Decompiler.__init__(self,
                                                  localSubrs,
                                                  globalSubrs)
        for subrs in [localSubrs, globalSubrs]:
            if subrs and not hasattr(subrs, "_used"):
                subrs._used = set()

    def op_callsubr(self, index):
        self.localSubrs._used.add(self.operandStack[-1]+self.localBias)
        psCharStrings.SimpleT2Decompiler.op_callsubr(self, index)

    def op_callgsubr(self, index):
        self.globalSubrs._used.add(self.operandStack[-1]+self.globalBias)
        psCharStrings.SimpleT2Decompiler.op_callgsubr(self, index)

class _DehintingT2Decompiler(psCharStrings.SimpleT2Decompiler):

    class Hints(object):
        def __init__(self):
            # Whether calling this charstring produces any hint stems
            self.has_hint = False
            # Index to start at to drop all hints
            self.last_hint = 0
            # Index up to which we know more hints are possible.
            # Only relevant if status is 0 or 1.
            self.last_checked = 0
            # The status means:
            # 0: after dropping hints, this charstring is empty
            # 1: after dropping hints, there may be more hints
            #    continuing after this
            # 2: no more hints possible after this charstring
            self.status = 0
            # Has hintmask instructions; not recursive
            self.has_hintmask = False
        pass

    def __init__(self, css, localSubrs, globalSubrs):
        self._css = css
        psCharStrings.SimpleT2Decompiler.__init__(self,
                                                  localSubrs,
                                                  globalSubrs)

    def execute(self, charString):
        old_hints = charString._hints if hasattr(charString, '_hints') else None
        charString._hints = self.Hints()

        psCharStrings.SimpleT2Decompiler.execute(self, charString)

        hints = charString._hints

        if hints.has_hint or hints.has_hintmask:
            self._css.add(charString)

        if hints.status != 2:
            # Check from last_check, make sure we didn't have any operators.
            for i in range(hints.last_checked, len(charString.program) - 1):
                if isinstance(charString.program[i], str):
                    hints.status = 2
                    break
                else:
                    hints.status = 1 # There's *something* here
            hints.last_checked = len(charString.program)

        if old_hints:
            assert hints.__dict__ == old_hints.__dict__

    def op_callsubr(self, index):
        subr = self.localSubrs[self.operandStack[-1]+self.localBias]
        psCharStrings.SimpleT2Decompiler.op_callsubr(self, index)
        self.processSubr(index, subr)

    def op_callgsubr(self, index):
        subr = self.globalSubrs[self.operandStack[-1]+self.globalBias]
        psCharStrings.SimpleT2Decompiler.op_callgsubr(self, index)
        self.processSubr(index, subr)

    def op_hstem(self, index):
        psCharStrings.SimpleT2Decompiler.op_hstem(self, index)
        self.processHint(index)
    def op_vstem(self, index):
        psCharStrings.SimpleT2Decompiler.op_vstem(self, index)
        self.processHint(index)
    def op_hstemhm(self, index):
        psCharStrings.SimpleT2Decompiler.op_hstemhm(self, index)
        self.processHint(index)
    def op_vstemhm(self, index):
        psCharStrings.SimpleT2Decompiler.op_vstemhm(self, index)
        self.processHint(index)
    def op_hintmask(self, index):
        psCharStrings.SimpleT2Decompiler.op_hintmask(self, index)
        self.processHintmask(index)
    def op_cntrmask(self, index):
        psCharStrings.SimpleT2Decompiler.op_cntrmask(self, index)
        self.processHintmask(index)

    def processHintmask(self, index):
        cs = self.callingStack[-1]
        hints = cs._hints
        hints.has_hintmask = True
        if hints.status != 2 and hints.has_hint:
            # Check from last_check, see if we may be an implicit vstem
            for i in range(hints.last_checked, index - 1):
                if isinstance(cs.program[i], str):
                    hints.status = 2
                    break
            if hints.status != 2:
                # We are an implicit vstem
                hints.last_hint = index + 1
                hints.status = 0
        hints.last_checked = index + 1

    def processHint(self, index):
        cs = self.callingStack[-1]
        hints = cs._hints
        hints.has_hint = True
        hints.last_hint = index
        hints.last_checked = index

    def processSubr(self, index, subr):
        cs = self.callingStack[-1]
        hints = cs._hints
        subr_hints = subr._hints

        if subr_hints.has_hint:
            if hints.status != 2:
                hints.has_hint = True
                hints.last_checked = index
                hints.status = subr_hints.status
                # Decide where to chop off from
                if subr_hints.status == 0:
                    hints.last_hint = index
                else:
                    hints.last_hint = index - 2 # Leave the subr call in
            else:
                # In my understanding, this is a font bug.
                # I.e., it has hint stems *after* path construction.
                # I've seen this in widespread fonts.
                # Best to ignore the hints I suppose...
                pass
                #assert 0
        else:
            hints.status = max(hints.status, subr_hints.status)
            if hints.status != 2:
                # Check from last_check, make sure we didn't have
                # any operators.
                for i in range(hints.last_checked, index - 1):
                    if isinstance(cs.program[i], str):
                        hints.status = 2
                        break
                hints.last_checked = index
            if hints.status != 2:
                # Decide where to chop off from
                if subr_hints.status == 0:
                    hints.last_hint = index
                else:
                    hints.last_hint = index - 2 # Leave the subr call in

class _DesubroutinizingT2Decompiler(psCharStrings.SimpleT2Decompiler):

    def __init__(self, localSubrs, globalSubrs):
        psCharStrings.SimpleT2Decompiler.__init__(self,
                                                  localSubrs,
                                                  globalSubrs)

    def execute(self, charString):
        # Note: Currently we recompute _desubroutinized each time.
        # This is more robust in some cases, but in other places we assume
        # that each subroutine always expands to the same code, so
        # maybe it doesn't matter. To speed up we can just not
        # recompute _desubroutinized if it's there. For now I just
        # double-check that it desubroutinized to the same thing.
        old_desubroutinized = charString._desubroutinized if hasattr(charString, '_desubroutinized') else None

        charString._patches = []
        psCharStrings.SimpleT2Decompiler.execute(self, charString)
        desubroutinized = charString.program[:]
        for idx,expansion in reversed (charString._patches):
            assert idx >= 2
            assert desubroutinized[idx - 1] in ['callsubr', 'callgsubr'], desubroutinized[idx - 1]
            assert type(desubroutinized[idx - 2]) == int
            if expansion[-1] == 'return':
                expansion = expansion[:-1]
            desubroutinized[idx-2:idx] = expansion
        if 'endchar' in desubroutinized:
            # Cut off after first endchar
            desubroutinized = desubroutinized[:desubroutinized.index('endchar') + 1]
        else:
            if not len(desubroutinized) or desubroutinized[-1] != 'return':
                desubroutinized.append('return')

        charString._desubroutinized = desubroutinized
        del charString._patches

        if old_desubroutinized:
            assert desubroutinized == old_desubroutinized

    def op_callsubr(self, index):
        subr = self.localSubrs[self.operandStack[-1]+self.localBias]
        psCharStrings.SimpleT2Decompiler.op_callsubr(self, index)
        self.processSubr(index, subr)

    def op_callgsubr(self, index):
        subr = self.globalSubrs[self.operandStack[-1]+self.globalBias]
        psCharStrings.SimpleT2Decompiler.op_callgsubr(self, index)
        self.processSubr(index, subr)

    def processSubr(self, index, subr):
        cs = self.callingStack[-1]
        cs._patches.append((index, subr._desubroutinized))


@_add_method(ttLib.getTableClass('CFF '))
def prune_post_subset(self, options):
    cff = self.cff
    for fontname in cff.keys():
        font = cff[fontname]
        cs = font.CharStrings

        # Drop unused FontDictionaries
        if hasattr(font, "FDSelect"):
            sel = font.FDSelect
            indices = _uniq_sort(sel.gidArray)
            sel.gidArray = [indices.index (ss) for ss in sel.gidArray]
            arr = font.FDArray
            arr.items = [arr[i] for i in indices]
            del arr.file, arr.offsets

        # Desubroutinize if asked for
        if options.desubroutinize:
            for g in font.charset:
                c,sel = cs.getItemAndSelector(g)
                c.decompile()
                subrs = getattr(c.private, "Subrs", [])
                decompiler = _DesubroutinizingT2Decompiler(subrs, c.globalSubrs)
                decompiler.execute(c)
                c.program = c._desubroutinized

        # Drop hints if not needed
        if not options.hinting:

            # This can be tricky, but doesn't have to. What we do is:
            #
            # - Run all used glyph charstrings and recurse into subroutines,
            # - For each charstring (including subroutines), if it has any
            #   of the hint stem operators, we mark it as such.
            #   Upon returning, for each charstring we note all the
            #   subroutine calls it makes that (recursively) contain a stem,
            # - Dropping hinting then consists of the following two ops:
            #     * Drop the piece of the program in each charstring before the
            #         last call to a stem op or a stem-calling subroutine,
            #     * Drop all hintmask operations.
            # - It's trickier... A hintmask right after hints and a few numbers
            #     will act as an implicit vstemhm. As such, we track whether
            #     we have seen any non-hint operators so far and do the right
            #     thing, recursively... Good luck understanding that :(
            css = set()
            for g in font.charset:
                c,sel = cs.getItemAndSelector(g)
                c.decompile()
                subrs = getattr(c.private, "Subrs", [])
                decompiler = _DehintingT2Decompiler(css, subrs, c.globalSubrs)
                decompiler.execute(c)
            for charstring in css:
                charstring.drop_hints()
            del css

            # Drop font-wide hinting values
            all_privs = []
            if hasattr(font, 'FDSelect'):
                all_privs.extend(fd.Private for fd in font.FDArray)
            else:
                all_privs.append(font.Private)
            for priv in all_privs:
                for k in ['BlueValues', 'OtherBlues',
                          'FamilyBlues', 'FamilyOtherBlues',
                          'BlueScale', 'BlueShift', 'BlueFuzz',
                          'StemSnapH', 'StemSnapV', 'StdHW', 'StdVW']:
                    if hasattr(priv, k):
                        setattr(priv, k, None)

        # Renumber subroutines to remove unused ones

        # Mark all used subroutines
        for g in font.charset:
            c,sel = cs.getItemAndSelector(g)
            subrs = getattr(c.private, "Subrs", [])
            decompiler = _MarkingT2Decompiler(subrs, c.globalSubrs)
            decompiler.execute(c)

        all_subrs = [font.GlobalSubrs]
        if hasattr(font, 'FDSelect'):
            all_subrs.extend(fd.Private.Subrs for fd in font.FDArray if hasattr(fd.Private, 'Subrs') and fd.Private.Subrs)
        elif hasattr(font.Private, 'Subrs') and font.Private.Subrs:
            all_subrs.append(font.Private.Subrs)

        subrs = set(subrs) # Remove duplicates

        # Prepare
        for subrs in all_subrs:
            if not hasattr(subrs, '_used'):
                subrs._used = set()
            subrs._used = _uniq_sort(subrs._used)
            subrs._old_bias = psCharStrings.calcSubrBias(subrs)
            subrs._new_bias = psCharStrings.calcSubrBias(subrs._used)

        # Renumber glyph charstrings
        for g in font.charset:
            c,sel = cs.getItemAndSelector(g)
            subrs = getattr(c.private, "Subrs", [])
            c.subset_subroutines (subrs, font.GlobalSubrs)

        # Renumber subroutines themselves
        for subrs in all_subrs:
            if subrs == font.GlobalSubrs:
                if not hasattr(font, 'FDSelect') and hasattr(font.Private, 'Subrs'):
                    local_subrs = font.Private.Subrs
                else:
                    local_subrs = []
            else:
                local_subrs = subrs

            subrs.items = [subrs.items[i] for i in subrs._used]
            del subrs.file
            if hasattr(subrs, 'offsets'):
                del subrs.offsets

            for subr in subrs.items:
                subr.subset_subroutines (local_subrs, font.GlobalSubrs)

        # Cleanup
        for subrs in all_subrs:
            del subrs._used, subrs._old_bias, subrs._new_bias

    return True

@_add_method(ttLib.getTableClass('cmap'))
def closure_glyphs(self, s):
    tables = [t for t in self.tables if t.isUnicode()]

    # Close glyphs
    for table in tables:
        if table.format == 14:
            for cmap in table.uvsDict.values():
                glyphs = {g for u,g in cmap if u in s.unicodes_requested}
                if None in glyphs:
                    glyphs.remove(None)
                s.glyphs.update(glyphs)
        else:
            cmap = table.cmap
            intersection = s.unicodes_requested.intersection(cmap.keys())
            s.glyphs.update(cmap[u] for u in intersection)

    # Calculate unicodes_missing
    s.unicodes_missing = s.unicodes_requested.copy()
    for table in tables:
        s.unicodes_missing.difference_update(table.cmap)

@_add_method(ttLib.getTableClass('cmap'))
def prune_pre_subset(self, options):
    if not options.legacy_cmap:
        # Drop non-Unicode / non-Symbol cmaps
        self.tables = [t for t in self.tables if t.isUnicode() or t.isSymbol()]
    if not options.symbol_cmap:
        self.tables = [t for t in self.tables if not t.isSymbol()]
    # TODO(behdad) Only keep one subtable?
    # For now, drop format=0 which can't be subset_glyphs easily?
    self.tables = [t for t in self.tables if t.format != 0]
    self.numSubTables = len(self.tables)
    return True # Required table

@_add_method(ttLib.getTableClass('cmap'))
def subset_glyphs(self, s):
    s.glyphs = None # We use s.glyphs_requested and s.unicodes_requested only
    for t in self.tables:
        if t.format == 14:
            # TODO(behdad) We drop all the default-UVS mappings
            # for glyphs_requested.  So it's the caller's responsibility to make
            # sure those are included.
            t.uvsDict = {v:[(u,g) for u,g in l
                                  if g in s.glyphs_requested or u in s.unicodes_requested]
                         for v,l in t.uvsDict.items()}
            t.uvsDict = {v:l for v,l in t.uvsDict.items() if l}
        elif t.isUnicode():
            t.cmap = {u:g for u,g in t.cmap.items()
                          if g in s.glyphs_requested or u in s.unicodes_requested}
        else:
            t.cmap = {u:g for u,g in t.cmap.items()
                          if g in s.glyphs_requested}
    self.tables = [t for t in self.tables
                   if (t.cmap if t.format != 14 else t.uvsDict)]
    self.numSubTables = len(self.tables)
    # TODO(behdad) Convert formats when needed.
    # In particular, if we have a format=12 without non-BMP
    # characters, either drop format=12 one or convert it
    # to format=4 if there's not one.
    return True # Required table

@_add_method(ttLib.getTableClass('DSIG'))
def prune_pre_subset(self, options):
    # Drop all signatures since they will be invalid
    self.usNumSigs = 0
    self.signatureRecords = []
    return True

@_add_method(ttLib.getTableClass('maxp'))
def prune_pre_subset(self, options):
    if not options.hinting:
        if self.tableVersion == 0x00010000:
            self.maxZones = 1
            self.maxTwilightPoints = 0
            self.maxFunctionDefs = 0
            self.maxInstructionDefs = 0
            self.maxStackElements = 0
            self.maxSizeOfInstructions = 0
    return True

@_add_method(ttLib.getTableClass('name'))
def prune_pre_subset(self, options):
    if '*' not in options.name_IDs:
        self.names = [n for n in self.names if n.nameID in options.name_IDs]
    if not options.name_legacy:
        # TODO(behdad) Sometimes (eg Apple Color Emoji) there's only a macroman
        # entry for Latin and no Unicode names.
        self.names = [n for n in self.names if n.isUnicode()]
    # TODO(behdad) Option to keep only one platform's
    if '*' not in options.name_languages:
        # TODO(behdad) This is Windows-platform specific!
        self.names = [n for n in self.names
                      if n.langID in options.name_languages]
    if options.obfuscate_names:
        namerecs = []
        for n in self.names:
            if n.nameID in [1, 4]:
                n.string = ".\x7f".encode('utf_16_be') if n.isUnicode() else ".\x7f"
            elif n.nameID in [2, 6]:
                n.string = "\x7f".encode('utf_16_be') if n.isUnicode() else "\x7f"
            elif n.nameID == 3:
                n.string = ""
            elif n.nameID in [16, 17, 18]:
                continue
            namerecs.append(n)
        self.names = namerecs
    return True    # Required table


# TODO(behdad) OS/2 ulUnicodeRange / ulCodePageRange?
# TODO(behdad) Drop AAT tables.
# TODO(behdad) Drop unneeded GSUB/GPOS Script/LangSys entries.
# TODO(behdad) Drop empty GSUB/GPOS, and GDEF if no GSUB/GPOS left
# TODO(behdad) Drop GDEF subitems if unused by lookups
# TODO(behdad) Avoid recursing too much (in GSUB/GPOS and in CFF)
# TODO(behdad) Text direction considerations.
# TODO(behdad) Text script / language considerations.
# TODO(behdad) Optionally drop 'kern' table if GPOS available
# TODO(behdad) Implement --unicode='*' to choose all cmap'ed
# TODO(behdad) Drop old-spec Indic scripts


class Options(object):

    class OptionError(Exception): pass
    class UnknownOptionError(OptionError): pass

    _drop_tables_default = ['BASE', 'JSTF', 'DSIG', 'EBDT', 'EBLC',
                            'EBSC', 'SVG ', 'PCLT', 'LTSH']
    _drop_tables_default += ['Feat', 'Glat', 'Gloc', 'Silf', 'Sill']  # Graphite
    _drop_tables_default += ['CBLC', 'CBDT', 'sbix', 'COLR', 'CPAL']  # Color
    _no_subset_tables_default = ['gasp', 'head', 'hhea', 'maxp',
                                 'vhea', 'OS/2', 'loca', 'name', 'cvt ',
                                 'fpgm', 'prep', 'VDMX', 'DSIG']
    _hinting_tables_default = ['cvt ', 'fpgm', 'prep', 'hdmx', 'VDMX']

    # Based on HarfBuzz shapers
    _layout_features_groups = {
        # Default shaper
        'common': ['ccmp', 'liga', 'locl', 'mark', 'mkmk', 'rlig'],
        'horizontal': ['calt', 'clig', 'curs', 'kern', 'rclt'],
        'vertical': ['valt', 'vert', 'vkrn', 'vpal', 'vrt2'],
        'ltr': ['ltra', 'ltrm'],
        'rtl': ['rtla', 'rtlm'],
        # Complex shapers
        'arabic': ['init', 'medi', 'fina', 'isol', 'med2', 'fin2', 'fin3',
                   'cswh', 'mset'],
        'hangul': ['ljmo', 'vjmo', 'tjmo'],
        'tibetan': ['abvs', 'blws', 'abvm', 'blwm'],
        'indic': ['nukt', 'akhn', 'rphf', 'rkrf', 'pref', 'blwf', 'half',
                  'abvf', 'pstf', 'cfar', 'vatu', 'cjct', 'init', 'pres',
                  'abvs', 'blws', 'psts', 'haln', 'dist', 'abvm', 'blwm'],
    }
    _layout_features_default = _uniq_sort(sum(
            iter(_layout_features_groups.values()), []))

    drop_tables = _drop_tables_default
    no_subset_tables = _no_subset_tables_default
    hinting_tables = _hinting_tables_default
    legacy_kern = False    # drop 'kern' table if GPOS available
    layout_features = _layout_features_default
    ignore_missing_glyphs = False
    ignore_missing_unicodes = True
    hinting = True
    glyph_names = False
    legacy_cmap = False
    symbol_cmap = False
    name_IDs = [1, 2]    # Family and Style
    name_legacy = False
    name_languages = [0x0409]    # English
    obfuscate_names = False    # to make webfont unusable as a system font
    notdef_glyph = True # gid0 for TrueType / .notdef for CFF
    notdef_outline = False # No need for notdef to have an outline really
    recommended_glyphs = False    # gid1, gid2, gid3 for TrueType
    recalc_bounds = False # Recalculate font bounding boxes
    recalc_timestamp = False # Recalculate font modified timestamp
    canonical_order = False # Order tables as recommended
    flavor = None  # May be 'woff' or 'woff2'
    desubroutinize = False # Desubroutinize CFF CharStrings

    def __init__(self, **kwargs):
        self.set(**kwargs)

    def set(self, **kwargs):
        for k,v in kwargs.items():
            if not hasattr(self, k):
                raise self.UnknownOptionError("Unknown option '%s'" % k)
            setattr(self, k, v)

    def parse_opts(self, argv, ignore_unknown=False):
        ret = []
        for a in argv:
            orig_a = a
            if not a.startswith('--'):
                ret.append(a)
                continue
            a = a[2:]
            i = a.find('=')
            op = '='
            if i == -1:
                if a.startswith("no-"):
                    k = a[3:]
                    v = False
                else:
                    k = a
                    v = True
                if k.endswith("?"):
                    k = k[:-1]
                    v = '?'
            else:
                k = a[:i]
                if k[-1] in "-+":
                    op = k[-1]+'='    # Op is '-=' or '+=' now.
                    k = k[:-1]
                v = a[i+1:]
            ok = k
            k = k.replace('-', '_')
            if not hasattr(self, k):
                if ignore_unknown is True or ok in ignore_unknown:
                    ret.append(orig_a)
                    continue
                else:
                    raise self.UnknownOptionError("Unknown option '%s'" % a)

            ov = getattr(self, k)
            if v == '?':
                    print("Current setting for '%s' is: %s" % (ok, ov))
                    continue
            if isinstance(ov, bool):
                v = bool(v)
            elif isinstance(ov, int):
                v = int(v)
            elif isinstance(ov, str):
                v = str(v) # redundant
            elif isinstance(ov, list):
                if isinstance(v, bool):
                    raise self.OptionError("Option '%s' requires values to be specified using '='" % a)
                vv = v.replace(',', ' ').split()
                if vv == ['']:
                    vv = []
                vv = [int(x, 0) if len(x) and x[0] in "0123456789" else x for x in vv]
                if op == '=':
                    v = vv
                elif op == '+=':
                    v = ov
                    v.extend(vv)
                elif op == '-=':
                    v = ov
                    for x in vv:
                        if x in v:
                            v.remove(x)
                else:
                    assert False

            setattr(self, k, v)

        return ret


class Subsetter(object):

    class SubsettingError(Exception): pass
    class MissingGlyphsSubsettingError(SubsettingError): pass
    class MissingUnicodesSubsettingError(SubsettingError): pass

    def __init__(self, options=None, log=None):

        if not log:
            log = Logger()
        if not options:
            options = Options()

        self.options = options
        self.log = log
        self.unicodes_requested = set()
        self.glyph_names_requested = set()
        self.glyph_ids_requested = set()

    def populate(self, glyphs=[], gids=[], unicodes=[], text=""):
        self.unicodes_requested.update(unicodes)
        if isinstance(text, bytes):
            text = text.decode("utf_8")
        for u in text:
            self.unicodes_requested.add(ord(u))
        self.glyph_names_requested.update(glyphs)
        self.glyph_ids_requested.update(gids)

    def _prune_pre_subset(self, font):

        for tag in font.keys():
            if tag == 'GlyphOrder': continue

            if(tag in self.options.drop_tables or
                 (tag in self.options.hinting_tables and not self.options.hinting) or
                 (tag == 'kern' and (not self.options.legacy_kern and 'GPOS' in font))):
                self.log(tag, "dropped")
                del font[tag]
                continue

            clazz = ttLib.getTableClass(tag)

            if hasattr(clazz, 'prune_pre_subset'):
                table = font[tag]
                self.log.lapse("load '%s'" % tag)
                retain = table.prune_pre_subset(self.options)
                self.log.lapse("prune '%s'" % tag)
                if not retain:
                    self.log(tag, "pruned to empty; dropped")
                    del font[tag]
                    continue
                else:
                    self.log(tag, "pruned")

    def _closure_glyphs(self, font):

        realGlyphs = set(font.getGlyphOrder())
        glyph_order = font.getGlyphOrder()

        self.glyphs_requested = set()
        self.glyphs_requested.update(self.glyph_names_requested)
        self.glyphs_requested.update(glyph_order[i]
                                     for i in self.glyph_ids_requested
                                     if i < len(glyph_order))

        self.glyphs_missing = set()
        self.glyphs_missing.update(self.glyphs_requested.difference(realGlyphs))
        self.glyphs_missing.update(i for i in self.glyph_ids_requested
                                   if i >= len(glyph_order))
        if self.glyphs_missing:
            self.log("Missing requested glyphs: %s" % self.glyphs_missing)
            if not self.options.ignore_missing_glyphs:
                raise self.MissingGlyphsSubsettingError(self.glyphs_missing)

        self.glyphs = self.glyphs_requested.copy()

        self.unicodes_missing = set()
        if 'cmap' in font:
            font['cmap'].closure_glyphs(self)
            self.glyphs.intersection_update(realGlyphs)
            self.log.lapse("close glyph list over 'cmap'")
        self.glyphs_cmaped = frozenset(self.glyphs)
        if self.unicodes_missing:
            missing = ["U+%04X" % u for u in self.unicodes_missing]
            self.log("Missing glyphs for requested Unicodes: %s" % missing)
            if not self.options.ignore_missing_unicodes:
                raise self.MissingUnicodesSubsettingError(missing)
            del missing

        if self.options.notdef_glyph:
            if 'glyf' in font:
                self.glyphs.add(font.getGlyphName(0))
                self.log("Added gid0 to subset")
            else:
                self.glyphs.add('.notdef')
                self.log("Added .notdef to subset")
        if self.options.recommended_glyphs:
            if 'glyf' in font:
                for i in range(min(4, len(font.getGlyphOrder()))):
                    self.glyphs.add(font.getGlyphName(i))
                self.log("Added first four glyphs to subset")

        if 'GSUB' in font:
            self.log("Closing glyph list over 'GSUB': %d glyphs before" %
                     len(self.glyphs))
            self.log.glyphs(self.glyphs, font=font)
            font['GSUB'].closure_glyphs(self)
            self.glyphs.intersection_update(realGlyphs)
            self.log("Closed glyph list over 'GSUB': %d glyphs after" %
                     len(self.glyphs))
            self.log.glyphs(self.glyphs, font=font)
            self.log.lapse("close glyph list over 'GSUB'")
        self.glyphs_gsubed = frozenset(self.glyphs)

        if 'glyf' in font:
            self.log("Closing glyph list over 'glyf': %d glyphs before" %
                     len(self.glyphs))
            self.log.glyphs(self.glyphs, font=font)
            font['glyf'].closure_glyphs(self)
            self.glyphs.intersection_update(realGlyphs)
            self.log("Closed glyph list over 'glyf': %d glyphs after" %
                     len(self.glyphs))
            self.log.glyphs(self.glyphs, font=font)
            self.log.lapse("close glyph list over 'glyf'")
        self.glyphs_glyfed = frozenset(self.glyphs)

        self.glyphs_all = frozenset(self.glyphs)

        self.log("Retaining %d glyphs: " % len(self.glyphs_all))

        del self.glyphs

    def _subset_glyphs(self, font):
        for tag in font.keys():
            if tag == 'GlyphOrder': continue
            clazz = ttLib.getTableClass(tag)

            if tag in self.options.no_subset_tables:
                self.log(tag, "subsetting not needed")
            elif hasattr(clazz, 'subset_glyphs'):
                table = font[tag]
                self.glyphs = self.glyphs_all
                retain = table.subset_glyphs(self)
                del self.glyphs
                self.log.lapse("subset '%s'" % tag)
                if not retain:
                    self.log(tag, "subsetted to empty; dropped")
                    del font[tag]
                else:
                    self.log(tag, "subsetted")
            else:
                self.log(tag, "NOT subset; don't know how to subset; dropped")
                del font[tag]

        glyphOrder = font.getGlyphOrder()
        glyphOrder = [g for g in glyphOrder if g in self.glyphs_all]
        font.setGlyphOrder(glyphOrder)
        font._buildReverseGlyphOrderDict()
        self.log.lapse("subset GlyphOrder")

    def _prune_post_subset(self, font):
        for tag in font.keys():
            if tag == 'GlyphOrder': continue
            clazz = ttLib.getTableClass(tag)
            if hasattr(clazz, 'prune_post_subset'):
                table = font[tag]
                retain = table.prune_post_subset(self.options)
                self.log.lapse("prune '%s'" % tag)
                if not retain:
                    self.log(tag, "pruned to empty; dropped")
                    del font[tag]
                else:
                    self.log(tag, "pruned")

    def subset(self, font):

        self._prune_pre_subset(font)
        self._closure_glyphs(font)
        self._subset_glyphs(font)
        self._prune_post_subset(font)


class Logger(object):

    def __init__(self, verbose=False, xml=False, timing=False):
        self.verbose = verbose
        self.xml = xml
        self.timing = timing
        self.last_time = self.start_time = time.time()

    def parse_opts(self, argv):
        argv = argv[:]
        for v in ['verbose', 'xml', 'timing']:
            if "--"+v in argv:
                setattr(self, v, True)
                argv.remove("--"+v)
        return argv

    def __call__(self, *things):
        if not self.verbose:
            return
        print(' '.join(str(x) for x in things))

    def lapse(self, *things):
        if not self.timing:
            return
        new_time = time.time()
        print("Took %0.3fs to %s" %(new_time - self.last_time,
                                    ' '.join(str(x) for x in things)))
        self.last_time = new_time

    def glyphs(self, glyphs, font=None):
        if not self.verbose:
            return
        self("Glyph names:", sorted(glyphs))
        if font:
            reverseGlyphMap = font.getReverseGlyphMap()
            self("Glyph IDs:    ", sorted(reverseGlyphMap[g] for g in glyphs))

    def font(self, font, file=sys.stdout):
        if not self.xml:
            return
        from fontTools.misc import xmlWriter
        writer = xmlWriter.XMLWriter(file)
        for tag in font.keys():
            writer.begintag(tag)
            writer.newline()
            font[tag].toXML(writer, font)
            writer.endtag(tag)
            writer.newline()


def load_font(fontFile,
              options,
              allowVID=False,
              checkChecksums=False,
              dontLoadGlyphNames=False,
              lazy=True):

    font = ttLib.TTFont(fontFile,
                        allowVID=allowVID,
                        checkChecksums=checkChecksums,
                        recalcBBoxes=options.recalc_bounds,
                        recalcTimestamp=options.recalc_timestamp,
                        lazy=lazy)

    # Hack:
    #
    # If we don't need glyph names, change 'post' class to not try to
    # load them.    It avoid lots of headache with broken fonts as well
    # as loading time.
    #
    # Ideally ttLib should provide a way to ask it to skip loading
    # glyph names.    But it currently doesn't provide such a thing.
    #
    if dontLoadGlyphNames:
        post = ttLib.getTableClass('post')
        saved = post.decode_format_2_0
        post.decode_format_2_0 = post.decode_format_3_0
        f = font['post']
        if f.formatType == 2.0:
            f.formatType = 3.0
        post.decode_format_2_0 = saved

    return font

def save_font(font, outfile, options):
    if options.flavor and not hasattr(font, 'flavor'):
        raise Exception("fonttools version does not support flavors.")
    font.flavor = options.flavor
    font.save(outfile, reorderTables=options.canonical_order)

def parse_unicodes(s):
    import re
    s = re.sub (r"0[xX]", " ", s)
    s = re.sub (r"[<+>,;&#\\xXuU\n    ]", " ", s)
    l = []
    for item in s.split():
        fields = item.split('-')
        if len(fields) == 1:
            l.append(int(item, 16))
        else:
            start,end = fields
            l.extend(range(int(start, 16), int(end, 16)+1))
    return l

def parse_gids(s):
    l = []
    for item in s.replace(',', ' ').split():
        fields = item.split('-')
        if len(fields) == 1:
            l.append(int(fields[0]))
        else:
            l.extend(range(int(fields[0]), int(fields[1])+1))
    return l

def parse_glyphs(s):
    return s.replace(',', ' ').split()

def main(args=None):

    if args is None:
        args = sys.argv[1:]

    if '--help' in args:
        print(__doc__)
        sys.exit(0)

    log = Logger()
    args = log.parse_opts(args)

    options = Options()
    args = options.parse_opts(args,
        ignore_unknown=['gids', 'gids-file',
                        'glyphs', 'glyphs-file',
                        'text', 'text-file',
                        'unicodes', 'unicodes-file',
                        'output-file'])

    if len(args) < 2:
        print("usage:", __usage__, file=sys.stderr)
        print("Try pyftsubset --help for more information.", file=sys.stderr)
        sys.exit(1)

    fontfile = args[0]
    args = args[1:]

    subsetter = Subsetter(options=options, log=log)
    outfile = fontfile + '.subset'
    glyphs = []
    gids = []
    unicodes = []
    wildcard_glyphs = False
    wildcard_unicodes = False
    text = ""
    for g in args:
        if g == '*':
            wildcard_glyphs = True
            continue
        if g.startswith('--output-file='):
            outfile = g[14:]
            continue
        if g.startswith('--text='):
            text += g[7:]
            continue
        if g.startswith('--text-file='):
            text += open(g[12:]).read().replace('\n', '')
            continue
        if g.startswith('--unicodes='):
            if g[11:] == '*':
                wildcard_unicodes = True
            else:
                unicodes.extend(parse_unicodes(g[11:]))
            continue
        if g.startswith('--unicodes-file='):
            for line in open(g[16:]).readlines():
                unicodes.extend(parse_unicodes(line.split('#')[0]))
            continue
        if g.startswith('--gids='):
            gids.extend(parse_gids(g[7:]))
            continue
        if g.startswith('--gids-file='):
            for line in open(g[12:]).readlines():
                gids.extend(parse_gids(line.split('#')[0]))
            continue
        if g.startswith('--glyphs='):
            if g[9:] == '*':
                wildcard_glyphs = True
            else:
                glyphs.extend(parse_glyphs(g[9:]))
            continue
        if g.startswith('--glyphs-file='):
            for line in open(g[14:]).readlines():
                glyphs.extend(parse_glyphs(line.split('#')[0]))
            continue
        glyphs.append(g)

    dontLoadGlyphNames = not options.glyph_names and not glyphs
    font = load_font(fontfile, options, dontLoadGlyphNames=dontLoadGlyphNames)
    log.lapse("load font")
    if wildcard_glyphs:
            glyphs.extend(font.getGlyphOrder())
    if wildcard_unicodes:
            for t in font['cmap'].tables:
                if t.isUnicode():
                    unicodes.extend(t.cmap.keys())
    assert '' not in glyphs

    log.lapse("compile glyph list")
    log("Text: '%s'" % text)
    log("Unicodes:", unicodes)
    log("Glyphs:", glyphs)
    log("Gids:", gids)

    subsetter.populate(glyphs=glyphs, gids=gids, unicodes=unicodes, text=text)
    subsetter.subset(font)

    save_font (font, outfile, options)
    log.lapse("compile and save font")

    log.last_time = log.start_time
    log.lapse("make one with everything(TOTAL TIME)")

    if log.verbose:
        import os
        log("Input font:% 7d bytes: %s" % (os.path.getsize(fontfile), fontfile))
        log("Subset font:% 7d bytes: %s" % (os.path.getsize(outfile), outfile))

    log.font(font)

    font.close()


__all__ = [
    'Options',
    'Subsetter',
    'Logger',
    'load_font',
    'save_font',
    'parse_gids',
    'parse_glyphs',
    'parse_unicodes',
    'main'
]

if __name__ == '__main__':
    main()
