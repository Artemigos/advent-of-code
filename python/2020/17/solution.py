import common

lines = common.read_file().splitlines()

# part 1
space = set()

for y in range(len(lines)):
    l = lines[y]
    for x in range(len(l)):
        if l[x] == '#':
            space.add((x, y, 0))

def iter_neighbors(point):
    x, y, z = point
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            for dz in range(-1, 2):
                if dx == dy == dz == 0:
                    continue
                yield (x+dx, y+dy, z+dz)

curr_space = space
for _ in range(6):
    new_space = set()
    neighbors = set()
    for a in curr_space:
        active_count = 0
        for n in iter_neighbors(a):
            if n in curr_space:
                active_count += 1
            else:
                neighbors.add(n)
        if active_count == 2 or active_count == 3:
            new_space.add(a)
    for n in neighbors:
        active_count = 0
        for nn in iter_neighbors(n):
            if nn in curr_space:
                active_count += 1
        if active_count == 3:
            new_space.add(n)
    curr_space = new_space

print(len(curr_space))

# part 2
space = set()

for y in range(len(lines)):
    l = lines[y]
    for x in range(len(l)):
        if l[x] == '#':
            space.add((x, y, 0, 0))

def iter_neighbors4(point):
    x, y, z, w = point
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            for dz in range(-1, 2):
                for dw in range(-1, 2):
                    if dx == dy == dz == dw == 0:
                        continue
                    yield (x+dx, y+dy, z+dz, w+dw)

curr_space = space
for _ in range(6):
    new_space = set()
    neighbors = set()
    for a in curr_space:
        active_count = 0
        for n in iter_neighbors4(a):
            if n in curr_space:
                active_count += 1
            else:
                neighbors.add(n)
        if active_count == 2 or active_count == 3:
            new_space.add(a)
    for n in neighbors:
        active_count = 0
        for nn in iter_neighbors4(n):
            if nn in curr_space:
                active_count += 1
        if active_count == 3:
            new_space.add(n)
    curr_space = new_space

print(len(curr_space))
