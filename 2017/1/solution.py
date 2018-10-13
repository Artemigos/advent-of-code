data = ''
with open('2017/1/data.txt') as f:
    data = f.read()

sum = 0

# part 1
# last = ''
# for c in data:
#     if c == last:
#         sum += int(c)
#     last = c

# if data[0] == data[-1]:
#     sum += int(data[0])

# part 2
half = int(len(data) / 2)
for i in range(len(data)):
    curr = int(data[i])
    i2 = i + half
    if i2 >= len(data):
        i2 -= len(data)
    nxt = int(data[i2])
    if curr == nxt:
        sum += curr

print(sum)
