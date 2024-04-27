from collections import defaultdict
import common

FRAME_SIZE = 25
nums = common.to_int(common.read_file('2020/09/data.txt').splitlines())

# part 1
result = None
for i in range(len(nums)-FRAME_SIZE):
    current = nums[i+FRAME_SIZE]
    found = False
    for a in range(FRAME_SIZE):
        for b in range(FRAME_SIZE):
            if a == b:
                continue
            if nums[i+a] + nums[i+b] == current:
                found = True
                break
        if found:
            break

    if not found:
        result = current
        break

print(result)

# part 2
acc = defaultdict(lambda: 0)
rng = None
for i in range(len(nums)):
    acc[i, i] = nums[i]
    for j in range(i+1, len(nums)):
        acc[i, j] = acc[i, j-1] + nums[j]
        if acc[i, j] == result:
            rng = range(i, j+1)
            break
    if rng is not None:
        break

filtered = list(map(lambda x: nums[x], rng))
print(min(filtered) + max(filtered))
