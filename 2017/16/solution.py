import common
# import array
# import numpy as np
import itertools

data = common.read_file('2017/16/data.txt')
moves = data.split(',')
repetitions = 1000000000
# repetitions = 1000
orda = ord('a')

def ordinal_of(character):
    return ord(character) - orda

state = list(range(ordinal_of('a'), ordinal_of('q')))
# state = array.array('b', state)
# state = np.array(state, dtype=np.int8)
len_state = len(state)
pos0 = 0
index_of = list(range(len_state))

def calc_index(pos, index):
    result = pos + index
    if result >= len_state:
        result -= len_state
    return result

precalculated_indexes = list()
for p in range(len_state):
    pos_vals = list()
    for i in range(len_state):
        pos_vals.append(calc_index(p, i))
    precalculated_indexes.append(pos_vals)

def swap_index(ch1, ch2):
    tmp = index_of[ch1]
    index_of[ch1] = index_of[ch2]
    index_of[ch2] = tmp

def create_spin_f(amount):
    def spin():
        global pos0
        pos0 -= amount
        # NOTE: range of input data allows simplifying
        # while pos0 < 0:
        #     pos0 += len_state
        # while pos0 >= len_state:
        #     pos0 -= len_state
        if pos0 < 0:
            pos0 += len_state
    return spin

def create_exchange_f(i1, i2):
    def exchange():
        ind1 = precalculated_indexes[pos0][i1]
        ind2 = precalculated_indexes[pos0][i2]
        ch1 = state[ind1]
        ch2 = state[ind2]
        state[ind1] = ch2
        state[ind2] = ch1
        # swap_index(ch1, ch2)
        # NOTE: pulled code in, since calls seem to be expensive
        tmp = index_of[ch1]
        index_of[ch1] = index_of[ch2]
        index_of[ch2] = tmp
    return exchange

def create_partner_f(ch1, ch2):
    def partner():
        i1 = index_of[ch1]
        i2 = index_of[ch2]
        state[i1] = ch2
        state[i2] = ch1
        # swap_index(ch1, ch2)
        # NOTE: pulled code in, since calls seem to be expensive
        tmp = index_of[ch1]
        index_of[ch1] = index_of[ch2]
        index_of[ch2] = tmp
    return partner

def get_full():
    for i in range(len_state):
        ind = precalculated_indexes[pos0][i]
        ch = chr(state[ind] + orda)
        yield ch

def parse_move(move):
    m_type = move[0]
    m_data = move[1:]

    if m_type == 's':
        amount = int(m_data)
        return create_spin_f(amount)
    if m_type == 'x':
        parts = m_data.split('/')
        return create_exchange_f(int(parts[0]), int(parts[1]))
    parts = m_data.split('/')
    return create_partner_f(ordinal_of(parts[0]), ordinal_of(parts[1]))

parsed_moves = list(map(parse_move, moves))
def apply_moves(moves, repetitions=1):
    for i in range(repetitions):
        for move in moves:
            move()
        if i % 100 == 0:
            print(i/10000000, '%')

# part 1
apply_moves(parsed_moves)
print(''.join(get_full()))

# part 2
apply_moves(parsed_moves, repetitions-1)
print(''.join(get_full()))
# NOTE: this is way to slow, needs optimization
