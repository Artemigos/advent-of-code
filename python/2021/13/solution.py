from collections import defaultdict
import common

lines = common.read_file().splitlines()
board = defaultdict(lambda: 0)
for i in range(len(lines)):
    line = lines[i]
    if line == '':
        break
    x, y = common.to_int(line.split(','))
    board[(x, y)] = 1

folds = []
for line in lines[i+1:]:
    axis, value = line.split()[2].split('=')
    folds.append((axis, int(value)))

# part 1 and 2

for i in range(len(folds)):
    axis, middle = folds[i]
    new_board = defaultdict(lambda: 0)
    if axis == 'x':
        for x, y in board:
            reflected = 2*middle - x
            if reflected < middle:
                new_board[(reflected, y)] = 1
            else:
                new_board[(x, y)] = 1
    else:
        for x, y in board:
            reflected = 2*middle - y
            if reflected < middle:
                new_board[(x, reflected)] = 1
            else:
                new_board[(x, y)] = 1
    board = new_board

    if i == 0:
        print(len(board))

w = max(map(lambda x: x[0], board.keys())) + 1
h = max(map(lambda x: x[1], board.keys())) + 1

for y in range(h):
    for x in range(w):
        if (x, y) in board:
            print('#', end='')
        else:
            print(' ', end='')
    print()
