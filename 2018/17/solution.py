import re
import sys
import queue
import numpy as np

sys.setrecursionlimit(10000)

def extract_ints(data: str):
    matches = re.findall(r'-?\d+', data)
    return list(map(int, matches))

def read_file(path: str) -> str:
    with open(path, 'r') as f:
        return f.read()

src = 'data'
if len(sys.argv) > 1:
    src = sys.argv[1]

fountain = (500, 0)

lines = [(x[0], extract_ints(x)) for x in read_file(f'2018/17/{src}.txt').splitlines()]
points = []
for (coord_type, [coord, start, stop]) in lines:
    opposite = 'x' if coord_type == 'y' else 'y'
    locals()[coord_type] = coord
    for i in range(start, stop+1):
        locals()[opposite] = i
        points.append((x, y))

minx = min(map(lambda x: x[0], points))
maxx = max(map(lambda x: x[0], points))
miny = min(map(lambda x: x[1], points))
maxy = max(map(lambda x: x[1], points))
print(minx, maxx)
print(miny, maxy)

mud_or_settled_l = np.zeros((maxx+3, maxy+3))
for point in points:
    mud_or_settled_l[point] = 1
wet = set()

def output_map(file: str):
    with open(f'2018/17/{file}.txt', 'w') as f:
        for y in range(np.shape(mud_or_settled_l)[1]):
            for x in range(minx-2, np.shape(mud_or_settled_l)[0]):
                if (x, y) in points:
                    f.write('#')
                elif mud_or_settled_l[x, y] == 1:
                    f.write('~')
                elif (x, y) in wet:
                    f.write('|')
                else:
                    f.write('.')
            f.write('\n')

# mud_or_settled = set(points)

def run(start_pos):
    global wet, mud_or_settled_l

    q = queue.deque()
    q.append((True, start_pos))

    while len(q) > 0:
        do_trickle, pos = q.popleft()
        print(len(q), end='\r')
        # trickle
        if do_trickle:
            while mud_or_settled_l[pos] == 0:
                wet.add(pos)
                pos = (pos[0], pos[1]+1)
                if pos[1] > maxy:
                    break
                if pos in wet:
                    break
            else:
                q.append((False, (pos[0], pos[1]-1)))
                # spread_from((pos[0], pos[1]-1))
        #spread
        else:
            while True:
                spread_over = set([pos])
                trickle_points = []

                # left
                curr_pos = pos
                left_hit_wall = False
                while True:
                    curr_pos = curr_pos[0]-1, curr_pos[1]
                    if mud_or_settled_l[curr_pos] == 1:
                        left_hit_wall = True
                        break
                    spread_over.add(curr_pos)
                    if mud_or_settled_l[curr_pos[0], curr_pos[1]+1] == 0:
                        trickle_points.append(curr_pos)
                        break

                # right
                curr_pos = pos
                right_hit_wall = False
                while True:
                    curr_pos = curr_pos[0]+1, curr_pos[1]
                    if mud_or_settled_l[curr_pos] == 1:
                        right_hit_wall = True
                        break
                    spread_over.add(curr_pos)
                    if mud_or_settled_l[curr_pos[0], curr_pos[1]+1] == 0:
                        trickle_points.append(curr_pos)
                        break

                if left_hit_wall and right_hit_wall:
                    for so in spread_over:
                        mud_or_settled_l[so] = 1
                    pos = pos[0], pos[1]-1 # prepare for next iteration
                else:
                    wet = wet.union(spread_over)
                    for tp in trickle_points:
                        q.append((True, tp))
                        # trickle_from(tp)
                    break

run(fountain)
print()

reached_by_water = set()
for x in range(np.shape(mud_or_settled_l)[0]):
    for y in range(np.shape(mud_or_settled_l)[1]):
        if mud_or_settled_l[x, y] == 1:
            reached_by_water.add((x, y))
reached_by_water = reached_by_water.difference(points)
print('part 2:', len(reached_by_water))
reached_by_water = [x for x in reached_by_water.union(wet) if x[1] >= miny]
print('part 1:', len(reached_by_water))

# output_map('end')
