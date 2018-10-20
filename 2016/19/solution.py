import common

data = 3012210
# data = 5 # sample
# data = 5000 # profiling

# part 1
elves = list(range(1, data+1))
keep_at = 0

while len(elves) > 1:
    le = len(elves)
    elves = [elf for i, elf in enumerate(elves) if i%2 == keep_at]
    keep_at = (le+keep_at)%2

print(elves[0])

# part 2
elves = dict()
for i in range(data):
    elves[i] = True
elf_len = len(elves)

def find_index(start, offset):
    i = start
    found = 0
    le = len(elves)
    while found < offset:
        i = (i+1)%le
        if elves[i]:
            found += 1
    return i

i = int(elf_len/2)
while elf_len > 1:
    offset = (elf_len%2)+1
    elves[i] = False
    elf_len -= 1
    i = find_index(i, offset)
    common.print_and_return(elf_len)

print()
print(find_index(0, 1)+1)
