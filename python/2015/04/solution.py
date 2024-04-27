import hashlib

data = b'iwrupvqb'

base_hash = hashlib.md5(data)

found5 = False
found6 = False
five = 0
six = 0

i = 0

while True:
    i += 1
    i_str = bytes(str(i), 'utf8')
    cp = base_hash.copy()
    cp.update(i_str)
    hx = cp.digest()

    if not found5 and hx[0] == 0 and hx[1] == 0 and hx[2]&0xF0 == 0:
        five = i
        found5 = True
    if not found6 and hx[0] == 0 and hx[1] == 0 and hx[2] == 0:
        six = i
        found6 = True

    if found5 and found6:
        break

print(five)
print(six)
