from collections import defaultdict
import common

nums = common.to_int(common.read_file().split(','))

fish = defaultdict(lambda: 0)
for num in nums:
    fish[num] += 1

# part 1 and 2

curr_fish = fish
for day in range(256):
    new_fish = defaultdict(lambda: 0)
    for i in range(1, 9):
        if i in curr_fish:
            new_fish[i-1] = curr_fish[i]
    new_fish[6] += curr_fish[0]
    new_fish[8] += curr_fish[0]
    curr_fish = new_fish

    if day == 79:
        print(sum(curr_fish.values()))

print(sum(curr_fish.values()))
