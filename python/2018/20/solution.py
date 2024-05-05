import queue
import common

data = common.read_file()[1:-1]

sample0 = 'WNE'
sample1 = 'ENWWW(NEEE|SSE(EE|N))'
sample2 = 'ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN'
sample3 = 'ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))'
sample4 = 'WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))'

dirs = ['N', 'E', 'S', 'W']

def parse_chain(expr):
    i = 0
    result = []

    while i < len(expr):
        curr = expr[i]
        if curr == '(':
            offset, parsed = parse_or(expr[i:])
            i += offset
            result.append(parsed)
            assert expr[i-1] == ')'
        elif curr in dirs:
            i += 1
            result.append(curr)
        else:
            break

    return i, result

def parse_or(or_data):
    curr_data = or_data
    curr_offset = 0
    result = []
    while curr_data[0] != ')':
        start = curr_data[1:]
        offset, parsed = parse_chain(start)
        curr_offset += (offset+1)
        curr_data = or_data[curr_offset:]
        result.append(parsed)

    return (curr_offset+1), tuple(result)

# def measure_chain(chain):
#     acc = 0
#     for item in chain:
#         if isinstance(item, tuple):
#             acc += measure_or(item)
#         else:
#             acc += 1
#     return acc

# def measure_or(or_data):
#     for item in or_data:
#         if len(item) == 0:
#             return 0

#     lens = map(measure_chain, or_data)
#     return max(lens)

def plus(a, b):
    return a[0]+b[0], a[1]+b[1]

dir_offsets = {
    'N': (0, -1),
    'E': (1, 0),
    'W': (-1, 0),
    'S': (0, 1)
}

def find_neighbors_chain(neighbors, chain, at):
    for item in chain:
        if at not in neighbors:
            neighbors[at] = set()
        if isinstance(item, tuple):
            find_neighbors_or(neighbors, item, at)
        else:
            offset = dir_offsets[item]
            new_pos = plus(at, offset)
            neighbors[at].add(new_pos)
            at = new_pos

def find_neighbors_or(neighbors, or_data, at):
    for item in or_data:
        find_neighbors_chain(neighbors, item, at)

def construct_chain(chain):
    result = ''
    for item in chain:
        if isinstance(item, tuple):
            result += construct_or(item)
        else:
            result += item
    return result

def construct_or(or_data):
    constructed = map(construct_chain, or_data)
    joined = '|'.join(constructed)
    return '('+joined+')'

def find_depth(neighbors):
    q = queue.deque([(0, (0, 0))])
    seen = set()
    max_depth = 0

    while len(q) > 0:
        depth, at = q.popleft()
        if at in seen:
            continue
        seen.add(at)
        if depth > max_depth:
            max_depth = depth
        if at in neighbors:
            for n in neighbors[at]:
                q.append((depth+1, n))

    return max_depth

def find_deep(neighbors, min_depth):
    q = queue.deque([(0, (0, 0))])
    seen = set()
    found = 0

    while len(q) > 0:
        depth, at = q.popleft()
        if at in seen:
            continue
        seen.add(at)
        if depth >= min_depth:
            found += 1
        if at in neighbors:
            for n in neighbors[at]:
                q.append((depth+1, n))

    return found

tests = [
    data,
    sample0,
    sample1,
    sample2,
    sample3,
    sample4
]

for test in tests:
    _, parsed = parse_chain(test)
    constructed = construct_chain(parsed)
    result = test == constructed
    if not result:
        print('failed reconstruction for:', test)
    neighbors = {}
    find_neighbors_chain(neighbors, parsed, (0, 0))
    depth = find_depth(neighbors)
    deep_amount = find_deep(neighbors, 1000)
    print(depth, deep_amount)
