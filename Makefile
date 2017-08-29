build: source/*.ufo build/ttf/*.ttf
	./build-ttf.sh
	./build-woff.sh
	./build-woff2.sh

build-with-dependencies: source/*.ufo build/ttf/*.ttf
	./build-ttf.sh --install-dependencies
	./build-woff.sh --install-dependencies
	./build-woff2.sh --install-dependencies

lint: shellcheck ufolint

shellcheck: build-ttf.sh build-woff.sh build-woff2.sh tools/scripts/install/ttfautohint-build.sh
	$@ $^

ufolint: source/*.ufo
	$@ $^
