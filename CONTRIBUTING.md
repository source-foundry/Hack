# Hack Typeface Design

Hack is a monospaced typeface that is designed to optimize the display of source code text.

This document outlines the core ideas on which we build to continually improve Hack. Ideally, they serve as a final rationale to decide disputes of whatever nature.

Design is a highly opinionated topic. Being a collaborative effort, we prefer to focus on the discussion about a change, rather than the final product of a change. In practical terms this means that for any substantial amount of work, we'd like to see an Issue Report or Pull Request which presents an idea or the approach for a change. By keeping the discussion open, not only will you get community feedback, it also allows us to judge your contribution on more than the final product.

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


# Issue Reporting

Issue reports from users are extremely important to foster the ongoing development of the typeface.  If you identify a problem, we request that you report it through a new issue report on the Github repository.  Please include the following information in your (bug) issue report:

- Hack font version
- variant(s) of the Hack fonts that are affected (Regular, Bold, Italic, BoldItalic)
- font size at which the problem was observed and whether it occurs at other sizes within the Core design target range (see above)
- operating system and version
- application where the issue was observed and version (important for us to understand the renderer involved)
- screenshot images that visually demonstrate the problem

Please describe what led to the problem in detail.


# Pull Requests

We highly encourage contributions to the Hack typeface source code, repository scripts, and documentation.  Please read and understand our design philosophy statement above in order to avoid frustration with work that we cannot merge upstream.  We are willing to consider pull requests that follow these design guidelines.  If you intend to submit changes that fall outside of the design guidelines, we highly suggest that you post an issue report with the proposed changes for discussion *before you do the work*.  There is never wasted work.  If a change is of value to you, it is likely to be of value to others and this is the perfect situation for a downstream fork of Hack that you can maintain and share with other users.

