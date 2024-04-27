import common

board = common.read_file('2020/11/data.txt').splitlines()
h = len(board)
w = len(board[0])

def count_seats(board, x_range=None, y_range=None):
    if x_range is None:
        x_range = range(w)
    if y_range is None:
        y_range = range(h)
    free = 0
    occupied = 0
    for x in x_range:
        if x < 0 or x >= w:
            continue
        for y in y_range:
            if y < 0 or y >= h:
                continue
            c = board[y][x]
            if c == 'L':
                free += 1
            elif c == '#':
                occupied += 1
    return free, occupied

def cpy(board):
    result = []
    for l in board:
        line = []
        for c in l:
            line.append(c)
        result.append(line)
    return result

# part 1
changed = True
brd_prev = cpy(board)

while changed:
    changed = False
    brd = cpy(brd_prev)
    for x in range(w):
        for y in range(h):
            c = brd_prev[y][x]
            if c == '.':
                continue
            empty, occupied = count_seats(
                brd_prev, range(x-1, x+2), range(y-1, y+2))
            if c == 'L':
                if occupied == 0:
                    changed = True
                    brd[y][x] = '#'
            else:  # '#'
                if occupied >= 4+1:  # +1 because counting counts itself
                    changed = True
                    brd[y][x] = 'L'
    brd_prev = brd

empty, occupied = count_seats(brd_prev)
print(occupied)

# part 2
def count_occupied(board, x, y):
    offsets = []
    for xx in range(-1, 2):
        for yy in range(-1, 2):
            offsets.append((xx, yy))
    offsets.remove((0, 0))

    acc = 0
    for of in offsets:
        dx, dy = of
        nx, ny = x, y
        while True:
            nx, ny = nx + dx, ny + dy
            if nx < 0 or ny < 0 or nx >= w or ny >= h:
                break
            c = board[ny][nx]
            if c == '#':
                acc += 1
                break
            elif c == 'L':
                break

    return acc

changed = True
brd_prev = cpy(board)

while changed:
    changed = False
    brd = cpy(brd_prev)
    for x in range(w):
        for y in range(h):
            c = brd_prev[y][x]
            if c == '.':
                continue
            occupied = count_occupied(brd_prev, x, y)
            if c == 'L':
                if occupied == 0:
                    changed = True
                    brd[y][x] = '#'
            else:  # '#'
                if occupied >= 5:  # +1 because counting counts itself
                    changed = True
                    brd[y][x] = 'L'
    brd_prev = brd

empty, occupied = count_seats(brd_prev)
print(occupied)
