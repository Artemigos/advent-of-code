import common
from collections import defaultdict, deque
import math

lines = common.read_file().splitlines()
board = set()
blizzards = defaultdict(lambda: [])
w = len(lines[0])
h = len(lines)
start = (1, 0)
end = (w-2, h-1)

for y in range(h):
    for x in range(w):
        if lines[y][x] == '#':
            board.add((x, y))
        elif lines[y][x] in '>v<^':
            blizzards[(x-1, y-1)].append(lines[y][x])

# precalculate blizzards
fw = w-2
fh = h-2
blizz_states = [blizzards]
loop_size = math.lcm(fw, fh)

for i in range(1, loop_size):
    last_state = blizz_states[-1]
    new_state = defaultdict(lambda: [])
    for x, y in last_state:
        for d in last_state[(x, y)]:
            if d == '>':
                new_state[((x+1)%fw, y)].append(d)
            elif d == 'v':
                new_state[(x, (y+1)%fh)].append(d)
            elif d == '<':
                new_state[((x-1)%fw, y)].append(d)
            elif d == '^':
                new_state[(x, (y-1)%fh)].append(d)
            else:
                raise '???'
    blizz_states.append(new_state)

# common
def solve(depth, start, end):
    q = deque([(depth, start[0], start[1])])
    seen = set()
    while len(q) > 0:
        depth, x, y = q.popleft()
        lp = depth%loop_size
        blizz = blizz_states[lp]
        pos = x, y
        b_pos = x-1, y-1
        if b_pos in blizz or pos in board or y < 0 or y >= h:
            continue
        k = x, y, lp
        if k in seen:
            continue
        seen.add(k)
        if pos == end:
            return depth
            break
        for n in common.neighbors_ortho(pos):
            q.append((depth+1, n[0], n[1]))
        q.append((depth+1, x, y))

# part 1
result = solve(0, start, end)
print(result)

# part 2
result = solve(result, end, start)
result = solve(result, start, end)
print(result)
