import common
from collections import deque

def build_forest(data):
    points = [tuple(common.extract_numbers(line)) for line in data.splitlines()]
    direct_connections = {}

    def manhattan_distance(p1, p2):
        return abs(p1[0]-p2[0])+abs(p1[1]-p2[1])+abs(p1[2]-p2[2])+abs(p1[3]-p2[3])

    for p in points:
        if p not in direct_connections:
            direct_connections[p] = []
        for p2 in points:
            if p == p2:
                continue
            if p2 not in direct_connections:
                direct_connections[p2] = []
            if manhattan_distance(p, p2) <= 3:
                direct_connections[p].append(p2)
                direct_connections[p2].append(p)

    unused_points = list(points)
    constellations = []
    while len(unused_points) > 0:
        start = unused_points[0]
        seen_points = set()
        q = deque([start])
        while len(q) > 0:
            p = q.popleft()
            if p in seen_points:
                continue
            seen_points.add(p)
            unused_points.remove(p)
            for rel in direct_connections[p]:
                q.append(rel)
        constellations.append(list(seen_points))
    return constellations

# part 1
constellations = build_forest(common.read_file())
print(len(constellations))
