import common

# parse
sections = common.read_file().split("\n\n")
sections = [x.splitlines() for x in sections]
data = []
for s in sections:
    w = len(s[0])
    h = len(s)
    rows = [0]*h
    cols = [0]*w
    for y in range(h):
        for x in range(w):
            num = 1 if s[y][x] == "#" else 0
            rows[y] <<= 1
            rows[y] += num
            cols[x] <<= 1
            cols[x] += num
    data.append((s, w, h, tuple(rows), tuple(cols)))

# part 1
acc = 0
max_w = 0
max_h = 0
for el in data:
    s, w, h, rows, cols = el
    max_w = max(max_w, w)
    max_h = max(max_h, h)
    for x in range(1, w):
        size = min(x, w-x)
        l = cols[x-size:x]
        r = cols[x:x+size][::-1]
        if l == r:
            acc += x
            break
    else:
        for y in range(1, h):
            size = min(y, h-y)
            l = rows[y-size:y]
            r = rows[y:y+size][::-1]
            if l == r:
                acc += 100*y
                break
        else:
            assert False, 'not found'
print(acc)

# part 2
twos = set([1 << i for i in range(150)])

acc = 0
for el in data:
    s, w, h, rows, cols = el
    for x in range(1, w):
        size = min(x, w-x)
        l = cols[x-size:x]
        r = cols[x:x+size][::-1]
        ln = 0
        rn = 0
        for n in l:
            ln <<= h
            ln += n
        for n in r:
            rn <<= h
            rn += n
        if ln^rn in twos:
            acc += x
            break
    else:
        for y in range(1, h):
            size = min(y, h-y)
            l = rows[y-size:y]
            r = rows[y:y+size][::-1]
            ln = 0
            rn = 0
            for n in l:
                ln <<= w
                ln += n
            for n in r:
                rn <<= w
                rn += n
            if ln^rn in twos:
                acc += 100*y
                break
        else:
            assert False, 'not found'
print(acc)
