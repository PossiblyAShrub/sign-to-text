#!/usr/bin/env bash

source ./venv/bin/activate

yapf --parallel --in-place pylint $(git ls-files '*.py')
