import common
year_common = common.import_year_common(2019)

tape = common.extract_numbers(common.read_file())

# part 1
acc = 0
for y in range(50):
    for x in range(50):
        mem = year_common.tape_to_mem(tape)
        output = year_common.run_intcode(mem, iter([x, y]))
        result = next(output)
        acc += result
print(acc)

# part 2
ranges = {0: range(1), 1: range(0), 2: range(0), 4: range(0), 7: range(0)}
def get_range(y, x_offset):
    if y in ranges:
        return ranges[y]
    x = x_offset
    started = False
    while True:
        mem = year_common.tape_to_mem(tape)
        output = year_common.run_intcode(mem, iter([x, y]))
        result = next(output)
        if not started and result == 1:
            start = x
            started = True
        elif started and result == 0:
            ranges[y] = range(start, x)
            return ranges[y]
        x += 1

size = 100
y = 1
while True:
    range2 = get_range(y, ranges[y-1][0] if len(ranges[y-1]) > 0 else 0)
    if y >= size-1:
        range1 = ranges[y-(size-1)]
        intersection = range(max(range1[0], range2[0]), min(range1[-1], range2[-1])+1) if len(range1) > 0 and len(range2) > 0 else range(0)
        if len(intersection) >= size:
            x = intersection[0]
            y -= (size-1)
            print(10000*x+y)
            break
    y += 1
