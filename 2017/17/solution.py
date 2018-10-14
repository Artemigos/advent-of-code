import queue

data = 314
# data = 3 # sample data
repetitions_1 = 2017
repetitions_2 = 50000000

def run(repetitions):
    state = queue.deque([0])
    for i in range(repetitions):
        moves = data%len(state) + 1
        state.rotate(-moves)
        state.appendleft(i+1)
        if i % 1000 == 0:
            print(i / (repetitions / 100), '%')
    return state

# part 1
state = run(repetitions_1)
print(state[1])

# part 2
state = run(repetitions_2)
i0 = state.index(0)
state.rotate(-i0)
print(state[0])
print(state[1])
