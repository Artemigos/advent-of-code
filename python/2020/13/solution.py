import common

lines = common.read_file().splitlines()
arrival = int(lines[0])
buses = []
offsets = []

i = 0
for x in lines[1].split(','):
    if x != 'x':
        buses.append(int(x))
        offsets.append(i)
    i += 1

# part 1
min_wait = max(buses) + 1
min_bus = -1

for bus in buses:
    wait = -arrival % bus
    if wait < min_wait:
        min_wait = wait
        min_bus = bus

print(min_wait * min_bus)

# part 2
import math

def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

acc = 0
curr_mul = buses[0]
curr_i = 1

while curr_i < len(buses):
    if (acc + offsets[curr_i]) % buses[curr_i] != 0:
        acc += curr_mul
    else:
        curr_mul = lcm(curr_mul, buses[curr_i])
        curr_i += 1

print(acc)
