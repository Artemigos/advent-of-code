import common

lines = common.read_file('2021/25/data.txt').splitlines()
w = len(lines[0])
h = len(lines)

board = {}
for y in range(h):
    for x in range(w):
        c = lines[y][x]
        if c != '.':
            board[(x, y)] = c

# part 1

i = 0
seen = set()
while True:
    i += 1
    new_board = {}
    for k in board:
        if board[k] != '>':
            new_board[k] = board[k]
            continue
        next_k = (k[0]+1)%w, k[1]
        if next_k not in board:
            new_board[next_k] = '>'
        else:
            new_board[k] = '>'
    board = new_board
    new_board = {}
    for k in board:
        if board[k] != 'v':
            new_board[k] = board[k]
            continue
        next_k = k[0], (k[1]+1)%h
        if next_k not in board:
            new_board[next_k] = 'v'
        else:
            new_board[k] = 'v'
    board = new_board

    acc = ''
    for y in range(h):
        for x in range(w):
            k = x, y
            if k in board:
                acc += board[k]
            else:
                acc += '.'
    if acc in seen:
        break
    seen.add(acc)

print(i)
