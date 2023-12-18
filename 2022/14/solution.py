import common

lines = common.read_file().splitlines()

board = set()

def sgn(x):
    if x < 0: return -1
    if x > 0: return 1
    return 0

def parse_point(p):
    l, r = p.split(',')
    return int(l), int(r)

for line in lines:
    points = line.split(' -> ')
    last = parse_point(points[0])
    for point in points[1:]:
        p = parse_point(point)
        x, y = p
        sx = sgn(x - last[0])
        sy = sgn(y - last[1])
        cx, cy = last
        while (cx, cy) != (x, y):
            board.add((cx, cy))
            cx += sx
            cy += sy
        board.add((cx, cy))
        last = p

max_y = max(map(lambda x: x[1], board))
src_x, src_y = 500, 0

# part 1
def next_pos(b, x, y):
    if (x, y+1) not in b:
        return x, y+1
    if (x-1, y+1) not in b:
        return x-1, y+1
    if (x+1, y+1) not in b:
        return x+1, y+1
    return None

b = set(board)
sands = 0
try:
    while True:
        last = None
        sand = src_x, src_y
        while sand is not None:
            last = sand
            sand = next_pos(b, *sand)
            if sand is not None and sand[1] > max_y:
                print(sands)
                assert False
        b.add(last)
        sands += 1
except:
    pass

# part 2
def next_pos(b, x, y):
    if y == max_y + 1:
        return None
    if (x, y+1) not in b:
        return x, y+1
    if (x-1, y+1) not in b:
        return x-1, y+1
    if (x+1, y+1) not in b:
        return x+1, y+1
    return None

b = set(board)
sands = 0
try:
    while True:
        last = None
        sand = src_x, src_y
        while sand is not None:
            last = sand
            sand = next_pos(b, *sand)
            if sand is None and last == (src_x, src_y):
                sands += 1
                print(sands)
                assert False
        b.add(last)
        sands += 1
except:
    pass
