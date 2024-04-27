import common

data = common.read_file('2017/1/data.txt')

# part 1
sum_acc = 0
last = ''

for c in data:
    if c == last:
        sum_acc += int(c)
    last = c

if data[0] == data[-1]:
    sum_acc += int(data[0])

print(sum_acc)

# part 2
sum_acc = 0
half = int(len(data) / 2)

for i in range(len(data)):
    curr = int(data[i])
    i2 = i + half
    if i2 >= len(data):
        i2 -= len(data)
    nxt = int(data[i2])
    if curr == nxt:
        sum_acc += curr

print(sum_acc)
