import common
import queue
import itertools

board = common.read_file().splitlines()
h = len(board)
w = len(board[0])
spots = 8

def can_go_to(x, y):
    if x < 0 or x >= w:
        return False
    if y < 0 or y >= h:
        return False
    return board[y][x] != '#'

def find(start_num):
    num_str = str(start_num)
    for y in range(h):
        for x in range(w):
            if board[y][x] == num_str:
                return (x, y)
    return None

def find_paths_to_other(start_num):
    start = find(start_num)
    dists = [None]*spots
    dists[start_num] = 0
    q = queue.deque([(0, start)])
    seen_positions = set()

    while len(q) > 0:
        depth, pos = q.popleft()
        if pos in seen_positions:
            continue
        seen_positions.add(pos)

        x, y = pos
        field = board[y][x] 
        if field != '.':
            found_num = int(field)
            dists[found_num] = depth
            if all(map(lambda x: x is not None, dists)):
                break
        if can_go_to(x-1, y):
            q.append((depth+1, (x-1, y)))
        if can_go_to(x+1, y):
            q.append((depth+1, (x+1, y)))
        if can_go_to(x, y+1):
            q.append((depth+1, (x, y+1)))
        if can_go_to(x, y-1):
            q.append((depth+1, (x, y-1)))

    return dists

dist_matrix = []
for i in range(spots):
    dists = find_paths_to_other(i)
    dist_matrix.append(dists)

travel_points = range(1, spots)

# part 1
travel_orders = itertools.permutations(travel_points)
min_dist = sum(dist_matrix[0])

for order in travel_orders:
    acc = 0
    last_point = 0
    for point in order:
        acc += dist_matrix[last_point][point]
        last_point = point

    if acc < min_dist:
        min_dist = acc

print(min_dist)

# part 2
travel_orders = itertools.permutations(travel_points)
min_dist = sum(dist_matrix[0])

for order in travel_orders:
    acc = 0
    last_point = 0
    for point in order:
        acc += dist_matrix[last_point][point]
        last_point = point

    acc += dist_matrix[last_point][0]

    if acc < min_dist:
        min_dist = acc

print(min_dist)
