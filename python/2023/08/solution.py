import common

lines = common.read_file().splitlines()

# part 1
moves = list(map(lambda c: 0 if c == 'L' else 1, lines[0]))
assoc = {}
for line in lines[2:]:
    f = line[:3]
    l = line[7:10]
    r = line[12:15]
    assoc[f] = (l, r)

curr = 'AAA'
i = 0
while True:
    move = moves[i % len(moves)]
    curr = assoc[curr][move]
    i += 1
    if curr == 'ZZZ':
        break
print(i)

# part 2
cursors = []
for k in assoc.keys():
    if k[-1] == 'A':
        cursors.append(k)
ci_x_diff = [(0, 0)] * len(cursors)
i = 0
while True:
    move = moves[i % len(moves)]
    can_end = True
    for ci in range(len(cursors)):
        cursors[ci] = assoc[cursors[ci]][move]
        if cursors[ci][-1] != 'Z':
            can_end = False
        else:
            ci_x_diff[ci] = (i, i - ci_x_diff[ci][0])
            print(ci_x_diff)
    i += 1
    if can_end:
        break
print(i)

# did the rest manually by calculating LCM of the loops
# TODO: do this programmatically
