import collections as coll
import queue
import itertools
import functools
import numpy as np
import re

def read_file(path: str) -> str:
    with open(path) as f:
        return f.read()

def read_lines(path: str) -> str:
    with open(path) as f:
        return f.read().splitlines()

def extract_words(data: str):
    return re.findall(r'\w+', data)

def extract_numbers(data: str):
    return [int(x) for x in re.findall(r'-?\d+', data)]

def parse_line(line: str):
    segments = line.split(' ')
    return (list(segments[0]), segments[2])

data = read_file('2018/12/data.txt').splitlines()
parsed = [parse_line(x) for x in data]

initial = '..##.#######...##.###...#..#.#.#..#.##.#.##....####..........#..#.######..####.#.#..###.##..##..#..#'
# initial = '#..#.#..##......###...###'

# generations = 20
# generations = 50000000000
generations = 200
size = len(initial)+150
i0 = -50
state = '.'*50+initial+'.'*100
state = list(state)

# dict
st100 = None
st101 = None
st102 = None

for g in range(generations):
    if g == 100:
        st100 = list(state)
    elif g == 101:
        st101 = list(state)
    elif g == 102:
        st102 = list(state)
    new_state = '.'*size
    new_state = list(new_state)
    for i in range(2, len(state)-2):
        for rule in parsed:
            if state[i-2:i+3] == rule[0]:
                new_state[i] = rule[1]
                break
        else:
            new_state[i] = '.'
    state = new_state

print()
mod100 = ['.','.']+st100[:-2]
mod101 = ['.']+st101[:-1]
print(mod100)
print(mod101)
print(st102)
print(mod100 == st102)

acc = 0
for i in range(len(state)):
    if state[i] == '#':
        acc += (i+i0)
print(acc)
