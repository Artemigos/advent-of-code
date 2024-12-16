import common
from igraph import Graph

lines = common.read_file().splitlines()

# part 1
nodes = []
edges = []

for line in lines:
    words = common.extract_words(line)
    for word in words:
        if word not in nodes:
            nodes.append(word)
    l, rights = words[0], words[1:]
    li = nodes.index(l)
    for r in rights:
        ri = nodes.index(r)
        edges.append((li, ri))

g = Graph(len(nodes), edges)
cut = g.mincut()
assert len(cut.cut) == 3
print(common.product(cut.sizes()))
