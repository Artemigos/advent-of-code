#!/bin/bash

set -euo pipefail

_year=${1?year required}

for _day in $(seq 1 24); do
    _day=$(printf "%02d" "$_day")
    _file=data/${_year}/${_day}/result.txt
    echo "Waiting for day $_day part 1..."
    clipnotify && xclip -o >"$_file"
    echo >>"$_file"
    echo "Waiting for day $_day part 2..."
    clipnotify && xclip -o >>"$_file"
    echo >>"$_file"
done

_day=25
_file=data/${_year}/${_day}/result.txt
echo "Waiting for day $_day part 1..."
clipnotify && xclip -o >"$_file"
echo >>"$_file"
