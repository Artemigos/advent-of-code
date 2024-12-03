import common

lines = common.read_file().splitlines()

class Node:
    def __init__(self, left = None, right = None, data = None):
        self.left = left
        self.right = right
        self.data = data

    def __repr__(self):
        if self.is_number():
            return repr(self.data)
        return '[' + repr(self.left) + ',' + repr(self.right) + ']'

    def copy(self):
        l = self.left.copy() if self.left else None
        r = self.right.copy() if self.right else None
        return Node(l, r, self.data)

    def is_number(self):
        return self.data is not None

    def calc_magnitude(self):
        if self.is_number():
            return self.data
        return 3*self.left.calc_magnitude() + 2*self.right.calc_magnitude()

    def traverse(self, parents=None):
        parents = parents or []
        if self.left is not None:
            yield from self.left.traverse(parents+[self])
        yield self, parents
        if self.right is not None:
            yield from self.right.traverse(parents+[self])

# parse

def read_num(data:str, offset:int):
    c = data[offset]
    if not c.isdigit():
        return offset, None
    val = ord(c) - ord('0')
    return offset+1, Node(data=val)

def read_pair(data:str, offset:int):
    if data[offset] != '[':
        return offset, None
    offset, child1 = read_node(data, offset+1)
    if data[offset] != ',':
        raise 'invalid data: "," expected'
    offset, child2 = read_node(data, offset+1)
    if data[offset] != ']':
        raise 'invalid data: "]" expected'
    return offset+1, Node(child1, child2)

def read_node(data:str, offset:int):
    offset, node = read_num(data, offset)
    if node is None:
        offset, node = read_pair(data, offset)
    if node is None:
        raise 'invalid data'
    return offset, node

numbers = []
for line in lines:
    offset, node = read_node(line, 0)
    assert offset == len(line)
    assert node is not None
    numbers.append(node)

# part 1

def reduce(node):
    node = node.copy()
    while True:
        nodes = list(node.traverse())
        explode_candidates = list(filter(lambda x: not x[0].is_number() and x[0].left.is_number() and x[0].right.is_number() and len(x[1]) >= 4, nodes))
        if explode_candidates:
            ex_node, parents = explode_candidates[0]
            i = nodes.index((ex_node, parents))
            for si in range(i-2, -1, -1):
                if nodes[si][0].is_number():
                    nodes[si][0].data += ex_node.left.data
                    break
            for si in range(i+2, len(nodes)):
                if nodes[si][0].is_number():
                    nodes[si][0].data += ex_node.right.data
                    break
            substitute = Node(data=0)
            if parents[-1].left is ex_node:
                parents[-1].left = substitute
            else:
                parents[-1].right = substitute
            continue
        split_candidates = list(filter(lambda x: x[0].is_number() and x[0].data > 9, nodes))
        if split_candidates:
            spl_node, parents = split_candidates[0]
            left_val = spl_node.data // 2
            right_val = spl_node.data - left_val
            substitute = Node(Node(data=left_val), Node(data=right_val))
            if spl_node is parents[-1].left:
                parents[-1].left = substitute
            else:
                parents[-1].right = substitute
            continue
        break
    return node

def add(n1, n2):
    return reduce(Node(n1, n2))

acc = numbers[0]
for n in numbers[1:]:
    acc = add(acc, n)

print(acc.calc_magnitude())

# part 2
results = []
for i in range(len(numbers)):
    for j in range(len(numbers)):
        if i == j:
            continue
        result = add(numbers[i], numbers[j]).calc_magnitude()
        results.append(result)

print(max(results))
