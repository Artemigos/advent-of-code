from collections import deque
import common

lines = common.read_file().splitlines()

# part 1

acc = 0
w = len(lines[0])
h = len(lines)
for x in range(w):
    for y in range(h):
        n = ord(lines[y][x])
        if (x == 0 or ord(lines[y][x-1]) > n) and (x == w-1 or ord(lines[y][x+1]) > n) and (y == 0 or ord(lines[y-1][x]) > n) and (y == h-1 or ord(lines[y+1][x]) > n):
            acc += n - 48 + 1

print(acc)

# part 2

# prepare data
board = []
for y in range(h):
    row = []
    for x in range(w):
        row.append(1 if lines[y][x] == '9' else 0)
    board.append(row)

def find_basin():
    for x in range(w):
        for y in range(h):
            if board[y][x] == 0:
                return x, y
    return None

sizes = []
basin = find_basin()
while basin is not None:
    size = 0
    q = deque([basin])
    while len(q) != 0:
        x, y = q.popleft()
        if board[y][x] == 1:
            continue
        size += 1
        board[y][x] = 1
        if x > 0:
            q.append((x-1, y))
        if x < w-1:
            q.append((x+1, y))
        if y > 0:
            q.append((x, y-1))
        if y < h-1:
            q.append((x, y+1))

    sizes.append(size)
    basin = find_basin()

sizes = sorted(sizes)
print(sizes[-3] * sizes[-2] * sizes[-1])
