import common

lines = common.read_file().splitlines()

def score_letter(letter):
    if ord(letter) >= ord('a'):
        return ord(letter) - ord('a') + 1 
    else:
        return ord(letter) - ord('A') + 27

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
