import common
import itertools
from operator import mul, add

lines = common.read_file().splitlines()

# part 1
acc = 0
for line in lines:
    result, nums = line.split(': ')
    result, nums = int(result), [int(x) for x in nums.split()]
    op_sets = itertools.product([add, mul], repeat=len(nums)-1)
    for op_set in op_sets:
        op_acc = nums[0]
        for i in range(len(op_set)):
            op_acc = op_set[i](op_acc, nums[i+1])
        if op_acc == result:
            acc += result
            break

print(acc)

# part 2
def concat(a, b):
    l = len(str(b))
    a *= pow(10, l)
    return a + b

acc = 0
for line in lines:
    result, nums = line.split(': ')
    result, nums = int(result), [int(x) for x in nums.split()]
    op_sets = itertools.product([add, mul, concat], repeat=len(nums)-1)
    for op_set in op_sets:
        op_acc = nums[0]
        for i in range(len(op_set)):
            op_acc = op_set[i](op_acc, nums[i+1])
        if op_acc == result:
            acc += result
            break

print(acc)
