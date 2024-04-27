import common
from collections import deque
from ast import literal_eval

lines = common.read_file().splitlines()

droplets = set()

for line in lines:
    droplets.add(literal_eval('('+line+')'))

# part 1
acc = 0
for d in droplets:
    acc += len([n for n in common.neighbors_ortho(d) if n not in droplets])

print(acc)

# part 2
min_x = min((d[0] for d in droplets))
max_x = max((d[0] for d in droplets))
min_y = min((d[1] for d in droplets))
max_y = max((d[1] for d in droplets))
min_z = min((d[2] for d in droplets))
max_z = max((d[2] for d in droplets))
rx = range(min_x, max_x+1)
ry = range(min_y, max_y+1)
rz = range(min_z, max_z+1)

full = set(droplets)
not_full = set()

for x in rx:
    for y in ry:
        for z in rz:
            p = x, y, z
            if p in full or p in not_full:
                continue
            q = deque([p])
            exited = False
            seen = set()
            while len(q) > 0:
                curr_p = q.popleft()
                cx, cy, cz = curr_p
                if curr_p in full or curr_p in seen:
                    continue
                if (cx not in rx) or (cy not in ry) or (cz not in rz):
                    exited = True
                    continue
                seen.add(curr_p)
                for n in common.neighbors_ortho(curr_p):
                    q.append(n)
            target = not_full if exited else full
            for curr_p in seen:
                target.add(curr_p)

acc = 0
for d in droplets:
    acc += len([n for n in common.neighbors_ortho(d) if n not in full])

print(acc)
