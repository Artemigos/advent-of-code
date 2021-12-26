target_x = range(211, 233)
target_y = range(-124, -68)

# part 1 and 2

x_hits = []
infinite_x_hits = []
for vx in range(1, target_x.stop):
    pos = 0
    i = 0
    while pos < target_x.stop and vx > i:
        pos += vx - i
        i += 1
        if pos in target_x:
            x_hits.append((vx, i))
    if vx == i and pos in target_x:
        infinite_x_hits.append((vx, i+1))

print(infinite_x_hits)

y_hits = []
curr_vy = target_y.start
while True:
    if curr_vy > -target_y.start:
        break
    vy = curr_vy
    curr_vy += 1
    pos = 0
    i = 0
    max_pos = 0
    while pos > target_y.start:
        pos += vy
        if pos > max_pos:
            max_pos = pos
        vy -= 1
        i += 1
        if pos in target_y:
            y_hits.append((vy+i, i, max_pos))

y_hits = sorted(y_hits, key=lambda x: x[2])

hits = []
while len(y_hits) > 0:
    vy, i, max_y = y_hits.pop()
    x_matches = list(filter(lambda x: x[1] == i, x_hits))
    for match in x_matches:
        vx, _ = match
        hits.append((vy, vx, max_y))
    inf_matches = list(filter(lambda x: x[1] <= i, infinite_x_hits))
    for match in inf_matches:
        vx, _ = match
        hits.append((vy, vx, max_y))

print(max(map(lambda x: x[2], hits)))
print(len(set(hits)))
