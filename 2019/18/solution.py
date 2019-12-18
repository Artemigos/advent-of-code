import common
from collections import deque
from queue import PriorityQueue

data = [list(x) for x in common.read_file('2019/18/data.txt').splitlines()]
w = len(data[0])
h = len(data)

spots = {}

for x in range(w):
    for y in range(h):
        c = data[y][x]
        if c != '#' and c != '.':
            spots[c] = (x, y)

def to_lower(c):
    if not is_upper_alpha(c):
        return c
    return chr(ord(c) + (ord('a')-ord('A')))

def is_upper_alpha(c):
    return c >= 'A' and c <= 'Z'

def is_lower_alpha(c):
    return c >= 'a' and c <= 'z'

keys_amount = len([x for x in spots.keys() if is_lower_alpha(x)])

def find_keys(start, possessed_keys):
    global data

    possessed_keys = set(possessed_keys)

    q = deque([(0, start)])
    seen = set()
    keys = {}

    while len(q) > 0:
        depth, pos = q.popleft()
        if pos in seen:
            continue
        seen.add(pos)

        c = data[pos[1]][pos[0]]
        if c == '#':
            continue
        elif is_upper_alpha(c) and to_lower(c) not in possessed_keys:
            continue
        elif is_lower_alpha(c) and c not in possessed_keys:
            keys[c] = depth
            continue
        else:
            for n in [(pos[0]-1, pos[1]), (pos[0]+1, pos[1]), (pos[0], pos[1]-1), (pos[0], pos[1]+1)]:
                q.append((depth+1, n))

    return keys

# part 1
q = PriorityQueue()
q.put((0, spots['@'], []))
min_dist = None
seen = {}

while not q.empty():
    dist, pos, keys = q.get()

    keys_key = tuple(sorted(keys)), pos
    if keys_key in seen and seen[keys_key] >= dist:
        continue
    if min_dist is not None and dist <= min_dist:
        continue
    if len(keys) == keys_amount:
        min_dist = dist
        continue
    seen[keys_key] = dist

    for key, key_dist in find_keys(pos, keys).items():
        q.put((dist-key_dist, spots[key], keys+[key]))

print('part 1:', -(min_dist or 0))

# part 2
data = [list(x) for x in common.read_file('2019/18/data.part2.txt').splitlines()]
w = len(data[0])
h = len(data)

spots = {}
robots = []

for x in range(w):
    for y in range(h):
        c = data[y][x]
        if is_lower_alpha(c) or is_upper_alpha(c):
            spots[c] = (x, y)
        elif c == '@':
            robots.append((x, y))

keys_amount = len([x for x in spots.keys() if is_lower_alpha(x)])

q = PriorityQueue()
q.put((0, robots, []))
min_dist = None
seen = {}

while not q.empty():
    dist, robots, keys = q.get()

    keys_key = list(sorted(keys))
    for robot in robots:
        for i in robot:
            keys_key.append(i)
    keys_key = tuple(keys_key)

    if keys_key in seen and seen[keys_key] >= dist:
        continue
    if min_dist is not None and dist <= min_dist:
        continue
    if len(keys) == keys_amount:
        min_dist = dist
        continue
    seen[keys_key] = dist

    for i in range(len(robots)):
        pos = robots[i]
        for key, key_dist in find_keys(pos, keys).items():
            q.put((
                dist-key_dist,
                robots[:i]+[spots[key]]+robots[i+1:],
                keys+[key]))

print('part 2:', -(min_dist or 0))
