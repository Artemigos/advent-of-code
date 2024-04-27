import common

lines = common.read_file('2016/20/data.txt').splitlines()
max_ip = 4294967295

def parse_line(line):
    segments = line.split('-')
    return range(int(segments[0]), int(segments[1])+1)

ranges = list(map(parse_line, lines))

# part 1
i = 0
while i <= max_ip:
    blocked = False
    for r in ranges:
        if i in r:
            blocked = True
            i = r.stop
            break
    if not blocked:
        print(i)
        break

def overlaps(r1: range, r2: range):
    if r1.start in r2 or r2.start in r1:
        return True
    return False

def join(r1: range, r2: range):
    return range(min([r1.start, r2.start]), max([r1.stop, r2.stop]))

# part 2
output_ranges = list(ranges)
while True:
    joined_ranges = []
    for r in output_ranges:
        for jr in joined_ranges:
            if overlaps(r, jr):
                joined_ranges.remove(jr)
                joined_ranges.append(join(r, jr))
                break
        else:
            joined_ranges.append(r)

    if len(joined_ranges) == len(output_ranges):
        break
    output_ranges = joined_ranges

lengths = sum(map(len, output_ranges))
allowed = max_ip+1-lengths
print(allowed)
