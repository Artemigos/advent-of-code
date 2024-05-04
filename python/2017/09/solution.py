import common

data = common.read_file()

level = 0
in_garbage = False
cancelling = False
points = 0
garbage_count = 0

for ch in data:
    if cancelling:
        cancelling = False
        continue
    if ch == '!':
        cancelling = True
        continue
    if in_garbage:
        if ch == '>':
            in_garbage = False
        else:
            garbage_count += 1
        continue
    if ch == '<':
        in_garbage = True
        continue
    if ch == '{':
        level += 1
        continue
    if ch == '}':
        points += level
        level -= 1
        continue

print(points)
print(garbage_count)
