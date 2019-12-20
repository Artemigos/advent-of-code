import common
import itertools

data = [ord(x)-ord('0') for x in common.read_file('2019/16/data.txt')]

# part 1
current = list(data)
for p in range(100):
    new = []
    for i in range(len(current)):
        if i % 1000 == 0:
            print(str(p+i/len(current))+'%                   ', end='\r')
        acc = 0
        inc = i+1
        for idx in range(i, len(current), 4*inc):
            acc += sum(current[idx:idx+inc])
            acc -= sum(current[idx+2*inc:idx+3*inc])

        new.append(abs(acc) % 10)
    current = new

print()
print('part 1:', ''.join(map(str, current[:8])))

# part 2
current = []
for _ in range(10000):
    current += data

offset = int(''.join(map(str, data[:7])))
current = current[offset:]

assert(offset > len(current)/2)

for p in range(100):
    new = []
    print(str(p)+'%                   ', end='\r')
    new.append(current[-1])
    for i in range(len(current)-2, -1, -1):
        acc = current[i] + new[-1]
        new.append(abs(acc) % 10)
    current = list(reversed(new))

print()
print('part 2:', ''.join(map(str, current[:8])))
