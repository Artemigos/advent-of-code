import common

lines = common.read_file('2021/03/data.txt').splitlines()
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
most_frequent = list(nums)
least_frequesnt = list(nums)
