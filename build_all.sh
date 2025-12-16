#!/bin/bash

set -euo pipefail

MIN_YEAR=2015
MAX_YEAR=2025

if [ $# -lt 1 ] || [ $# -gt 2 ]; then
    echo "Usage: ./build_all.sh <LANG> [YEAR]"
    exit 1
fi

source './year_maxes.sh'

if [ $# -eq 2 ]; then
    MIN_YEAR=$2
    MAX_YEAR=$2
fi

_lang=$1

for _year in $(seq "$MIN_YEAR" "$MAX_YEAR"); do
    for _day in $(seq 1 "${year_maxes[$_year]}"); do
        _day=$(printf "%02d" "$_day")
        echo "Building $_year/$_day..."
        ./run.sh build "$_lang" "$_year" "$_day"
    done
done
