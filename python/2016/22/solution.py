import queue
import common

lines = common.read_file().splitlines()[2:]

def parse_line(line: str):
    segments = line.split()
    name_segments = segments[0].split('-')
    x = int(name_segments[-2][1:])
    y = int(name_segments[-1][1:])
    used = int(segments[2][:-1])
    avail = int(segments[3][:-1])
    return (x, y, used, avail)

nodes_lst = list(map(parse_line, lines))

# part 1
found = 0
for i in range(len(nodes_lst)):
    for j in range(i+1, len(nodes_lst)):
        x1, y1, used1, avail1 = nodes_lst[i]
        x2, y2, used2, avail2 = nodes_lst[j]
        if used1 > 0 and used1 <= avail2:
            found += 1
        if used2 > 0 and used2 <= avail1:
            found += 1

print(found)

# part 2
w = 31
h = 31
wanted = 30,0

# preview map
def create_grid(w, h):
    grid = []
    for _ in range(h):
        grid.append(['']*w)
    return grid
grid = create_grid(w, h)
for x, y, used, avail in nodes_lst:
    if used > 400:
        grid[y][x] = '#'
    elif used == 0:
        grid[y][x] = '_'
    elif (x, y) == wanted:
        grid[y][x] = '!'
    else:
        grid[y][x] = '.'
# for y in range(h):
#     for x in range(w):
#         print(grid[y][x], end='')
#     print()

# data figured out from preview
zero = 13, 27

def is_movable(pos):
    x, y = pos
    if x < 0 or x >= w or y < 0 or y >= h:
        return False
    if y == 15 and x >= 5:
        return False
    return True

# actual solution
def find_moves(state):
    zero, wanted = state
    x, y = zero
    neighbors = [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]
    for n in neighbors:
        if is_movable(n):
            if n == wanted:
                yield n, zero
            else:
                yield n, wanted

q = queue.deque([(0, (zero, wanted))])
seen_states = set()

while len(q) > 0:
    depth, state = q.popleft()
    if state in seen_states:
        continue
    seen_states.add(state)

    zero, wanted = state
    if wanted == (0, 0):
        print(depth)
        break

    # common.print_and_return(depth)
    for m in find_moves(state):
        q.append((depth+1, m))
