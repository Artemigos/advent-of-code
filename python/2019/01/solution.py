import common

data = common.to_int(common.read_file().splitlines())

# part 1
acc = 0
for num in data:
    acc += (num // 3) - 2

print(str(acc))

# part 2
acc = 0
for num in data:
    cost = max((num // 3) - 2, 0)
    while cost > 0:
        acc += cost
        cost = max((cost // 3) - 2, 0)

print(str(acc))
