import common
import queue

data = int(common.read_file().strip())
# data = 3 # sample data
repetitions_1 = 2017
repetitions_2 = 50000000


def run(repetitions):
    state = queue.deque([0])
    for i in range(repetitions):
        moves = data % len(state) + 1
        state.rotate(-moves)
        state.appendleft(i+1)
        # if i % 1000 == 0:
        #     common.print_and_return(i / (repetitions / 100), '%')
    # print()
    return state


# part 1
result_state = run(repetitions_1)
print(result_state[1])

# part 2
result_state = run(repetitions_2)
i0 = result_state.index(0)
result_state.rotate(-i0)
# print(result_state[0])
print(result_state[1])
