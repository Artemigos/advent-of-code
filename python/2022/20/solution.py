import common

nums = [int(x) for x in common.read_file().splitlines()]

class Node:
    def __init__(self, v, l: "Node", r: "Node"):
        self.v = v
        self.l = l
        self.r = r

nodes = [Node(n, None, None) for n in nums]

for i in range(len(nodes)):
    il = (i-1)%len(nodes)
    ir = (i+1)%len(nodes)
    nodes[i].l = nodes[il]
    nodes[i].r = nodes[ir]

# part 1
zero_node = None
for node in nodes:
    if node.v == 0:
        zero_node = node
        continue
    node.l.r = node.r
    node.r.l = node.l
    if node.v < 0:
        curr = node
        for _ in range(-node.v):
            curr = curr.l
        l = curr.l
        r = curr
    else:
        curr = node
        for _ in range(node.v):
            curr = curr.r
        l = curr
        r = curr.r
    node.l = l
    node.r = r
    l.r = node
    r.l = node

assert zero_node is not None
curr = zero_node
acc = 0
for _ in range(3):
    for _ in range(1000):
        curr = curr.r
    acc += curr.v

print(acc)

# part 2
nodes = [Node(n, None, None) for n in nums]

for i in range(len(nodes)):
    il = (i-1)%len(nodes)
    ir = (i+1)%len(nodes)
    nodes[i].l = nodes[il]
    nodes[i].r = nodes[ir]

zero_node = None
mod_num = len(nodes)-1
for node in nodes:
    node.v = node.v * 811589153
for _ in range(10):
    for node in nodes:
        if node.v == 0:
            zero_node = node
            continue
        node.l.r = node.r
        node.r.l = node.l
        if node.v < 0:
            curr = node
            amount = mod_num - (node.v % mod_num)
            for _ in range(amount):
                curr = curr.l
            l = curr.l
            r = curr
        else:
            curr = node
            amount = node.v % mod_num
            for _ in range(amount):
                curr = curr.r
            l = curr
            r = curr.r
        node.l = l
        node.r = r
        l.r = node
        r.l = node

assert zero_node is not None
curr = zero_node
acc = 0
for _ in range(3):
    for _ in range(1000):
        curr = curr.r
    acc += curr.v

print(acc)
