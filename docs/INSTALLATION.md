# Desktop Installation

Hack is available for download in either [OTF][otf_latest] or [TTF][ttf_latest] formats. The best format and install approach depends on your operating system. If you do not know which format is optimal for your system, the TTF files should be used as your default.

Because Hack is under active development and updates are released frequently we highly recommended using a package manager or other auto-updating utility.  While the package manager releases may be a bit delayed relative to the repository releases, the package managers automate and simplify font updates on your system.  Please note that the Hack packages in these package managers are not maintained by the Hack project developers.  If you come across a problem with the release schedule in your package manager, please report it directly to the respective package maintainer on your platform.

## OS X

The easiest way to install and update Hack on OS X is to use the [Homebrew](http://brew.sh/) package manager. To install the fonts on OS X use the command:

    $ brew cask install caskroom/fonts/font-hack


**OS X Users Please Note**: There has been a change in the Homebrew-Cask system that requires an update of `brew-cask`.  If you encounter an error during your Hack install attempt, please execute the following command and then install with the above command again:

```
$ brew uninstall --force brew-cask && brew update
```

Please see [issue report #169](https://github.com/chrissimpkins/Hack/issues/169) for additional details.

To install the fonts manually you may use either the [OTF][otf_latest] or [TTF][ttf_latest] formats. Download the zip file and extract it. Double clicking each of the font files will open a preview in [Font Book](https://support.apple.com/en-us/HT201749) and the "Install Font" button will copy the font to the correct system location.

## Linux / BSD

Most Linux and BSD systems can handle either [TTF][ttf_latest] or [OTF][otf_latest] format fonts. We are aware of package manager support on the following distros:

* *Arch Linux*: install the [ttf-hack](https://www.archlinux.org/packages/community/any/ttf-hack/) package from the community repository ([otf-hack](https://aur.archlinux.org/packages/otf-hack/) is available in the AUR):

        $ pacman -S ttf-hack

* *Fedora / CentOS*: install from [copr](https://copr.fedoraproject.org/coprs/heliocastro/hack-fonts/). For Fedora >= 23:

        $ dnf install dnf-plugins-core
        $ dnf copr enable heliocastro/hack-fonts
        $ dnf install hack-fonts

  For Fedora <= 22 and CentOS <= 7:

        $ yum install yum-plugin-copr
        $ yum copr enable heliocastro/hack-fonts

* *Gentoo Linux*: install the [media-fonts/hack](https://packages.gentoo.org/packages/media-fonts/hack) package from the main Portage tree:

        $ emerge -av media-fonts/hack

* *Ubuntu / Debian*: install either [fonts-hack-ttf](http://packages.ubuntu.com/xenial/fonts-hack-ttf) or [fonts-hack-otf](http://packages.ubuntu.com/xenial/fonts-hack-otf). Packages are currently available for Ubuntu Xenial or later and the Debian unstable branch:

        $ apt-get install fonts-hack-ttf

   For older systems either manually download and install one of the deb packages or see the [manual install instructions](https://wiki.ubuntu.com/Fonts) and [issue report #189](https://github.com/chrissimpkins/Hack/issues/189).

For other systems, check for packages using your distro's package manager search function. If no packages exist download your preferred format and copy the font files to either your system font folder (often `/usr/share/fonts/`) or user font folder (often `~/.local/share/fonts/`). On systems using Fontconfig you may need to regenerate the font caches and indexes after copying the files (e.g. `fc-cache -s; mkfontscale <install_path>; mkfontdir <install_path>`).


## Windows

As of v2.020, we recommend that users of Windows 7 through Windows 10 use the [Hack Windows installer](https://github.com/source-foundry/Hack-windows-installer/releases/latest) to install the Hack fonts. This tool addresses a number of common Windows font installation issues that have led to a wide range of rendering problems for our users.  To view more information about the installer, rationale for its use, the source code, and the VirusTotal report, please see the [Hack Windows Installer repository](https://github.com/source-foundry/Hack-windows-installer).

If you would prefer to install the files manually, we recommend that you use the [TTF][ttf_latest] fonts.  Download the zip archive, extract the files, and double click on the fonts to view them in the font previewer. Click the *Install* button to install them on your system. If you have previously installed the Hack fonts on your system and are having issues with the installation of a newer version, please remove the old Hack fonts before you attempt the new font install. Open `Control Panel`, navigate to `Appearance and Personalization`, then `Fonts`, right click on each of the Hack fonts and delete them. Restart your computer and install the fonts as described above. See [issue report #152](https://github.com/chrissimpkins/Hack/issues/152) and [issue report #177](https://github.com/chrissimpkins/Hack/issues/177) for additional information.

More information about font installation and upgrade issues on the Windows platform is available on the [Font Installation Issues](https://github.com/source-foundry/Hack-windows-installer/blob/master/FontInstallationIssues.md) document in the Hack Windows Installer repository.
