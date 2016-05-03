
# Hack  [![Contributors](https://img.shields.io/badge/contributors-104-orange.svg?style=flat)](https://github.com/chrissimpkins/Hack/blob/master/CONTRIBUTORS.md)

### a typeface designed for source code

No frills. No gimmicks. Hack is hand groomed and optically balanced to be a workhorse face for code. It has deep roots in the libre, open source typeface community and expands upon the contributions of the [Bitstream Vera](https://www.gnome.org/fonts/) &amp; [DejaVu](http://dejavu-fonts.org/wiki/Main_Page) projects.

[Read more](docs/ABOUT.md) about Hack, visit the [project website](http://sourcefoundry.org/hack/), take a look at a complete [type specimen](http://chrissimpkins.github.io/Hack/font-specimen.html) or browse the [CHANGELOG](CHANGELOG.md).

The font binaries are released under a license that permits unlimited print, desktop, and web use for commercial and non-commercial applications. More details in [LICENSE.md](LICENSE.md)

<a href="https://sourcefoundry.org/hack/"><img src="img/hack-specimen-2.png" alt="Hack &mdash; a typeface designed for source code" width="728"></a>

---

## Quick installation

We recommend use of the **TrueType** (`.ttf`) version of Hack for most users.

#### Mac OS X and Linux

1. Download the [latest version of Hack][ttf_latest].
2. Extract the files from the archive (`.zip`) and open them.
3. Follow the instructions from your operating system.
4. Enjoy!

#### Windows

To simplify the installation process on Windows systems, we've created the [Hack Windows Installer](https://github.com/source-foundry/Hack-windows-installer/releases/latest) (`.exe`) which will guide you through the installation process. This installer addresses a number of common rendering issues that occur with font installs on the Windows platform and is the recommended approach on the Windows platform.

**NOTE ON UPDATING**<br>
If you are updating your version of Hack, be sure to remove the previously installed version first to avoid conflicts. For more information, see [INSTALLATION.md](docs/INSTALLATION.md).

A [build with CFF curves][otf_latest] (`.otf`) is available for those who prefer this format.

---

## Advanced options

Because Hack is under active development and updates are released frequently, we highly recommended the convenience of a package manager or other auto-updating utility if this is available on your platform. While the package manager releases may be a bit delayed relative to the repository releases, the package managers automate and simplify font updates on your system.

### Package managers and desktop installation

Details on using package managers and/or advanced manual desktop installation options can be found in [INSTALLATION.md](docs/INSTALLATION.md).

Hack can be installed and updated via various package managers. We are aware of package manager support on the following systems/distros:

- **Mac OS X**: `brew cask install caskroom/fonts/font-hack`
- **Arch Linux**: `pacman -S ttf-hack`
- **Fedora / CentOS**: `copr`, `dnf` or `yum`
- **Gentoo Linux**: `emerge -av media-fonts/hack`
- **Ubuntu / Debian**: `apt-get install fonts-hack-ttf`

<!-- TODO @david: the Fedora/CentOS are a set of multiline commands, how best to display these (see original README).  Users will need all of the info contained previously -->

### Web font usage

Hack is available in all commonly used web font formats. See [WEBFONT_USAGE.md](docs/WEBFONT_USAGE.md) for more details, or use the snippets below to quickly include Hack via a CDN (thanks to the generous gang at [jsDelivr](https://github.com/jsdelivr/jsdelivr)). **Bold** and _italic_ styles are included by default and work out-of-the-box via the `<strong>` and `<em>` tags.

**&lt;head&gt; Section of HTML file**

```html
<link rel="stylesheet" href="//cdn.jsdelivr.net/font-hack/2.020/css/hack.min.css">
```
**CSS file**

```css
code { font-family: Hack, monospace; }
```

### Additional tools for customization

**font-line** is a tool that lets you easily modify the default line spacing of Hack (20% UPM). See the [font-line repository](https://github.com/source-foundry/font-line) for more details, and be sure to check out the [line-spacing directory of the repository](https://github.com/chrissimpkins/Hack/tree/master/tools/line-spacing) for shell scripts that automate the entire process across several commonly used line spacing defaults.

---

## Overview of features

- **Typeface Name**: Hack
- **Category**: Monospaced
- **Powerline Support**: Yes
- **Number of Glyphs**: 1561
- **Included Glyph Sets**: ASCII, etc. **TODO**
- **Included Styles**: Regular, Bold, Italic, Bold Italic
- **Latest Release**: v2.020 (2016-04-29)

---

### License

**Hack** &copy; 2015-2016, Christopher Simpkins (with Reserved Font Name _Hack_)<br>
**Bitstream Vera Sans Mono** &copy; 2003 Bitstream, Inc. (with Reserved Font Names _Bitstream_ and _Vera_)

<!--
**Hack** &copy; 2015-2016, Christopher Simpkins with Reserved Font Name Hack.<br>
Hack Open Font License &amp; Bitstream Vera License

**Bitstream Vera Sans Mono** &copy; 2003 Bitstream, Inc. with Reserved Font Names Bitstream and Vera<br>
Bitstream Vera License
-->

See [LICENSE.md](https://github.com/chrissimpkins/Hack/blob/master/LICENSE.md) for the full texts of the licenses.

[otf_latest]: https://github.com/chrissimpkins/Hack/releases/download/v2.020/Hack-v2_020-otf.zip
[ttf_latest]: https://github.com/chrissimpkins/Hack/releases/download/v2.020/Hack-v2_020-ttf.zip
