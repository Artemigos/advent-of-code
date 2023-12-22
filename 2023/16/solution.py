import common
from collections import deque

board = common.read_file().splitlines()
w = len(board[0])
h = len(board)

LEFT = 1
UP = 2
RIGHT = 3
DOWN = 4

def rot(dir, c):
    if dir == LEFT:
        if c == '/':
            return [DOWN]
        if c == '\\':
            return [UP]
        if c == '|':
            return [UP, DOWN]
        return [LEFT]
    if dir == RIGHT:
        if c == '/':
            return [UP]
        if c == '\\':
            return [DOWN]
        if c == '|':
            return [UP, DOWN]
        return [RIGHT]
    if dir == UP:
        if c == '/':
            return [RIGHT]
        if c == '\\':
            return [LEFT]
        if c == '-':
            return [LEFT, RIGHT]
        return [UP]
    if dir == DOWN:
        if c == '/':
            return [LEFT]
        if c == '\\':
            return [RIGHT]
        if c == '-':
            return [LEFT, RIGHT]
        return [DOWN]
    assert False, 'should never reach here'

def off(pt, dir):
    if dir == LEFT:
        return (pt[0]-1, pt[1])
    if dir == RIGHT:
        return (pt[0]+1, pt[1])
    if dir == UP:
        return (pt[0], pt[1]-1)
    if dir == DOWN:
        return (pt[0], pt[1]+1)
    assert False, 'should never reach here'

# part 1
def calc_energy(board, entry, entry_dir):
    seen = set()
    pts = set()
    q = deque([(entry, entry_dir)])
    while len(q) > 0:
        pt, dir = q.popleft()
        if (pt, dir) in seen:
            continue
        x, y = pt
        if x < 0 or x >= w or y < 0 or y >= h:
            continue
        seen.add((pt, dir))
        pts.add(pt)
        for d in rot(dir, board[y][x]):
            q.append((off(pt, d), d))
    return len(pts)

print(calc_energy(board, (0, 0), RIGHT))

# part 2
mx = 0
for x in range(w):
    mx = max(mx, calc_energy(board, (x, 0), DOWN))
    mx = max(mx, calc_energy(board, (x, h-1), UP))
for y in range(w):
    mx = max(mx, calc_energy(board, (0, y), RIGHT))
    mx = max(mx, calc_energy(board, (w-1, y), LEFT))
print(mx)
