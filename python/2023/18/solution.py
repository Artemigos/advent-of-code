import common

lines = common.read_file().splitlines()

# parse
moves = [(x.split(' ')[0], int(x.split(' ')[1])) for x in lines]
def off(x, y, dir, amount=1):
    if dir == 'U':
        return x, y-amount
    if dir == 'D':
        return x, y+amount
    if dir == 'L':
        return x-amount, y
    if dir == 'R':
        return x+amount, y
    assert False, 'unknown direction ' + dir

def corner(d1, d2):
    if d1 == 'R':
        if d2 == 'U':
            return 'J'
        if d2 == 'D':
            return '7'
        assert False, 'oh no ' + d1 + d2
    if d1 == 'L':
        if d2 == 'U':
            return 'L'
        if d2 == 'D':
            return 'F'
        assert False, 'oh no ' + d1 + d2
    if d1 == 'U':
        if d2 == 'L':
            return '7'
        if d2 == 'R':
            return 'F'
        assert False, 'oh no ' + d1 + d2
    if d1 == 'D':
        if d2 == 'L':
            return 'J'
        if d2 == 'R':
            return 'L'
        assert False, 'oh no ' + d1 + d2
    assert False, 'unknown direction ' + d1

# part 1
board = {}
x, y = 0, 0
for move_i in range(len(moves)):
    move = moves[move_i]
    dir, num = move
    edge_c = '-' if dir in ['L', 'R'] else '|'
    for i in range(num):
        x, y =  off(x, y, dir)
        board[(x, y)] = edge_c
    next_dir = moves[(move_i+1)%len(moves)][0]
    board[(x, y)] = corner(dir, next_dir)

min_x = min((x[0] for x in board.keys()))
max_x = max((x[0] for x in board.keys()))
min_y = min((x[1] for x in board.keys()))
max_y = max((x[1] for x in board.keys()))

acc = len(board)
for y in range(min_y, max_y+1):
    we_in = False
    edge_entered_with = None
    for x in range(min_x, max_x+1):
        c = board.get((x, y))
        if c is None:
            if we_in:
                acc += 1
        elif c == '|':
            we_in = not we_in
        elif c in ['F', 'L']:
            edge_entered_with = c
        elif c in ['7', 'J']:
            assert edge_entered_with is not None, 'did not enter edge'
            if edge_entered_with == 'F' and c == 'J' or edge_entered_with == 'L' and c == '7':
                we_in = not we_in
print(acc)

# part 2
moves = []
for line in lines:
    _, _, color = line.split(' ')
    num = int(color[2:7], base=16)
    dir_num = int(color[7:8], base=16)
    if dir_num == 0:
        dir = 'R'
    elif dir_num == 1:
        dir = 'D'
    elif dir_num == 2:
        dir = 'L'
    elif dir_num == 3:
        dir = 'U'
    else:
        assert False, 'unknown direction'
    moves.append((dir, num))

points = []

from collections import defaultdict
vert_bars = defaultdict(lambda: common.ranges())
hori_bars = defaultdict(lambda: common.ranges())

x, y = 0, 0
for move_i in range(len(moves)):
    move = moves[move_i]
    dir, num = move
    bx, by = off(x, y, dir)
    x, y =  off(x, y, dir, num)
    if bx == x:
        ly, ry = (by, y) if by < y else (y+1, by+1)
        vert_bars[x] = vert_bars[x].union(range(ly, ry))
    else:
        lx, rx = (bx, x) if bx < x else (x+1, bx+1)
        hori_bars[y] = hori_bars[y].union(range(lx, rx))
    points.append((x, y))

vert_stops = sorted(vert_bars.keys())
hori_stops = sorted(hori_bars.keys())
all_x = [x[0] for x in points]
all_y = [x[1] for x in points]
min_x = min(all_x)
max_x = max(all_x)
min_y = min(all_y)
max_y = max(all_y)

xs = common.ranges(min_x, max_x+1)
ys = common.ranges(min_y, max_y+1)
w = len(xs)
h = len(ys)

for x in all_x:
    xs = xs.difference(range(x, x+1))

for y in all_y:
    ys = ys.difference(range(y, y+1))

xranges = sorted(xs._ranges, key=lambda r: r.start)
yranges = sorted(ys._ranges, key=lambda r: r.start)

acc = len(points)
for stop in vert_bars:
    acc += len(vert_bars[stop])
for stop in hori_bars:
    acc += len(hori_bars[stop])
for yr in yranges:
    in_rs = common.ranges()
    rstart = None
    for stop in vert_stops:
        if len(yr) != len(vert_bars[stop].intersection(yr)):
            continue
        if rstart is None:
            rstart = stop+1
        else:
            in_rs = in_rs.union(range(rstart, stop))
            rstart = None
    for xr in xranges:
        if len(xr) == len(in_rs.intersection(xr)):
            acc += len(xr)*len(yr)

for y in hori_stops:
    in_rs = common.ranges()
    rstart = None
    def flip(edge_start, edge_end):
        global in_rs
        global rstart
        if rstart is None:
            rstart = edge_end+1
        else:
            in_rs = in_rs.union(range(rstart, edge_start))
            rstart = None

    enter_i = None
    enter = None
    for x in vert_stops:
        if y in vert_bars[x]:
            flip(x, x)
        if (x, y) not in points:
            continue
        i = points.index((x, y))
        if enter_i is None or enter is None:
            enter_i = i
            enter = (x, y)
        else:
            dir = moves[i][0]
            enter_x = enter[0]
            if dir in ['U', 'D']:
                prev_dir = dir
                next_dir = moves[(i+2)%len(moves)][0]
            else:
                prev_dir = moves[(i-1)%len(moves)][0]
                next_dir = moves[(i+1)%len(moves)][0]
            if prev_dir == next_dir:
                flip(enter_x, x)
            else:
                if rstart is not None:
                    flip(enter_x, enter_x)
                    flip(x, x)
            enter_i = enter = None

    acc += len(in_rs)

for x in vert_stops:
    in_rs = common.ranges()
    rstart = None
    def flip(edge_start, edge_end):
        global in_rs
        global rstart
        if rstart is None:
            rstart = edge_end+1
        else:
            in_rs = in_rs.union(range(rstart, edge_start))
            rstart = None

    enter_i = None
    enter = None
    for y in hori_stops:
        if x in hori_bars[y]:
            flip(y, y)
        if (x, y) not in points:
            continue
        i = points.index((x, y))
        if enter_i is None or enter is None:
            enter_i = i
            enter = (x, y)
        else:
            dir = moves[i][0]
            enter_y = enter[1]
            if dir in ['L', 'R']:
                prev_dir = dir
                next_dir = moves[(i+2)%len(moves)][0]
            else:
                prev_dir = moves[(i-1)%len(moves)][0]
                next_dir = moves[(i+1)%len(moves)][0]
            if prev_dir == next_dir:
                flip(enter_y, y)
            else:
                if rstart is not None:
                    flip(enter_y, enter_y)
                    flip(y, y)
            enter_i = enter = None

    overlap = common.ranges([range(a, a+1) for a in hori_stops])
    in_rs = in_rs.difference(overlap)
    acc += len(in_rs)

print(acc)
