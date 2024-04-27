import common
from collections import deque

board = common.read_file().splitlines()
w = len(board[0])
h = len(board)

def connects_left(x, y):
    return x > 0 and board[y][x-1] in ['-', 'L', 'F']
def connects_right(x, y):
    return x < w-1 and board[y][x+1] in ['-', 'J', '7']
def connects_up(x, y):
    return y > 0 and board[y-1][x] in ['|', '7', 'F']
def connects_down(x, y):
    return y < h-1 and board[y+1][x] in ['|', 'L', 'J']

start = (0, 0)
for y in range(h):
    for x in range(w):
        if board[y][x] == 'S':
            start = (x, y)
            if connects_left(x, y) and connects_up(x, y):
                board[y] = board[y].replace('S', 'J')
            elif connects_left(x, y) and connects_right(x, y):
                board[y] = board[y].replace('S', '-')
            elif connects_left(x, y) and connects_down(x, y):
                board[y] = board[y].replace('S', '7')
            elif connects_up(x, y) and connects_right(x, y):
                board[y] = board[y].replace('S', 'L')
            elif connects_up(x, y) and connects_down(x, y):
                board[y] = board[y].replace('S', '|')
            elif connects_right(x, y) and connects_down(x, y):
                board[y] = board[y].replace('S', 'F')
            else:
                assert False, 'should not reach here'
            break
    else:
        continue
    break

# part 1
q: deque[tuple[int, int, int]] = deque([(start[0], start[1], 0)])
max_dist = 0
seen: set[tuple[int, int]] = set()
on_loop: set[tuple[int, int]] = set()
while len(q) > 0:
    x, y, dist = q.popleft()
    on_loop.add((x, y))
    if (x, y) in seen:
        continue
    if dist > max_dist:
        max_dist = dist
    seen.add((x, y))
    if connects_left(x, y) and connects_right(x-1, y):
        q.append((x-1, y, dist+1))
    if connects_right(x, y) and connects_left(x+1, y):
        q.append((x+1, y, dist+1))
    if connects_up(x, y) and connects_down(x, y-1):
        q.append((x, y-1, dist+1))
    if connects_down(x, y) and connects_up(x, y+1):
        q.append((x, y+1, dist+1))

print(max_dist)

# part 2
acc = 0
for y in range(h):
    inside = False
    entered_loop_with = None
    for x in range(w):
        we_in = (x, y) in on_loop
        c = board[y][x]
        if we_in and c == '|':
            inside = not inside
        elif we_in and c in ['L', 'F']:
            entered_loop_with = c
        elif we_in and c == '-':
            pass
        elif we_in and c in ['J', '7']:
            if (entered_loop_with, c) == ('L', '7') or (entered_loop_with, c) == ('F', 'J'):
                inside = not inside
            entered_loop_with = None
        elif we_in:
            assert False, 'should never happen'
        else:
            if inside:
                acc += 1

print(acc)
