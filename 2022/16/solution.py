from collections import deque
import common

lines = common.read_file().splitlines()

valves = {}
for line in lines:
    room = line[6:8]
    rate = common.extract_numbers(line)[0]
    destinations = line.split('valves ')[1] if 'valves ' in line else line.split('valve ')[1]
    destinations = destinations.split(', ')
    valves[room] = (rate, destinations)

#rnt(repr(valves))

worth = [k for k in valves if valves[k][0] > 1]
#print(repr(worth))

distances = {}

for start in ['AA'] + worth:
    distances[start] = {}
    q = deque([(start, 0)])
    seen = set()
    while len(q) > 0:
        at, depth = q.popleft()
        if at in seen:
            continue
        seen.add(at)
        distances[start][at] = depth
        for n in valves[at][1]:
            q.append((n, depth+1))

#print(repr(distances))

# part 1
q = deque([(30, 'AA', 0, set())])
results = []
while len(q) > 0:
    time, at, released, opened = q.popleft()
    if time <= 0:
        results.append(released)
        continue
    available_moves = [v for v in worth if v not in opened]
    if len(available_moves) == 0:
        results.append(released)
        continue
    for move in available_moves:
        d = distances[at][move] + 1
        points_for_open = valves[move][0]
        time_open = time - d
        if time_open <= 0:
            results.append(released)
            continue
        new_opened = set(opened)
        new_opened.add(move)
        q.append((time_open, move, released+time_open*points_for_open, new_opened))

#print(repr(results))
print(max(results))

# part 2
#q = deque([(26, 'AA', 26, 'AA', 26, 0, set())])
#results = []
#while len(q) > 0:
#    time, at, at_time, el_at, el_at_time, released, opened = q.popleft()
#    if time <= 0:
#        results.append(released)
#        continue
#
#    available_moves = [v for v in worth if v not in opened and v != el_at and v != at]
#    if len(available_moves) == 0:
#        if at_time < time:
#            points_for_open = valves[at][0]
#            new_opened = set(opened)
#            new_opened.add(at)
#            q.append((at_time, at, at_time, el_at, None, released+at_time*points_for_open, new_opened))
#        elif el_at_time < time:
#            points_for_open = valves[el_at][0]
#            new_opened = set(opened)
#            new_opened.add(el_at)
#            q.append((at_time, at, None, el_at, el_at_time, released+el_at_time*points_for_open, new_opened))
#        else:
#            results.append(released)
#        continue
#    for move in available_moves:
#        points_for_open = valves[move][0]
#        if at_time == time:
#            d = distances[at][move] + 1
#            time_open = time - d
#            if time_open <= 0:
#                results.append(released)
#                continue
#            new_opened = set(opened)
#            new_opened.add(move)
#            q.append((time_open, move, released+time_open*points_for_open, new_opened))

#print(max(results))

q = deque([((26, 'AA', 0), (26, 'AA', 0), 0, dict())])
results = []
while len(q) > 0:
    me, el, released, opened_at = q.popleft()
    #print(me, el, released, repr(opened_at))
    if me is None or el is None:
        is_me = me is not None
    else:
        is_me = me[0] >= el[0]
    this = me if is_me else el
    other = el if is_me else me

    time, at, this_release = this
    released += this_release

    if time <= 0:
        results.append(released)
        continue
    performed_moves = 0
    for move in worth:
        if other is not None and move == other[1]:
            #print(f'skipping {move} because other is doing it')
            continue
        d = distances[at][move] + 1
        time_open = time - d
        if move in opened_at and opened_at[move] >= time_open:
            #print(f'skip {move} because already opened')
            continue

        points_for_open = valves[move][0]

        if time_open <= 0:
            #print(f'skipping {move} because would take too long')
            continue

        performed_moves += 1

        new_opened_at = dict(opened_at)
        new_opened_at[move] = time_open

        this_data = (time_open, move, time_open*points_for_open)
        if is_me:
            #print(f'moving me {at} to {move}')
            q.appendleft((this_data, other, released, new_opened_at))
        else:
            #print(f'moving elephant {at} to {move}')
            q.appendleft((other, this_data, released, new_opened_at))

    if performed_moves == 0:
        if other is None:
            results.append(released)
        else:
            results.append(released+other[2])
        #print('added result', results[-1])

print(max(results))
