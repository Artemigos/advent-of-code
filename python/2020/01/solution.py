import common

nums = common.to_int(common.read_file('2020/01/data.txt').splitlines())

# part 1
found = False
for num1 in nums:
    for num2 in nums:
        if num1 + num2 == 2020:
            print(num1 * num2)
            found = True
            break
    if found:
        break

# part 2

for num1 in nums:
    for num2 in nums:
        for num3 in nums:
            if num1 + num2 + num3 == 2020:
                print(num1 * num2 * num3)
                exit(0)
