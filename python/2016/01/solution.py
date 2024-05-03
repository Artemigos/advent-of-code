import common

data = common.read_file()
move_strs = data.split(', ')

pos = (0, 0)
direction = (0, -1)

def move(pos, offset, times=1):
    return (pos[0]+offset[0]*times, pos[1]+offset[1]*times)

visited = set()
looking_for_repeats = True
part2_result = 0
for m in move_strs:
    dir_change = m[0]
    move_val = int(m[1:])

    if dir_change == 'R':
        direction = (-direction[1], direction[0])
    else:
        direction = (direction[1], -direction[0])

    for i in range(move_val):
        pos = move(pos, direction)

        # part 2
        if looking_for_repeats:
            if pos in visited:
                part2_result = sum(pos)
                looking_for_repeats = False
            else:
                visited.add(pos)

print(sum(pos))
print(part2_result)
