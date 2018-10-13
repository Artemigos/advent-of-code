import itertools
import queue
import common

data = common.read_file('2017/12/data.txt')
lines = data.splitlines()

def parse_line(line):
    segments = line.split(' ')
    left = int(segments[0])
    right = list(map(lambda x: int(x.rstrip(',')), segments[2:]))
    return (left, right)

node_data = dict()
for l, r in map(parse_line, lines):
    node_data[l] = (r, False)

def search_connected(init_node, node_data):
    # BFS
    q = queue.Queue()
    q.put(init_node)
    found = 0

    while not q.empty():
        el = q.get()
        connected, visited = node_data[el]
        if visited:
            continue
        found += 1
        for c in connected:
            q.put(c)
        node_data[el] = (connected, True)

    return (found, node_data)

# part 1
# found, _ = search_connected(0, node_data)
# print(found)

# part 2
groups = 0
while True:
    not_visited = list(filter(lambda x: not node_data[x][1], node_data))
    if len(not_visited) == 0:
        break
    groups += 1
    first = not_visited[0] 
    _, node_data = search_connected(first, node_data)

print(groups)
