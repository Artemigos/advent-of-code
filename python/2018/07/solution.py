import collections as coll
import queue
import re
import common

lines = common.read_file().splitlines()
parsed = [re.findall(r'\w+', x) for x in lines]

deps = coll.defaultdict(set)
steps = set()

for row in parsed:
    deps[row[7]].add(row[1])
    steps.add(row[1])
    steps.add(row[7])

available = set()
acc = ''
for s in steps:
    if s not in deps:
        available.add(s)
while len(available) > 0:
    nxt = min(available)
    available.remove(nxt)
    acc += nxt
    for d in deps:
        if nxt in deps[d]:
            for dd in deps[d]:
                if dd not in acc:
                    break
            else:
                available.add(d)

print(acc)


workers = queue.PriorityQueue()
for i in range(5):
    workers.put(0)

available = queue.PriorityQueue()
for s in steps:
    if s not in deps:
        available.put((0, s))

acc = ''
while not available.empty():
    when, el = available.get()
    worker = workers.get()
    ready_after = max([when, worker])
    cost = 60
    cost += ord(el[0])-ord('A')+1
    finish = ready_after+cost
    acc += el
    for d in deps:
        if el in deps[d]:
            for dd in deps[d]:
                if dd not in acc:
                    break
            else:
                available.put((finish, d))
    workers.put(finish)

while not workers.empty():
    print('worker finish at', workers.get())
print(acc)
