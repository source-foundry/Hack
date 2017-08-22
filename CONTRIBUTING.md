# Hack Typeface Design

Hack is a monospaced typeface that is designed to optimize the display of source code text.

This document outlines the core ideas on which we build to continually improve Hack. Ideally, they serve as a final rationale to decide disputes of whatever nature.

## Design Targets

Hack is a general purpose typeface for source code. The _needs of the many_ describe our core design targets. Generally, an issue that affects 90% of users, gets a higher priority than one that 'only' affects 10%.

### Core

- **ASCII glyph set**; generally speaking, all source code is limited to ASCII. Content/comments/documentation, on the other hand, often includes non-ASCII characters. The former gets precendence over the latter.
- We focus on an accepted **single glyph style** for each glyph in the typeface sets.  Glyph shape changes that are intended to address our design goals take precedence over changes that are purely subjective in nature.
- Font-sizes between **8-14 px**, line-height >= 1
- **Cross-platform**, cross font renderer support on Linux, OS X, and Windows operating systems
- Usage in **common developer scenarios** (on digital displays): text editors, terminals, embedded as webfont, etc.

## Goals, areas of improvement

- **Legibility** - establish differences in the appearance of similar glyph shapes so as to properly identify different Unicode code points
- **Readability** - glyph shape and spacing optimizations to improve the capacity to read character-character, word-word, and code block-code block combinations in source code
- **Visual semantics** - establish semantic commonalities for glyphs used in source code text and create common visual designs within these semantic groups


