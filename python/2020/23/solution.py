import common

data = list(map(int, common.read_file().strip()))

class LinkedRotBufNode:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next_node = next_node

def find_destination_value(curr_node:LinkedRotBufNode, moving_values:list, min_val, max_val):
    destination_value = curr_node.value-1
    if destination_value < min_val:
        destination_value = max_val
    while destination_value in moving_values:
        destination_value -= 1
        if destination_value < min_val:
            destination_value = max_val
    return destination_value

def play(cups, moves):
    # prepare data
    min_val = min(cups)
    max_val = max(cups)

    nodes = {}
    first_node = None
    last_node = None

    for x in cups:
        node = LinkedRotBufNode(x)
        nodes[x] = node
        if first_node is None:
            first_node = node
        if last_node is not None:
            last_node.next_node = node
        last_node = node

    last_node.next_node = first_node

    # run moves
    curr = first_node
    for _ in range(moves):
        # collect affected nodes
        first_moved = curr.next_node
        moving_values = [first_moved.value, first_moved.next_node.value, first_moved.next_node.next_node.value]
        last_moved = first_moved.next_node.next_node
        first_left = last_moved.next_node
        destination_value = find_destination_value(curr, moving_values, min_val, max_val)
        move_after = nodes[destination_value]
        move_before = move_after.next_node

        # reattach nodes
        curr.next_node = first_left
        move_after.next_node = first_moved
        last_moved.next_node = move_before

        curr = first_left

    return nodes

# part 1
nodes = play(data, 100)

# collect result
curr = nodes[1].next_node
acc = ''
while curr.value != 1:
    acc += str(curr.value)
    curr = curr.next_node

print(acc)

# part 2
cups = data + list(range(10, 1000001))
nodes = play(cups, 10000000)

one = nodes[1]
print(one.next_node.value * one.next_node.next_node.value)
