import common

data = common.read_file('2017/7/data.txt')
lines = data.splitlines()

def parse_line(line):
    segments = line.split(' ')
    parent = segments[0]
    for child in segments[3:]:
        yield (parent, child.rstrip(','))

relations = dict()

for line in lines:
    for (parent, child) in parse_line(line):
        relations[child] = parent

current = list(relations.keys())[0]
while True:
    if current not in relations.keys():
        break
    current = relations[current]

print(current)
