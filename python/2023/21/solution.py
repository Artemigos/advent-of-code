from dataclasses import dataclass
import common
from collections import deque

board = common.read_file().splitlines()
w = len(board[0])
h = len(board)
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

@dataclass
class DistMap:
    start: tuple[int, int]
    distances: list[list[int | None]]
    walkable_even: set[tuple[int, int]]
    walkable_odd: set[tuple[int, int]]
    max_dist: int

def get_distances(fx: int, fy: int) -> DistMap:
    distances: list[list[int | None]] = []
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

start_distances = get_distances(*start)

# part 1
steps = 64
acc = 0
for x, y in start_distances.walkable_even:
    d = start_distances.distances[y][x]
    if d is not None and d <= steps:
        acc += 1
print(acc)

# part 2
assert w == h
steps = 26501365
distances_covered = steps // w
walkable_even = len(start_distances.walkable_even)
walkable_odd = len(start_distances.walkable_odd)
corners_even = 0
for x, y in start_distances.walkable_even:
    d = start_distances.distances[y][x]
    if d is not None and d > w // 2:
        corners_even += 1
corners_odd = 0
for x, y in start_distances.walkable_odd:
    d = start_distances.distances[y][x]
    if d is not None and d > w // 2:
        corners_odd += 1

# NOTE: I needed help figuring this one out, but the solution is cool
print(walkable_odd * ((distances_covered + 1)**2) + walkable_even * (distances_covered**2) + distances_covered * corners_even - (distances_covered + 1) * corners_odd)
