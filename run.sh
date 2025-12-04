#!/bin/bash

set -euo pipefail

print-help() {
    cat <<EOF
Usage: ./run.sh <MODE> <LANG> <PROBLEM_YEAR> <PROBLEM_DAY>

MODE          mode of operation, can be either run, test or diff
LANG          code language, e.g. python, go
PROBLEM_YEAR  year of the problem, e.g. 2023
PROBLEM_DAY   day of the problem, e.g. 18
EOF
}

run-python() {
    cd python
    local _pycmd=pypy3
    if [ ! -x "$(command -v pypy3)" ]; then
        _pycmd=python3
    fi
    $_pycmd -m "$1.$2.solution" "../$3"
}

run-go() {
    cd go
    go run "aoc/$1/$2" "../$3"
}

run-rust() {
    echo "not implemented"
    exit 1
}

run-zig() {
    local _main=zig/$1/$2/main
    if [[ -x "$_main" ]]; then
        "$_main" "$3"
    else
        zig run "$_main.zig" -- "$3"
    fi
}

build-zig() {
    {
        cd "zig/$1/$2"
        zig build-exe -O ReleaseFast -fllvm main.zig
    }
}

if [ $# != 4 ]; then
    print-help
    exit 1
fi

_mode=$1
_lang=$2
_problem_year=$3
_problem_day=$4

case $_mode in
    run|test|diff|build) ;;
    *) echo "Unknown mode: $_mode"; exit 1 ;;
esac

case $_lang in
    python|go|rust|zig) ;;
    *) echo "Unknown language: $_lang"; exit 1 ;;
esac

_data_file=data/${_problem_year}/${_problem_day}/data.txt
_result_file=data/${_problem_year}/${_problem_day}/result.txt

if [ ! -f "$_data_file" ]; then
    echo "Data file not available"
    exit 1
fi

if [ "$_mode" == "run" ]; then
    "run-$_lang" "$_problem_year" "$_problem_day" "$_data_file"
elif [ "$_mode" == "diff" ]; then
    if [ ! -f "$_result_file" ]; then
        echo "Result file not available"
        exit 1
    fi

    "run-$_lang" "$_problem_year" "$_problem_day" "$_data_file" | diff "$_result_file" -
elif [ "$_mode" == "build" ]; then
    case $_lang in
        zig) ;;
        *) echo "Build not supported for language: $_lang"; exit 1 ;;
    esac

    "build-$_lang" "$_problem_year" "$_problem_day"
else
    if [ ! -f "$_result_file" ]; then
        echo "Result file not available"
        exit 1
    fi

    echo -n "$_problem_year/$_problem_day: "
    "run-$_lang" "$_problem_year" "$_problem_day" "$_data_file" 2>/dev/null | diff "$_result_file" >/dev/null - && echo OK || { echo FAIL; exit 1; }
fi
