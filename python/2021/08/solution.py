import common

lines = common.read_file().splitlines()
entries = []
for line in lines:
    clues, outputs = line.split(' | ')
    sorted_clues = list(map(lambda x: ''.join(sorted(x)), clues.split()))
    sorted_outputs = list(map(lambda x: ''.join(sorted(x)), outputs.split()))
    entries.append((sorted_clues, sorted_outputs))

# part 1

acc = 0
for entry in entries:
    counted = filter(lambda x: len(x) in [2, 3, 4, 7], entry[1])
    acc += len(list(counted))

print(acc)

# part 2

outputs = []
for entry in entries:
    digit_map = {}
    one = next(filter(lambda x: len(x) == 2, entry[0]))
    digit_map[one] = 1
    four = next(filter(lambda x: len(x) == 4, entry[0]))
    digit_map[four] = 4
    seven = next(filter(lambda x: len(x) == 3, entry[0]))
    digit_map[seven] = 7
    eight = next(filter(lambda x: len(x) == 7, entry[0]))
    digit_map[eight] = 8
    six = next(filter(lambda x: len(x) == 6 and not set(x).issuperset(set(one)), entry[0]))
    digit_map[six] = 6
    nine = next(filter(lambda x: len(x) == 6 and set(x).issuperset(set(four)), entry[0]))
    digit_map[nine] = 9
    zero = next(filter(lambda x: len(x) == 6 and x != six and x != nine, entry[0]))
    digit_map[zero] = 0
    three = next(filter(lambda x: len(x) == 5 and set(x).issuperset(set(one)), entry[0]))
    digit_map[three] = 3
    five = next(filter(lambda x: len(x) == 5 and x != three and set(x).issubset(set(nine)), entry[0]))
    digit_map[five] = 5
    two = next(filter(lambda x: len(x) == 5 and x != three and x != five, entry[0]))
    digit_map[two] = 2

    out = digit_map[entry[1][0]]*1000 + digit_map[entry[1][1]]*100 + digit_map[entry[1][2]]*10 + digit_map[entry[1][3]]
    outputs.append(out)

print(sum(outputs))
