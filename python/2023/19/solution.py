import common
from collections import deque

workflow_data, parts_data = common.read_file().split('\n\n')

# parse
parts = [tuple(common.extract_numbers(x)) for x in parts_data.splitlines()]
workflows = {}
for line in workflow_data.splitlines():
    k, rest = line.split('{')
    rest = rest[:-1]
    rules = rest.split(',')
    unconditional = rules[-1]
    rs = []
    for r in rules[:-1]:
        cond, target = r.split(':')
        f = eval('lambda x, m, a, s: ' + cond)
        rs.append((f, target, cond))
    rs.append((lambda *_: True, unconditional, 'x>-1'))
    workflows[k] = rs

# part 1
acc = 0
for part in parts:
    curr = 'in'
    while curr not in ['A', 'R']:
        w = workflows[curr]
        for r in w:
            f, target, _ = r
            if f(*part):
                curr = target
                break
    if curr == 'A':
        acc += sum(part)
print(acc)

# part 2
n2i = {
    'x': 0,
    'm': 1,
    'a': 2,
    's': 3,
}

part = (range(1, 4001), range(1, 4001), range(1, 4001), range(1, 4001))
q = deque()
q.append(('in', part))
acc = 0
while len(q) != 0:
    curr, part = q.popleft()
    if curr == 'A':
        acc += common.product(map(len, part))
        continue
    if curr == 'R':
        continue
    if any([len(x) == 0 for x in part]):
        continue
    w = workflows[curr]
    remainder = list(part)
    for r in w:
        _, target, cond = r
        vi = n2i[cond[0]]
        val = int(cond[2:])
        if cond[1] == '>':
            npart = list(remainder)
            npart[vi] = range(max(val+1, npart[vi].start), npart[vi].stop)
            remainder[vi] = range(remainder[vi].start, min(remainder[vi].stop, val+1))
            q.append((target, npart))
        else: # '<'
            npart = list(remainder)
            npart[vi] = range(npart[vi].start, min(npart[vi].stop, val))
            remainder[vi] = range(max(val, remainder[vi].start), remainder[vi].stop)
            q.append((target, npart))
print(acc)
