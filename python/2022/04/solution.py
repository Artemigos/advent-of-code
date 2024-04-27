import common

lines = common.read_file().splitlines()

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

p1_acc = 0
p2_acc = 0
for l_elf, r_elf in assignments:
    inter = intersect_range(l_elf, r_elf)
    if inter == l_elf or inter == r_elf:
        p1_acc += 1
    if len(inter) > 0:
        p2_acc += 1

print(p1_acc)
print(p2_acc)
