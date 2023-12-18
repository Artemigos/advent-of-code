import common

lines = common.read_file().splitlines()

acc = 0
acc2 = 0
for line in lines:
    nums = common.extract_numbers(line)
    sets = [nums]
    curr = nums
    while not all(map(lambda x: x == 0, curr)):
        new = [0]*(len(curr)-1)
        for i in range(1, len(curr)):
            new[i-1] = curr[i] - curr[i-1]
        sets.append(new)
        curr = new

    # part 1
    sets[-1].append(0)
    for set_i in range(len(sets)-2, -1, -1):
        sets[set_i].append(sets[set_i][-1] + sets[set_i+1][-1])
    acc += sets[0][-1]

    # part 2
    sets[-1].insert(0, 0)
    for set_i in range(len(sets)-2, -1, -1):
        sets[set_i].insert(0, sets[set_i][0] - sets[set_i+1][0])
    acc2 += sets[0][0]

print(acc)
print(acc2)
