import common

lines = common.read_file('2022/03/data.txt').splitlines()

def score_letter(letter):
    return ord(letter) - ord('a') + 1 if ord(letter) >= ord('a') else ord(letter) - ord('A') + 27

# part 1
acc = 0
for line in lines:
    middle = len(line)//2
    left, right = line[:middle], line[middle:]
    common = set(left).intersection(set(right))
    assert len(common) == 1
    acc += score_letter(common.pop())

print(acc)

# part 2
acc = 0
for i in range(0, len(lines), 3):
    common = set(lines[i]).intersection(set(lines[i+1])).intersection(set(lines[i+2]))
    assert len(common) == 1
    acc += score_letter(common.pop())

print(acc)
