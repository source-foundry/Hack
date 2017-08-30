default: build

build: ttf webfonts

build-with-dependencies: source/*.ufo
	./build-ttf.sh --install-dependencies
	./build-woff.sh --install-dependencies
	./build-woff2.sh --install-dependencies
	./build-subsets.sh

lint: shellcheck ufolint

shellcheck: build-ttf.sh build-woff.sh build-woff2.sh build-subsets.sh tools/scripts/install/ttfautohint-build.sh
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
