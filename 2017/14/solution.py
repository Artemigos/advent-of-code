import numpy as np
import common

data = 'hwlqcszp'
# data = 'flqrgnkx' # sample data

rows = list()

# part 1
count = 0
for r in range(128):
    hash_input = data + '-' + str(r)
    ints, representation = common.knot_hash_full(hash_input)
    rows.append(ints)
    for i in range(len(ints)):
        for b in range(8):
            if (ints[i] & (1 << b)) > 0:
                count += 1

print(count)


# part 2
def is_used(x, y):
    num_i = int(x/8)
    bit = 7-(x % 8)
    num = rows[y][num_i]
    return (num & (1 << bit)) > 0


regions = np.zeros((128, 128))


def can_fill(x, y):
    if x < 0 or y < 0 or x >= 128 or y >= 128:
        return False
    if not is_used(x, y):
        return False
    if regions[x, y] > 0:
        return False
    return True


def fill_region(x, y, region):
    if not can_fill(x, y):
        return
    regions[x, y] = region
    fill_region(x-1, y, region)
    fill_region(x, y-1, region)
    fill_region(x+1, y, region)
    fill_region(x, y+1, region)


curr_region = 0
for pos in range(128*128):
    x = int(pos/128)
    y = pos % 128
    if can_fill(x, y):
        curr_region += 1
        fill_region(x, y, curr_region)

print(curr_region)
