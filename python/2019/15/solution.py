import random
from collections import defaultdict, deque
import common
year_common = common.import_year_common(2019)

tape = common.extract_numbers(common.read_file('2019/15/data.txt'))
pos = 0, 0
new_pos = None

def move(pos, direction):
    if direction == 1:
        return pos[0], pos[1]+1
    if direction == 2:
        return pos[0], pos[1]-1
    if direction == 3:
        return pos[0]-1, pos[1]
    return pos[0]+1, pos[1]

def input_generator(next_dir):
    global pos
    global new_pos

    while True:
        direction = next(next_dir)

        new_pos = move(pos, direction)
        yield direction

# part 1
mem = year_common.tape_to_mem(tape)
pos = 0, 0
explored = {(0, 0): (0, False)} # (x, y) -> (distance, is fully explored)

class FinishedException(Exception): pass
def next_dir():
    global pos

    while True:
        for d in range(1, 5):
            n = move(pos, d)
            if n not in explored:
                yield d
                break
        else:
            for d in range(1, 5):
                n = move(pos, d)
                _, is_fully_explored = explored[n]
                if not is_fully_explored:
                    yield d
                    break
            else:
                raise FinishedException()

output = year_common.run_intcode(mem, input_generator(next_dir()))

try:
    while True:
        result = next(output)
        if result == 0:
            explored[new_pos] = -1, True
        else:
            curr_dist, _ = explored[pos]
            pos = new_pos
            if result == 2:
                print('part 1:', curr_dist+1)
                oxygen_pos = pos

        neighbors = [move(pos, d) for d in range(1, 5)]
        explored_neighbors = len([n for n in neighbors if n in explored and explored[n][1]])
        is_fully_explored = explored_neighbors >= 3
        dist = min(curr_dist+1, explored[pos][0]) if pos in explored else curr_dist+1
        explored[pos] = dist, is_fully_explored

except StopIteration:
    print('intcode halted unexpectedly')
    exit(1)
except FinishedException:
    pass

# part 2
moves = deque([(0, oxygen_pos)])
seen = set()
max_dist = 0

while len(moves) > 0:
    dist, pos = moves.popleft()
    if pos in seen:
        continue
    seen.add(pos)
    if explored[pos][0] == -1:
        continue
    if dist > max_dist:
        max_dist = dist
    for d in range(1, 5):
        n = move(pos, d)
        moves.append((dist+1, n))

print('part 2:', max_dist)
