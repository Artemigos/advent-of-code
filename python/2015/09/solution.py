import common
import itertools

locations = set()
distances = dict()

lines = common.read_file().splitlines()

for line in lines:
    segments = line.split()
    locations.add(segments[0])
    locations.add(segments[2])
    distances[segments[0], segments[2]] = int(segments[4])
    distances[segments[2], segments[0]] = int(segments[4])

min_dist = None
max_dist = 0
for order in itertools.permutations(locations):
    dist = 0
    for i in range(len(order)-1):
        dist += distances[order[i], order[i+1]]
    if min_dist is None or dist < min_dist:
        min_dist = dist
    if dist > max_dist:
        max_dist = dist

print(min_dist)
print(max_dist)
