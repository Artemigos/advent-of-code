#!/bin/bash

set -euo pipefail

MAX_YEAR=${MAX_YEAR:-2023}

if [ $# -ne 1 ]; then
    echo "Usage: ./test_all.sh <LANG>"
    exit 1
fi

_lang=$1
_passed=0
_total=0

for _year in $(seq 2015 "$MAX_YEAR"); do
    for _day in $(seq 1 25); do
        _total=$((_total + 1))
        _day=$(printf "%02d" "$_day")
        if ./run.sh test "$_lang" "$_year" "$_day"; then
            _passed=$((_passed + 1))
        fi
    done
done

echo "$_passed/$_total passed"
