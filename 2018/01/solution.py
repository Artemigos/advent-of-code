import itertools

nums = list(map(int, open('2018/01/data.txt')))

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
