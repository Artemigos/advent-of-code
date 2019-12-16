import common
import itertools

data = list(map(lambda x: ord(x)-ord('0'), common.read_file('2019/16/data.txt')))
pattern = [0, 1, 0, -1]
def patter_generator(n):
    initial = True
    while True:
        for val in pattern:
            for _ in range(n):
                if initial:
                    initial = False
                    continue
                yield val

current = list(data)
for _ in range(100):
    new = []
    for i in range(len(current)):
        acc = 0
        curr_pattern = list(itertools.islice(patter_generator(i+1), len(current)))
        for j in range(len(current)):
            acc += curr_pattern[j]*current[j]
        new.append(abs(acc)%10)
    current = new

print('part 1:', ''.join(map(str, current[:8])))
