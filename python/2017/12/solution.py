import queue
import common

data = common.read_file()
lines = data.splitlines()


def parse_line(line):
    segments = line.split(' ')
    left = int(segments[0])
    right = list(map(lambda x: int(x.rstrip(',')), segments[2:]))
    return left, right


node_data = {l: (r, False) for l, r in map(parse_line, lines)}


def search_connected(init_node, all_nodes):
    q = queue.Queue()
    q.put(init_node)
    group_size = 0

    while not q.empty():
        el = q.get()
        connected, visited = all_nodes[el]
        if visited:
            continue
        group_size += 1
        for c in connected:
            q.put(c)
        all_nodes[el] = (connected, True)

    return group_size, all_nodes


# part 1
found, _ = search_connected(0, node_data)
print(found)

# part 2
groups = 0
while True:
    not_visited = list(filter(lambda x: not node_data[x][1], node_data))
    if len(not_visited) == 0:
        break
    groups += 1
    first = not_visited[0] 
    _, node_data = search_connected(first, node_data)

print(groups+1)  # +1 because the 0 group was already marked as visited
