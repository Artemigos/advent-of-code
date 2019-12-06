import common
from collections import deque

data = common.read_file('2019/06/data.txt').splitlines()
relations = list(map(lambda x: x.split(')'), data))

is_orbited = {}
is_orbiting = {}
planets = set()

for l, r in iter(relations):
    if l not in is_orbited:
        is_orbited[l] = []

    is_orbited[l].append(r)
    is_orbiting[r] = l
    planets.add(l)
    planets.add(r)

# part 1
amount = 0
for planet in planets:
    curr = planet
    while curr in is_orbiting:
        curr = is_orbiting[curr]
        amount += 1

print('part 1:', amount)

# part 2
seen = set()
steps = deque([('YOU', 0)])

while len(steps) > 0:
    where, dist = steps.popleft()
    if where == 'SAN':
        print('part 2:', dist-2) # first and last step are not counted
        break
    if where in seen:
        continue
    seen.add(where)
    if where in is_orbited:
        for x in is_orbited[where]:
            steps.append((x, dist+1))
    if where in is_orbiting:
        steps.append((is_orbiting[where], dist+1))
