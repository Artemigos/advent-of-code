import common

lines = common.read_file().splitlines()

# part 1
sum = 0
for line in lines:
    first = -1
    last = -1
    for c in line:
        if ord(c) >= ord('0') and ord(c) <= ord('9'):
            d = int(c)
            if first < 0:
                first = d
            last = d
    sum += 10*first + last

print(sum)

# part 2

words = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
sum = 0

for line in lines:
    first = -1
    last = -1
    def set_digits(val):
        global first
        global last
        if first < 0:
            first = val
        last = val

    i = 0
    for i in range(len(line)):
        c = line[i]
        if ord(c) >= ord('0') and ord(c) <= ord('9'):
            d = int(c)
            set_digits(d)
        else:
            for j in range(len(words)):
                word = words[j]
                if line[i:].startswith(word):
                    d = j + 1
                    set_digits(d)
                    break
        i += 1
    sum += 10*first + last

print(sum)
