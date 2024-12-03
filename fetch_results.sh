#!/bin/bash

set -euo pipefail

_year=${1?year required}

for _day in $(seq 1 25); do
    _day=$(printf "%02d" "$_day")
    _file=data/${_year}/${_day}/result.txt
    echo "Waiting for day $_day... [ENTER]"
    read
    wl-paste >"$_file"
done
