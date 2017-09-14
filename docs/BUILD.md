## Build dependencies

Hack is compiled from UFO v2 spec source files to ttf, woff, and woff2 fonts with free, open source build tools.  You can either install the tools manually or use the automated build dependency installation approach documented below.

### Desktop font (ttf) build dependencies

To build the Hack desktop fonts (ttf) from source you will need the following build dependencies:

- [fontmake](https://github.com/fonttools/fonttools) Python executable
- [fonttools](https://github.com/googlei18n/fontmake) Python library
- [ttfautohint](https://www.freetype.org/ttfautohint/) executable (includes Harfbuzz and FreeType dependencies)

### Web font (woff + woff2) build dependencies

To build the Hack web fonts from source you will need all of the build dependencies listed above for desktop font builds.  In addition you will need the following dependencies for the web font build steps:

- [sfnt2woff-zopfli](https://github.com/bramstein/sfnt2woff-zopfli) C++ executable
- [woff2_compress](https://github.com/source-foundry/woff2) C++ executable


### Automated build dependency installation

Install all build dependencies for desktop and web fonts with the following make command:

```
$ make build-with-dependencies
```

This will install all necessary build dependencies and complete a build of all desktop and web fonts.


## Automated font builds

After the build dependencies are installed, use make targets from the root of the Hack repository to build font sets.


#### Build all desktop and web fonts (including web font subsets)

```
$ make
```

#### Build ttf desktop fonts

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

Web fonts are available on the path `build/web` from the root of the repository upon completion of your build.
