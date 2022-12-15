import common

lines = common.read_file('2022/04/data.txt').splitlines()

assignments = []
for line in lines:
    l, r = line.split(',')
    nums = list(map(int, l.split('-')))
    l_elf = range(nums[0], nums[1]+1)
    nums = list(map(int, r.split('-')))
    r_elf = range(nums[0], nums[1]+1)
    assignments.append((l_elf, r_elf))

def intersect_range(r1: range, r2: range) -> range:
    return range(max(r1.start, r2.start), min(r1.stop, r2.stop))

# part 1
acc = 0
for l_elf, r_elf in assignments:
    inter = intersect_range(l_elf, r_elf)
    if inter == l_elf or inter == r_elf:
        acc += 1

print(acc)

# part 2
acc = 0
for l_elf, r_elf in assignments:
    inter = intersect_range(l_elf, r_elf)
    if len(inter) > 0:
        acc += 1

print(acc)
