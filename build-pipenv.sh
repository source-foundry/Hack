#!/bin/sh

# /////////////////////////////////////////////////////////////////
#
# build-pipenv.sh
#  A shell script that creates a virtualenv for Hack font builds
#  Copyright 2018 Christopher Simpkins
#  MIT License
#
#  Usage: ./build-pipenv.sh
#
# /////////////////////////////////////////////////////////////////

if ! which pipenv
	then
		echo "Unable to detect a pipenv install.  Please install with 'pip install pipenv' then repeat your build attempt." 1>&2
		exit 1
fi

# install fontTools and fontmake build dependencies with pipenv
pipenv install --ignore-pipfile fontmake fontTools

# test for fontmake install in venv
if ! pipenv run fontmake --version
	then
		echo "Unable to detect fontmake install with pipenv.  Please repeat your build attempt." 1>&2
		exit 1
fi

# test for fontTools install in venv
if ! pipenv run python -c "import fontTools"
	then
		echo "Unable to detect fontTools install with pipenv.  Please repeat your build attempt." 1>&2
		exit 1
fi

# print environment used for build to std output stream

echo "================================="
echo "  PYTHON BUILD ENVIRONMENT"
echo "================================="
echo " "

pipenv graph

echo " "
echo "================================="
echo "  END PYTHON BUILD ENVIRONMENT"
echo "================================="
echo " "
