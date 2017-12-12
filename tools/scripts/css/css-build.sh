#!/bin/sh

#######################################
# Copyright 2017 Christopher Simpkins
# MIT License
#######################################

# This script builds the Hack web font CSS files from CSS file templates
#  by adding a git commit sha1 stamp to the URL string

# Dependency:
#  Ink - https://github.com/chrissimpkins/ink (Go text templating application)
#      - install with `go get github.com/chrissimpkins/ink`

# Usage:
#  execute script from root of Hack repository with make using the following:
#      $ make css


ink --replace="$(git log --pretty=format:'%h' --abbrev-commit -1)" build/web/hack.css.in build/web/hack-subset.css.in
