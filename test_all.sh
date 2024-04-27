#!/bin/bash

set -euo pipefail

MAX_YEAR=${MAX_YEAR:-2023}

if [ $# -ne 1 ]; then
    echo "Usage: ./test_all.sh <LANG>"
    exit 1
fi

_lang=$1

for _year in $(seq 2015 "$MAX_YEAR"); do
    for _day in $(seq 1 25); do
        _day=$(printf "%02d" "$_day")
        ./run.sh test "$_lang" "$_year" "$_day"
    done
done
