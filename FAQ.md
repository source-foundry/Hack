# FAQ

### Contents

- [Installation](#installation)
- [Bugs/errors](#bugserrors)
- [License](#license)
- [Contribute](#contribute)
- [Modifications/Derivatives](#modificationsderivatives)
- [Tinkering](#tinkering)

## Installation

#### How do I download the current version of the Hack desktop fonts?

You can find the [current release of our desktop fonts](https://github.com/source-foundry/Hack/releases/latest) in our releases list.  We recommend that Windows users consider the [Windows installer](https://github.com/source-foundry/Hack-windows-installer) as it addresses font caching issues for initial and repeat installs (for upgrades) that are problematic on the Windows platform.  Hack packages are also available through many package managers for those who would prefer to use this approach.

#### What build format are the Hack desktop fonts released in?

The Hack desktop fonts are released in TrueType format (`.ttf`).

#### How do I download the current version of the Hack web fonts?

Please download the [current release of our web fonts](https://github.com/source-foundry/Hack/releases/latest) from our releases list.

#### What build format are the Hack web fonts released in?

The Hack web fonts are released in Web Open Font Format version 1.0 (`*.woff`) and 2.0 (`*.woff2`).

#### How do I install Hack?

Please see the Quick Installation guide on our [README.md](README.md) page.  If you have further questions, please refer to the font installation instructions for your platform.  A web search should yield all of the information that you need.

#### How do I upgrade Hack?

You can download [the latest release of desktop and web fonts]((https://github.com/source-foundry/Hack/releases/latest)).  We recommend that Windows users upgrade with the [Windows installer](https://github.com/source-foundry/Hack-windows-installer) as it addresses problematic font caching issues that take place on the Windows platform.  Hack packages are also available through many package managers for those who would prefer to use this approach.


#### Is there a web font CDN that I can use in my web pages?

Yes.  See the Web Font Usage section of the [README.md](README.md) document for details.

#### How do I find the changes that occurred in recent releases?

Please review the [CHANGELOG.md](CHANGELOG.md) document.


## Bugs/errors

#### I found a problem with Hack, what do I do?

Please search our issue reports and confirm that your problem has not already been reported or solved.  If it appears to be a new issue, please review the issue reporting information in our [CONTRIBUTING.md](CONTRIBUTING.md) document and then file a new issue report with the necessary information to address your problem.

#### How do I find my installed Hack version number?

Please refer to documentation for your operating system to determine how to find the font version string for installed fonts.  If you cannot find a solution, you can install and use our [font-v tool](https://github.com/source-foundry/font-v) to view the version string with the command `font-v report [font path]`.


## License

#### How is Hack licensed?

Hack is a derivative of upstream Bitstream Vera Sans Mono and DejaVu Sans Mono source.  The Hack changes are licensed under the MIT license.  Bitstream Vera Sans Mono is licensed under the Bitstream Vera license and maintains reserved font names “Bitstream” and “Vera”.  The DejaVu changes to the Bitstream Vera source were committed to the public domain.

You may view the full text of the license in [LICENSE.md](LICENSE.md).

#### Am I allowed to modify glyphs in Hack?

Yes.

#### Am I allowed to extend the character sets in Hack?

Yes.

#### Am I allowed to subset (decrease character set support) Hack?

Yes.

#### Am I allowed to create new build file types for Hack?

Yes.

#### Am I allowed to redistribute an unmodified version of Hack?

Yes.

#### Am I allowed to redistribute a modified version of Hack?

Yes.

#### Do I need to rename a modified version of “Hack”?

As of v3.000, the reserved font name "Hack" was removed from our license.  You may use the name "Hack" for modified versions of the source, though we encourage you to change the name in a way that indicates how this differs from the upstream source if you intend to release the typeface to others.  See the Modifications/Derviatives section of the FAQ below for more information.

#### Do I need to provide attribution when I use Hack?

No.

#### Do I need to maintain the license with modified or unmodified software that is derived from the Hack source?

Yes.


## Contribute

#### Do you accept design contributions to Hack?

Yes.  Design contributions are welcomed and encouraged. Please review and familiarize yourself with the design guidelines in the [CONTRIBUTING.md](CONTRIBUTING.md) documentation before you begin work intended as a contribution to the upstream project.  If you question whether the work is acceptable in the upstream, we ask that you file a new issue report to discuss it before you begin.  Having said that, there is no wasted work and if your changes are not appropriate for the upstream source, a new downstream fork with changes that are important to you (and that you maintain) is very much encouraged.

#### How are my design contributions to Hack licensed?

Changes to the Hack source are licensed under the MIT license.  Please confirm that this is acceptable to you before you submit contributions for design changes.  We do not accept design contributions under a different license.

#### I am not a professional typeface designer, can I contribute design changes to Hack?

Absolutely.  To our knowledge, no contributor who has committed design changes to Hack has a background in professional typeface design or formal typeface design training.  We developed an itch that needed to be scratched, combed websites and books for information, viewed lots (and lots and lots more) of typefaces, installed font editors and learned how to use them, and then went to work.  We continue to learn ourselves.  You are simply at a bit earlier stage of the same journey.  Dive in, learn, and let's see what you can come up with.

#### Do you accept source/script contributions to Hack?

Yes. Changes to current scripts are licensed under the MIT license.  If you intend to submit new, non-UFO (i.e. typeface design) source and would like to license it in a different way, please file an issue report to discuss this before you perform the work.

#### I have never contributed to an open source project.  Does the Hack project support brand new open source contributors?

Yes! Yes! Yes!  We would love to have individuals who are brand new to the open source development community experience collaborative free, open source development for the first time through the Hack project.  We were all there at one stage and had to get past the initial contribution jitters.  Putting your work out in the open for the first time can be a daunting, vulnerable experience and there is a great deal to learn about how the open source contribution workflow works.  Don't let this stop you because this could be the first step on a long path of participation in collaborative open source software development.  We would love to kickstart the work of a new open source developer and intend to maintain a very receptive environment for new participants.  Read the [CONTRIBUTING.md](CONTRIBUTING.md) document, then feel free to pitch ideas that you have as [new issue reports](https://github.com/source-foundry/Hack/issues/new) on the repository.  Let us know that you are new in town so that we can provide assistance where you might need it to get started.

#### Can I submit ideas about design changes?

Yes.  Please understand our design priorities as defined in the [CONTRIBUTING.md](CONTRIBUTING.md) document and file your ideas as new issue reports.  If you feel that the design priorities should be modified, feel free to submit a pull request with suggested changes or file a new issue report.  We can discuss these modifications with either approach.

#### How are my contributions to the Hack project recognized?

Contributors are listed in the [CONTRIBUTORS.md](docs/CONTRIBUTORS.md) list.

#### Who is considered a contributor to the Hack project?

We attempt to broadly acknowledge contributions to the project as defined in the Contributors section of the [CONTRIBUTING.md](CONTRIBUTING.md) document.  Please refer to that document for further details.


## Modifications/Derivatives

#### I want to modify the Hack design and release it myself.  Is this OK?

Yes.

#### I want to add character sets to Hack and release it myself.  Is this OK?

Yes.

#### I want to decrease character set support in Hack and release it myself.  Is this OK?

Yes.

#### I want to change Hack build file types and release it myself.  Is this OK?

Yes.

#### I want to change the hinting approach used in Hack and release it myself.  Is this OK?

Yes.

#### Do I need to provide attribution if I release my own project derived from Hack source?

No.

#### Do I need to modify the name of the typeface if I release a modified version?

As of v3.000, the reserved font name "Hack" was removed from the license.  It is no longer necessary to change the name for modified versions of the Hack source.  Redistribution of modified source under the same name can be confusing to users and we would encourage you to modify the name in a way that clarifies your project goals relative to the upstream source if you intend to release the fonts to others.  One approach is to add another term to the basename "Hack".  For instance, a derivative that supports source code ligatures might be named "Hack Ligature" and a derivative that replaces the oval filled zero with a forward slash zero might be called "Hack Slash".

#### Can I use Hack in the name of my own derived typeface (e.g. Hack Better)?

Yes, this is highly encouraged if you modify the source and release it with the intent for others to use it.

#### Can I change the name of a derived version and not use Hack in the name?

Yes.

#### If I make minor changes to the source and release this as my own project is this considered plagiarism?

No.  Absolutely not.  This is well within the bounds of the license and you are welcome to do so.  There are niche needs that some users have and our goal is to support these however minor through the development of derivative projects.  We are attempting to make the build process, build tooling, and ability to pull any upstream source changes into your own downstream derivative as straightforward and simple as possible in order to support this.  Also understand that you must maintain the upstream license in downstream derivatives.

## Tinkering

#### Do you offer alternate styles of Hack glyphs that I can use to customize the fonts?

Yes!  The [alt-hack stylistic alternate glyph library](https://github.com/source-foundry/alt-hack) is available with `*.glif` files that contain new glyph designs for glyphs that exist in the Hack character sets.  Copy the `.glif` file from the alt-hack library to the Hack source and overwrite the existing `.glif` file.  Then rebuild the fonts with the instructions in [docs/BUILD.md](docs/BUILD.md).

#### How do I change the font name?

The simplest approach is to open the UFO source code in a font editor and follow the instructions in the editor documentation, then re-save the UFO source to maintain the name changes (if you plan for repeat builds from source) and rebuild the font files.

#### How do I modify the line spacing in Hack?

We built the tool [font-line](https://github.com/source-foundry/font-line) to increase and decrease line spacing in Hack (and any other font).  Please see the documentation in the font-line repository README for details.

#### How do I modify the version string in a derivative that I create from the Hack source?

You can approach this by either modifying the version in the UFO source or through the use of our [font-v](https://github.com/source-foundry/font-v) versioning tool. Please see the font-v repository for detailed usage instructions.
