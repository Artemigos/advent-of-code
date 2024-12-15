import common

board, moves = common.read_file().split('\n\n')
board = board.splitlines()
moves = ''.join(moves.splitlines())
w = len(board[0])
h = len(board)

Point = tuple[int, int]
boxes_data: set[Point] = set()
start: Point = 0, 0

for y in range(h):
    for x in range(w):
        c = board[y][x]
        if c == 'O':
            boxes_data.add((x, y))
        elif c == '@':
            start = x, y

# part 1
boxes = set(boxes_data)
def displace(pos: Point, off: Point) -> bool:
    global boxes, board
    if pos not in boxes:
        return board[pos[1]][pos[0]] != '#'

    nbox = (pos[0]+off[0], pos[1]+off[1])
    if not displace(nbox, off):
        return False

    boxes.remove(pos)
    boxes.add(nbox)
    return True

curr = start
for move in moves:
    nxt = curr
    off = (0, 0)
    if move == '<':
        nxt = (nxt[0]-1, nxt[1])
        off = (off[0]-1, off[1])
    elif move == '>':
        nxt = (nxt[0]+1, nxt[1])
        off = (off[0]+1, off[1])
    elif move == '^':
        nxt = (nxt[0], nxt[1]-1)
        off = (off[0], off[1]-1)
    elif move == 'v':
        nxt = (nxt[0], nxt[1]+1)
        off = (off[0], off[1]+1)
    else:
        raise Exception('???')
    x, y = nxt
    if board[y][x] == '#':
        continue
    if displace(nxt, off):
        curr = nxt

acc = 0
for x, y in boxes:
    acc += y*100 + x
print(acc)

# part 2
walls: set[Point] = set()
for y in range(h):
    for x in range(w):
        if board[y][x] == '#':
            walls.add((x*2, y))
            walls.add((x*2+1, y))
boxes = set()
for x, y in boxes_data:
    boxes.add((x*2, y))
start = start[0]*2, start[1]

def displace2(pos: Point, off: Point):
    global boxes
    other_pos = pos[0]-1, pos[1]
    if pos in boxes:
        nbox = pos[0]+off[0], pos[1]+off[1]
        other_nbox = nbox[0]+1, nbox[1]
        if off[1] != 0: # left/right movement moves onto itself - don't displace that
            displace2(nbox, off)
            displace2(other_nbox, off)
        elif off[0] == -1:
            displace2(nbox, off)
        else:
            displace2(other_nbox, off)
        boxes.remove(pos)
        boxes.add(nbox)
    elif other_pos in boxes:
        nbox = other_pos[0]+off[0], other_pos[1]+off[1]
        other_nbox = nbox[0]+1, nbox[1]
        if off[1] != 0: # left/right movement moves onto itself - don't displace that
            displace2(nbox, off)
            displace2(other_nbox, off)
        elif off[0] == -1:
            displace2(nbox, off)
        else:
            displace2(other_nbox, off)
        boxes.remove(other_pos)
        boxes.add(nbox)
def can_displace(pos: Point, off: Point) -> bool:
    other_pos = pos[0]-1, pos[1]
    if pos not in boxes and other_pos not in boxes:
        return pos not in walls
    if pos in boxes:
        nbox = (pos[0]+off[0], pos[1]+off[1])
        other_nbox = nbox[0]+1, nbox[1]
        if off[1] != 0: # left/right movement moves onto itself - don't check that
            if not can_displace(nbox, off) or not can_displace(other_nbox, off):
                return False
        elif off[0] == -1:
            if not can_displace(nbox, off):
                return False
        else:
            if not can_displace(other_nbox, off):
                return False
    else:
        nbox = (other_pos[0]+off[0], other_pos[1]+off[1])
        other_nbox = nbox[0]+1, nbox[1]
        if off[1] != 0: # left/right movement moves onto itself - don't check that
            if not can_displace(nbox, off) or not can_displace(other_nbox, off):
                return False
        elif off[0] == -1:
            if not can_displace(nbox, off):
                return False
        else:
            if not can_displace(other_nbox, off):
                return False
    return True

curr = start
for move in moves:
    nxt = curr
    off = (0, 0)
    if move == '<':
        nxt = (nxt[0]-1, nxt[1])
        off = (off[0]-1, off[1])
    elif move == '>':
        nxt = (nxt[0]+1, nxt[1])
        off = (off[0]+1, off[1])
    elif move == '^':
        nxt = (nxt[0], nxt[1]-1)
        off = (off[0], off[1]-1)
    elif move == 'v':
        nxt = (nxt[0], nxt[1]+1)
        off = (off[0], off[1]+1)
    else:
        raise Exception('???')
    if nxt in walls:
        continue
    if can_displace(nxt, off):
        displace2(nxt, off)
        curr = nxt

acc = 0
for x, y in boxes:
    acc += y*100 + x
print(acc)
