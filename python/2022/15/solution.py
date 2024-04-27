import common
from common import ranges
import sys
import os

lines = common.read_file().splitlines()
file = os.path.basename(sys.argv[1])

detections = []
beacons = set()

for line in lines:
    nums = list(common.extract_numbers(line))
    detections.append(((nums[0], nums[1]), (nums[2], nums[3])))
    beacons.add((nums[2], nums[3]))

# part 1
check_y = 10 if file == 'sample.txt' else 2000000
space = ranges()

for d in detections:
    covered_dist = common.manhattan_dist(d[0], d[1])
    dy = abs(check_y - d[0][1])
    left = covered_dist - dy
    if left < 0:
        continue
    r = range(d[0][0]-left, d[0][0]+left+1)
    space = space.union(r)

for b in beacons:
    if b[1] == check_y:
        space = space.difference(range(b[0], b[0]+1))

print(len(space))

# part 2
def p2_new():
    max_size = range(0, (20 if file == 'sample.txt' else 4000000)+1)
    s = []
    for y in max_size:
        s.append(ranges(max_size))

    for d in detections:
        covered_dist = common.manhattan_dist(d[0], d[1])
        for y in range(max(d[0][1]-covered_dist, 0), min(max_size.stop, d[0][1]+covered_dist)):
            dy = abs(y - d[0][1])
            left = covered_dist - dy
            if left < 0:
                continue
            r = range(d[0][0]-left, d[0][0]+left+1)
            s[y] = s[y].difference(r)

    for y in max_size:
        if len(s[y]) > 0:
            print(s[y][0]*4000000+y)
            break

p2_new()
