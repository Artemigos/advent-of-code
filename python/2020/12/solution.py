import common

lines = common.read_file('2020/12/data.txt').splitlines()
lines = list(map(lambda l: (l[0], int(l[1:])), lines))

def turn_right(pos):
    return -pos[1], pos[0]

def turn_left(pos):
    return pos[1], -pos[0]

# part 1
curr_pos = (0, 0)
curr_rot = (1, 0)

for l in lines:
    instr, num = l
    if instr == 'N':
        curr_pos = curr_pos[0], curr_pos[1] - num
    elif instr == 'S':
        curr_pos = curr_pos[0], curr_pos[1] + num
    elif instr == 'W':
        curr_pos = curr_pos[0] - num, curr_pos[1]
    elif instr == 'E':
        curr_pos = curr_pos[0] + num, curr_pos[1]
    elif instr == 'L':
        for _ in range(num//90):
            curr_rot = turn_left(curr_rot)
    elif instr == 'R':
        for _ in range(num//90):
            curr_rot = turn_right(curr_rot)
    elif instr == 'F':
        curr_pos = curr_pos[0] + curr_rot[0]*num, curr_pos[1] + curr_rot[1]*num
    else:
        raise 'unknown instruction'

print(abs(curr_pos[0]) + abs(curr_pos[1]))

# part 2
curr_pos = (0, 0)
curr_way = (10, -1)

for l in lines:
    instr, num = l
    if instr == 'N':
        curr_way = curr_way[0], curr_way[1] - num
    elif instr == 'S':
        curr_way = curr_way[0], curr_way[1] + num
    elif instr == 'W':
        curr_way = curr_way[0] - num, curr_way[1]
    elif instr == 'E':
        curr_way = curr_way[0] + num, curr_way[1]
    elif instr == 'L':
        for _ in range(num//90):
            curr_way = turn_left(curr_way)
    elif instr == 'R':
        for _ in range(num//90):
            curr_way = turn_right(curr_way)
    elif instr == 'F':
        curr_pos = curr_pos[0] + curr_way[0]*num, curr_pos[1] + curr_way[1]*num
    else:
        raise 'unknown instruction'

print(abs(curr_pos[0]) + abs(curr_pos[1]))
