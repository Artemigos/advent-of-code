from functools import cache
import common

nums = common.extract_numbers(common.read_file().strip())

# part 1
@cache
def expands_to(num: int) -> list[int]:
    if num == 0:
        return [1]
    s = str(num)
    if len(s)%2 == 0:
        h = len(s)//2
        return [int(s[:h]), int(s[h:])]
    else:
        return [num * 2024]

@cache
def expands_to_count(num: int, blinks: int) -> int:
    assert blinks > 0
    expanded = expands_to(num)
    if blinks == 1:
        return len(expanded)
    acc = 0
    for e in expanded:
        acc += expands_to_count(e, blinks - 1)
    return acc

acc = 0
for num in nums:
    acc += expands_to_count(num, 25)
print(acc)

# part 2
acc = 0
for num in nums:
    acc += expands_to_count(num, 75)
print(acc)
