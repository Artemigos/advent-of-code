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
    return extract_words(line)

data = read_lines('2018/07/data.txt')
parsed = [parse_line(x) for x in data]

deps = coll.defaultdict(set)
steps = set()

for row in parsed:
    deps[row[7]].add(row[1])
    steps.add(row[1])
    steps.add(row[7])

available = set()
acc = ''
for s in steps:
    if s not in deps:
        available.add(s)
while len(available) > 0:
    nxt = min(available)
    available.remove(nxt)
    acc += nxt
    for d in deps:
        if nxt in deps[d]:
            for dd in deps[d]:
                if dd not in acc:
                    break
            else:
                available.add(d)

print(acc)


workers = queue.PriorityQueue()
for i in range(5):
    workers.put(0)

available = queue.PriorityQueue()
for s in steps:
    if s not in deps:
        available.put((0, s))

acc = ''
while not available.empty():
    when, el = available.get()
    worker = workers.get()
    ready_after = max([when, worker])
    cost = 60
    cost += ord(el[0])-ord('A')+1
    finish = ready_after+cost
    acc += el
    for d in deps:
        if el in deps[d]:
            for dd in deps[d]:
                if dd not in acc:
                    break
            else:
                available.put((finish, d))
    workers.put(finish)

while not workers.empty():
    print('worker finish at', workers.get())
print(acc)
