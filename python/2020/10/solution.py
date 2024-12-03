from functools import lru_cache
import common

nums = common.to_int(common.read_file().splitlines())

sorted_nums = sorted(nums)

# part 1
prev = 0
acc1 = 0
acc3 = 0
for i in range(len(nums)):
    diff = sorted_nums[i] - prev
    if diff == 1:
        acc1 += 1
    elif diff == 3:
        acc3 += 1
    prev = sorted_nums[i]
acc3 += 1

print(acc1*acc3)

# part 2
@lru_cache(maxsize=None)
def num_of_paths(idx):
    if idx == len(sorted_nums)-1:
        return 1

    curr = sorted_nums[idx]
    acc = 0

    for i in range(idx+1, len(sorted_nums)):
        nxt = sorted_nums[i]
        if nxt > curr + 3:
            break
        acc += num_of_paths(i)

    return acc

acc = 0
for i in range(len(sorted_nums)):
    nxt = sorted_nums[i]
    if nxt > 3:
        break
    acc += num_of_paths(i)

print(acc)
