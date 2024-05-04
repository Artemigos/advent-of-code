import common

data = common.read_file()
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
    return node, weight


relations = {child: parent for parent, child in common.flat_map(parse_line_to_relations, lines)}
current = list(relations.keys())[0]

while True:
    if current not in relations.keys():
        break
    current = relations[current]

print(current)

# part 2
nodes = list(map(parse_line_with_weight, lines))
weights = {node: weight for node, weight in nodes}
rev_rels = {}
for node, weight in nodes:
    curr = node
    while curr in relations.keys():
        parent = relations[curr]
        if parent not in rev_rels:
            rev_rels[parent] = set()
        rev_rels[parent].add(curr)
        curr = parent
        weights[curr] += weight

curr = current
while True:
    ch = [(x, weights[x]) for x in rev_rels[curr]]
    counts = {}
    for n, w in ch:
        if w in counts:
            counts[w] += 1
        else:
            counts[w] = 1
    ch_incorrect = len(counts) > 1
    if not ch_incorrect:
        break
    if len(ch) == 2:
        assert False, 'inconclusive who is incorrect'
    for k in counts:
        if counts[k] == 1:
            incorrect_w = k
            break
    else:
        assert False, 'failed child weight has more occurences?'
    for n, w in ch:
        if w == incorrect_w:
            incorrect_n = n
            break
    else:
        assert False, 'child with incorrect weight not found'
    curr = incorrect_n

siblings = list(rev_rels[relations[curr]])
siblings.remove(curr)
correct_sibling = siblings[0]

for n, w in nodes:
    if n == curr:
        incorrect_sibling_w = w
        break
else:
    assert False, 'incorrect sibling not found'

incorrect_total_w = weights[curr]
correct_total_w = weights[correct_sibling]

diff = correct_total_w - incorrect_total_w
print(incorrect_sibling_w + diff)
