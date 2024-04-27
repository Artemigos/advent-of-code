#!/bin/bash

set -euo pipefail

MIN_YEAR=2015
MAX_YEAR=2023

if [ $# -lt 1 ] || [ $# -gt 2 ]; then
    echo "Usage: ./test_all.sh <LANG> [YEAR]"
    exit 1
fi

if [ $# -eq 2 ]; then
    MIN_YEAR=$2
    MAX_YEAR=$2
fi

_lang=$1
_passed=0
_total=0

for _year in $(seq "$MIN_YEAR" "$MAX_YEAR"); do
    for _day in $(seq 1 25); do
        _total=$((_total + 1))
        _day=$(printf "%02d" "$_day")
        if ./run.sh test "$_lang" "$_year" "$_day"; then
            _passed=$((_passed + 1))
        fi
    done
done

echo "$_passed/$_total passed"
