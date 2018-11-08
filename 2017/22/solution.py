import common

data = common.read_file('2017/22/data.txt')
lines = data.splitlines()
steps_1 = 10000
steps_2 = 10000000
side = len(lines)
mid = int((side-1)/2)

# part 1

infected = set()
for y in range(side):
    for x in range(side):
        if lines[y][x] == '#':
            infected.add((x, y))


def rot_left(d):
    return d[1], -d[0]


def rot_right(d):
    return -d[1], d[0]


pos = (mid, mid)
direction = (0, -1)
added_infections = 0
for i in range(steps_1):
    # print(i)
    if pos in infected:
        direction = rot_right(direction)
        infected.remove(pos)
    else:
        direction = rot_left(direction)
        infected.add(pos)
        added_infections += 1
    pos = (pos[0]+direction[0], pos[1]+direction[1])

print(added_infections)

# part 2

s_infected = 1
s_weakened = 2
s_flagged = 3
infected = dict()
for y in range(side):
    for x in range(side):
        if lines[y][x] == '#':
            infected[(x, y)] = s_infected


def rev(d):
    return -d[0], -d[1]


pos = (mid, mid)
direction = (0, -1)
added_infections = 0
for i in range(steps_2):
    if pos in infected.keys():
        status = infected[pos]
        if status == s_infected:
            direction = rot_right(direction)
            infected[pos] = s_flagged
        elif status == s_weakened:
            infected[pos] = s_infected
            added_infections += 1
        else:  # s_flagged
            direction = rev(direction)
            infected.pop(pos)
    else:  # clean
        direction = rot_left(direction)
        infected[pos] = s_weakened
    pos = (pos[0]+direction[0], pos[1]+direction[1])

print(added_infections)
