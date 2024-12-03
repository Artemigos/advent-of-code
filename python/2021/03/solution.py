import common

lines = common.read_file().splitlines()
nums = [int(x, 2) for x in lines]
w = len(lines[0])

# part 1
acc = [0]*w
for num in nums:
    for i in range(w):
        acc[i] += ((num & (1 << i)) >> i)

gamma = 0
half = len(lines) // 2
for i in range(w):
    if acc[i] > half:
        gamma |= (1 << i)

mask = int(''.join(['1']*w), 2)
epsilon = ~gamma & mask

print(gamma*epsilon)

# part 2

most_common = list(lines)

for bit in range(len(most_common[0])):
    zeros = []
    ones = []
    for line in most_common:
        if line[bit] == '1':
            ones.append(line)
        else:
            zeros.append(line)
    most_common = zeros if len(zeros) > len(ones) else ones
    if len(most_common) == 1:
        break

num1 = int(most_common[0], 2)
least_common = list(lines)

for bit in range(len(least_common[0])):
    zeros = []
    ones = []
    for line in least_common:
        if line[bit] == '1':
            ones.append(line)
        else:
            zeros.append(line)
    least_common = ones if len(ones) < len(zeros) else zeros
    if len(least_common) == 1:
        break

num2 = int(least_common[0], 2)
print(num1*num2)
