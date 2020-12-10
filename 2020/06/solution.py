from collections import defaultdict
import common

lines = common.read_file('2020/06/data.txt').splitlines()

# part 1
groups = []
group = defaultdict(lambda: 0)

for l in lines:
    if l == '':
        groups.append(group)
        group = defaultdict(lambda: 0)
    for c in l:
        group[c] += 1

groups.append(group)
group = None

acc = 0
for g in groups:
    acc += len(g)

print(acc)

# part 2
groups = []
group = None

for l in lines:
    if l == '':
        groups.append(group)
        group = None
        continue
    if group is None:
        group = set(l)
    else:
        group = group.intersection(set(l))

groups.append(group)
group = None

acc = 0
for g in groups:
    acc += len(g)

print(acc)
