import hashlib
import common

data = b'ffykfhsq'

md5 = hashlib.md5()
md5.update(data)

# part 1
i = 0
digits = ''
while True:
    cp = md5.copy()
    cp.update(bytes(str(i), 'utf8'))
    result = cp.hexdigest()

    if result[:5] == '00000':
        digits += result[5]
        common.print_and_return(digits)
        if len(digits) == 8:
            break

    i += 1

print()

# part 2
i = 0
digits = ['', '', '', '', '', '', '', '']
allowed_positions = set(['0', '1', '2', '3', '4', '5', '6', '7'])

def print_digits():
    view = ''.join(map(lambda x: ' ' if x == '' else x, digits))
    common.print_and_return(view)

while True:
    cp = md5.copy()
    cp.update(bytes(str(i), 'utf8'))
    result = cp.hexdigest()

    if result[:5] == '00000' and result[5] in allowed_positions:
        pos = int(result[5])
        if digits[pos] == '':
            digits[pos] = result[6]
            print_digits()
            if all(digits):
                break

    i += 1

print()
