all: build

archives:
	./build-archives.sh

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

css:
	tools/scripts/css/css-build.sh

lint: shellcheck ufolint

pipenv:
	./build-pipenv.sh

shellcheck: *.sh tools/scripts/css/*.sh tools/scripts/install/*.sh
	$@ $^

subsets: pipenv
	./build-subsets.sh

ttf: pipenv
	./build-ttf.sh

ttf-system:
	./build-ttf.sh --system

ufolint: source/*.ufo
	$@ $^

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

.PHONY: all archives build build-with-dependencies build-local-ttfa build-local-sfnt2woffzopfli build-local-woff2 build-system compile-local-dep css lint pipenv shellcheck subsets ttf ttf-system ufolint webfonts webfonts-system woff woff-system woff2 woff2-system
