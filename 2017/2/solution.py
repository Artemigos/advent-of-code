import common

data = common.read_file('2017/2/data.txt')
table = common.split_table(data)

sum = 0
for row in table:
    ints = list(map(lambda x: int(x), row))
    # part 1
    # mx = max(ints)
    # mn = min(ints)
    # sum += (mx - mn)

    # part 2
    found = False
    for i in range(len(ints)):
        for j in range(len(ints)):
            if i != j and ints[i] % ints[j] == 0:
                sum += ints[i] / ints[j]
                found = True
                break

        if found: break
    if found: continue

print(sum)
