# Hack Font Builds from Source Files

Hack is compiled from UFO v2 spec source files to ttf, woff, and woff2 fonts with free, open source build tools. The default build approach requires a *nix platform (macOS, Linux, a Unix-like development platform for Windows such as MinGW) and uses pinned build dependency versions to support font files that render reproducibly (relative to upstream repository builds) in a given rendering environment. See the bottom of this document for an alternative approach that uses system-installed versions of all build dependencies and supports build dependency versions that differ from those used in the upstream repository.

## Quickstart
The following commands will do the following:

1. Clone the Hack source repository
2. Install the `pipenv` dependency
3. Compile and install a local version `ttfautohint` (i.e., *off of the system PATH*)
4. Build *.ttf desktop fonts
5. Build *.woff web fonts (including subsets)
6. Build *.woff2 web fonts (including subsets)

**Quickstart Hack font compile process**

```
$ git clone https://github.com/source-foundry/Hack.git
$ cd Hack
$ pip3 install pipenv
$ make compile-local-dep
$ make
```

The build process takes minutes to complete on the average system.  You will see a great deal of text stream by in your terminal during the build.  This text stream is normal and expected during the build.

You will find the compiled fonts in the build directory (located in the top level of the source repository) after you complete these steps.

Detailed instructions follow if you have difficulties with any of the above steps.  If you encounter an error that is not addressed in this build documentation, please report it as a new issue report on the repository.  *Please review the entire build document below to confirm that we have not explained how to address your problem before you submit a new issue report*!

## Contents

- [Build dependency installation](#build-dependencies)
	- [Python interpreter](#python-interpreter-dependency)
	- [ttf desktop font dependencies](#desktop-font-ttf-dependencies)
	- [woff and woff2 web font dependencies](#web-font-woff--woff2-dependencies)
- [Automated font builds with make](#automated-font-builds)
- [Build paths](#build-paths)
- [Uninstall build dependencies](#uninstall-build-dependencies)

## Build dependencies

### Python interpreter dependency

The Hack fonts are built with a Python version 3 interpreter.  The Python interpreter version is fixed at each git commit. You may view the Python interpreter in use at any commit in the Pipfile and Pipfile.lock files that are located in the root directory of the repository.  [Click here](https://sourcegraph.com/search?q=repo:%5Egithub%5C.com/source-foundry/Hack%24%40master+python_version) to search for these values in the current HEAD commit of the master branch.

If this version of the Python interpreter is not available on your development system, you may install [`pyenv`](https://github.com/pyenv/pyenv-installer) before you attempt your build.  If `pyenv` is installed before the build, `pipenv` will automatically install the interpreter defined in the Hack build in the virtual environment used for the build, even if it is not installed on your system.

The pyenv project defines the following command as a supported approach to install `pyenv`:


**Pull and install the pyenv executable**

```
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
```

### Desktop font (ttf) dependencies

To build the Hack desktop fonts (ttf) from source you will need the following build dependencies:

- [pipenv](https://github.com/pypa/pipenv) Python executable
- [fontmake](https://github.com/googlei18n/fontmake) Python executable
- [fonttools](https://github.com/fonttools/fonttools) Python library
- [ttfautohint](https://www.freetype.org/ttfautohint/) executable (includes Harfbuzz and FreeType dependencies)

`fontmake` and `fontTools` are automatically installed during the compile process.

`pipenv` must be installed manually with the following command before you attempt a build:

**Install pipenv**

```
$ pip3 install pipenv
```

`ttfautohint` (including its Harfbuzz and FreeType dependencies) can be installed locally on the path defined for use in Hack builds with the following command:

**Compile and install a local copy of ttfautohint**

```
$ make compile-local-dep
```

This path is defined as the following subdirectory on your $HOME path:

- ttfautohint: `$HOME/ttfautohint-build`

### Web font (woff + woff2) dependencies

To build the Hack web fonts from source you will need all of the build dependencies listed above for desktop font builds and the following additional dependencies:

- [sfnt2woff-zopfli](https://github.com/bramstein/sfnt2woff-zopfli) C++ executable
- [woff2_compress](https://github.com/source-foundry/woff2) C++ executable

The sfnt2woff-zopfli executable and woff2_compress executable are compiled and installed on a local build path (i.e., off of system PATH) with the following command:

**Compile and install local copies of sfnt2woff-zopfli and woff2_compress**

```
$ make compile-local-dep
```

These paths are defined as the following subdirectories on your $HOME path:

- sfnt2woff-zopfli: `$HOME/sfnt2woff-zopfli-build`
- woff2: `$HOME/woff2`

## Automated font builds

After the build dependencies are installed, use make targets from the root of the Hack repository to build font sets.  The following commands build the regular, bold, italic, and bold italic variants of the respective build types:


#### Build all desktop and web fonts (including web font subsets)

```
$ make
```

#### Build ttf desktop fonts only

```
$ make ttf
```

#### Build all web fonts (includes woff, woff2 with character subsets)

```
$ make webfonts
```

#### Build woff web fonts only (complete sets only)

```
$ make woff
```

#### Build woff2 web fonts only (complete sets only)

```
$ make woff2
```


#### Build woff and woff2 subsets only

```
$ make subsets
```

## Build paths

### Desktop fonts (ttf)

Desktop fonts are available on the path `build/ttf` from the root of the repository upon completion of your build.


### Web fonts (woff + woff2)

Web fonts are available on the path `build/web/fonts` from the root of the repository upon completion of your build.  CSS files that may be used with your web font builds are available on the path `build/web`.

## Uninstall build dependencies

Python packages that are used during the build process are installed in a virtual environment with `pipenv`.  The virtual environment and all Python packages installed in that environment can be eliminated with the execution of the following command in the root of the repository:

```
$ pipenv -rm
```

All compiled project build dependencies installed as part of this build process can be uninstalled with the following commands:

```
$ rm -rf ~/ttfautohint-build
$ rm -rf ~/sfnt2woff-zopfli-build
$ rm -rf ~/woff2
```

In cases where a compile did not proceed to completion (e.g., you intentionally exited early, or an exception was raised that led to an early termination of the build), a temporary directory may still exist in the root of the repository on the path `master_ttf`.  This directory can be removed with:

```
$ rm -rf master_ttf
```

## Compile with system PATH installed build dependencies

The following make targets are available for those who would like to build with system PATH installed versions of all build dependencies.  This approach allows you build with dependency versions that differ from those used in the upstream project.  Please see the note at the bottom of this section for caveats to this approach.

#### System PATH build dependency compiles of all fonts

```
$ make build-system
```

#### System PATH build dependency compiles of desktop fonts

```
$ make ttf-system
```

#### System PATH build dependency compiles of all web fonts

```
$ make webfonts-system
```

#### System PATH build dependency compiles of woff web fonts

```
$ make woff-system
```

#### System PATH build dependency compiles of woff web fonts

```
$ make woff2-system
```

You must install all build dependencies before use of these make targets.  Please refer to the documentation for the respective build dependency projects for details about installations.  While we release these system PATH installed compile make targets to simplify the approach to builds for users who prefer not to (or cannot) create a development environment that matches the one used for our upstream builds, this approach is not otherwise supported or tested in this repository.  Please understand this caveat if you intend to release fonts built with this approach in a production environment as differences in the build dependency versions can alter font renders.
