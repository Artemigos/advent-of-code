import common

def num_gen(start = 0):
    acc = start
    while True:
        acc *= 2
        yield acc
        acc *= 2
        acc += 1

fitting = filter(lambda x: x >= 2572, num_gen())

print(next(fitting) - 2572)
