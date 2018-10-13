import itertools
import common

data = common.read_file('2017/10/data.txt').strip()
ints = common.to_int(data.split(','))

def knot_hash(key, repeat=1):
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

result = knot_hash(ints)
print(result[0] * result[1])
