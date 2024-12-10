import common
from collections import deque

lines = common.read_file().splitlines()
w = len(lines[0])
h = len(lines)
trailheads = set()

for y in range(h):
    for x in range(w):
        if lines[y][x] == '0':
            trailheads.add((x, y))

# part 1 and 2
acc1 = 0
acc2 = 0
for head in trailheads:
    q: deque[tuple[int, int, int]] = deque([(0, *head)])
    ends = []
    while q:
        dist, x, y = q.popleft()
        if x < 0 or y < 0 or x >= w or y >= h:
            continue
        if lines[y][x] != str(dist):
            continue
        if dist == 9:
            ends.append((x, y))
            continue
        q.append((dist + 1, x + 1, y))
        q.append((dist + 1, x - 1, y))
        q.append((dist + 1, x, y + 1))
        q.append((dist + 1, x, y - 1))
    acc1 += len(set(ends))
    acc2 += len(ends)

print(acc1)
print(acc2)
