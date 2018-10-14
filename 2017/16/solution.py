import common
import queue

data = common.read_file('2017/16/data.txt')
moves = data.split(',')
repetitions = 1000000000
# repetitions = 1000
orda = ord('a')

def ordinal_of(character):
    return ord(character) - orda

state = list(range(ordinal_of('a'), ordinal_of('q')))
state = queue.deque(state)
len_state = len(state)

def create_spin_f(amount):
    def spin():
        state.rotate(amount)
    return spin

def create_exchange_f(i1, i2):
    def exchange():
        ch1 = state[i1]
        state[i1] = state[i2]
        state[i2] = ch1
    return exchange

def create_partner_f(ch1, ch2):
    def partner():
        i1 = state.index(ch1)
        i2 = state.index(ch2)
        state[i1] = ch2
        state[i2] = ch1
    return partner

def get_full():
    for i in range(len_state):
        ch = chr(state[i] + orda)
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

def calc_state_hash():
    h = 0
    for i in range(len_state):
        h = h << 4
        h += state[i]
    return h

parsed_moves = list(map(parse_move, moves))
def apply_moves(moves, repetitions=1):
    seen_states = dict()
    for i in range(repetitions):
        for move in moves:
            move()
        h = calc_state_hash()
        if h in seen_states.keys():
            print('loop detected! loop length:', i-seen_states[h])
        seen_states[h] = i

# part 1
apply_moves(parsed_moves)
print(''.join(get_full()))

# part 2
# apply_moves(parsed_moves, repetitions-1)
# NOTE: loop detection showed that the states repeat every 30 applications
apply_moves(parsed_moves, 9)
print(''.join(get_full()))
