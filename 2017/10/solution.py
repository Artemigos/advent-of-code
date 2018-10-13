import functools
import itertools
import operator
import common

data = common.read_file('2017/10/data.txt').strip()
ints = common.to_int(data.split(','))
ascii_data = common.to_ord(data) + [17, 31, 73, 47, 23]

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

# part 2
result2 = knot_hash(ascii_data, 64)
xored = list()
for i in range(16):
    segment = result2[i*16:(i+1)*16]
    acc = functools.reduce(operator.xor, segment)
    xored.append(acc)
representation = ''.join(map(lambda x: hex(x)[2:].rjust(2, '0'), xored))
print(representation)
