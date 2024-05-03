import itertools
import functools
import common

weights = [int(x) for x in common.read_file().splitlines()]

def product(iterable):
    return functools.reduce(lambda acc, x: acc*x, iterable, 1)

def solve(group_weight):
    min_groups = []
    for group_size in range(1, len(weights)):
        min_groups = [p for p in itertools.permutations(weights, group_size) if sum(p) == group_weight]
        if len(min_groups) > 0:
            break

    entanglements = [product(p) for p in min_groups]
    print(min(entanglements))

solve(int(sum(weights)/3))
solve(int(sum(weights)/4))
