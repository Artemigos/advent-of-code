import numpy as np
import common

data = common.read_file().splitlines()
parsed = [common.extract_numbers(x) for x in data]

points = []

cp = [list(x) for x in parsed]

mx = 100000
my = 100000
mi = 0
for i in range(0, 10158+1):
    for p in cp:
        p[0] += p[2]
        p[1] += p[3]

    minx = min(map(lambda x: x[0], cp))
    maxx = max(map(lambda x: x[0], cp))
    miny = min(map(lambda x: x[1], cp))
    maxy = max(map(lambda x: x[1], cp))
    dx = maxx - minx
    dy = maxy - miny
    if dy < my:
        my = dy
        mx = dx
        mi = i

print(mi, mx, my)

minx = min(map(lambda x: x[0], cp))
miny = min(map(lambda x: x[1], cp))
board = np.zeros((mx+1, my+1))
for r in cp:
    x = r[0]-minx
    y = r[1]-miny
    board[x, y] = 1

for y in range(board.shape[1]):
    for x in range(board.shape[0]):
        if board[x, y] > 0:
            print('#', end='')
        else:
            print('.', end='')
    print()
