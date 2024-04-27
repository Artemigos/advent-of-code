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

data = read_file('2018/08/data.txt')
parsed = extract_numbers(data)
print(len(parsed))

nodes = []

def read_node(i):
    n_ch = parsed[i]
    n_meta = parsed[i+1]
    curr_i = 2
    childred = []
    for _ in range(n_ch):
        result = read_node(i+curr_i)
        curr_i += result[0]
        childred.append(result)
    meta = parsed[i+curr_i:i+curr_i+n_meta]
    val = sum(meta)
    if len(childred) > 0:
        val = 0
        for x in meta:
            xi = x-1
            if xi < 0 or xi >= len(childred):
                continue
            val += childred[xi][3]
    node = (curr_i+n_meta, childred, meta, val)
    nodes.append(node)
    return node

root = read_node(0)

s = 0
for n in nodes:
    s += sum(n[2])

print(s)
print(root[3])
