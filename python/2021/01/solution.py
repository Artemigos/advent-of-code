import common

nums = common.to_int(common.read_file().splitlines())

# part 1
acc = 0
for i in range(1, len(nums)):
    if nums[i-1] < nums[i]:
        acc += 1

print(acc)

# part 2
acc = 0
for i in range(3, len(nums)):
    if nums[i-3] < nums[i]:
        acc += 1

print(acc)
