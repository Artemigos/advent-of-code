import common

lines = common.read_file().splitlines()
w = len(lines[0])
h = len(lines)

rolling_stones = set()
stationary_stones = set()
for y in range(h):
    for x in range(w):
        if lines[y][x] == '#':
            stationary_stones.add((x, y))
        elif lines[y][x] == 'O':
            rolling_stones.add((x, y))

# part 1
def move_north():
    for y in range(h):
        for x in range(w):
            if (x, y) not in rolling_stones:
                continue
            ny = y
            while True:
                ny -= 1
                if ny < 0:
                    break
                if (x, ny) in stationary_stones or (x, ny) in rolling_stones:
                    break
            ny += 1
            if y != ny:
                rolling_stones.remove((x, y))
                rolling_stones.add((x, ny))

move_north()

def calculate_load():
    acc = 0
    for y in range(h):
        for x in range(w):
            if (x, y) in rolling_stones:
                acc += h-y
    return acc
print(calculate_load())

# part 2
def move_west():
    for x in range(w):
        for y in range(h):
            if (x, y) not in rolling_stones:
                continue
            nx = x
            while True:
                nx -= 1
                if nx < 0:
                    break
                if (nx, y) in stationary_stones or (nx, y) in rolling_stones:
                    break
            nx += 1
            if x != nx:
                rolling_stones.remove((x, y))
                rolling_stones.add((nx, y))

def move_south():
    for y in range(h-1, -1, -1):
        for x in range(w):
            if (x, y) not in rolling_stones:
                continue
            ny = y
            while True:
                ny += 1
                if ny >= h:
                    break
                if (x, ny) in stationary_stones or (x, ny) in rolling_stones:
                    break
            ny -= 1
            if y != ny:
                rolling_stones.remove((x, y))
                rolling_stones.add((x, ny))

def move_east():
    for x in range(w-1, -1, -1):
        for y in range(h):
            if (x, y) not in rolling_stones:
                continue
            nx = x
            while True:
                nx += 1
                if nx >= w:
                    break
                if (nx, y) in stationary_stones or (nx, y) in rolling_stones:
                    break
            nx -= 1
            if x != nx:
                rolling_stones.remove((x, y))
                rolling_stones.add((nx, y))

LIMIT = 1000000000
seen = {}
def verity_state(at_cycle_pos, i):
    assert at_cycle_pos in range(4)
    k = 0
    for y in range(h):
        for x in range(w):
            k <<= 1
            if (x, y) in rolling_stones:
                k += 1
    k <<= 2
    k += at_cycle_pos
    if k in seen:
        loop_size = i - seen[k]
        increases = (LIMIT - i) // loop_size
        i += increases * loop_size
    else:
        seen[k] = i
    return i

verity_state(1, 0)
move_west()
verity_state(2, 0)
move_south()
verity_state(3, 0)
move_east()

i = 1
while i < LIMIT:
    i = verity_state(0, i)
    move_north()
    i = verity_state(1, i)
    move_west()
    i = verity_state(2, i)
    move_south()
    i = verity_state(3, i)
    move_east()

    i += 1

print(calculate_load())
