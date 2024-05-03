import common

nums = common.extract_numbers(common.read_file())
row = nums[0]
column = nums[1]

# looking for ordinal for this cell
ordinal = 1
for i in range(row):
    ordinal += i
for i in range(column-1):
    ordinal += row+1+i

start = 20151125
curr = start
for i in range(1, ordinal):
    curr *= 252533
    curr %= 33554393

print(curr)
