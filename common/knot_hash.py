import functools
import operator
from typing import List, Tuple
import common

def knot_hash(key: List[int], repeat=1) -> List[int]:
    hash_data = list(range(256))

    skip = 0
    pos = 0

    def inc_pos(pos, amount):
        pos += amount
        while pos >= len(hash_data):
            pos -= len(hash_data)
        return pos

    for _ in range(repeat):
        for l in key:
            start_pos = pos
            elements = list()
            for i in range(l):
                elements.append(hash_data[pos])
                pos = inc_pos(pos, 1)
            elements.reverse()
            pos = start_pos
            for i in range(l):
                hash_data[pos] = elements[i]
                pos = inc_pos(pos, 1)
            pos = inc_pos(pos, skip)
            skip += 1

    return hash_data

def knot_hash_full(key: str) -> Tuple[List[int], str]:
    inp = common.to_ord(key) + [17, 31, 73, 47, 23]
    result = knot_hash(inp, 64)
    xored = list()
    for i in range(16):
        segment = result[i*16:(i+1)*16]
        acc = functools.reduce(operator.xor, segment)
        xored.append(acc)
    representation = ''.join(map(lambda x: hex(x)[2:].rjust(2, '0'), xored))
    return (xored, representation)
