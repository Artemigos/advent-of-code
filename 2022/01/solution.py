import common

lines = common.read_file().splitlines()

current_elf = 0
elves = []

for line in lines:
    if not line:
        elves.append(current_elf)
        current_elf = 0
    else:
        current_elf += int(line)

elves.append(current_elf)
elves = list(sorted(elves))

# part 1
print(elves[-1])

# part 2
print(sum(elves[-3:]))
