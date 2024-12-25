import common

charts = common.read_file().split('\n\n')
keys: list[tuple[int, int, int, int, int]] = []
locks: list[tuple[int, int, int, int, int]] = []
for chart in charts:
    lines = chart.splitlines()
    assert len(lines[0]) == 5
    assert len(lines) == 7
    is_key = lines[0] == '.....'
    lines = lines[1:-1]
    cols = []
    for x in range(5):
        r = range(4, -1, -1) if is_key else range(5)
        acc = 0
        for y in r:
            if lines[y][x] == '#':
                acc += 1
            else:
                cols.append(acc)
                break
        else:
            cols.append(5)
    assert len(cols) == 5
    if is_key:
        keys.append(tuple(cols))
    else:
        locks.append(tuple(cols))

acc = 0
for lock in locks:
    for key in keys:
        for x in range(5):
            if lock[x] + key[x] > 5:
                break
        else:
            acc += 1
print(acc)
