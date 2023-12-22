import common
from queue import PriorityQueue

board = common.read_file().splitlines()
w = len(board[0])
h = len(board)

LEFT = 0
UP = 1
RIGHT = 2
DOWN = 3

def turns(dir):
    if dir == LEFT or dir == RIGHT:
        return [UP, DOWN, dir]
    else:
        return [LEFT, RIGHT, dir]

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

Pos = tuple[int, int]
Dir = tuple[int, int]
QItem = tuple[int, Pos, Dir]
KItem = tuple[Pos, Dir]

# part 1
q: PriorityQueue[QItem] = PriorityQueue()
q.put((int(board[0][1]), (1, 0), (RIGHT, 1)))
q.put((int(board[1][0]), (0, 1), (DOWN, 1)))
seen: set[KItem] = set()

while not q.empty():
    heat, (x, y), (dir, streak) = q.get()
    k = (x, y), (dir, streak)
    if k in seen:
        continue
    seen.add(k)
    if (x, y) == (w-1, h-1):
        print(heat)
        break
    for t in turns(dir):
        nx, ny = off((x, y), t)       
        if nx < 0 or nx >= w or ny < 0 or ny >= h:
            continue
        s = streak + 1 if t == dir else 1
        if s > 3:
            continue
        nh = int(board[ny][nx])
        el = (heat+nh, (nx, ny), (t, s))
        q.put(el)

# part 2
q = PriorityQueue()
q.put((int(board[0][1]), (1, 0), (RIGHT, 1)))
q.put((int(board[1][0]), (0, 1), (DOWN, 1)))
seen = set()

while not q.empty():
    heat, (x, y), (dir, streak) = q.get()
    k = (x, y), (dir, streak)
    if k in seen:
        continue
    seen.add(k)
    if (x, y) == (w-1, h-1) and streak >= 4:
        print(heat)
        break
    for t in turns(dir):
        nx, ny = off((x, y), t)       
        if nx < 0 or nx >= w or ny < 0 or ny >= h:
            continue
        if streak < 4 and t != dir:
            continue
        s = streak + 1 if t == dir else 1
        if s > 10:
            continue
        nh = int(board[ny][nx])
        el = (heat+nh, (nx, ny), (t, s))
        q.put(el)
