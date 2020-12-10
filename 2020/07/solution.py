from collections import deque
import common

def cut_off_last_word(s):
    i = s.rindex(' ')
    return s[:i]

lines = common.read_file('2020/07/data.txt').splitlines()
lines = common.pipe_map(
    lambda x: x.rstrip('.'),
    lambda x: x.split(' contain '),
    lambda x: (cut_off_last_word(x[0]), list(map(cut_off_last_word, x[1].split(', ')))),
    lines
)

graph = {}
rev_graph = {}
for l in lines:
    k, edges = l
    graph[k] = {}
    for e in edges:
        if e == 'no other':
            continue

        i = e.find(' ')
        num = int(e[:i])
        color = e[i+1:]
        graph[k][color] = num

        if color not in rev_graph:
            rev_graph[color] = {}
        rev_graph[color][k] = num

# part 1
contain_gold = set()
q = deque()
q.append('shiny gold')

while len(q) > 0:
    el = q.popleft()
    if el not in rev_graph:
        continue
    edges = rev_graph[el]
    for e in edges:
        contain_gold.add(e)
        q.append(e)

print(len(contain_gold))

# part 2
acc = 0
q = deque()
q.append('shiny gold')

while len(q) > 0:
    el = q.popleft()
    if el not in graph:
        continue
    edges = graph[el]
    for k, v in edges.items():
        acc += v
        for i in range(v):
            q.append(k)

print(acc)
