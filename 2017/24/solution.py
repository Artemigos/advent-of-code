import common
import itertools

lines = common.read_file('2017/24/data.txt').splitlines()
# lines = ['0/2', '2/2', '2/3', '3/4', '3/5', '0/1', '10/1', '9/10']

def parse_line(line):
    segments = line.split('/')
    return (int(segments[0]), int(segments[1]))

components = list(map(parse_line, lines))

def build_component_tree(parent, components):
    children = dict()
    def build(c, port):
        cmps_mod = list(components)
        cmps_mod.remove(c)
        children[c] = build_component_tree(c[port], cmps_mod)

    for c in components:
        if c[0] == parent:
            build(c, 1)
        elif c[1] == parent:
            build(c, 0)
    return children

tree = build_component_tree(0, components)

def yield_sums(node: dict):
    if len(node.keys()) == 0:
        yield 0
    else:
        for k in node.keys():
            k_sum = sum(k)
            for s in yield_sums(node[k]):
                yield k_sum + s

max_sum = max(yield_sums(tree))
print(max_sum)

# part 2

def yield_lengths_and_sums(node: dict):
    if len(node.keys()) == 0:
        yield (0, 0)
    else:
        for k in node.keys():
            k_sum = sum(k)
            for l, s in yield_lengths_and_sums(node[k]):
                yield (l+1, s+k_sum)

max_len = 0
max_str = 0
for l, s in yield_lengths_and_sums(tree):
    if l > max_len or (l == max_len and s > max_str):
        max_len = l
        max_str = s

print(max_len)
print(max_str)
