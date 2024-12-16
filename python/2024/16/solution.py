import common
from queue import PriorityQueue

lines = common.read_file().splitlines()
w = len(lines[0])
h = len(lines)

start = 0, 0
end = 0, 0
for y in range(h):
    for x in range(w):
        if lines[y][x] == 'S':
            start = (x, y)
        elif lines[y][x] == 'E':
            end = (x, y)

# part 1
Item = tuple[int, int, int, int, int]
q: PriorityQueue[Item] = PriorityQueue()
q.put((0, start[0], start[1], 1, 0))
seen: set[tuple[int, int, int, int]] = set()
min_depth = 0
while not q.empty():
    depth, x, y, dx, dy = q.get()
    c = lines[y][x]
    if c == '#':
        continue
    if c == 'E':
        min_depth = depth
        break
    k = x, y, dx, dy
    if k in seen:
        continue
    seen.add(k)
    q.put((depth+1, x+dx, y+dy, dx, dy))
    q.put((depth+1000, x, y, -dy, dx))
    q.put((depth+1000, x, y, dy, -dx))

print(min_depth)

# part 2
# NOTE: takes ~30s
Item2 = tuple[int, int, int, int, int, list[tuple[int, int]]]
q2: PriorityQueue[Item2] = PriorityQueue()
q2.put((0, start[0], start[1], 1, 0, []))
seen2: dict[tuple[int, int, int, int], int] = {}
on_optimal_paths: set[tuple[int, int]] = set([start, end])
while not q2.empty():
    depth, x, y, dx, dy, path = q2.get()
    if depth > min_depth:
        continue
    c = lines[y][x]
    if c == '#':
        continue
    if c == 'E':
        for pos in path:
            on_optimal_paths.add(pos)
        continue
    k = x, y, dx, dy
    if k in seen2 and seen2[k] < depth:
        continue
    seen2[k] = depth
    q2.put((depth+1, x+dx, y+dy, dx, dy, path + [(x, y)]))
    q2.put((depth+1000, x, y, -dy, dx, path + [(x, y)]))
    q2.put((depth+1000, x, y, dy, -dx, path + [(x, y)]))

print(len(on_optimal_paths))
