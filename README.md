
# Hack

[![Build Status](https://travis-ci.org/source-foundry/Hack.svg?branch=master)](https://travis-ci.org/source-foundry/Hack) [![Contributors](https://img.shields.io/badge/contributors-106-orange.svg?style=flat)](https://github.com/chrissimpkins/Hack/blob/master/docs/CONTRIBUTORS.md)

### A typeface designed for source code

Hack is designed to be a workhorse typeface for code. It has deep roots in the libre, open source typeface community and expands upon the contributions of the [Bitstream Vera](https://www.gnome.org/fonts/) &amp; [DejaVu](http://dejavu-fonts.org/wiki/Main_Page) projects.  The project is in active development.  We welcome your input and contributions.

### Contents

* [Quick installation](#user-content-quick-installation)
* [Package manager installation](#user-content-package-managers)
* [Web font usage](#user-content-web-font-usage)
* [Additional tools for customization](#additional-tools-for-hack-font-customization)
* [Overview of features](#user-content-overview-of-features)
* [Resources](#user-content-resources)
* [License](#user-content-license)

The font binaries are released under a license that permits unlimited print, desktop, and web use for commercial and non-commercial applications. For additional details about licensing, please see [LICENSE.md](LICENSE.md).

<a href="https://sourcefoundry.org/hack/"><img src="img/hack-specimen-2.png" alt="Hack &mdash; a typeface designed for source code" width="728"></a>

## Quick installation

**NOTE ON FONT UPDATES**
*If you are updating your version of Hack, be sure to remove the previously installed version and clear your font cache first to avoid conflicts that can lead to platform-specific rendering errors.  Many platforms/distros offer package managers that automate this process. We release a Windows installer to automate the install/update process on the Windows platform. See below for additional details.*

#### Mac OS X and Linux

1. Download the [latest version of Hack][ttf_latest].
2. Extract the files from the archive (`.zip`) and click to open them.
3. Follow the instructions from your operating system.
4. Enjoy!

#### Windows

To simplify the installation process on Windows systems, we've created the [Hack Windows Installer](https://github.com/source-foundry/Hack-windows-installer/releases/latest) which will guide you through the installation process. This installer addresses a number of common rendering issues that occur with font installs/updates on the Windows platform and is the recommended approach for Windows users.

#### Chrome/ChromeOS

To use with [Secure Shell](https://chrome.google.com/webstore/detail/secure-shell/pnhechapfaindjhompbnflcldabbghjo),
edit the following fields in Options:

  - font-family: `"Hack"`
  - user-css: `https://cdn.jsdelivr.net/font-hack/2.020/css/hack-extended.min.css`

#### Font release recommendations

For general screen use on the desktop, we recommend the [TTF builds][ttf_latest] of Hack for most users.  [OTF builds][otf_latest] are available for those who prefer this font format. For detailed installation instructions, see [INSTALLATION.md](docs/INSTALLATION.md).


## Package managers

We highly recommend the convenience of a community developed package manager or other auto-updating utility if this is available on your platform. While the package manager releases may be a bit delayed relative to the repository releases, the package managers were designed to tune and automate font installs and updates on your system.

We are aware of Hack support in the following package managers (with associated package names):

- **Arch Linux**: `ttf-hack`
- **Chocolatey (Windows)**: `hackfont`
- **Debian**: `fonts-hack-ttf`
- **Fedora / CentOS**: `dnf-plugins-core :: heliocastro/hack-fonts :: hack-fonts`
- **Gentoo Linux**: `media-fonts/hack`
- **Homebrew Cask (OS X)**: `caskroom/fonts/font-hack`
- **OpenSUSE**: `hack-fonts`
- **Ubuntu**: `fonts-hack-ttf`
- **Visual Studio Package Manager**: `hack.font`

Details on package manager use and advanced manual desktop installation options can be found in [INSTALLATION.md](docs/INSTALLATION.md).

## Web font usage

Hack is available in all commonly used web font formats. See [WEBFONT_USAGE.md](docs/WEBFONT_USAGE.md) for more details, or use the snippets below to quickly include Hack via a CDN (thanks to the generous gang at [jsDelivr](https://github.com/jsdelivr/jsdelivr)). **Bold** and *italic* styles are included by default and work out-of-the-box via the `<strong>` and `<em>` tags.

#### 1. Add Hack to HTML

Include one of the following in the &lt;head&gt; section of your HTML file:

**Basic Latin + Latin-1 Supplement Character Set Character Set**

```html
<link rel="stylesheet" href="//cdn.jsdelivr.net/font-hack/2.020/css/hack.min.css">
```

**Full Character Set**

```html
<link rel="stylesheet" href="//cdn.jsdelivr.net/font-hack/2.020/css/hack-extended.min.css">
```

#### 2. Add Hack to CSS


```css
pre, code { font-family: Hack, monospace; }
```

## Additional tools for Hack font customization

### Line Spacing Adjustments

**font-line** is a tool that lets you easily modify the default line spacing of Hack (20% UPM). See the [font-line repository](https://github.com/source-foundry/font-line) for more details, and be sure to check out the [line-spacing directory of the repository](https://github.com/chrissimpkins/Hack/tree/master/tools/line-spacing) for shell scripts that automate the entire process across several commonly used line spacing defaults.

## Overview of features

- **Typeface Name**: Hack
- **Category**: Monospaced
- **Powerline Support**: Yes
- **Number of Glyphs**: 1561
- **Included Styles**: Regular, Bold, Italic, Bold Italic
- **Latest Release**: v2.020

## Resources
* [About Hack](docs/ABOUT.md)
* [Full specimen](http://chrissimpkins.github.io/Hack/font-specimen.html)
* [Changelog](CHANGELOG.md)
* [Project website](http://sourcefoundry.org/hack/)
* [Contributors](docs/CONTRIBUTORS.md)


## License

**Hack** &copy; 2015-2017, Christopher Simpkins (with Reserved Font Name _Hack_).

**Bitstream Vera Sans Mono** &copy; 2003 Bitstream, Inc. (with Reserved Font Names _Bitstream_ and _Vera_).

See [LICENSE.md](https://github.com/chrissimpkins/Hack/blob/master/LICENSE.md) for the full texts of the licenses.



<!-- THE FOLLOWING LINKS ARE ALSO USED IN INSTALLATION.MD -->

[otf_latest]: https://github.com/chrissimpkins/Hack/releases/download/v2.020/Hack-v2_020-otf.zip
[ttf_latest]: https://github.com/chrissimpkins/Hack/releases/download/v2.020/Hack-v2_020-ttf.zip
