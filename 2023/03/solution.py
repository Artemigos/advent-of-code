import common

lines = common.read_file().splitlines()

# parse
w = len(lines[0])
h = len(lines)

numbers = {}
symbols = {}

num_status = ''
num_idx = 0
num_positions = []
def push_digit(digit, x, y):
    global num_status, num_idx, num_positions
    num_status += digit
    num_positions.append((x, y))
def flush_number():
    global num_status, num_idx, num_positions
    if len(num_status) > 0:
        identity = (num_idx, int(num_status))
        for pos in num_positions:
            numbers[pos] = identity
        num_status = ''
        num_idx += 1
        num_positions = []

for y in range(h):
    line = lines[y]
    for x in range(w):
        c = line[x]
        if ord(c) >= ord('0') and ord(c) <= ord('9'):
            push_digit(c, x, y)
        elif c != '.':
            flush_number()
            symbols[x, y] = c
        else:
            flush_number()
    flush_number()
flush_number()

# part 1
neighboring_numbers = set()

for pos in symbols:
    for n in common.neighbors_all(pos):
        if n in numbers:
            neighboring_numbers.add(numbers[n])

acc = 0
for identity in neighboring_numbers:
    _, num = identity
    acc += num

print(acc)

# part 2
ratios = []
for pos in symbols:
    c = symbols[pos]
    if c != '*':
        continue
    ns = set()
    for n in common.neighbors_all(pos):
        if n in numbers:
            ns.add(numbers[n])
    if len(ns) != 2:
        continue
    ns = list(ns)
    ratios.append(ns[0][1] * ns[1][1])

print(sum(ratios))
