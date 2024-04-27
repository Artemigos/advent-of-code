import common

board = common.read_file().splitlines()
w = len(board[0])
h = len(board)

# find planets
planets = []
for y in range(h):
    for x in range(w):
        if board[y][x] == '#':
            planets.append((x, y))

# find expanded rows and cols
expanded_rows = []
expanded_cols = []
for y in range(h):
    if all((c == '.' for c in board[y])):
        expanded_rows.append(y)

for x in range(w):
    if all((board[y][x] == '.' for y in range(h))):
        expanded_cols.append(x)

# part 1
def p_dist(p1, p2, expand_space_by):
    dx = abs(p2[0] - p1[0])
    dy = abs(p2[1] - p1[1])
    dist = dx+dy
    for r in expanded_rows:
        if r > p1[1] and r < p2[1] or r > p2[1] and r < p1[1]:
            dist += expand_space_by
    for c in expanded_cols:
        if c > p1[0] and c < p2[0] or c > p2[0] and c < p1[0]:
            dist += expand_space_by
    return dist

acc = 0
for p1 in planets:
    for p2 in planets:
        if p1 == p2:
            continue
        acc += p_dist(p1, p2, 1)

print(acc//2)

# part 2
acc = 0
for p1 in planets:
    for p2 in planets:
        if p1 == p2:
            continue
        acc += p_dist(p1, p2, 999999)

print(acc//2)
