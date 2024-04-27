import common

data = common.read_file('2017/8/data.txt')
lines = data.splitlines()

registries = set()
curr_max = 0


def convert_line(line):
    segments = line.split(' ')
    segments[1] = '+=' if segments[1] == 'inc' else '-='
    segments += ['else', '0']
    registries.add(segments[0])
    registries.add(segments[4])
    return ' '.join(segments)


commands = list(map(convert_line, lines))
for r in registries:
    locals()[r] = 0

for c in commands:
    exec(c)
    curr_locals = locals()
    r_values = map(lambda x: curr_locals[x], registries)
    max_val = max(r_values)
    if max_val > curr_max:
        curr_max = max_val

curr_locals = locals()
r_values = map(lambda x: curr_locals[x], registries)
print(max(r_values))
print(curr_max)
