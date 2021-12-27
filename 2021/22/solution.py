from typing import List, Tuple
import common

lines = common.read_file('2021/22/data.txt').splitlines()
rules = []
for line in lines:
    status, rest = line.split(' ')
    status = (status == 'on')
    ranges = []
    for range_str in rest.split(','):
        _, values = range_str.split('=')
        values = values.split('..')
        l = int(values[0])
        r = int(values[1])+1
        ranges.append(range(l, r))
    assert len(ranges) == 3
    rules.append((status, tuple(ranges)))

# part 1 and 2

def volume(cube):
    return len(cube[0])*len(cube[1])*len(cube[2])

def intersect(cube1, cube2):
    def isect_rng(r1: range, r2: range):
        start = max(r1.start, r2.start)
        stop = min(r1.stop, r2.stop)
        if start >= stop:
            return None
        return range(start, stop)
    x_section = isect_rng(cube1[0], cube2[0])
    y_section = isect_rng(cube1[1], cube2[1])
    z_section = isect_rng(cube1[2], cube2[2])
    if not x_section or not y_section or not z_section:
        return None
    return (x_section, y_section, z_section)

def find_volume_change(prev_rules, curr_rule):
    curr_add, curr_cube = curr_rule
    limited_rules = [(x[0], intersect(x[1], curr_cube)) for x in prev_rules]
    limited_rules = [x for x in limited_rules if x[1] is not None]
    added = 0
    for i in range(len(limited_rules)):
        a, r = find_volume_change(limited_rules[:i], limited_rules[i])
        added += a - r
    if curr_add:
        return volume(curr_cube) - added, 0
    else:
        return 0, added

acc = 0
for i in range(len(rules)):
    added, removed = find_volume_change(rules[:i], rules[i])
    acc += added - removed

_, removed = find_volume_change(rules, (False, tuple([range(-50, 51)]*3)))
print(removed)
print(acc)
