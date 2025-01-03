from functools import cache

import common

lines = common.read_file().splitlines()

# part 1 and 2
# NOTE: a lot of trial and error
# some paths are likely in the wrong order (only the first one matters for solution)
# I got mine by reversing the pair that occur in my input and checking if that lowers the calculated result
# this means, that there are a lot of pairs in the wrong order
Paths = dict[str, dict[str, list[str]]]
numpad_paths: Paths = {
    "7": {
        "7": [""],
        "8": [">"],
        "9": [">>"],
        "4": ["v"],
        "5": ["v>", ">v"],
        "6": ["v>>", ">>v"],
        "1": ["vv"],
        "2": [">vv", "vv>"],
        "3": [">>vv", "vv>>"],
        "0": [">vvv"],
        "A": [">>vvv"],
    },
    "8": {
        "7": ["<"],
        "8": [""],
        "9": [">"],
        "4": ["v<", "<v"],
        "5": ["v"],
        "6": ["v>", ">v"],
        "1": ["vv<", "<vv"],
        "2": ["vv"],
        "3": ["vv>", ">vv"],
        "0": ["vvv"],
        "A": ["vvv>", ">vvv"],
    },
    "9": {
        "7": ["<<"],
        "8": ["<"],
        "9": [""],
        "4": ["v<<", "<<v"],
        "5": ["v<", "<v"],
        "6": ["v"],
        "1": ["vv<<", "<<vv"],
        "2": ["vv<", "<vv"],
        "3": ["vv"],
        "0": ["vvv<", "<vvv"],
        "A": ["vvv"],
    },
    "4": {
        "7": ["^"],
        "8": ["^>", ">^"],
        "9": ["^>>", ">>^"],
        "4": [""],
        "5": [">"],
        "6": [">>"],
        "1": ["v"],
        "2": ["v>", ">v"],
        "3": ["v>>", ">>v"],
        "0": [">vv"],
        "A": [">>vv"],
    },
    "5": {
        "7": ["<^", "^<"],
        "8": ["^"],
        "9": ["^>", ">^"],
        "4": ["<"],
        "5": [""],
        "6": [">"],
        "1": ["v<", "<v"],
        "2": ["v"],
        "3": ["v>", ">v"],
        "0": ["vv"],
        "A": ["vv>", ">vv"],
    },
    "6": {
        "7": ["<<^", "^<<"],
        "8": ["^<", "<^"],
        "9": ["^"],
        "4": ["<<"],
        "5": ["<"],
        "6": [""],
        "1": ["v<<", "<<v"],
        "2": ["v<", "<v"],
        "3": ["v"],
        "0": ["vv<", "<vv"],
        "A": ["vv"],
    },
    "1": {
        "7": ["^^"],
        "8": ["^^>", ">^^"],
        "9": ["^^>>", ">>^^"],
        "4": ["^"],
        "5": ["^>", ">^"],
        "6": ["^>>", ">>^"],
        "1": [""],
        "2": [">"],
        "3": [">>"],
        "0": [">v"],
        "A": [">>v"],
    },
    "2": {
        "7": ["^^<", "<^^"],
        "8": ["^^"],
        "9": ["^^>", ">^^"],
        "4": ["^<", "<^"],
        "5": ["^"],
        "6": ["^>", ">^"],
        "1": ["<"],
        "2": [""],
        "3": [">"],
        "0": ["v"],
        "A": ["v>", ">v"],
    },
    "3": {
        "7": ["^^<<", "<<^^"],
        "8": ["<^^", "^^<"],
        "9": ["^^"],
        "4": ["^<<", "<<^"],
        "5": ["^<", "<^"],
        "6": ["^"],
        "1": ["<<"],
        "2": ["<"],
        "3": [""],
        "0": ["v<", "<v"],
        "A": ["v"],
    },
    "0": {
        "7": ["^^^<"],
        "8": ["^^^"],
        "9": ["^^^>", ">^^^"],
        "4": ["^^<"],
        "5": ["^^"],
        "6": ["^^>", ">^^"],
        "1": ["^<"],
        "2": ["^"],
        "3": ["^>", ">^"],
        "0": [""],
        "A": [">"],
    },
    "A": {
        "7": ["^^^<<"],
        "8": ["<^^^", "^^^<"],
        "9": ["^^^"],
        "4": ["^^<<"],
        "5": ["<^^", "^^<"],
        "6": ["^^"],
        "1": ["^<<"],
        "2": ["^<", "<^"],
        "3": ["^"],
        "0": ["<"],
        "A": [""],
    },
}
dirpad_paths: Paths = {
    "^": {
        "^": [""],
        "A": [">"],
        "<": ["v<"],
        "v": ["v"],
        ">": ["v>", ">v"],
    },
    "A": {
        "^": ["<"],
        "A": [""],
        "<": ["v<<"],
        "v": ["<v", "v<"],
        ">": ["v"],
    },
    "<": {
        "^": [">^"],
        "A": [">>^"],
        "<": [""],
        "v": [">"],
        ">": [">>"],
    },
    "v": {
        "^": ["^"],
        "A": ["^>", ">^"],
        "<": ["<"],
        "v": [""],
        ">": [">"],
    },
    ">": {
        "^": ["<^", "^<"],
        "A": ["^"],
        "<": ["<<"],
        "v": ["<"],
        ">": [""],
    },
}


@cache
def calc_steps(fro: str, to: str, depth: int) -> int:
    assert depth > 0
    path = dirpad_paths[fro][to][0] + "A"
    if depth == 1:
        return len(path)
    acc = 0
    prev = "A"
    for c in path:
        acc += calc_steps(prev, c, depth - 1)
        prev = c
    return acc


def solve(in_between_robots: int):
    acc = 0
    for line in lines:
        curr = ""
        prev = "A"
        for c in line:
            curr += numpad_paths[prev][c][0]
            curr += "A"
            prev = c
        curr_steps = 0
        prev = "A"
        for c in curr:
            curr_steps += calc_steps(prev, c, in_between_robots)
            prev = c
        as_num = int(line[:-1])
        acc += as_num * curr_steps
    print(acc)


solve(2)
solve(25)
