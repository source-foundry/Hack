all: build

archives:
	postbuild_processing/archive_prep/archiver.sh

build: ttf webfonts

build-with-dependencies: source/*.ufo
	./build-ttf.sh --install-dependencies
	./build-woff.sh --install-dependencies
	./build-woff2.sh --install-dependencies
	./build-subsets.sh

css:
	tools/scripts/css/css-build.sh

lint: shellcheck ufolint

shellcheck: build-ttf.sh build-woff.sh build-woff2.sh build-subsets.sh tools/scripts/install/ttfautohint-build.sh postbuild_processing/archive_prep/archiver.sh tools/scripts/css/css-build.sh
	$@ $^

subsets: source/*.ufo
	./build-subsets.sh

ttf:
	./build-ttf.sh

ufolint: source/*.ufo
	$@ $^

webfonts:
	./build-woff.sh
	./build-woff2.sh
	./build-subsets.sh

woff:
	./build-woff.sh

woff2:
	./build-woff2.sh
