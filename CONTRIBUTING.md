# Hack Typeface Design

Hack is a monospaced typeface that is designed to optimize the display of source code text.

This document outlines the core ideas on which we build to continually improve Hack. Ideally, they serve as a final rationale to decide disputes of whatever nature.

Design is a highly subjective and opinionated topic. Being a collaborative effort, we prefer to focus on the discussion about a change, rather than the final product of a change. In practical terms this means that for any substantial amount of work, we'd like to see an Issue Report or Pull Request which presents an idea or the approach for a change. By keeping the discussion open, not only will you get community feedback, it also allows us to judge your contribution on more than the final product.

## Design Targets

Hack is a general purpose typeface for source code. The _needs of the many_ describe our core design targets. Generally, an issue that affects a majority of users receives higher priority than an issue that affects a minority of users.

### Core

- **ASCII glyph set**; generally speaking, all source code is limited to the ASCII set. Content/comments/documentation, on the other hand, often includes non-ASCII characters. The former gets precedence over the latter.
- We focus on an accepted **single glyph style** for each glyph in the typeface sets.  Glyph shape changes that are intended to address our design goals take precedence over changes that are purely subjective in nature.  We offer the [alt-hack](https://github.com/source-foundry/alt-hack) repository for alternate Hack glyph styles and contributions of alternate styles are welcomed there.
- Font-sizes between **8-14 px**, line-height >= 1
- **Cross-platform**, cross font renderer support on Linux, OS X, and Windows operating systems.  Changes that address cross platform issues take precedence over issues that address platform specific issues.  Changes that improve the typeface on some platforms but decrease its usability on others are generally not acceptable and belong in a fork that is intended for the platforms targeted for these changes.
- Usage in **common source code display scenarios** (on digital displays): text editors, terminals, embedded as web fonts, etc.

## Goals, areas of improvement

- **Legibility** - establish differences in the appearance of similar glyph shapes so as to properly identify different Unicode code points
- **Readability** - glyph shape and spacing optimizations to improve the capacity to read character-character, word-word, and code block-code block combinations in source code
- **Visual semantics** - establish semantic commonalities for glyphs used in source code text and create common visual designs within these semantic groups


# Issue Reporting

Issue reports from users are extremely important to foster the ongoing development of the typeface.

Before you report an issue, please confirm that you have installed the current version of the Hack typeface on your system. See the [README.md page](README.md) for details.

If you identify a problem, we request that you report it through a new issue report on the Github repository.  Please include the following information in your (bug) issue report:

- Font version (or timeframe when you downloaded the fonts if you do not know)
- Where you obtained the fonts (e.g. repository download, package manager, another source)
- variant(s) of the Hack fonts that are affected (Regular, Bold, Italic, BoldItalic)
- font size at which the problem was observed and whether it occurs at other sizes within the Core design target range (see above)
- operating system and version
- application where the issue was observed and version (important for us to understand the renderer involved)
- screenshot images that visually demonstrate the problem

Please describe what led to the problem in detail.


# Pull Requests

We highly encourage contributions to the Hack typeface source code, repository scripts, and documentation.  To view areas where we currently need your help, check out the active issues [Contribute! label](https://github.com/source-foundry/Hack/labels/Contribute%21).


Please read and understand our design philosophy statement above in order to avoid frustration with work that we cannot merge upstream.  We are willing to consider pull requests that follow these design guidelines. Having said that, there is never wasted work.  If a change is of value to you, it is likely to be of value to others and this is the perfect situation for a downstream fork of Hack that you can maintain and share with other users.

## Pull requests for design changes

Contributors who submit source modifications intended for merge into the Hack repository must license these changes according to [LICENSE.md](LICENSE.md).  If this is not acceptable, please do not submit your work for consideration.

Contributors who modify the UFO source code should familiarize themselves with the UFO source specification.  The Hack typeface currently uses version 2 of the UFO specification and documentation is available [here](http://unifiedfontobject.org/versions/ufo2/index.html).

For pull requests that modify the design of the typeface, we request that you limit your source commits to the following changes unless we have discussed and explicitly requested additional file changes as part of the contribution.


### Glyph modifications

Modifications include all existing glyph design changes, glyph additions, and glyph deletions.

- Only include the modified `glyphs/*.glif` source files for the modified glyphs in your pull request commits
- Modification of other source files is not acceptable and pull requests will not be accepted until the above condition is met

You can achieve this design modification workflow with one of the following approaches:

- maintain a separate local directory for your design modifications and copy the `glyphs/*.glif` files that are changed to your local clone of the Hack source, then push to your remote repository fork for your pull request
- modify the Hack source in your local clone of the Hack repository and do not commit file changes other than those that are accepted in pull requests (i.e. only include `*.ufo/glyphs/*.glif` files in your commits)
- modify the Hack source in your local clone of the Hack repository, commit all files, replace all `*plist` files with the upstream versions then perform a git squash commit to eliminate the `*.plist` file changes in the git history (this approach can be used for those who didn't read the instructions and have already commited unacceptable file changes)


## Pull requests for script changes

Contributors who submit script source modifications intended for merge into the Hack repository must license these changes according to the license specified in the script header for existing files.  For new files, please discuss your license with us in an issue report before you submit your work for consideration.

Please add an issue report that describes the issue that your pull request is intended to address (and that the pull request will close when merged).

We request that you try not to add additional external dependencies to the project with your commits.  This has the potential to prevent releases of Hack packages on some platforms.  If you need to add a new dependency to the project, we suggest that you discuss this with us in advance through an issue report so that we can confirm that this is acceptable.

## Pull requests for documentation changes

We love help with our docs!  This includes anything from simple misspelling or grammar changes to major revisions of poorly written sections.  For minor changes, a simple pull request suffices.  For major edits, we recommend that you discuss the changes with us in an issue report before you go to the effort.

# Contributors

Contributions to the project come in many forms and we **want** to broadly acknowledge those who spend time and effort to improve the project.  We understand that many contributions to open source projects are not in the form of changes to the code base and therefore not automatically recognized in the Github repository UI.  Use case specialists play an extremely important role in the improvement of this typeface.  Individuals who have knowledge of the intricacies of open source typeface licensing, understand open source project redistribution processes, have the capacity to view errors and test in unique platform x font renderer situations, and many other areas that extend beyond the "source code commit" criterion have contributed their expertise to improve Hack. Understanding this issue, we maintain a [CONTRIBUTORS.md](docs/CONTRIBUTORS.md) list to acknowledge project contributors for their time and efforts under our own defintion of a project contribution.  If you feel that you have helped to improve Hack and your contributions have been overlooked (i.e. you are not included on the contributors list), please let us know so that we can rectify this issue!  In all likelihood this is an oversight and not intended to be a slight.
