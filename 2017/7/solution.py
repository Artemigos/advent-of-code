import common

data = common.read_file('2017/7/data.txt')
lines = data.splitlines()

def parse_line_to_relations(line):
    segments = line.split(' ')
    parent = segments[0]
    for child in segments[3:]:
        yield (parent, child.rstrip(','))

def parse_line_with_weight(line):
    segments = line.split(' ')
    node = segments[0]
    weight = int(segments[1][1:-1])
    return (node, weight)

relations = dict()

for line in lines:
    for (parent, child) in parse_line_to_relations(line):
        relations[child] = parent

current = list(relations.keys())[0]
while True:
    if current not in relations.keys():
        break
    current = relations[current]

# part 2
nodes = list(map(parse_line_with_weight, lines))
weights = dict()
for node, weight in nodes:
    weights[node] = weight
for node, weight in nodes:
    curr = node
    while curr in relations.keys():
        curr = relations[curr]
        weights[curr] += weight

s_weights = sorted(weights, key= lambda x: weights[x])

for k in s_weights:
    print(k, weights[k])
# NOTE: with this data I did manual analysis

print(current)
