import common

data = common.read_file('2018/02/data.txt').splitlines()

twos = 0
threes = 0
for line in data:
    letters = dict()
    for l in line:
        if l in letters:
            letters[l] += 1
        else:
            letters[l] = 1

    if any(filter(lambda x: letters[x] == 2, letters)):
        twos += 1
    if any(filter(lambda x: letters[x] == 3, letters)):
        threes += 1
print(twos * threes)

for i1 in range(len(data)):
    for i2 in range(i1+1, len(data)):
        line1 = data[i1]
        line2 = data[i2]
        acc = ''
        for i in range(len(line1)):
            if line1[i] == line2[i]:
                acc += line1[i]
        if len(acc) + 1 == len(line1):
            print(acc)
