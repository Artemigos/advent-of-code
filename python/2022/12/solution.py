from collections import deque
import common

board = common.read_file().splitlines()
w = len(board[0])
h = len(board)
start = None
end = None

for y in range(h):
    board[y] = list(board[y])
    for x in range(w):
        if board[y][x] == 'S':
            start = (x, y)
            board[y][x] = 'a'
        if board[y][x] == 'E':
            end = (x, y)
            board[y][x] = 'z'

def height(x, y):
    if x < 0 or x >= w or y < 0 or y >= h:
        return None
    return ord(board[y][x]) - ord('a')

# part 1
def find_from(sx, sy):
    moves = deque([(sx, sy, 0)])
    seen = set()
    while len(moves) > 0:
        x, y, depth = moves.popleft()
        if (x, y) in seen:
            continue
        seen.add((x, y))

        if end == (x, y):
            return depth

        ch = height(x, y)

        neighbors = [
            (x-1, y),
            (x+1, y),
            (x, y-1),
            (x, y+1),
        ]

        for nx, ny in neighbors:
            nh = height(nx, ny)
            if nh is not None and nh - ch <= 1:
                moves.append((nx, ny, depth+1))

print(find_from(start[0], start[1]))

# part 2
acc = None

# TODO: optimize to search from end and mark distances
for y in range(h):
    for x in range(w):
        if board[y][x] == 'a':
            dist = find_from(x, y)
            if acc is None or (dist is not None and dist < acc):
                acc = dist

print(acc)
