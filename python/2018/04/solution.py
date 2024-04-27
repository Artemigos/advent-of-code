import common
import collections as coll

def parse_line(line: str):
    segments = common.extract_words(line)
    time = tuple(map(int, segments[0:5]))
    return (*time, *segments[5:])

data = common.read_file('2018/04/data.txt').splitlines()
parsed = [parse_line(x) for x in sorted(data)]

guard = 0
asleep = coll.defaultdict(dict)
last_sleep_key = None
for ev in parsed:
    y, M, d, H, mnt, *ev_data = ev
    k = (y, M, d, H, mnt)

    if ev_data[0] == 'Guard':
        guard = int(ev_data[1])
    elif ev_data[0] == 'wakes':
        rng = asleep[guard][last_sleep_key]
        asleep[guard][last_sleep_key] = range(rng.start, mnt)
    else:
        last_sleep_key = k
        asleep[guard][k] = range(mnt, 60)

max_guard = -1
max_val = 0
for g in asleep:
    grd = asleep[g]
    sleeping = sum(map(lambda k: len(grd[k]), grd))
    if sleeping > max_val:
        max_guard = g
        max_val = sleeping

grd = asleep[max_guard]

def calc_max_mnt_for_guard(grd):
    minutes = coll.defaultdict(int)
    for k, v in grd.items():
        for mnt in range(60):
            if mnt in v:
                minutes[mnt] += 1

    max_mnt = -1
    max_val = 0
    for mnt, val in minutes.items():
        if val > max_val:
            max_mnt = mnt
            max_val = val
    return max_mnt, max_val

max_mnt, _ = calc_max_mnt_for_guard(grd)
print(max_guard * max_mnt)

# part 2
max_val = 0
for g in asleep:
    grd = asleep[g]
    mnt, val = calc_max_mnt_for_guard(grd)
    if val > max_val:
        max_guard = g
        max_mnt = mnt
        max_val = val

print(max_guard * max_mnt)
