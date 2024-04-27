from .file_utils import *
from .parsing import *
from .d3 import *
from .ranges import *

def manhattan_dist(p1, p2):
    assert len(p1) == len(p2)
    acc = 0
    for i in range(len(p1)):
        acc += abs(p1[i] - p2[i])
    return acc

def neighbors_ortho(p, dims=None):
    if dims is not None:
        assert len(p) == len(dims)
    for i in range(len(p)):
        np = list(p)
        np[i] = p[i]-1
        yield tuple(np)
        np[i] = p[i]+1
        yield tuple(np)

def neighbors_all(p):
    import itertools
    for combination in itertools.product([-1, 0, 1], repeat=len(p)):
        if all(map(lambda x: x == 0, combination)):
            continue
        yield tuple((x + combination[i] for i, x in enumerate(p)))

def product(nums):
    from functools import reduce
    return reduce(lambda x, y: x * y, nums, 1)
