from collections import deque
import common

lines = common.read_file().splitlines()
directions = []

for line in lines:
    curr_i = 0
    directions_acc = []
    while curr_i < len(line):
        l = 2 if line[curr_i] in {'n', 's'} else 1
        directions_acc.append(line[curr_i:curr_i+l])
        curr_i += l
    directions.append(directions_acc)

# part 1
field = set()
for line in directions:
    x, y = 0, 0
    for d in line:
        if d == 'nw':
            y -= 1
            x -= 1
        elif d == 'ne':
            y -= 1
        elif d == 'w':
            x -= 1
        elif d == 'e':
            x += 1
        elif d == 'sw':
            y += 1
        elif d == 'se':
            y += 1
            x += 1
        else:
            raise 'unknown direction'
    pos = x, y
    if pos in field:
        field.remove(pos)
    else:
        field.add(pos)

print(len(field))

# part 2
neighbors = [
    (-1, -1), (0, -1),
    (-1, 0), (1, 0),
    (0, 1), (1, 1)
]
def perform_step(field):
    result = set()
    seen = set()
    q = deque(field)
    while len(q) > 0:
        pos = q.popleft()
        if pos in seen:
            continue
        seen.add(pos)
        x, y = pos
        flipped = pos in field
        flipped_neighbors = 0
        for ndx, ndy in neighbors:
            nx = x + ndx
            ny = y + ndy
            npos = nx, ny
            if npos in field:
                flipped_neighbors += 1
            elif flipped:
                q.append(npos)

        if flipped and (flipped_neighbors == 1 or flipped_neighbors == 2):
            result.add(pos)
        if not flipped and flipped_neighbors == 2:
            result.add(pos)
    return result

for _ in range(100):
    field = perform_step(field)

print(len(field))
