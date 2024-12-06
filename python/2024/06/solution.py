import common

lines = common.read_file().splitlines()
w = len(lines[0])
h = len(lines)
start = (0, 0)
dir = (0, -1)
def rot(dir):
    return (-dir[1], dir[0])

for y in range(h):
    for x in range(w):
        if lines[y][x] == '^':
            start = (x, y)
            break
    else:
        continue
    break

# part 1
seen = set()
curr = start
while True:
    x, y = curr
    seen.add(curr)
    dx, dy = dir
    nx, ny = x + dx, y + dy
    if nx < 0 or ny < 0 or nx >= w or ny >= h:
        break
    if lines[ny][nx] == '#':
        dir = rot(dir)
    else:
        curr = (nx, ny)

print(len(seen))

# part 2
def simulate_loop(curr, dir):
    added_obstacle = curr[0] + dir[0], curr[1] + dir[1]
    seen = set()
    dir = rot(dir)
    while True:
        x, y = curr
        k = dir, x, y
        if k in seen:
            return True
        seen.add(k)
        dx, dy = dir
        nx, ny = x + dx, y + dy
        if nx < 0 or ny < 0 or nx >= w or ny >= h:
            return False
        if lines[ny][nx] == '#' or (nx, ny) == added_obstacle:
            dir = rot(dir)
        else:
            curr = (nx, ny)

added = set()
curr = start
dir = (0, -1)
seen = set()
while True:
    x, y = curr
    seen.add(curr)
    dx, dy = dir
    nx, ny = x + dx, y + dy
    if nx < 0 or ny < 0 or nx >= w or ny >= h:
        break
    if lines[ny][nx] == '#':
        dir = rot(dir)
    else:
        npos = nx, ny
        if npos != start and npos not in seen and simulate_loop((x, y), dir):
            added.add(npos)
        curr = npos

print(len(added))
