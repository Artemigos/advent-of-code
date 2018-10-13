import common

data = common.read_file('2017/6/data.txt')
cells = data.split('\t')

state = common.to_int(cells)
steps = 0
seen = set()
seen_at_step = dict()

def state_to_int():
    acc = 0
    for i in range(0, len(state)):
        acc *= 100
        acc += state[i]
    return acc

while True:
    state_val = state_to_int()
    if state_val in seen:
        break
    seen.add(state_val)
    seen_at_step[state_val] = steps
    steps += 1

    # find max
    max_val = 0
    max_i = 0

    for i in range(0, len(state)):
        if state[i] > max_val:
            max_val = state[i]
            max_i = i

    # redistribute
    state[max_i] = 0
    left = max_val
    next_i = max_i
    while left > 0:
        next_i += 1
        if next_i >= len(state):
            next_i = 0
        state[next_i] += 1
        left -= 1

print(steps)
print(steps - seen_at_step[state_to_int()])
