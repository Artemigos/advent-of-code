import common

lines = common.read_file().splitlines()
line_len = len(lines[0])

collectors = []
for i in range(line_len):
    collectors.append(dict())

for l in lines:
    for i in range(line_len):
        coll = collectors[i]
        if l[i] in coll.keys():
            coll[l[i]] += 1
        else:
            coll[l[i]] = 1

# part 1
for i in range(line_len):
    mk, _ = max(collectors[i].items(), key=lambda x: x[1])
    print(mk, end='')

print()

# part 2
for i in range(line_len):
    mk, _ = min(collectors[i].items(), key=lambda x: x[1])
    print(mk, end='')

print()
