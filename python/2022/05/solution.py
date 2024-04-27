import common

lines = common.read_file().splitlines()

# parse
stacks = []
moves = []
stacks2 = []

for i in range(len(lines[0]) // 4 + 1):
    stacks.append([])
    stacks2.append([])

in_stacks = True
for line in lines:
    if in_stacks is None:
        in_stacks = False
        continue
    elif in_stacks:
        if line[1].isdigit():
            in_stacks = None
            continue
        for i in range(len(line) // 4 + 1):
            c = line[i*4+1]
            if c != ' ':
                stacks[i].insert(0, c)
                stacks2[i].insert(0, c)
    else:
        moves.append(tuple(common.extract_numbers(line)))

# part 1
for amount, start, end in moves:
    for i in range(amount):
        stacks[end-1].append(stacks[start-1].pop())

for stack in stacks:
    print(stack[-1], end='')
print()

# part 2
for amount, start, end in moves:
    to_move = stacks2[start-1][-amount:]
    stacks2[start-1] = stacks2[start-1][:-amount]
    for crate in to_move:
        stacks2[end-1].append(crate)

for stack in stacks2:
    print(stack[-1], end='')
print()
