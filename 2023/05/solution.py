import common

data = common.read_file()

# parse
sections = data.split('\n\n')
seeds = common.extract_numbers(sections[0])

def read_map(section: str):
    result = []
    for line in section.splitlines()[1:]:
        nums = common.extract_numbers(line)
        source = range(nums[1], nums[1]+nums[2])
        offset = nums[0]-nums[1]
        result.append((source, offset))
    return result

maps = []
for section in sections[1:]:
    mapping = read_map(section)
    maps.append(mapping)

# part 1
low = None
for seed in seeds:
    curr = seed
    for m in maps:
        for rule in m:
            source, offset = rule
            if curr in source:
                curr += offset
                break
    if low is None or curr < low:
        low = curr

print(low)

# part 2
def intersect(r1: range, r2: range):
    return range(max(r1.start, r2.start), min(r1.stop, r2.stop))
def r_offset(r: range, offset: int):
    return range(r.start+offset, r.stop+offset)
def r_remove(r1: range, r2: range):
    if r1.start > r2.start:
        return range(max(r1.start, r2.stop), r1.stop)
    else:
        return range(r1.start, min(r1.stop, r2.start))

def map_ranges(source_ranges, mapping):
    result = []
    found_source = []

    # find map offsets
    for r in source_ranges:
        for rule in mapping:
            source, offset = rule
            i = intersect(r, source)
            if len(i) > 0:
                found_source.append(i)
                result.append(r_offset(i, offset))

    # forward the rest
    for r in source_ranges:
        curr = r
        for found in found_source:
            curr = r_remove(curr, found)
        if len(curr) > 0:
            result.append(curr)

    return result

seed_ranges = []
for i in range(0, len(seeds), 2):
    start = seeds[i]
    count = seeds[i+1]
    seed_ranges.append(range(start, start+count))

curr = seed_ranges
for m in maps:
    curr = map_ranges(curr, m)

low = min([r.start for r in curr])
print(low)
