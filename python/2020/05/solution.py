import common

lines = common.read_file().splitlines()
lines = list(map(lambda x: x.replace('F', '0').replace('B', '1').replace('L', '0').replace('R', '1'), lines))
nums = list(map(lambda x: int(x, base=2), lines))

# part 1
max_id = max(nums)
print(max_id)

# part 2
for i in range(min(nums), max(nums)+1):
    if i not in nums:
        print(i)
        break
