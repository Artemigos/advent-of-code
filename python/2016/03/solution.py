import common

lines = common.read_file().splitlines()
data = [common.extract_numbers(x) for x in lines]

# part 1
possible = 0
for row in data:
    mx = max(row)
    if sum(row)-mx > mx:
        possible += 1

print(possible)

# part 2
possible = 0
for y in range(0, len(data), 3):
    for x in range(3):
        row = [data[y][x], data[y+1][x], data[y+2][x]]
        mx = max(row)
        if sum(row)-mx > mx:
            possible += 1

print(possible)
