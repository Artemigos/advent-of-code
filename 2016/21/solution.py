import common
import queue

lines = common.read_file('2016/21/data.txt').splitlines()

# part 1
password = 'abcdefgh'

def scramble(pswd):
    password = queue.deque(pswd)
    for line in lines:
        segments = line.split(' ')
        code = segments[0]

        if code == 'swapp':
            i1 = int(segments[1])
            i2 = int(segments[2])
            tmp = password[i1]
            password[i1] = password[i2]
            password[i2] = tmp
        elif code == 'swapl':
            i1 = password.index(segments[1])
            i2 = password.index(segments[2])
            tmp = password[i1]
            password[i1] = password[i2]
            password[i2] = tmp
        elif code == 'rotl':
            amount = int(segments[1])
            password.rotate(-amount)
        elif code == 'rotr':
            amount = int(segments[1])
            password.rotate(amount)
        elif code == 'rotrel':
            amount = password.index(segments[1])
            if amount >= 4:
                amount += 1
            amount += 1
            password.rotate(amount)
        elif code == 'revp':
            start = int(segments[1])
            stop = int(segments[2])
            swaps = int((stop-start+1)/2)
            for i in range(swaps):
                tmp = password[start+i]
                password[start+i] = password[stop-i]
                password[stop-i] = tmp
        elif code == 'movp':
            i1 = int(segments[1])
            i2 = int(segments[2])
            val = password[i1]
            password.remove(val)
            password.insert(i2, val)
        else:
            raise Exception('huh?')
    return ''.join(password)

print(scramble(password))

# part 2
password = queue.deque('fbgdceah')
# lines = ['rotrel f'] # test

def do_op(pswd, op):
    password = queue.deque(pswd)
    segments = op.split(' ')
    code = segments[0]

    if code == 'swapp':
        i1 = int(segments[1])
        i2 = int(segments[2])
        tmp = password[i1]
        password[i1] = password[i2]
        password[i2] = tmp
    elif code == 'swapl':
        i1 = password.index(segments[1])
        i2 = password.index(segments[2])
        tmp = password[i1]
        password[i1] = password[i2]
        password[i2] = tmp
    elif code == 'rotl':
        amount = int(segments[1])
        password.rotate(amount)
    elif code == 'rotr':
        amount = int(segments[1])
        password.rotate(-amount)
    elif code == 'rotrel':
        curr_i = password.index(segments[1])
        rev_table = {
            1: 0,
            3: 1,
            5: 2,
            7: 3,
            2: 4,
            4: 5,
            6: 6,
            0: 7
        }
        new_i = rev_table[curr_i]
        amount = new_i-curr_i
        password.rotate(amount)
    elif code == 'revp':
        start = int(segments[1])
        stop = int(segments[2])
        swaps = int((stop-start+1)/2)
        for i in range(swaps):
            tmp = password[start+i]
            password[start+i] = password[stop-i]
            password[stop-i] = tmp
    elif code == 'movp':
        i1 = int(segments[1])
        i2 = int(segments[2])
        val = password[i2]
        password.remove(val)
        password.insert(i1, val)
    else:
        raise Exception('huh?')

    return password

for line in reversed(lines):
    password = do_op(password, line)

print(''.join(password))
