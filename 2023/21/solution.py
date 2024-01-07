from functools import cache
import math
from typing import Optional

import common
from collections import deque

board = common.read_file().splitlines()
w = len(board[0])
h = len(board)
steps = 6 if common.is_sample_data() else 64
start = (0, 0)

for y in range(h):
    for x in range(w):
        if board[y][x] == 'S':
            start = (x, y)
            board[y] = board[y].replace('S', '.')
            break
    else:
        continue
    break

# part 1
at_steps: set[tuple[int, int]] = set()
seen: set[tuple[int, int, int]] = set()
q: deque[tuple[int, int, int]] = deque()
q.append((0, start[0], start[1]))
while len(q) > 0:
    depth, x, y = q.popleft()
    if x < 0 or y < 0 or x >= w or y >= h:
        continue
    if board[y][x] == '#':
        continue
    if (depth, x, y) in seen:
        continue
    seen.add((depth, x, y))
    if depth == steps:
        at_steps.add((x, y))
        continue
    q.append((depth+1, x-1, y))
    q.append((depth+1, x+1, y))
    q.append((depth+1, x, y-1))
    q.append((depth+1, x, y+1))

print(len(at_steps))

# part 2
# NOTE: taking advantage of the fact that maps' outside ring is all dots
assert w == h
steps = 5000 if common.is_sample_data() else 26501365
step_parity = steps % 2
distances_covered = steps // w

# find all walkable tiles
tl = tr = bl = br = 0
walkable: set[tuple[int, int]] = set()
q = deque()
q.append((0, start[0], start[1]))
while len(q) > 0:
    depth, x, y = q.popleft()
    if x < 0 or y < 0 or x >= w or y >= h:
        continue
    if board[y][x] == '#':
        continue
    if (x, y) in walkable:
        continue
    walkable.add((x, y))
    if (x, y) == (0, 0):
        tl = depth
    elif (x, y) == (w-1, 0):
        tr = depth
    elif (x, y) == (0, h-1):
        bl = depth
    elif (x, y) == (w-1, h-1):
        br = depth
    q.append((depth+1, x-1, y))
    q.append((depth+1, x+1, y))
    q.append((depth+1, x, y-1))
    q.append((depth+1, x, y+1))

# figure out how many spots get covered if tile is covered entirely
curr_parity_block: set[tuple[int, int]] = set()
curr_parity = (start[0]+start[1])%2
for p in walkable:
    x, y = p
    if (x+y)%2 == curr_parity:
        curr_parity_block.add((x, y))
if w % 2 == 0:
    other_parity_block = curr_parity_block
else:
    other_parity_block = walkable.difference(curr_parity_block)

curr_parity_block_covers = len(curr_parity_block)
other_parity_block_covers = len(other_parity_block)

# create distance maps from corners
def get_distances(fx: int, fy: int) -> list[list[Optional[int]]]:
    distances: list[list[Optional[int]]] = []
    for _ in range(h):
        distances.append([None] * w)
    seen: set[tuple[int, int]] = set()
    q: deque[tuple[int, int, int]] = deque()
    q.append((0, fx, fy))
    while len(q) > 0:
        depth, x, y = q.popleft()
        if x < 0 or y < 0 or x >= w or y >= h:
            continue
        if board[y][x] == '#':
            continue
        if (x, y) in seen:
            continue
        seen.add((x, y))
        distances[y][x] = depth
        q.append((depth+1, x-1, y))
        q.append((depth+1, x+1, y))
        q.append((depth+1, x, y-1))
        q.append((depth+1, x, y+1))
    return distances

def collect_corner(cx, cy, init_corner_dist):
    distances = get_distances(cx, cy)
    max_distance = -1
    for row in distances:
        for num in row:
            if num is not None and num > max_distance:
                max_distance = num

    # sum completely covered tiles
    skips_before_limit = (steps - init_corner_dist - 2 - max_distance) // w
    full_repetitions = (skips_before_limit * (skips_before_limit + 1)) // 2
    curr_repetitions = int(math.pow(math.ceil(skips_before_limit / 2), 2))
    other_repetitions = full_repetitions - curr_repetitions

    # add fully covered tiles from cardinal directions and self
    curr_repetitions += skips_before_limit // 2 + 1
    other_repetitions += math.ceil(skips_before_limit / 2)

    acc = curr_repetitions*curr_parity_block_covers + other_parity_block_covers*other_repetitions

    # walk partially covered corner tiles
    i = 0
    while True:
        if (skips_before_limit + i) % 2 == 0:
            wkbl = curr_parity_block
        else:
            wkbl = other_parity_block
        corner_dist = br + 2 + (skips_before_limit + i) * w
        if corner_dist > steps:
            break
        tile_acc = 0
        for y in range(h):
            for x in range(w):
                if (x, y) in wkbl and distances[y][x] + corner_dist <= steps:
                    tile_acc += 1
        acc += (skips_before_limit + i + 1) * tile_acc
        i += 1

    return acc

print(sum([
    collect_corner(0, 0, tl),
    collect_corner(w-1, 0, tr),
    collect_corner(0, h-1, bl),
    collect_corner(w-1, h-1, br),
]))

# TODO: walk cardinal directions
def find_closest(sx: int, sy: int, tester):
    seen: set[tuple[int, int]] = set()
    depth_limit = None
    equivalent_results = []
    q: deque[tuple[int, int, int]] = deque()
    q.append((0, sx, sy))
    while len(q) > 0:
        depth, x, y = q.popleft()
        if x < 0 or y < 0 or x >= w or y >= h:
            continue
        if depth_limit is not None and depth_limit < depth:
            continue
        if board[y][x] == '#':
            continue
        if (x, y) in seen:
            continue
        seen.add((x, y))
        if tester(x, y):
            equivalent_results.append((depth, x, y))
            depth_limit = depth
        q.append((depth+1, x-1, y))
        q.append((depth+1, x+1, y))
        q.append((depth+1, x, y-1))
        q.append((depth+1, x, y+1))
    if len(equivalent_results) == 0:
        raise Exception('could not find matching position')
    if len(equivalent_results) > 1:
        print('found equivalents', equivalent_results)
    return equivalent_results[0]

# print(start)
# print(find_closest(start[0], start[1], lambda x, y: y == 0))
# print(find_closest(start[0], start[1], lambda x, y: y == h-1))
# print(find_closest(start[0], start[1], lambda x, y: x == 0))
# print(find_closest(start[0], start[1], lambda x, y: x == w-1))

# x_seen = set()
# cx = start[0]
# cy = start[1]
# while cx not in x_seen:
#     x_seen.add(cx)
#     depth, nx, ny = find_closest(cx, cy, lambda _, y: y == 0)
#     print(depth, nx, ny)
#     cx, cy = nx, h-1
#
# print(x_seen)

@cache
def find_distance_map_right(norm_col0: tuple):
    distances: list[list[Optional[int]]] = []
    for _ in range(h):
        distances.append([None] * w)
    seen = set()
    q = deque()
