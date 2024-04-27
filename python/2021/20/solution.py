import common

lines = common.read_file('2021/20/data.txt').splitlines()
reference = lines[0]
board = lines[2:]
w = len(board[0])
h = len(board)

# precalculate things

bit_index = []
for i in range(8):
    a = []
    for j in range(8):
        b = []
        for k in range(8):
            idx = (i<<6)|(j<<3)|(k)
            b.append(1 if reference[idx] == '#' else 0)
        a.append(b)
    bit_index.append(a)

next_num = []
for i in range(8):
    a = []
    for j in range(2):
        nxt = ((i&3)<<1)|j
        a.append(nxt)
    next_num.append(a)

nboard = []
for y in range(h):
    row = [0]
    for x in range(w):
        n = 1 if board[y][x] == '#' else 0
        row.append(next_num[row[x]][n])
    row.append(next_num[row[-1]][0])
    row.append(next_num[row[-1]][0])
    row.append(next_num[row[-1]][0])
    nboard.append(row)

# part 1 and 2

# print(bit_index[0][0][0])
# print(bit_index[7][7][7])
# observation - the infinite field oscillates between '#' and '.'

def make_step(nboard):
    w = len(nboard[0])
    h = len(nboard)
    new_board = []
    curr_inf = nboard[0][0]
    next_inf = bit_index[curr_inf][curr_inf][curr_inf]
    next_inf = (next_inf<<2)|(next_inf<<1)|next_inf

    def get_at(x, y):
        if x < 0 or x >= w or y < 0 or y >= h:
            return curr_inf
        return nboard[y][x]

    for y in range(h+2):
        row = [next_inf]
        for x in range(w+2):
            bit = bit_index[get_at(x, y-2)][get_at(x, y-1)][get_at(x, y)]
            val = next_num[row[-1]][bit]
            row.append(val)
        new_board.append(row)
    return new_board

def convert_back(nboard):
    board = []
    for y in range(len(nboard)):
        row = ''
        for x in range(0, len(nboard[y]), 3):
            for c in bin(nboard[y][x])[2:].rjust(3, '0'):
                row += '#' if c == '1' else '.'
        board.append(row)
    return board

def show_result(result):
    display = convert_back(result)
    acc = 0
    for y in range(len(display)):
        for c in display[y]:
            if c == '#':
                acc += 1
    print(acc)

result = nboard
for i in range(50):
    result = make_step(result)
    if i == 1:
        show_result(result)
show_result(result)
