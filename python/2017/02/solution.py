import common

data = common.read_file()
table = common.split_table(data)

# part 1
sum_acc = 0
for row in table:
    ints = list(map(lambda x: int(x), row))
    mx = max(ints)
    mn = min(ints)
    sum_acc += (mx - mn)

print(sum_acc)

# part 2
sum_acc = 0
for row in table:
    ints = list(map(lambda x: int(x), row))
    found = False
    for i in range(len(ints)):
        for j in range(len(ints)):
            if i != j and ints[i] % ints[j] == 0:
                sum_acc += ints[i] // ints[j]
                found = True
                break

        if found:
            break
    if found:
        continue

print(sum_acc)
