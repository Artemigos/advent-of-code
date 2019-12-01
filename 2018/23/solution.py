import re

with open('2018/23/data.txt', 'r') as f:
    lines = f.read().splitlines()

rows = []

for line in lines:
    num_strs = re.findall(r'-?\d+', line)
    rows.append(tuple(map(int, num_strs)))

max_range_bot = max(rows, key=lambda x: x[3])
max_range_bot_pos = max_range_bot[:3]
max_range_bot_range = max_range_bot[3]

def manhattan_dist(pos1, pos2):
    return abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])+abs(pos1[2]-pos2[2])

in_range_count = 0
for row in rows:
    dist = manhattan_dist(max_range_bot_pos, row)
    if dist <= max_range_bot_range:
        in_range_count += 1

print(in_range_count)

# part 2
max_intersects = 0
for i in range(len(rows)):
    intersect_count = 0
    for row in rows:
        dist = manhattan_dist(rows[i], row)
        if dist <= rows[i][3]+row[3]:
            intersect_count += 1
    if intersect_count > max_intersects:
        max_intersects = intersect_count
    print(f'{i:-4} {intersect_count}')
print(max_intersects)
