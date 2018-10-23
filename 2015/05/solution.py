import common

lines = common.read_file('2015/05/data.txt').splitlines()
vowels = 'aeiou'

# part 1
nice_num = 0
for line in lines:
    vowels_num = 0
    if 'ab' in line or 'cd' in line or 'pq' in line or 'xy' in line:
        continue
    last_c = ''
    repeated_c_satisfied = False
    for c in line:
        if c in vowels:
            vowels_num += 1
        if not repeated_c_satisfied and c == last_c:
            repeated_c_satisfied = True
        last_c = c

    if repeated_c_satisfied and vowels_num >= 3:
        nice_num += 1

print(nice_num)

# part 2
nice_num = 0
for line in lines:
    pattern1_found = False
    for i in range(len(line)-3):
        for j in range(i+2, len(line)-1):
            if line[i] == line[j] and line[i+1] == line[j+1]:
                pattern1_found = True
                break
        if pattern1_found:
            break

    pattern2_found = False
    for i in range(len(line)-2):
        if line[i] == line[i+2]:
            pattern2_found = True
            break

    if pattern1_found and pattern2_found:
        nice_num += 1

print(nice_num)
