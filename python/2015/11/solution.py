# import common

data = 'vzbxkghb'
# data = 'abcdefgh' # sample 1

def pass_iterator(start=data):
    ord_a = ord('a')
    ord_z = ord('z')
    letters = list(map(ord, start))
    def add_to_digit(i):
        if i < 0 :
            return False
        letters[i] += 1
        if letters[i] > ord_z:
            letters[i] = ord_a
            return add_to_digit(i-1)
        return True
    while add_to_digit(len(letters)-1):
        decoded = list(map(chr, letters))
        yield ''.join(decoded)

series = [
    'abc', 'bcd', 'cde', 'def', 'efg', 'fgh',
    'pqr', 'qrs', 'rst', 'stu', 'tuv', 'uvw', 'vwx', 'wxy', 'xyz'
]

def find_next_pass(current):
    for p in pass_iterator(current):
        # common.print_and_return(p)

        if 'i' in p or 'l' in p or 'o' in p:
            continue

        for s in series:
            if s in p:
                break
        else:
            continue

        found_pair = ''
        for i in range(len(p)-3):
            if p[i] == p[i+1]:
                found_pair = p[i]
                break
        else:
            continue

        for j in range(i+2, len(p)-1):
            if p[j] == p[j+1] and p[j] != found_pair:
                break
        else:
            continue

        return p

# part 1
pass1 = find_next_pass(data)
print(pass1)

# part 2
pass2 = find_next_pass(pass1)
print(pass2)
