import common
year_common = common.import_year_common(2019)

tape = common.extract_numbers(common.read_file('2019/17/data.txt'))

mem = year_common.tape_to_mem(tape)
x, y = 0, 0
board = {}
maxx = 0
maxy = 0

for o in year_common.run_intcode(mem, iter([])):
    board[x, y] = chr(o)

    if x > maxx:
        maxx = x
    if y > maxy:
        maxy = y

    if o == 10:
        y += 1
        x = 0
    else:
        x += 1

acc = 0
for y in range(maxy):
    for x in range(maxx):
        if board[x, y] == '#' and (x-1, y) in board and board[x-1, y] == '#' and (x+1, y) in board and board[x+1, y] == '#' \
            and (x, y-1) in board and board[x, y-1] == '#' and (x, y+1) in board and board[x, y+1] == '#':
            acc += x*y

print('part 1:', acc)

# part 2
# manual analysis
# L, 10, R, 12, R, 12, R, 6, R, 10, L, 10, L, 10, R, 12, R, 12, R, 10, L, 10, L, 12, R, 6, R, 6, R, 10, L, 10, R, 10, L, 10, L, 12, R, 6, R, 6, R, 10, L, 10, R, 10, L, 10, L, 12, R, 6, L, 10, R, 12, R, 12, R, 10, L, 10, L, 12, R, 6
sequence = 'C,B,C,A,B,A,B,A,C,A\n'
program_A = 'R,10,L,10,L,12,R,6\n'
program_B = 'R,6,R,10,L,10\n'
program_C = 'L,10,R,12,R,12\n'

input_data = sequence + program_A + program_B + program_C

input_asked = False
def input_generator():
    global input_asked
    input_asked = True

    for c in input_data:
        yield ord(c)
    yield ord('n')
    yield 10

mem = year_common.tape_to_mem(tape)
mem[0] = 2

print('part 2:')
for x in year_common.run_intcode(mem, input_generator()):
    if x < 256:
        print(chr(x), end='')
    else:
        print(x)
