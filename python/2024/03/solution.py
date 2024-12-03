import common
import re

lines = common.read_file().splitlines()

# part 1
acc = 0
for line in lines:
    i = 0
    while i < len(line):
        match = re.match(r'^mul\(\d{1,3},\d{1,3}\)', line[i:])
        if match is not None:
            val = match.group()
            l, r = map(int, val[4:-1].split(','))
            acc += l * r
            i += len(val)
        else:
            i += 1

print(acc)

# part 2
acc = 0
enabled = True
for line in lines:
    i = 0
    while i < len(line):
        if enabled:
            match = re.match(r'^mul\(\d{1,3},\d{1,3}\)', line[i:])
            if match is not None:
                val = match.group()
                l, r = map(int, val[4:-1].split(','))
                acc += l * r
                i += len(val)
                continue

        match = re.match(r'^do\(\)', line[i:])
        if match is not None:
            enabled = True
            i += len(match.group())
            continue

        match = re.match(r'^don\'t\(\)', line[i:])
        if match is not None:
            enabled = False
            i += len(match.group())
            continue

        i += 1

print(acc)
