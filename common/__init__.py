from .file_utils import *
from .parsing import *
from .d3 import *

def manhattan_dist(p1, p2):
    assert len(p1) == len(p2)
    acc = 0
    for i in range(len(p1)):
        acc += abs(p1[i] - p2[i])
    return acc