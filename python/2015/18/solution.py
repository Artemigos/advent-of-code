import common

lines = common.read_file().splitlines()

initial_state = []

for line in lines:
    row = []
    for c in line:
        val = 1 if c == '#' else 0
        row.append(val)
    initial_state.append(row)

w = len(initial_state[0])
h = len(initial_state)

current = initial_state
steps = 100

def run_step(current):
    def at(x, y):
        if x < 0 or x >= w or y < 0 or y >= h:
            return 0
        return current[y][x]

    result = []
    for y in range(h):
        row = []
        for x in range(w):
            neighbors = sum([
                at(x, y-1),
                at(x+1, y-1),
                at(x+1, y),
                at(x+1, y+1),
                at(x, y+1),
                at(x-1, y+1),
                at(x-1, y),
                at(x-1, y-1)
            ])
            me = current[y][x]
            if me == 1 and (neighbors == 2 or neighbors == 3):
                row.append(1)
            elif me == 0 and neighbors == 3:
                row.append(1)
            else:
                row.append(0)
        result.append(row)
    return result

# part 1
for i in range(steps):
    current = run_step(current)

on_num = sum(map(sum, current))
print(on_num)

# part 2
current = initial_state

def update_corners():
    current[0][0] = 1
    current[0][-1] = 1
    current[-1][0] = 1
    current[-1][-1] = 1

update_corners()

for i in range(steps):
    current = run_step(current)
    update_corners()

on_num = sum(map(sum, current))
print(on_num)
