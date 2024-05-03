import common

data = common.read_file()

floor = 0
first_basement_at = 0
for i in range(len(data)):
    if data[i] == '(':
        floor += 1
    else:
        floor -= 1

    if floor < 0 and first_basement_at == 0:
        first_basement_at = i+1

print(floor)
print(first_basement_at)
