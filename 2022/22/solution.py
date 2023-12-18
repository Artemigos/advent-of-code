import common

lines = common.read_file().splitlines()
board = lines[:-2]
directions = lines[-1]
walkable = set()
wall = set()
moves = []
start = None
rows = []
columns = []

for y in range(len(board)):
    for x in range(len(board[y])):
        if board[y][x] == '.':
            walkable.add((x, y))
            if y == 0 and start is None:
                start = (x, y)
        elif board[y][x] == '#':
            wall.add((x, y))

acc = ''
for c in directions:
    if not c.isdigit():
        if acc != '':
            moves.append(int(acc))
            acc = ''
        moves.append(c)
    else:
        acc += c
moves.append(int(acc))

# part 1
curr = start
c_dir = 0
for move in moves:
    if isinstance(move, int):
        if c_dir == 0:
            dx = 1
            dy = 0
        elif c_dir == 1:
            dx = 0
            dy = 1
        elif c_dir == 2:
            dx = -1
            dy = 0
        else:
            dx = 0
            dy = -1
        for _ in range(move):
            nxt = (curr[0]+dx, curr[1]+dy)
            if nxt in walkable:
                curr = nxt
            elif nxt in wall:
                break
            else: # wrap around
                if dx == 0: # find row
                    if dy == 1: # find min
                        nx = nxt[0]
                        ny = min([p[1] for p in list(walkable)+list(wall) if p[0] == nxt[0]])
                    else: # find max
                        nx = nxt[0]
                        ny = max([p[1] for p in list(walkable)+list(wall) if p[0] == nxt[0]])
                else: # find column
                    if dx == 1: # find min
                        nx = min([p[0] for p in list(walkable)+list(wall) if p[1] == nxt[1]])
                        ny = nxt[1]
                    else: # find max
                        nx = max([p[0] for p in list(walkable)+list(wall) if p[1] == nxt[1]])
                        ny = nxt[1]
                nxt = (nx, ny)
                if nxt in walkable:
                    curr = (nx, ny)
                elif nxt in wall:
                    break
                else:
                    raise '???'
    else: # rotate
        if move == 'R':
            c_dir += 1
        elif move == 'L':
            c_dir -= 1
        else:
            raise '???'
        c_dir %= 4

score = 1000*(curr[1]+1) + 4*(curr[0]+1) + c_dir
print(score)

# part 2
side = 50

# this is specific to my input:
# instead of trying to programatically analyze how the cube connects, I hardcoded the face transitions
def get_wrap(x, y, c_dir):
    if y == -1:
        if x // side == 1:
            return (0, x-50+150, 0)
        elif x // side == 2:
            return (x-100, len(board)-1, 3)
        else:
            raise '???'
    elif y == len(board):
        assert x//side == 0
        return (x+100, 0, 1)
    elif y == side and c_dir == 1:
        assert x//side == 2
        return (99, x-100+50, 2)
    elif y == 3*side and c_dir == 1:
        assert x//side == 1
        return (49, x-50+150, 2)
    elif y == 99 and c_dir == 3:
        assert x//side == 0
        return (50, x+50, 0)
    elif x == 49 and c_dir == 2:
        if y//side == 0:
            return (0, 149-y, 0)
        elif y//side == 1:
            return (y-50, 100, 1)
        else:
            raise '???'
    elif x == 150:
        assert y//side == 0
        return (99, 149-y, 2)
    elif x == 100 and c_dir == 0:
        if y//side == 1:
            return (y-50+100, 49, 3)
        elif y//side == 2:
            return (149, 49-(y-100), 2)
        else:
            raise '???'
    elif x == -1:
        if y//side == 2:
            return (50, 49-(y-100), 0)
        elif y//side == 3:
            return (y-150+50, 0, 1)
        else:
            raise '???'
    elif x == 50 and c_dir == 0:
        assert y//side == 3
        return (y-150+50, 149, 3)
    raise 'oh no'

def get_movement(c_dir):
    if c_dir == 0:
        dx = 1
        dy = 0
    elif c_dir == 1:
        dx = 0
        dy = 1
    elif c_dir == 2:
        dx = -1
        dy = 0
    else:
        dx = 0
        dy = -1
    return dx, dy


curr = start
c_dir = 0
for move in moves:
    if isinstance(move, int):
        dx, dy = get_movement(c_dir)
        for _ in range(move):
            nxt = (curr[0]+dx, curr[1]+dy)
            if nxt in walkable:
                curr = nxt
            elif nxt in wall:
                break
            else: # wrap around
                nx, ny, n_dir = get_wrap(nxt[0], nxt[1], c_dir)
                nxt = (nx, ny)
                if nxt in walkable:
                    curr = (nx, ny)
                    c_dir = n_dir
                    dx, dy = get_movement(c_dir)
                elif nxt in wall:
                    break
                else:
                    raise '???'
    else: # rotate
        if move == 'R':
            c_dir += 1
        elif move == 'L':
            c_dir -= 1
        else:
            raise '???'
        c_dir %= 4

score = 1000*(curr[1]+1) + 4*(curr[0]+1) + c_dir
print(score)
