import common
from functools import lru_cache

steps = common.read_file().strip().split(',')

# part 1
@lru_cache(maxsize=None)
def hsh(step):
    acc = 0
    for c in step:
        acc += ord(c)
        acc *= 17
        acc &= 0xFF
    return acc

print(sum(map(hsh, steps)))

# part 2
BOXES = 256
boxes = [[] for _ in range(BOXES)]

for step in steps:
    minus_i = step.find('-')
    if minus_i >= 0:
        label = step[:minus_i]
        q = boxes[hsh(label)]
        for el in q:
            if el[0] == label:
                q.remove(el)
                break
    else:
        label, focus = step.split('=')
        focus = int(focus)
        q = boxes[hsh(label)]
        for i in range(len(q)):
            el = q[i]
            if el[0] == label:
                q[i] = (label, focus)
                break
        else:
            q.append((label, focus))

print(sum([
    (bi+1) * (li+1) * boxes[bi][li][1]
    for bi in range(BOXES)
    for li in range(len(boxes[bi]))
]))
