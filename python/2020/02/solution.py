import re
import common

lines = common.read_file().splitlines()

amount = 0
amount2 = 0
for line in lines:
    segments = re.split(r'[\- :]', line)
    password = segments[4]
    c = segments[2]

    # part 1
    rng = range(int(segments[0]), int(segments[1])+1)
    occurances = password.count(c)
    if occurances in rng:
        amount += 1

    # part 2
    c1 = password[int(segments[0])-1]
    c2 = password[int(segments[1])-1]
    if c1 != c2 and (c1 == c or c2 == c):
        amount2 += 1

print(amount)
print(amount2)
