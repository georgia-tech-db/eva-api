#!/bin/sh

# This script should return a non-zero value if either
# linter fails or the pytest fails. This is important for the Travis.

# Run linter (checks code style)
pip install flake8
pip install coverage
flake8 --select E,F src/ test/ --exclude src/filters,src/parser/evaql
linter_code=$?
# Run unit tests
coverage run -m unittest discover ./test
test_code=$?
if [ $linter_code -ne 0 ];
then
    exit $linter_code
else
    exit $test_code
fi