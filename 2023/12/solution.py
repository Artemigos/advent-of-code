import common
from functools import cache

lines = common.read_file().splitlines()

@cache
def fd(l, *nums):
    acc = 0
    for i in range(len(l)):
        s = nums[0]
        segment = [c != '.' for c in l[i:i+s]]
        if len(segment) == s and all(segment) and (i+s >= len(l) or l[i+s] != '#'):
            if len(nums) == 1:
                if all((c != '#' for c in l[i+s:])):
                    acc += 1
            else:
                acc += fd(l[i+s+1:], *nums[1:])
        if l[i] == '#':
            break
    return acc

# part 1
def proc1(line):
    pat, num_str = line.split(' ')
    nums = common.extract_numbers(num_str)
    return fd(pat, *nums)

print(sum(map(proc1, lines)))

# part 2
def proc2(line):
    pat, num_str = line.split(' ')
    nums = common.extract_numbers(num_str) * 5
    pat = '?'.join([pat] * 5)
    return fd(pat, *nums)

print(sum(map(proc2, lines)))
