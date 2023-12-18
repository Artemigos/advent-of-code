import common

lines = common.read_file().splitlines()
pairs = []
flat = []

for i in range(0, len(lines), 3):
    left = eval(lines[i])
    right = eval(lines[i+1])
    pairs.append((left, right))
    flat.append(left)
    flat.append(right)

# part 1
def cmp(l, r):
    tl = type(l)
    tr = type(r)
    if tl == int and tr == int:
        if l == r:
            return None
        return l < r
    if tl == list and tr == list:
        for i in range(min(len(l), len(r))):
            res = cmp(l[i], r[i])
            if res is not None:
                return res
        if len(l) == len(r):
            return None
        return len(l) < len(r)
    if tl == int:
        return cmp([l], r)
    return cmp(l, [r])

acc = 0
for i in range(len(pairs)):
    if cmp(pairs[i][0], pairs[i][1]) == True:
        acc += (i+1)

print(acc)

# part 2
import functools
def cmp2(l, r):
    res = cmp(l, r)
    if res == False:
        return 1
    if res == True:
        return -1
    return 0

flat.append([[2]])
flat.append([[6]])

s = list(sorted(flat, key=functools.cmp_to_key(cmp2)))
i1 = s.index([[2]])
i2 = s.index([[6]])
print((i1+1)*(i2+1))
