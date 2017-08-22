build: source/*.ufo
	./build.sh

build-with-dependencies: source/*.ufo
	./build.sh --install-dependencies

lint: shellcheck ufolint

shellcheck: build.sh
	$@ $^

ufolint: source/*.ufo
	$@ $^
