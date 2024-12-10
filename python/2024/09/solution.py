import common

data = common.read_file().strip()
w = sum((int(x) for x in data))

# part 1
space: list[tuple[int | None, range]] = []
def expand_space() -> list[int | None]:
    result: list[int | None] = []
    for el in space:
        id, rng = el
        result += [id]*len(rng)
    return result

pos = 0
id = 0
for i in range(len(data)):
    on_file = (i%2) == 0
    l = int(data[i])
    rng = range(pos, pos+l)
    if on_file:
        space.append((id, rng))
        id += 1
    else:
        space.append((None, rng))
    pos += l

final_w = sum((int(data[i]) for i in range(0, len(data), 2)))
expanded = expand_space()
acc = list(expanded[:final_w])
take_from = list(reversed(expanded[final_w:]))

i, j = 0, 0
while i < final_w:
    if acc[i] is None:
        while take_from[j] is None:
            j += 1
        acc[i] = take_from[j]
        j += 1
    i += 1

score = 0
for i, id in enumerate(acc):
    if id is not None:
        score += i * id
print(score)

# part 2
empties = [x for x in space if x[0] is None]
result_ranges = []

for el in reversed([x for x in space if x[0] is not None]):
    id, rng = el
    found = None
    for i, empty in enumerate(empties):
        empty_id, empty_rng = empty
        if empty_rng.start >= rng.start:
            break
        if len(empty_rng) >= len(rng):
            found = empty_rng
            break
    if found is not None:
        if len(found) == len(rng):
            result_ranges.append((id, range(found.start, found.stop)))
            empties = empties[:i] + empties[i+1:]
        else:
            result_ranges.append((id, range(found.start, found.start+len(rng))))
            empties[i] = (None, range(found.start+len(rng), found.stop))
    else:
        result_ranges.append(el)

score = 0
for el in result_ranges:
    id, rng = el
    for i in rng:
        score += i * id

print(score)
