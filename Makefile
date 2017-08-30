default: build

build: ttf webfonts

build-with-dependencies: source/*.ufo build/ttf/*.ttf
	./build-ttf.sh --install-dependencies
	./build-woff.sh --install-dependencies
	./build-woff2.sh --install-dependencies
	./build-subsets.sh

lint: shellcheck ufolint

shellcheck: build-ttf.sh build-woff.sh build-woff2.sh build-subsets.sh tools/scripts/install/ttfautohint-build.sh
	$@ $^

ttf: source/*.ufo
	./build-ttf.sh

ufolint: source/*.ufo
	$@ $^

webfonts: source/*.ufo build/ttf/*.ttf
	./build-woff.sh
	./build-woff2.sh
	./build-subsets.sh

woff: build/ttf/*.ttf
	./build-woff.sh

woff2: build/ttf/*.ttf
	./build-woff2.sh
