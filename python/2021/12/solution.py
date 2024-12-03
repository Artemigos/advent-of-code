from collections import defaultdict, deque
import common

lines = common.read_file().splitlines()
connections = defaultdict(lambda: [])
for line in lines:
    l, r = line.split('-')
    connections[l].append(r)
    connections[r].append(l)

# part 1

paths = 0
q = deque([('start', defaultdict(lambda: 0))])
while len(q) > 0:
    node, visits = q.popleft()
    if node[0].islower() and visits[node] == 1:
        continue
    if node == 'end':
        paths += 1
        continue
    new_visits = defaultdict(lambda: 0, visits)
    new_visits[node] += 1
    for connection in connections[node]:
        q.append((connection, new_visits))

print(paths)

# part 2

paths = 0
q = deque([('start', defaultdict(lambda: 0), False)])
while len(q) > 0:
    node, visits, seen_small_twice = q.popleft()
    if node == 'end':
        paths += 1
        continue
    if node == 'start' and visits[node] == 1:
        continue
    if node[0].islower() and visits[node] > 0 and seen_small_twice:
        continue
    new_visits = defaultdict(lambda: 0, visits)
    new_visits[node] += 1
    if node[0].islower() and new_visits[node] == 2:
        seen_small_twice = True
    for connection in connections[node]:
        q.append((connection, new_visits, seen_small_twice))

print(paths)
