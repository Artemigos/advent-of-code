import common
from collections import defaultdict, deque

data = [ list(x) for x in common.read_file('2019/20/data.txt').splitlines()]
w = len(data[0])
h = len(data)

# index portals
def is_portal_marker(c):
    return c != ' ' and c != '.' and c != '#'

portal_defs = defaultdict(lambda: [])
for x in range(w):
    for y in range(h):
        c = data[y][x]
        if is_portal_marker(c):
            if x+1 < w and is_portal_marker(data[y][x+1]):
                label = c+data[y][x+1]
                if x+2 < w and data[y][x+2] == '.':
                    drop_pos = x+2, y
                else:
                    drop_pos = x-1, y
                portal_defs[label].append(drop_pos)
            elif y+1 < h and is_portal_marker(data[y+1][x]):
                label = c+data[y+1][x]
                if y+2 < h and data[y+2][x] == '.':
                    drop_pos = x, y+2
                else:
                    drop_pos = x, y-1
                portal_defs[label].append(drop_pos)

portals = {}
start = None
end = None
for label, locations in portal_defs.items():
    if label == 'AA':
        start = locations[0]
    elif label == 'ZZ':
        end = locations[0]
    else:
        portals[locations[0]] = locations[1]
        portals[locations[1]] = locations[0]

for y in range(h):
    for x in range(w):
        if (x, y) in portals:
            print('X', end='')
        else:
            print(data[y][x], end='')
    print()
print()

# part 1
q = deque([(0, start)])
seen = set()
while len(q) > 0:
    depth, pos = q.popleft()
    if pos == end:
        print('part 1:', depth)
        break

    if pos in seen:
        continue
    seen.add(pos)

    x, y = pos
    c = data[y][x]
    if c != '.':
        continue

    for n in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
        q.append((depth+1, n))

    if pos in portals:
        q.append((depth+1, portals[pos]))
