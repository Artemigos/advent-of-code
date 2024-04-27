import itertools
import functools

weights = [
    1, 3, 5, 11, 13,
    17, 19, 23, 29, 31,
    41, 43, 47, 53, 59,
    61, 67, 71, 73, 79,
    83, 89, 97, 101, 103,
    107, 109, 113
]

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
