import common
from collections import deque

data = common.read_file()
lines = data.splitlines()
w = len(lines[0])
h = len(lines)
start_y, start_x = divmod(data.find('S'), w+1)
end_y, end_x = divmod(data.find('E'), w+1)

# part 1
def walk(start_x, start_y) -> dict[tuple[int, int], int]:
    dist_map = {}
    q = deque()
    q.append((0, start_x, start_y))
    seen = set()
    while q:
        depth, x, y = q.popleft()
        k = x, y
        if k in seen:
            continue
        seen.add(k)
        dist_map[(x, y)] = depth
        for n in common.neighbors_ortho(k):
            nx, ny = n
            if lines[ny][nx] != '#':
                q.append((depth+1, nx, ny))
    return dist_map

start_dist_map = walk(start_x, start_y)
end_dist_map = walk(end_x, end_y)
uncheated_dist = end_dist_map[(start_x, start_y)]

solutions = []
for y in range(h):
    for x in range(w):
        k = x, y
        dist = start_dist_map.get(k)
        if dist is None or dist >= uncheated_dist:
            continue
        for n1 in common.neighbors_ortho(k):
            n1x, n1y = n1
            if lines[n1y][n1x] != '#':
                continue
            for n2 in common.neighbors_ortho(n1):
                n2x, n2y = n2
                if n2x < 0 or n2y < 0 or n2x >= w or n2y >= h:
                    continue
                if lines[n2y][n2x] == '#':
                    continue
                final_dist = dist + 2 + end_dist_map[n2]
                if final_dist < uncheated_dist:
                    solutions.append((final_dist, n1, n2))

print(len([x for x in solutions if uncheated_dist - x[0] >= 100]))

# part 2
solutions = []
for y in range(h):
    for x in range(w):
        k = x, y
        dist = start_dist_map.get(k)
        if dist is None or dist >= uncheated_dist:
            continue
        for dy in range(-20, 21):
            for dx in range(-20, 21):
                ddist = abs(dx) + abs(dy)
                if ddist < 2 or ddist > 20:
                    continue
                fx, fy = x+dx, y+dy
                if fx < 0 or fy < 0 or fx >= w or fy >= h:
                    continue
                if lines[fy][fx] == '#':
                    continue
                final_dist = dist + ddist + end_dist_map[(fx, fy)]
                if final_dist < uncheated_dist:
                    solutions.append((final_dist, k, (fx, fy)))

print(len([x for x in solutions if uncheated_dist - x[0] >= 100]))
