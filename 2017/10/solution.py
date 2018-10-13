import functools
import itertools
import operator
import common

data = common.read_file('2017/10/data.txt').strip()
ints = common.to_int(data.split(','))
ascii_data = common.to_ord(data) + [17, 31, 73, 47, 23]

# NOTE: implementation of knot hash was moved to common

result = common.knot_hash(ints)
print(result[0] * result[1])

# part 2
result2 = common.knot_hash(ascii_data, 64)
xored = list()
for i in range(16):
    segment = result2[i*16:(i+1)*16]
    acc = functools.reduce(operator.xor, segment)
    xored.append(acc)
representation = ''.join(map(lambda x: hex(x)[2:].rjust(2, '0'), xored))
print(representation)
