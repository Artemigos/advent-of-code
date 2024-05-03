import queue
import common

data = int(common.read_file().strip())

def can_step(x, y):
    num = x*x + 3*x + 2*x*y + y + y*y + data
    bin_num = bin(num)
    cnt = bin_num.count('1')
    steppable = cnt%2 == 0
    return steppable

# part 1
moves = queue.deque([(0, (1, 1))])
seen_positions = set()

while len(moves) > 0:
    depth, move = moves.popleft()
    if move == (31, 39):
        print(depth)
        break
    if move in seen_positions:
        continue
    seen_positions.add(move)
    x, y = move
    if x < 0 or y < 0:
        continue
    if not can_step(x, y):
        continue
    moves.append((depth+1, (x+1, y)))
    moves.append((depth+1, (x-1, y)))
    moves.append((depth+1, (x, y+1)))
    moves.append((depth+1, (x, y-1)))

# part 2
moves = queue.deque([(0, (1, 1))])
seen_positions = set()

while len(moves) > 0:
    depth, move = moves.popleft()
    if depth >= 51:
        break
    x, y = move
    if x < 0 or y < 0:
        continue
    if not can_step(x, y):
        continue
    if move in seen_positions:
        continue
    seen_positions.add(move)
    moves.append((depth+1, (x+1, y)))
    moves.append((depth+1, (x-1, y)))
    moves.append((depth+1, (x, y+1)))
    moves.append((depth+1, (x, y-1)))

print(len(seen_positions))
