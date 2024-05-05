import itertools
import common

nums = [int(x) for x in common.read_file().splitlines()]

# part 1
print(sum(nums))

# part 2
acc = 0
seen = set()
for n in itertools.cycle(nums):
    if acc in seen:
        print(acc)
        break
    seen.add(acc)
    acc += n
