import common

lines = common.read_file('2017/24/data.txt').splitlines()
# lines = ['0/2', '2/2', '2/3', '3/4', '3/5', '0/1', '10/1', '9/10']


def parse_line(line):
    segments = line.split('/')
    return int(segments[0]), int(segments[1])


components = list(map(parse_line, lines))


def build_component_tree(parent, components):
    children = dict()

    def build(component, port):
        components_mod = list(components)
        components_mod.remove(component)
        children[component] = build_component_tree(component[port], components_mod)

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
            for inner_sum in yield_sums(node[k]):
                yield k_sum + inner_sum


max_sum = max(yield_sums(tree))
print(max_sum)


# part 2
def yield_lengths_and_sums(node: dict):
    if len(node.keys()) == 0:
        yield (0, 0)
    else:
        for k in node.keys():
            k_sum = sum(k)
            for inner_length, inner_sum in yield_lengths_and_sums(node[k]):
                yield (inner_length + 1, inner_sum + k_sum)


max_len = 0
max_str = 0
for curr_len, curr_sum in yield_lengths_and_sums(tree):
    if curr_len > max_len or (curr_len == max_len and curr_sum > max_str):
        max_len = curr_len
        max_str = curr_sum

print(max_len)
print(max_str)
