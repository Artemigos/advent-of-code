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
    return line

# data = read_file('2018/11/data.txt').splitlines()
# parsed = [parse_line(x) for x in data]

data = 9306
powers = np.zeros((300, 300))

for x in range(1, 301):
    for y in range(1, 301):
        rack_id = x+10
        powa = rack_id*y + data
        powa *= rack_id
        powa %=1000
        powa //= 100
        powa -= 5
        powers[x-1, y-1] = powa

def find_max_pow(sizes):
    maxp = -100000
    maxx=0
    maxy=0
    maxn = 0

    for n in sizes:
        for x in range(300-n+1):
            for y in range(300-n+1):
                p = np.sum(powers[x:x+n, y:y+n])
                if p > maxp:
                    maxp = p
                    maxx = x+1
                    maxy = y+1
                    maxn = n

    return (maxp, maxx, maxy, maxn)

print(find_max_pow([3]))
print(find_max_pow(range(1, 301)))
