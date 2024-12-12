import common
from collections import deque

lines = common.read_file().splitlines()
w = len(lines[0])
h = len(lines)

# part 1

# detect regions
def walk(x: int, y: int, c: str, seen: set[tuple[int, int]]) -> list[tuple[int, int]]:
    result: list[tuple[int, int]] = []
    q: deque[tuple[int, int]] = deque([(x, y)])
    while q:
        x, y = q.popleft()
        if x < 0 or x >= w or y < 0 or y >= h:
            continue
        if (x, y) in seen:
            continue
        nc = lines[y][x]
        if nc != c:
            continue
        seen.add((x, y))
        result.append((x, y))
        q.append((x + 1, y))
        q.append((x - 1, y))
        q.append((x, y + 1))
        q.append((x, y - 1))
    return result

regions: list[tuple[str, list[tuple[int, int]]]] = []
seen: set[tuple[int, int]] = set()
for y in range(h):
    for x in range(w):
        if (x, y) in seen:
            continue
        c = lines[y][x]
        region = walk(x, y, c, seen)
        regions.append((c, region))

# solve
acc = 0
for _, points in regions:
    area = len(points)
    perimeter = 0
    for p in points:
        x, y = p
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if (x+dx, y+dy) not in points:
                perimeter += 1
    acc += area * perimeter
print(acc)

# part 2
acc = 0
for _, points in regions:
    area = len(points)
    vert_lines: list[tuple[int, int, range]] = []
    horiz_lines: list[tuple[int, int, range]] = []
    for p in points:
        x, y = p
        for dx in [-1, 1]:
            if (x+dx, y) not in points:
                x_before = min(x, x+dx)
                x_inside = dx
                prev = None
                nxt = None
                for l in vert_lines:
                    if x_before == l[0] and x_inside == l[1] and l[2].stop == y:
                        prev = l
                    if x_before == l[0] and x_inside == l[1] and l[2].start == y+1:
                        nxt = l
                rng = range(y, y+1)
                if prev is not None:
                    vert_lines.remove(prev)
                    rng = range(prev[2].start, rng.stop)
                if nxt is not None:
                    vert_lines.remove(nxt)
                    rng = range(rng.start, nxt[2].stop)
                vert_lines.append((x_before, x_inside, rng))
        for dy in [-1, 1]:
            if (x, y+dy) not in points:
                y_before = min(y, y+dy)
                y_inside = dy
                prev = None
                nxt = None
                for l in horiz_lines:
                    if y_before == l[0] and y_inside == l[1] and l[2].stop == x:
                        prev = l
                    if y_before == l[0] and y_inside == l[1] and l[2].start == x+1:
                        nxt = l
                rng = range(x, x+1)
                if prev is not None:
                    horiz_lines.remove(prev)
                    rng = range(prev[2].start, rng.stop)
                if nxt is not None:
                    horiz_lines.remove(nxt)
                    rng = range(rng.start, nxt[2].stop)
                horiz_lines.append((y_before, y_inside, rng))

    sides = len(vert_lines) + len(horiz_lines)
    acc += sides * area
print(acc)
