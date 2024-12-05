from dataclasses import dataclass
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

@dataclass
class DistMap:
    start: tuple[int, int]
    distances: list[list[Optional[int]]]
    walkable_even: set[tuple[int, int]]
    walkable_odd: set[tuple[int, int]]
    max_dist: int

# create distance maps from corners
def get_distances(fx: int, fy: int) -> DistMap:
    distances: list[list[Optional[int]]] = []
    for _ in range(h):
        distances.append([None] * w)
    walkable_even: set[tuple[int, int]] = set()
    walkable_odd: set[tuple[int, int]] = set()
    max_dist = 0
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
        curr_walkable = walkable_even if depth % 2 == 0 else walkable_odd
        curr_walkable.add((x, y))
        max_dist = max(max_dist, depth)
        q.append((depth+1, x-1, y))
        q.append((depth+1, x+1, y))
        q.append((depth+1, x, y-1))
        q.append((depth+1, x, y+1))
    return DistMap((fx, fy), distances, walkable_even, walkable_odd, max_dist)

def collect_corner(cx, cy, init_corner_dist):
    distances = get_distances(cx, cy)

    # sum completely covered tiles
    skips_before_limit = (steps - init_corner_dist - 2 - distances.max_dist) // w
    full_repetitions = (skips_before_limit * (skips_before_limit + 1)) // 2
    curr_repetitions = int(math.pow(math.ceil(skips_before_limit / 2), 2))
    other_repetitions = full_repetitions - curr_repetitions

    # add fully covered tiles from cardinal directions and self
    curr_repetitions += skips_before_limit // 2 + 1
    other_repetitions += math.ceil(skips_before_limit / 2)

    acc = curr_repetitions*len(distances.walkable_even) + len(distances.walkable_odd)*other_repetitions

    # walk partially covered corner tiles
    i = 0
    while True:
        if (skips_before_limit + i) % 2 == 0:
            wkbl = distances.walkable_even
        else:
            wkbl = distances.walkable_odd
        corner_dist = init_corner_dist + 2 + (skips_before_limit + i) * w
        if corner_dist > steps:
            break
        tile_acc = 0
        for y in range(h):
            for x in range(w):
                if (x, y) in wkbl and distances.distances[y][x] + corner_dist <= steps:
                    tile_acc += 1
        acc += (skips_before_limit + i + 1) * tile_acc
        i += 1

    return acc

start_distances = get_distances(*start).distances
tl = start_distances[0][0]
tr = start_distances[0][w-1]
bl = start_distances[h-1][0]
br = start_distances[h-1][w-1]

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
