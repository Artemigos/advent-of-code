import itertools
import common

data = [int(x) for x in common.read_file().splitlines()]

target = 150

# part 1
found_num = 0
for r in range(1, len(data)):
    for cmb in itertools.combinations(data, r):
        if sum(cmb) == target:
            found_num += 1

print(found_num)

# part 2
found_num = 0
for r in range(1, len(data)):
    found = False
    for cmb in itertools.combinations(data, r):
        if sum(cmb) == target:
            found = True
            found_num += 1
    if found:
        break

print(found_num)
