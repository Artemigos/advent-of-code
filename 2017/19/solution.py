import common

data = common.read_file('2017/19/data.txt')
board = data.splitlines()
start_x = board[0].index('|')

direction = (1, 0)

turns = {
    (1, 0): [(0, 1), (0, -1)],
    (-1, 0): [(0, 1), (0, -1)],
    (0, 1): [(1, 0), (-1, 0)],
    (0, -1): [(1, 0), (-1, 0)]
}

current = (0, start_x)

def add(pos, offset):
    return (pos[0] + offset[0], pos[1] + offset[1])

def at(pos):
    return board[pos[0]][pos[1]]

def update_direction(direction):
    if at(add(current, direction)) != ' ':
        return direction
    if at(add(current, turns[direction][0])) != ' ':
        return turns[direction][0]
    if at(add(current, turns[direction][1])) != ' ':
        return turns[direction][1]
    return None

acc = ''
steps = 1
while True:
    direction = update_direction(direction)
    if direction is None:
        break
    current = add(current, direction)
    steps += 1
    val = at(current)
    if val != '-' and val != '|' and val != '+':
        acc += val

print(acc)
print(steps)
