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
    return extract_numbers(line)

data = read_file('2018/10/data.txt').splitlines()
parsed = [parse_line(x) for x in data]

points = []

cp = [list(x) for x in parsed]

mx = 100000
my = 100000
mi = 0
for i in range(0, 10158+1):
    for p in cp:
        p[0] += p[2]
        p[1] += p[3]

    minx = min(map(lambda x: x[0], cp))
    maxx = max(map(lambda x: x[0], cp))
    miny = min(map(lambda x: x[1], cp))
    maxy = max(map(lambda x: x[1], cp))
    dx = maxx - minx
    dy = maxy - miny
    if dy < my:
        my = dy
        mx = dx
        mi = i

print(mi, mx, my)

minx = min(map(lambda x: x[0], cp))
miny = min(map(lambda x: x[1], cp))
board = np.zeros((mx+1, my+1))
for r in cp:
    x = r[0]-minx
    y = r[1]-miny
    board[x, y] = 1

for y in range(board.shape[1]):
    for x in range(board.shape[0]):
        if board[x, y] > 0:
            print('#', end='')
        else:
            print('.', end='')
    print()
