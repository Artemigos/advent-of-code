import common

nums = [common.extract_numbers(x) for x in common.read_file().splitlines()]
data = [(x[1], x[3]) for x in nums]

def solve(data):
    status = list(data)

    # time offset alignment
    for i in range(len(status)):
        curr = status[i]
        status[i] = curr[0], (curr[1]+i+1)%curr[0]

    max_loop = status[5]
    time = 0

    def offset(time, amount=max_loop[0]):
        time += amount
        for i in range(len(status)):
            curr = status[i]
            status[i] = curr[0], (curr[1]+amount)%curr[0]
        return time

    time = offset(time, max_loop[0]-max_loop[1])

    def is_aligned_at_zero():
        return all(map(lambda x: x[1] == 0, status))

    while not is_aligned_at_zero():
        time = offset(time)

    print(time)

solve(data)
data.append((11, 0))
solve(data)
