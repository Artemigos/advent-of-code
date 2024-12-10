from collections import deque
import common

lines = common.read_file().splitlines()
w = len(lines[0])
h = len(lines)

# part 1
# NOTE: this is a DAG
# (concluded from looking at data and using some temporary code to verify)

# find intersections (graph nodes)
Node = tuple[int, int]
intersections: set[Node] = set()
for y in range(h):
    if y == 0 or y == h-1:
        continue
    for x in range(w):
        if x == 0 or x == w-1:
            continue
        if lines[y][x] == '#':
            continue
        acc = 0
        for n in common.neighbors_ortho((x, y)):
            nx, ny = n
            c = lines[ny][nx]
            if c != '#':
                acc += 1
        if acc > 2:
            intersections.add((x, y))

start = (lines[0].find('.'), 0)
end = (lines[-1].find('.'), h-1)
intersections.add(start)
intersections.add(end)

# walk edges
edges: dict[Node, dict[Node, int]] = {}
def add(fro: Node, to: Node, weight: int):
    global edges
    if fro not in edges:
        edges[fro] = {}
    edges[fro][to] = weight
def mov(x: int, y: int, dir: str) -> tuple[int, int]:
    if dir == '<':
        return x-1, y
    elif dir == '>':
        return x+1, y
    elif dir == '^':
        return x, y-1
    elif dir == 'v':
        return x, y+1
    else:
        assert False
for node in intersections:
    x, y = node
    q: deque[tuple[int, int, int, str]] = deque()
    if y > 0 and lines[y-1][x] in '^.':
        q.append((x, y-1, 1, '^'))
    if y < h-1 and lines[y+1][x] in 'v.':
        q.append((x, y+1, 1, 'v'))
    if lines[y][x-1] in '<.':
        q.append((x-1, y, 1, '<'))
    if lines[y][x+1] in '>.':
        q.append((x+1, y, 1, '>'))
    while q:
        nx, ny, depth, dir = q.popleft()
        if (nx, ny) in intersections:
            add(node, (nx, ny), depth)
            continue
        c = lines[ny][nx]
        assert c != '#'
        if c != dir:
            if (dir in '<>' and c in '<>') or (dir in '^v' and c in '^v'):
                continue
        if c != '.':
            dir = c
            next_x, next_y = mov(nx, ny, dir)
            next_c = lines[next_y][next_x]
            if next_c == '#':
                continue
            q.append((next_x, next_y, depth+1, dir))
        else:
            next_x, next_y = mov(nx, ny, dir)
            next_c = lines[next_y][next_x]
            if next_c == '#':
                # at turn, rotate
                rotations = '<>' if dir in '^v' else '^v'
                for rot_dir in rotations:
                    next_x, next_y = mov(nx, ny, rot_dir)
                    next_c = lines[next_y][next_x]
                    if next_c != '#':
                        dir = rot_dir
                        break
                else:
                    continue
            q.append((next_x, next_y, depth+1, dir))

# find longest path
q2: deque[tuple[Node, int]] = deque([(start, 0)])
longest = 0
while q2:
    node, dist = q2.popleft()
    if node == end:
        longest = max(longest, dist)
        continue
    for nxt in edges[node]:
        q2.append((nxt, edges[node][nxt] + dist))

print(longest)

# part 2
# NOTE: well... not a DAG anymore

# add opposite edges
for n1 in list(edges.keys()):
    for n2 in edges[n1]:
        add(n2, n1, edges[n1][n2])

# find longest path - slightly slow, ~1min
q3: deque[tuple[Node, list[Node], int]] = deque([(start, [], 0)])
longest = 0
while q3:
    node, seen, dist = q3.popleft()
    if node == end:
        longest = max(longest, dist)
        continue
    if node in seen:
        continue
    for nxt in edges[node]:
        q3.append((nxt, seen + [node], edges[node][nxt] + dist))

print(longest)
