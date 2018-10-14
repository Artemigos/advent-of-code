import common

data = common.read_file('2017/16/data.txt')
moves = data.split(',')
repetitions = 1000000000

state = list(map(chr, range(ord('a'), ord('q'))))
len_state = len(state)
pos0 = 0
pos_index = list(range(len_state))
orda = ord('a')

def ordinal_of(character):
    return ord(character) - orda

def index_of(character):
    return pos_index[ordinal_of(character)]

def swap_index(ch1, ch2):
    i1 = ordinal_of(ch1)
    i2 = ordinal_of(ch2)
    tmp = pos_index[i1]
    pos_index[i1] = pos_index[i2]
    pos_index[i2] = tmp

def calc_index(index):
    result = pos0 + index
    if result >= len_state:
        result -= len_state
    return result

def spin(amount):
    global pos0
    pos0 -= amount
    while pos0 < 0:
        pos0 += len_state
    while pos0 >= len_state:
        pos0 -= len_state

def exchange(i1, i2):
    i1 = calc_index(i1)
    i2 = calc_index(i2)
    v1 = state[i1]
    v2 = state[i2]
    state[i1] = v2
    state[i2] = v1
    swap_index(v1, v2)

def partner(v1, v2):
    i1 = index_of(v1)
    i2 = index_of(v2)
    state[i1] = v2
    state[i2] = v1
    swap_index(v1, v2)

def get_full():
    for i in range(len_state):
        ind = calc_index(i)
        yield state[ind]

def parse_move(move):
    m_type = move[0]
    m_data = move[1:]

    if m_type == 's':
        amount = int(m_data)
        return (m_type, amount)
    if m_type == 'x':
        parts = m_data.split('/')
        return (m_type, (int(parts[0]), int(parts[1])))
    parts = m_data.split('/')
    return (m_type, (parts[0], parts[1]))

parsed_moves = list(map(parse_move, moves))
def apply_moves(moves, repetitions=1):
    for i in range(repetitions):
        for t, v in moves:
            if t == 's':
                spin(v)
            elif t == 'x':
                exchange(v[0], v[1])
            else:
                partner(v[0], v[1])
        if i % 100 == 0:
            print(i/10000000, '%')

# part 1
apply_moves(parsed_moves)
print(''.join(get_full()))

# part 2
apply_moves(parsed_moves, repetitions-1)
print(''.join(get_full()))
# NOTE: this is way to slow, needs optimization
