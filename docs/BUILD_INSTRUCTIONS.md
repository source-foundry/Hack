# How to build Hack from source

To build Hack from the UFO source files, you need the following build application dependencies:

- [fontTools](https://github.com/fonttools/fonttools) - must be able to import into a Python module
- [fontmake](https://github.com/googlei18n/fontmake) - must be accessible as a PATH executable
- [ttfautohint](https://www.freetype.org/ttfautohint/) (Version 1.6+) - may be installed in a temporary local directory (see below) or installed on PATH

## Build Dependency Management

### Install the dependencies

You can install all necessary build dependencies with our build.sh script and the `--install-dependencies` flag.  This script is found in the root of the Hack repository.  Clone the Hack repository to your system with the following command:

```
$ git clone https://github.com/source-foundry/Hack.git
```

Navigate to the root of the Hack repository with:

```
$ cd Hack
```

and excecute the following command:

```
$ ./build.sh --install-dependencies
```

The execution of this script with the `--install-dependencies` flag installs all build dependencies and builds the ttf fonts from source to final compiled ttf fonts that are intended for end users.  These build files can be found in the repository on the path `build/ttf/`.

### How dependencies are installed

- The Python fontTools library is installed with `pip install fonttools`.
- The Python fontmake executable is installed with `pip install fontmake`.
- ttfautohint and its build dependencies are installed locally on the path `$HOME/ttfautohint-build`.  The ttfautohint executable is found on the path `$HOME/ttfautohint-build/local/bin/ttfautohint`.


### How to remove installed build dependencies

If you are not setting up a development environment that requires repeat builds (e.g. to make changes, test, and contribute back upstream or to create a new Hack fork project), you can remove the build dependencies with the following set of commands:

```
$ pip uninstall fonttools
$ pip uninstall fontmake
$ rm -rf "$HOME/ttfautohint-build"
```

## Build Hack fonts

If your system already meets all build dependency requirements, you can build without the dependency install step by navigating to the root of the Hack repository and executing the command:

```
$ ./build.sh
```
