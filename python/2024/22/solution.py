import common

lines = common.read_file().splitlines()
nums = list(map(int, lines))


# part 1
def nxt(num: int) -> int:
    mask = 2**24 - 1
    b = num << 6
    num ^= b
    num &= mask
    b = num >> 5
    num ^= b
    num &= mask
    b = num << 11
    num ^= b
    num &= mask
    return num


acc = 0
for num in nums:
    for _ in range(2000):
        num = nxt(num)
    acc += num
print(acc)

# part 2
lookups = []
all_diffs = set()
for num in nums:
    diffs: list[int] = []
    sequence: list[int] = []
    prev = num
    for _ in range(2000):
        curr = nxt(prev)
        diffs.append((curr % 10) - (prev % 10))
        sequence.append(curr)
        prev = curr
    lookup = dict()
    assert len(diffs) == len(sequence)
    for i in range(3, len(diffs)):
        k = tuple(diffs[i - 3 : i + 1])
        all_diffs.add(k)
        if k not in lookup:
            lookup[k] = sequence[i]
    lookups.append(lookup)

max_acc = 0
for k in all_diffs:
    acc = 0
    for lookup in lookups:
        acc += (lookup.get(k) or 0) % 10
    max_acc = max(max_acc, acc)
print(max_acc)
