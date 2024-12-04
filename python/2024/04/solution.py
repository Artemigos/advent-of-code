import common

lines = common.read_file().splitlines()
w = len(lines[0])
h = len(lines)

# part 1
acc = 0

# horizontal scan
for line in lines:
    for i in range(w-3):
        section = line[i:i+4]
        if section == 'XMAS' or section == 'SAMX':
            acc += 1

# vertical scan
for x in range(w):
    for y in range(h-3):
        section = ''.join([lines[y+i][x] for i in range(4)])
        if section == 'XMAS' or section == 'SAMX':
            acc += 1

# \ diagonal scan
for x in range(w-3):
    for y in range(h-3):
        section = ''.join([lines[y+i][x+i] for i in range(4)])
        if section == 'XMAS' or section == 'SAMX':
            acc += 1

# / diagonal scan
for x in range(w-3):
    for y in range(3, h):
        section = ''.join([lines[y-i][x+i] for i in range(4)])
        if section == 'XMAS' or section == 'SAMX':
            acc += 1

print(acc)

# part 2
acc = 0
allowed_around = ['MMSS', 'MSMS', 'SMSM', 'SSMM']

for x in range(1, w-1):
    for y in range(1, h-1):
        if lines[y][x] == 'A':
            around = lines[y-1][x-1] + lines[y-1][x+1] + lines[y+1][x-1] + lines[y+1][x+1]
            if around in allowed_around:
                acc += 1

print(acc)
