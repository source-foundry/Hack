build: source/*.ufo
	./build.sh
	./build-woff.sh
	./build-woff2.sh

build-with-dependencies: source/*.ufo build/ttf/*.ttf
	./build.sh --install-dependencies
	./build-woff.sh --install-dependencies
	./build-woff2.sh --install-dependencies

lint: shellcheck ufolint

shellcheck: build.sh build-woff.sh build-woff2.sh
	$@ $^

ufolint: source/*.ufo
	$@ $^
