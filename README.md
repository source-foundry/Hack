
# Hack  [![Contributors](https://img.shields.io/badge/contributors-104-orange.svg?style=flat)](https://github.com/chrissimpkins/Hack/blob/master/CONTRIBUTORS.md)

### a typeface designed for source code

No frills. No gimmicks. Hack is hand groomed and optically balanced to be a workhorse face for code. It has deep roots in the libre, open source typeface community and expands upon the contributions of the [Bitstream Vera](https://www.gnome.org/fonts/) &amp; [DejaVu](http://dejavu-fonts.org/wiki/Main_Page) projects.

[Read more](docs/ABOUT.md) about Hack, visit the [project website](http://sourcefoundry.org/hack/), take a look at a complete [type specimen](http://chrissimpkins.github.io/Hack/font-specimen.html) or marvel at the [CHANGELOG](CHANGELOG.md).

<a href="https://sourcefoundry.org/hack/"><img src="img/hack-specimen-2.png" alt="Hack &mdash; a typeface designed for source code" width="728"></a>

The font binaries are released under a license that permits unlimited print, desktop, and web use for commercial and non-commercial applications. More details in [LICENSE.md](LICENSE.md)

---

## Quick installation

We recommended using the **TrueType** (`.ttf`) version of Hack. An OpenType (`.otf`) build is available for experienced users.

#### Mac OS X and Linux

1. Download the [latest version of Hack](ttf_latest).
2. Extract the files from the archive (`.zip`) and open them.
3. Follow the instructions from your operating system.
4. Enjoy!

**NOTE ON UPDATING**<br>
If you are updating your version of Hack, be sure to remove the previously installed version first to avoid conflicts. For more information, see [INSTALLATION.md](docs/INSTALLATION.md).

#### Windows

To simplify the installation process on Windows systems, we've created the [Hack Windows Installer](https://github.com/source-foundry/Hack-windows-installer/releases/tag/v1.1.2) (`.exe`) which will guide you through the installation process. The installer will also clean up any previous installation of Hack.

---

## Advanced options

Because Hack is under active development and updates are released frequently, we highly recommended using a package manager or other auto-updating utility. While the package manager releases may be a bit delayed relative to the repository releases, the package managers automate and simplify font updates on your system.

### Package managers and desktop installation

Details on using package managers and/or advanced manual desktop installation options can be found in [INSTALLATION.md](docs/INSTALLATION.md).

Hack can be installed and updated via various package managers. We are aware of package manager support on the following systems/distros:

- **Mac OS X**: `homebrew`
- **Arch Linux**: `pacman`
- **Fedora / CentOS**: `copr`, `dnf` or `yum`
- **Gentoo Linux**: `emerge`
- **Ubuntu / Debian**: `apt-get`

<!-- TODO @chris: no idea if the wording of the above makes any sense for package manager users -->

### Web font usage

Hack is available in all the regular webfont formats. See [WEBFONT_USAGE.md](docs/WEBFONT_USAGE.md) for more details, or use the snippets below to quickly include Hack via a CDN by the generous gang at [jsDelivr](https://github.com/jsdelivr/jsdelivr). **Bold** and _italic_ styles are included by default and work out-of-the-box via the `<strong>` and `<em>` tags.

```html
<link rel="stylesheet" href="//cdn.jsdelivr.net/font-hack/2.020/css/hack.min.css">
```

```css
code {
	font-family: Hack, monospace;
}
```

### Additional tools for customization

**font-line** is a tool that lets you easily modify the default line spacing of Hack. See the [font-line repository](https://github.com/source-foundry/font-line) for more details, and be sure to check out the [line-spacing repository](https://github.com/chrissimpkins/Hack/tree/master/tools/line-spacing) for some font-line automation.

---

### Overview of features

- **Typeface Name**: Hack
- **Category**: Monospaced
- **Powerline Support**: Yes
- **Number of Glyphs**: 1561
- **Included Glyph Sets**: TODO
- **Included Styles**: Regular, Bold, Italic, Bold Italic
- **Latest Release**: v2.020 (2016-04-29)

---

### License

<!-- TODO Are the two lines with the names of the licences required (since they are also in LICENSE.md)? -->

**Hack** &copy; 2015-2016, Christopher Simpkins (with Reserved Font Name _Hack_)<br>
**Bitstream Vera Sans Mono** &copy; 2003 Bitstream, Inc. (with Reserved Font Names _Bitstream_ and _Vera_)

<!--
**Hack** &copy; 2015-2016, Christopher Simpkins with Reserved Font Name Hack.<br>
Hack Open Font License &amp; Bitstream Vera License

**Bitstream Vera Sans Mono** &copy; 2003 Bitstream, Inc. with Reserved Font Names Bitstream and Vera<br>
Bitstream Vera License
-->

See [LICENSE.md](https://github.com/chrissimpkins/Hack/blob/master/LICENSE.md) for the full texts of these licences.

[otf_latest]: https://github.com/chrissimpkins/Hack/releases/download/v2.020/Hack-v2_020-otf.zip
[ttf_latest]: https://github.com/chrissimpkins/Hack/releases/download/v2.020/Hack-v2_020-ttf.zip
