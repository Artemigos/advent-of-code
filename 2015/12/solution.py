import json
import common

data = common.read_file('2015/12/data.txt')
obj = json.loads(data)

# part 1
def sum_nums(node):
    if type(node) == int:
        return node
    if type(node) == str:
        return 0
    if type(node) == list:
        vals = [sum_nums(subnode) for subnode in node]
        return sum(vals)
    # dict
    vals = [sum_nums(node[k]) for k in node.keys()]
    return sum(vals)

num_sum = sum_nums(obj)
print(num_sum)

# part 2
def sum_nums2(node):
    if type(node) == int:
        return node
    if type(node) == str:
        return 0
    if type(node) == list:
        vals = [sum_nums2(subnode) for subnode in node]
        return sum(vals)
    # dict
    if 'red' in node.values():
        return 0
    vals = [sum_nums2(node[k]) for k in node.keys()]
    return sum(vals)

num_sum = sum_nums2(obj)
print(num_sum)
