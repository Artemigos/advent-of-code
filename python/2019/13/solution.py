from collections import defaultdict
import common
year_common = common.import_year_common(2019)

tape = common.extract_numbers(common.read_file())

# part 1
mem = year_common.tape_to_mem(tape)
it = year_common.run_intcode(mem, iter([]))

blocks = 0
try:
    while True:
        x = next(it)
        y = next(it)
        tile = next(it)

        if tile == 2:
            blocks += 1
except StopIteration:
    pass

print(blocks)

# part 2
mem = year_common.tape_to_mem(tape)
mem[0] = 2
board = defaultdict(lambda: 0)
paddles = []
balls = []
score = 0
maxx = 0
maxy = 0

def update_board(x, y, tile):
    global board
    global paddles
    global balls

    pos = x, y
    if pos in paddles:
        paddles.remove(pos)
    if pos in balls:
        balls.remove(pos)

    if tile == 3:
        paddles.append(pos)
    elif tile == 4:
        balls.append(pos)

    board[pos] = tile

def sign(num):
    return num//abs(num) if num != 0 else 0

def print_board():
    for y in range(maxy+1):
        for x in range(maxx+1):
            pos = x, y
            if board[pos] == 1:
                print('▓', end='')
            elif board[pos] == 2:
                print('X', end='')
            elif board[pos] == 3:
                print('-', end='')
            elif board[pos] == 4:
                print('o', end='')
            else:
                print(' ', end='')
        print()
    print()

def controls():
    global board
    global balls
    global paddles
    global maxx
    global maxy

    maxx = max(map(lambda x: x[0], board.keys()))
    maxy = max(map(lambda x: x[1], board.keys()))

    while True:
        # print_board()
        move_diff = balls[0][0]-paddles[0][0]
        yield sign(move_diff)

it = year_common.run_intcode(mem, controls())

try:
    while True:
        x = next(it)
        y = next(it)
        tile = next(it)

        if (x, y) == (-1, 0):
            score = tile

        update_board(x, y, tile)
except StopIteration:
    pass

print(score)
