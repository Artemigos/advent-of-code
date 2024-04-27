import common
from collections import deque

lines = common.read_file().splitlines()

rates = {}
connections = {}

for line in lines:
    room = line[6:8]
    rate = common.extract_numbers(line)[0]
    destinations = line.split('valves ')[1] if 'valves ' in line else line.split('valve ')[1]
    destinations = destinations.split(', ')
    rates[room] = rate
    connections[room] = destinations

worth = set((v for v in rates.keys() if rates[v] > 0))
worth_connections = dict()

for v in ['AA'] + list(worth):
    q = deque([(v, 0)])
    seen = dict()
    while len(q) > 0:
        room, depth = q.popleft()
        if room in seen:
            continue
        seen[room] = depth+1
        for n in connections[room]:
            q.append((n, depth+1))
    worth_connections[v] = seen

# part 1
start_t = 30
q = deque([('AA', 0, start_t, list(worth))])
max_release = 0

while len(q) > 0:
    at, pts, time, remaining = q.popleft()
    max_release = max(max_release, pts)

    for r in remaining:
        new_time = time - worth_connections[at][r]
        if new_time <= 0:
            continue

        new_pts = pts + new_time*rates[r]
        new_remaining = list(remaining)
        new_remaining.remove(r)
        q.append((r, new_pts, new_time, new_remaining))

print(max_release)

# part 2
start_t = 26
q = deque([('AA', 0, start_t, 'AA', 0, start_t, list(worth))])
max_release = 0
seen = dict()

while len(q) > 0:
    at1, pts1, time1, at2, pts2, time2, remaining = q.popleft()
    curr_pts = pts1+pts2
    k = at1+at2+''.join(sorted(remaining))
    if k in seen and curr_pts <= seen[k]:
        continue
    seen[k] = curr_pts

    max_release = max(max_release, curr_pts)

    for r in remaining:
        new_remaining = list(remaining)
        new_remaining.remove(r)

        new_time1 = time1 - worth_connections[at1][r]
        if new_time1 > 0:
            new_pts = pts1 + new_time1*rates[r]
            q.append((r, new_pts, new_time1, at2, pts2, time2, new_remaining))

        new_time2 = time2 - worth_connections[at2][r]
        if new_time2 > 0:
            new_pts = pts2 + new_time2*rates[r]
            q.append((at1, pts1, time1, r, new_pts, new_time2, new_remaining))

print(max_release)
