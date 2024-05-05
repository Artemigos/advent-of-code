import collections
import common

board = common.read_file().splitlines()
board = [list(x) for x in board]
w = len(board[0])
h = len(board)

part1_steps = 10
part2_steps = 1000000000

def output_board():
    for line in board:
        print(''.join(line))

def get_at(x, y):
    if 0 <= x < w and 0 <= y < h:
        return board[y][x]
    return None

def set_at(x, y, val):
    board[y][x] = val

def get_neighbors(x, y):
    yield x-1, y-1
    yield x, y-1
    yield x+1, y-1
    yield x-1, y
    yield x+1, y
    yield x-1, y+1
    yield x, y+1
    yield x+1, y+1

def step():
    result = []
    for y in range(h):
        row = []
        result.append(row)
        for x in range(w):
            cnt = collections.Counter()
            for n in get_neighbors(x, y):
                cnt[get_at(*n)] += 1
            me = get_at(x, y)
            if me == '.':
                if cnt['|'] >= 3:
                    row.append('|')
                else:
                    row.append('.')
            elif me == '|':
                if cnt['#'] >= 3:
                    row.append('#')
                else:
                    row.append('|')
            else:
                if cnt['#'] >= 1 and cnt['|'] >= 1:
                    row.append('#')
                else:
                    row.append('.')
    return result

for i in range(part1_steps):
    board = step()

def collect_results():
    final_countdown = collections.Counter()
    for y in range(h):
        for x in range(w):
            final_countdown[get_at(x, y)] += 1

    print(final_countdown['|'], final_countdown['#'], final_countdown['|']*final_countdown['#'])

output_board()
collect_results()

# part 2

seen_at = {}

def hash_board():
    acc = 0
    for y in range(h):
        for x in range(w):
            acc = acc << 2
            me = board[y][x]
            if me == '|':
                acc += 1
            elif me == '#':
                acc += 2
    return acc

loop_size = None

for i in range(part2_steps-part1_steps):
    board = step()
    hsh = hash_board()
    if hsh in seen_at:
        loop_size = i-seen_at[hsh]
    seen_at[hsh] = i

    if loop_size is not None:
        left_steps = part2_steps-part1_steps-i-1
        if left_steps % loop_size == 0:
            break

output_board()
collect_results()
