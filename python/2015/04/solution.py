import hashlib

data = b'iwrupvqb'

base_hash = hashlib.md5(data)

i = 0
while True:
    i += 1
    i_str = bytes(str(i), 'utf8')
    cp = base_hash.copy()
    cp.update(i_str)
    hx = cp.hexdigest()
    if hx[:5] == '00000':
        print('5 zeros:', i)
    if hx[:6] == '000000':
        print('6 zeros:', i)
        break
