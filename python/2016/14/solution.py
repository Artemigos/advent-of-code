import hashlib
import queue
import common

data = bytes(common.read_file().strip(), encoding='utf8')
# data = b'abc'
base_hash = hashlib.md5(data)

# part 1
threes = list()

keys_found = 0
i = -1
while True:
    i += 1
    cp_hash = base_hash.copy()
    cp_hash.update(bytes(str(i), 'utf8'))
    hsh = cp_hash.hexdigest()

    charas = queue.deque(['', ''], maxlen=2)
    charas5 = queue.deque(['', '', '', ''], maxlen=4)
    three_found = False
    for c in hsh:
        if c == charas[0] and c == charas[1] and not three_found:
            threes.append((i, c))
            three_found = True
        if c == charas5[0] and c == charas5[1] and c == charas5[2] and c == charas5[3]:
            finished_threes = list(filter(lambda x: x[1] == c and i-x[0] <= 1000 and x[0] != i, threes))
            for f3 in finished_threes:
                threes.remove(f3)
                keys_found += 1
                # common.print_and_return(keys_found)
                if keys_found == 64:
                    print(f3[0])
                    break
        charas.append(c)
        charas5.append(c)
    if keys_found == 64:
        break

# part 2
threes = list()

keys_found = 0
i = -1
while True:
    i += 1
    cp_hash = base_hash.copy()
    cp_hash.update(bytes(str(i), 'utf8'))
    hsh = cp_hash.hexdigest()
    for _ in range(2016):
        im_sad = hashlib.md5(bytes(hsh, 'utf8'))
        hsh = im_sad.hexdigest()

    charas = queue.deque(['', ''], maxlen=2)
    charas5 = queue.deque(['', '', '', ''], maxlen=4)
    three_found = False
    for c in hsh:
        if c == charas[0] and c == charas[1] and not three_found:
            threes.append((i, c))
            three_found = True
        if c == charas5[0] and c == charas5[1] and c == charas5[2] and c == charas5[3]:
            finished_threes = list(filter(lambda x: x[1] == c and i-x[0] <= 1000 and x[0] != i, threes))
            for f3 in finished_threes:
                threes.remove(f3)
                keys_found += 1
                # common.print_and_return(keys_found)
                if keys_found == 64:
                    print(f3[0])
                    exit(0)
        charas.append(c)
        charas5.append(c)
