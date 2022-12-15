import common

data = common.read_file('2022/06/data.txt')

# part 1
for i in range(3, len(data)):
    if len(set(data[i-4:i])) == 4:
        print(i)
        break

# part 2
for i in range(13, len(data)):
    if len(set(data[i-14:i])) == 14:
        print(i)
        break
