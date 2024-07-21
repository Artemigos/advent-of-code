import common

data = tuple([tuple(x) for x in common.read_file().splitlines()])
w = len(data[0])
h = len(data)

# part 1
def calc_biodiversity(state):
    acc = 0
    for y in reversed(range(h)):
        for x in reversed(range(w)):
            acc <<= 1
            if state[y][x] == '#':
                acc += 1
    return acc

seen = set([data])
curr = data

def check_if_bug(x, y):
    return 1 if x in range(w) and y in range(h) and curr[y][x] == '#' else 0

while True:
    new_state = []
    for y in range(h):
        new_row = []
        for x in range(w):
            bug_neighbors = check_if_bug(x-1, y) + check_if_bug(x+1, y) + check_if_bug(x, y-1) + check_if_bug(x, y+1)
            if curr[y][x] == '#':
                new_row.append('#' if bug_neighbors == 1 else '.')
            else:
                new_row.append('#' if bug_neighbors == 1 or bug_neighbors == 2 else '.')
        new_state.append(tuple(new_row))
    curr = tuple(new_state)
    if curr in seen:
        print(calc_biodiversity(curr))
        break
    seen.add(curr)

# part 2
def get_neighbors(bug):
    result = []

    level, x, y = bug
    if x == 0:
        result.append((level-1, 1, 2))
    elif x == 4:
        result.append((level-1, 3, 2))

    if y == 0:
        result.append((level-1, 2, 1))
    elif y == 4:
        result.append((level-1, 2, 3))

    if (x, y) == (1, 2):
        for inner_y in range(5):
            result.append((level+1, 0, inner_y))
    elif (x, y) == (3, 2):
        for inner_y in range(5):
            result.append((level+1, 4, inner_y))
    elif (x, y) == (2, 1):
        for inner_x in range(5):
            result.append((level+1, inner_x, 0))
    elif (x, y) == (2, 3):
        for inner_x in range(5):
            result.append((level+1, inner_x, 4))

    if x > 0 and (x, y) != (3, 2):
        result.append((level, x-1, y))
    if x < 4 and (x, y) != (1, 2):
        result.append((level, x+1, y))
    if y > 0 and (x, y) != (2, 3):
        result.append((level, x, y-1))
    if y < 4 and (x, y) != (2, 1):
        result.append((level, x, y+1))

    return result

bugs = []
for y in range(h):
    for x in range(w):
        if data[y][x] == '#':
            bugs.append((0, x, y))

for i in range(200):
    to_check = set()
    new_bugs = []
    for bug in bugs:
        to_check.add(bug)
        for n in get_neighbors(bug):
            to_check.add(n)

    for spot in to_check:
        neighbors = sum((1 for n in get_neighbors(spot) if n in bugs))
        if spot in bugs and neighbors == 1:
            new_bugs.append(spot)
        elif spot not in bugs and (neighbors == 1 or neighbors == 2):
            new_bugs.append(spot)

    bugs = new_bugs

print(len(bugs))
