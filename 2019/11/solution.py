import common
from collections import defaultdict
year_common = common.import_year_common(2019)

tape = common.extract_numbers(common.read_file('2019/11/data.txt'))

state = defaultdict(lambda: 0)
pos = 0, 0
curr_dir = 0

X = 0
Y = 1

def move_forward():
    global pos
    global curr_dir
    if curr_dir == 0:
        offset = 0, -1
    elif curr_dir == 1:
        offset = 1, 0
    elif curr_dir == 2:
        offset = 0, 1
    else:
        offset = -1, 0
    pos = pos[X]+offset[X], pos[Y]+offset[Y]

def robot_input():
    global pos
    global state
    while True:
        yield state[pos]

# part 1
mem = year_common.tape_to_mem(tape)
try:
    iterator = year_common.run_intcode(mem, robot_input())
    while True:
        color = next(iterator)
        state[pos] = color
        direction = next(iterator)
        if direction == 0:
            curr_dir -= 1
        else:
            curr_dir += 1
        curr_dir %= 4
        move_forward()
except StopIteration:
    pass

print('part 1:', len(state))

# part 2
state = defaultdict(lambda: 0)
pos = 0, 0
state[pos] = 1
curr_dir = 0

mem = year_common.tape_to_mem(tape)
try:
    iterator = year_common.run_intcode(mem, robot_input())
    while True:
        color = next(iterator)
        state[pos] = color
        direction = next(iterator)
        if direction == 0:
            curr_dir -= 1
        else:
            curr_dir += 1
        curr_dir %= 4
        move_forward()
except StopIteration:
    pass

min_x = min(map(lambda x: x[0], state.keys()))
max_x = max(map(lambda x: x[0], state.keys()))
min_y = min(map(lambda x: x[1], state.keys()))
max_y = max(map(lambda x: x[1], state.keys()))

print('part 2:')
for y in range(min_y, max_y+1):
    for x in range(min_x, max_x+1):
        print('▓' if state[x, y] == 1 else ' ', end='')
    print()
