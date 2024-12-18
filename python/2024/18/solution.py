import common
from collections import deque

lines = common.read_file().splitlines()
w, h = 71, 71
part1_count = 1024

# part 1
def run(count: int) -> int | None:
    obstacles: set[tuple[int, int]] = set()
    for line in lines[:count]:
        x, y = map(int, line.split(','))
        obstacles.add((x, y))

    q: deque[tuple[int, int, int]] = deque([(0, 0, 0)])
    seen: set[tuple[int, int]] = set()
    while q:
        depth, x, y = q.popleft()
        if x < 0 or x >= w or y < 0 or y >= h:
            continue
        k = x, y
        if k in obstacles or k in seen:
            continue
        if (x, y) == (w - 1, h - 1):
            return depth
        seen.add(k)
        for n in common.neighbors_ortho(k):
            nx, ny = n
            q.append((depth + 1, nx, ny))
    return None

print(run(part1_count))

# part 2
max_good = part1_count
min_bad = len(lines)

while max_good < min_bad-1:
    mid = (min_bad - max_good) // 2 + max_good
    result = run(mid)
    if result is None:
        min_bad = mid
    else:
        max_good = mid

# NOTE: max_good is the **amount** bytes that can fall
# as an index, it points at the first byte that cuts off the path
print(lines[max_good])
