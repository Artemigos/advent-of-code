from collections import defaultdict
import common

file_lines = common.read_file().splitlines()
lines = []
for line in file_lines:
    points = line.split(' -> ')
    x1,y1 = common.to_int(points[0].split(','))
    x2,y2 = common.to_int(points[1].split(','))
    lines.append((x1, y1, x2, y2))

# part 1 and 2
board = defaultdict(lambda: 0)
board_full = defaultdict(lambda: 0)
for line  in lines:
    x1, y1, x2, y2 = line
    if x1 == x2:
        for i in range(min(y1, y2), max(y1, y2)+1):
            board[(x1, i)] += 1
            board_full[(x1, i)] += 1
    elif y1 == y2:
        for i in range(min(x1, x2), max(x1, x2)+1):
            board[(i, y1)] += 1
            board_full[(i, y1)] += 1
    else: # diagonal
        x_sign = 1 if x2 > x1 else -1
        y_sign = 1 if y2 > y1 else -1
        curr = x1, y1
        for i in range(abs(x2-x1)+1):
            x = x1 + i*x_sign
            y = y1 + i*y_sign
            board_full[(x, y)] += 1

print(len(list(filter(lambda x: x > 1, board.values()))))
print(len(list(filter(lambda x: x > 1, board_full.values()))))
