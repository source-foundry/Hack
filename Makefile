all: build

# FONT COMPILES

#
# Recommended usage:
#
#     The following targets build *.ttf, *.woff, *.woff2 (including *.woff and *.woff2 subsets):
#
#       `make` - builds fonts with pinned build dependency versions of all Python and local, compiled C/C++ projects
#       `make build-system` - builds fonts with system PATH installed versions of build dependencies
#
#    Dependency installs for default builds with `make` can be executed with:
#
#      1) pip3 install pipenv
#      2) make compile-local-dep
#
#    Optional dependency install for `make` if your development system does not support the defined Python interpreter version:
#
#      3) curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
#

build: ttf webfonts

build-with-dependencies: compile-local-dep ttf webfonts

build-system: ttf-system webfonts-system

build-local-ttfa:
	tools/scripts/install/ttfautohint-build.sh

build-local-sfnt2woffzopfli:
	tools/scripts/install/sfnt2woff-zopfli-build.sh

build-local-woff2:
	tools/scripts/install/woff2-compress-build.sh

compile-local-dep: build-local-ttfa build-local-sfnt2woffzopfli build-local-woff2

pipenv:
	./build-pipenv.sh

subsets: pipenv
	./build-subsets.sh

subsets-system:
	./build-subsets.sh --system

ttf: pipenv
	./build-ttf.sh

ttf-system:
	./build-ttf.sh --system

webfonts: woff woff2 subsets

webfonts-system: woff-system woff2-system subsets-system

woff: pipenv
	./build-woff.sh

woff-system:
	./build-woff.sh --system

woff2: pipenv
	./build-woff2.sh

woff2-system:
	./build-woff2.sh --system


# RELEASE PREP

archives:
	./build-archives.sh

css:
	tools/scripts/css/css-build.sh


# TESTING

lint: shellcheck ufolint

shellcheck: *.sh tools/scripts/css/*.sh tools/scripts/install/*.sh
	$@ $^

ufolint: source/*.ufo
	$@ $^


# PHONY TARGETS

.PHONY: all archives build build-with-dependencies build-local-ttfa build-local-sfnt2woffzopfli build-local-woff2 build-system compile-local-dep css lint pipenv shellcheck subsets subsets-system ttf ttf-system ufolint webfonts webfonts-system woff woff-system woff2 woff2-system
