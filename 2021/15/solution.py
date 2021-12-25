from collections import deque, defaultdict
from queue import PriorityQueue
import common

lines = common.read_file('2021/15/data.txt').splitlines()
board = [common.to_int(x) for x in lines]
w = len(lines[0])
h = len(lines)

# part 1

def solve(board, w, h):
    distances = {}
    q = PriorityQueue()
    q.put((0, (1, 0)))
    q.put((0, (0, 1)))
    while not q.empty():
        dist, coords = q.get()
        x, y = coords
        if x < 0 or x >= w or y < 0 or y >= h:
            continue
        dist += board[y][x]
        if (x, y) in distances and dist >= distances[(x, y)]:
            continue
        distances[(x, y)] = dist
        if (x, y) == (w-1, h-1):
            break
        q.put((dist, (x-1, y)))
        q.put((dist, (x+1, y)))
        q.put((dist, (x, y-1)))
        q.put((dist, (x, y+1)))

    print(distances[(w-1, h-1)])

solve(board, w, h)

# part 2

extended_board = []
for ty in range(5):
    for y in range(h):
        row = []
        for tx in range(5):
            for x in range(w):
                num = board[y][x] + ty + tx
                while num > 9:
                    num -= 9
                row.append(num)
        extended_board.append(row)

solve(extended_board, w*5, h*5)