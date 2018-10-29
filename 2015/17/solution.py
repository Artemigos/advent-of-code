import itertools

data = [
    43, 3, 4, 10, 21,
    44, 4, 6, 47, 41,
    34, 17, 17, 44, 36,
    31, 46, 9, 27, 38
]

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
