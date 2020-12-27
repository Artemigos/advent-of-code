from collections import deque
import common

lines = common.read_file('2020/20/data.txt').splitlines()
lines.append('')
tiles = {}
SIZE = 10

curr_tile = 0
line_acc = []

for line in lines:
    if line.startswith('Tile'):
        curr_tile = int(line.split(' ')[1].split(':')[0])
    elif line == '':
        tiles[curr_tile] = line_acc
        line_acc = []
    else:
        line_acc.append(line)

# part 1
def flip(x): return int(f'{x:010b}'[::-1], 2)

borders = {}
for k in tiles:
    board = tiles[k]
    u, r, d, l = 0, 0, 0, 0
    for i in range(SIZE):
        val_u = 1 if board[0][i] == '#' else 0
        val_d = 1 if board[-1][-i-1] == '#' else 0
        val_l = 1 if board[-i-1][0] == '#' else 0
        val_r = 1 if board[i][-1] == '#' else 0
        shft = SIZE-i-1
        u |= (val_u << shft)
        d |= (val_d << shft)
        l |= (val_l << shft)
        r |= (val_r << shft)

    borders[k] = u, r, d, l

def get_all_arrangements(tile_borders):
    # non-flipped rotations
    u, r, d, l = tile_borders
    yield 0, (u, r, d, l)
    yield 1, (l, u, r, d)
    yield 2, (d, l, u, r)
    yield 3, (r, d, l, u)

    # flipped rotations
    u, r, d, l = flip(u), flip(r), flip(d), flip(l)
    yield 4, (u, l, d, r)
    yield 5, (r, u, l, d)
    yield 6, (d, r, u, l)
    yield 7, (l, d, r, u)

def get_arrangement(tile_borders, arrangement_id):
    return list(get_all_arrangements(tile_borders))[arrangement_id][1]

maap = {}
k0 = list(borders.keys())[0]
maap[0, 0] = k0, 0

q = deque([(0, 0)])
seen = set()
used_tiles = set([k0])
while len(q) > 0:
    x, y = q.popleft()
    if (x, y) in seen:
        continue
    seen.add((x, y))

    curr_k, curr_arrangement = maap[(x, y)]
    curr_borders = get_arrangement(borders[curr_k], curr_arrangement)

    # find tile neighbor
    def find_match(new_pos, curr_border_i, neighbor_border_i):
        for k in borders:
            if k in used_tiles:
                continue
            for arrangement_id, b in get_all_arrangements(borders[k]):
                if flip(b[neighbor_border_i]) == curr_borders[curr_border_i]:
                    maap[new_pos] = k, arrangement_id
                    used_tiles.add(k)
                    q.append(new_pos)
                    break
            else:
                continue
            break

    find_match((x, y-1), 0, 2)
    find_match((x, y+1), 2, 0)
    find_match((x-1, y), 3, 1)
    find_match((x+1, y), 1, 3)

min_x = min(x[0] for x in maap.keys())
min_y = min(x[1] for x in maap.keys())
max_x = max(x[0] for x in maap.keys())
max_y = max(x[1] for x in maap.keys())

lu = maap[(min_x, min_y)][0]
ld = maap[(min_x, max_y)][0]
ru = maap[(max_x, min_y)][0]
rd = maap[(max_x, max_y)][0]
print(lu*ld*ru*rd)

# part 2
TILE_BORDER = 1 # can set to 0 to keep borders that should be thrown out - for debugging purposes
H = (max_y-min_y+1) * (SIZE-2*TILE_BORDER)
a_map = ['']*H

# reduce the map
def translate_pos(x, y, arrangement_id, dim=SIZE):
    rot = arrangement_id & 3
    if rot == 1:
        x, y = y, dim-x-1
    elif rot == 2:
        x, y = dim-x-1, dim-y-1
    elif rot == 3:
        x, y = dim-y-1, x
    elif rot != 0:
        raise 'err'
    if arrangement_id >= 4:
        x = dim-x-1
    return x, y

for ty in range(max_y-min_y+1):
    for tx in range(max_x-min_x+1):
        tile_k, tile_arrangement_id = maap[(min_x+tx, min_y+ty)]
        tile = tiles[tile_k]
        for y in range(SIZE-2*TILE_BORDER):
            for x in range(SIZE-2*TILE_BORDER):
                ox, oy = x+TILE_BORDER, y+TILE_BORDER
                ox, oy = translate_pos(ox, oy, tile_arrangement_id)
                ry = ty * (SIZE-2*TILE_BORDER) + y
                a_map[ry] += tile[oy][ox]

A_MAP_SIZE = len(a_map)

# print map
COLOR_GRID = False
COLOR_GRID_SIZE = SIZE
COLOR_ON = set([0, SIZE-1])
PRINT_MAP = False

if PRINT_MAP:
    for y in range(A_MAP_SIZE):
        l = a_map[y]
        for x in range(A_MAP_SIZE):
            should_color = COLOR_GRID and (x%COLOR_GRID_SIZE in COLOR_ON or y%COLOR_GRID_SIZE in COLOR_ON)
            if should_color:
                print('\033[91m', end='')
            print(l[x], end='')
            if should_color:
                print('\033[0m', end='')
        print()

# sea monster description
SEA_MONSTER_W = 20
SEA_MONSTER_H = 3
SEA_MONSTER = [
    (0, 1), (1, 2), (4, 2), (5, 1),
    (6, 1), (7, 2), (10, 2), (11, 1),
    (12, 1), (13, 2), (16, 2), (17, 1),
    (18, 0), (18, 1), (19, 1)
]

monster_in_fields = set()

# find monsters
for arrangement_id in range(8):
    for y in range(A_MAP_SIZE - SEA_MONSTER_H):
        for x in range(A_MAP_SIZE - SEA_MONSTER_W):
            for mx, my in SEA_MONSTER:
                ox, oy = translate_pos(x+mx, y+my, arrangement_id, dim=A_MAP_SIZE)
                if a_map[oy][ox] != '#':
                    break
            else:
                for mx, my in SEA_MONSTER:
                    ox, oy = translate_pos(x+mx, y+my, arrangement_id, dim=A_MAP_SIZE)
                    monster_in_fields.add((ox, oy))

# count unoccupied fields
unoccupied = 0
for y in range(A_MAP_SIZE):
    for x in range(A_MAP_SIZE):
        if a_map[y][x] == '#' and (x, y) not in monster_in_fields:
            unoccupied += 1

print(unoccupied)