import common
# from time import sleep
from itertools import combinations

lines = common.read_file().splitlines()
w, h = 101, 103

robots: list[tuple[int, int, int, int]] = []
for line in lines:
    x, y, vx, vy = common.extract_numbers(line)
    robots.append((x, y, vx, vy))

# part 1
curr = list(robots)
for _ in range(100):
    for i in range(len(curr)):
        x, y, vx, vy = curr[i]
        curr[i] = (x+vx)%w, (y+vy)%h, vx, vy

quadrant_ranges = [
    (range(w // 2), range(h // 2)),
    (range(w // 2 + 1, w), range(h // 2)),
    (range(w // 2), range(h // 2 + 1, h)),
    (range(w // 2 + 1, w), range(h // 2 + 1, h)),
]
quadrants = [0, 0, 0, 0]
for x, y, _, _ in curr:
    for q in range(4):
        if x in quadrant_ranges[q][0] and y in quadrant_ranges[q][1]:
            quadrants[q] += 1

print(common.product(quadrants))

# part 2
# NOTE: all robots loop after exactly w*h seconds
curr = list(robots)
s = None
for s in range(w*h):
    positions: set[tuple[int, int]] = set()
    for i in range(len(curr)):
        x, y, vx, vy = curr[i]
        x = (x+vx)%w
        y = (y+vy)%h
        curr[i] = x, y, vx, vy
        positions.add((x, y))

    distances = 0
    count = 0
    for l, r in combinations(positions, 2):
        distances += abs(l[0] - r[0]) + abs(l[1] - r[1])
        count += 1
    avg = distances / count
    # arbitrary threshold, picked after observing what kind of values I'm getting
    # correct iteration has avg distance of ~40
    # evrything else is above 50
    if avg < 45:
        print(s+1)
        break
        # print(s, distances / count)
        # for y in range(h):
        #     for x in range(w):
        #         c = '#' if (x, y) in positions else ' '
        #         print(c, end='')
        #     print()
        # print()
        # sleep(0.1)
