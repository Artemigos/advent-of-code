from itertools import combinations

import common

lines = common.read_file().splitlines()
edges = set()
neighbors: dict[str, set[str]] = {}
for line in lines:
    left, right = line.split("-")
    edges.add((left, right))
    edges.add((right, left))
    if left not in neighbors:
        neighbors[left] = set([right])
    else:
        neighbors[left].add(right)
    if right not in neighbors:
        neighbors[right] = set([left])
    else:
        neighbors[right].add(left)

# part 1
acc = 0
for node1 in neighbors:
    for node2 in neighbors[node1]:
        for node3 in neighbors[node2]:
            if (node1, node3) not in edges:
                continue
            if node1[0] == "t" or node2[0] == "t" or node3[0] == "t":
                acc += 1

# NOTE: there are 6 ways to order 3 elements and we will find all of them
print(acc // 6)

# part 2
biggest_cluster = []
for node1 in neighbors:
    node_neighbors = neighbors[node1]
    min_neighbors = max(1, len(biggest_cluster) - 1)
    for how_many in range(len(node_neighbors), min_neighbors, -1):
        for combo in combinations(node_neighbors, how_many):
            is_cluster = all([pair in edges for pair in combinations(combo, 2)])
            if is_cluster and len(combo) >= len(biggest_cluster):
                biggest_cluster = [node1] + list(combo)
biggest_cluster = sorted(biggest_cluster)
print(",".join(biggest_cluster))
