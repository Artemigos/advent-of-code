import common
from collections import defaultdict

lines = common.read_file().splitlines()
elves = set()

for y in range(len(lines)):
    for x in range(len(lines[0])):
        if lines[y][x] == '#':
            elves.add((x, y))

def choose_move(i, elves, x, y):
    # all neighbors
    ns = [
        (x-1, y-1), (x, y-1), (x+1, y-1),
        (x+1, y), (x+1, y+1),
        (x, y+1), (x-1, y+1),
        (x-1, y)]

    # if no elves close, don't move
    for n in ns:
        if n in elves:
            break
    else:
        return None

    # neighbors in order for north, south, west, east
    dirs = [
        ns[:3],
        ns[4:7],
        ns[6:] + ns[:1],
        ns[2:5],
    ]

    # positions after move in order for north, south, west, east
    dir_results = [
        (x, y-1),
        (x, y+1),
        (x-1, y),
        (x+1, y),
    ]

    # check moves in all directions, order based on iteration
    for di in range(len(dirs)):
        idx = (i+di) % len(dirs)
        if all([p not in elves for p in dirs[idx]]):
            return dir_results[idx]

    return None

curr_elves = elves
i = 0
while True:
    moved = False
    moves = dict()
    destinations = defaultdict(lambda: 0)
    for e in curr_elves:
        move = choose_move(i, curr_elves, *e)
        if move is not None:
            moves[e] = move
            destinations[move] += 1
    new_elves = set()
    for e in curr_elves:
        if e not in moves:
            new_elves.add(e)
            continue
        m = moves[e]
        if destinations[m] > 1:
            new_elves.add(e)
            continue
        new_elves.add(m)
        moved = True
    curr_elves = new_elves
    i += 1

    # part 1
    if i == 10:
        min_x = min([e[0] for e in curr_elves])
        max_x = max([e[0] for e in curr_elves])
        min_y = min([e[1] for e in curr_elves])
        max_y = max([e[1] for e in curr_elves])

        print((max_x-min_x+1)*(max_y-min_y+1)-len(elves))

    if not moved:
        break

# part 2
print(i)
