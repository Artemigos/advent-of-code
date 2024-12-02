import common

lines = common.read_file().splitlines()

# part 1
def check_report(nums: list[int]) -> bool:
    dir = None
    for i in range(1, len(nums)):
        diff = nums[i] - nums[i-1]
        if dir is None:
            dir = diff
        elif (dir < 0) != (diff < 0):
            return False
        diff = abs(diff)
        if diff < 1 or diff > 3:
            return False
    return True

acc = 0
for line in lines:
    if check_report(common.extract_numbers(line)):
        acc += 1

print(acc)

# part 2
acc = 0
for line in lines:
    nums = common.extract_numbers(line)
    if check_report(nums):
        acc += 1
        continue
    for i in range(len(nums)):
        new_nums = nums[:i] + nums[i+1:]
        if check_report(new_nums):
            acc += 1
            break

print(acc)
