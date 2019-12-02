import numpy as np
import queue

depth = 7863
target = 14,760
mod = 20183

size = target[0]*3, target[1]*3
erosions = np.zeros(size)
types = np.zeros(size)

def fill_data(at, geological_index):
    lvl = (geological_index+depth)%mod
    erosions[at] = lvl
    types[at] = lvl%3

fill_data((0, 0), 0)
fill_data(target, 0)

for i in range(1, max(size)):
    if i < size[0]:
        fill_data((i, 0), i*16807)
    if i < size[1]:
        fill_data((0, i), i*48271)

for y in range(1, size[1]):
    for x in range(1, size[0]):
        lvl = erosions[x-1, y]*erosions[x, y-1]
        fill_data((x, y), lvl)

danger = int(np.sum(types[:target[0]+1, :target[1]+1]))
print(danger)

# part 2
# tools
NEITHER = 0
GEAR = 1
TORCH = 2
# types
ROCKY = 0
WET = 1
NARROW = 2

def can_go(at, tool):
    x, y = at
    if x < 0 or y < 0:
        return False
    if x >= size[0] or y >= size[1]:
        return False
    t = types[at]
    if t == ROCKY:
        return tool == GEAR or tool == TORCH
    elif t == WET:
        return tool == NEITHER or tool == GEAR
    else:
        return tool == NEITHER or tool == TORCH

def tool_switch(at, tool):
    t = types[at]
    if t == ROCKY:
        return GEAR if tool == TORCH else TORCH
    elif t == WET:
        return NEITHER if tool == GEAR else GEAR
    else:
        return NEITHER if tool == TORCH else TORCH

def neighbors(at):
    x, y = at
    yield x, y-1
    yield x-1, y
    yield x+1, y
    yield x, y+1

q = queue.PriorityQueue()
q.put((0, (0, 0), TORCH))
seen = set()

while not q.empty():
    time, at, tool = q.get()
    if at == target and tool == TORCH:
        print(time)
        break
    if (at, tool) in seen:
        continue
    seen.add((at, tool))
    if not can_go(at, tool):
        continue
    # movements
    for n in neighbors(at):
        q.put((time+1, n, tool))
    # tool switch
    new_tool = tool_switch(at, tool)
    q.put((time+7, at, new_tool))
