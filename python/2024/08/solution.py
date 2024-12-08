import common
import itertools

sample = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""

lines = common.read_file().splitlines()
# lines = sample.splitlines()
w = len(lines[0])
h = len(lines)

antennas: dict[str, list[tuple[int, int]]] = {}
def add(k, x, y):
    global antennas
    if k not in antennas:
        antennas[k] = []
    antennas[k].append((x, y))

for y in range(h):
    for x in range(w):
        c = lines[y][x]
        if c != '.':
            add(c, x, y)

# part 1
antinodes = set()
def acc(x, y):
    global antinodes
    if x < 0 or y < 0 or x >= w or y >= h:
        return False
    antinodes.add((x, y))
    return True

for k in antennas:
    points = antennas[k]
    for a1, a2 in itertools.combinations(points, 2):
        dx, dy = a2[0] - a1[0], a2[1] - a1[1]
        nx, ny = a2[0] + dx, a2[1] + dy
        acc(nx, ny)
        nx, ny = a1[0] - dx, a1[1] - dy
        acc(nx, ny)

print(len(antinodes))

# part 2
# NOTE: this solution ignores the fact that dx and dy could
# be divisible by the same number, but it gave me the correct result
antinodes = set()
for k in antennas:
    points = antennas[k]
    for a1, a2 in itertools.combinations(points, 2):
        dx, dy = a2[0] - a1[0], a2[1] - a1[1]
        nx, ny = a2
        while acc(nx, ny):
            nx += dx
            ny += dy
        nx, ny = a1
        while acc(nx, ny):
            nx -= dx
            ny -= dy

print(len(antinodes))
