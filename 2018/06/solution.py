import common
import collections as coll

data = common.read_file('2018/06/data.txt').splitlines()
parsed = [tuple(common.extract_numbers(x)) for x in data]

minx = min(map(lambda x: x[0], parsed))
miny = min(map(lambda x: x[1], parsed))
maxx = max(map(lambda x: x[0], parsed))
maxy = max(map(lambda x: x[1], parsed))
dx = maxx-minx+1
dy = maxy-miny+1
print(minx, maxx, miny, maxy)

def diffs(x, y):
    for row in parsed:
        rx, ry = row
        diff = abs(rx-x) + abs(ry-y)
        yield diff
        

def min_diff(x, y):
    min_d = 50000
    min_i = None
    dfs = list(diffs(x, y))
    for i in range(len(dfs)):
        diff = dfs[i]
        if diff < min_d:
            min_d = diff
            min_i = i
        elif diff == min_d:
            min_i = -1
    return min_i

x_range = list(range(minx-dy, minx+dy))
y_range = list(range(miny-dx, maxy+dx))
counts = coll.Counter()
broke_letter = set()
for x in x_range:
    for y in y_range:
        i = min_diff(x, y)
        if y == y_range[0] or y == y_range[-1] or x == x_range[0] or x == x_range[-1]:
            broke_letter.add(i)
        counts[i] += 1

def iexcept(data, i_remove):
    return filter(lambda x: x not in i_remove, data)

print(max(map(lambda x: counts[x], iexcept(counts.keys(), broke_letter))))

for i in range(50):
    if i in broke_letter:
        continue
    print(i, counts[i])

inc_amount = 500
x_range = list(range(minx-inc_amount, minx+inc_amount))
y_range = list(range(miny-inc_amount, maxy+inc_amount))
count = 0
for x in x_range:
    for y in y_range:
        diff = sum(diffs(x, y))
        if diff < 10000:
            if y == y_range[0] or y == y_range[-1] or x == x_range[0] or x == x_range[-1]:
                print('edge touch detected!')
            count += 1

print(count)
