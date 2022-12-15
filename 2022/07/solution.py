import common

lines = common.read_file('2022/07/data.txt').splitlines()

folders = set(['/'])
files = set()

# parse
def p(x):
    return '/'+'/'.join(x)

curr = []
for line in lines:
    if line[0] == '$':
        if line[2:4] == 'cd':
            where = line[5:]
            if where == '..':
                curr.pop()
            elif where == '/':
                curr = []
            else:
                curr.append(where)
    else:
        if line [:3] == 'dir':
            name = line[4:]
            folders.add(p(curr + [name]))
        else:
            segments = line.split(' ')
            size = int(segments[0])
            name = segments[1]
            files.add((p(curr+[name]), size))

# part 1
acc = 0
sizes = {}
for folder in folders:
    f_acc = 0
    for path, size in files:
        if path.startswith(folder):
            f_acc += size
    sizes[folder] = f_acc
    if f_acc <= 100000:
        acc += f_acc

print(acc)

# part 2
used = sizes['/']
total = 70000000
free = total - used
needed = 30000000 - free
assert needed > 0

print(min(filter(lambda x: x >= needed, sizes.values())))
