import common

left = []
right = []
for line in common.read_file().splitlines():
    l, r = line.split()
    l, r = int(l), int(r)
    left.append(l)
    right.append(r)

# part 1
left = list(sorted(left))
right = list(sorted(right))

acc = 0
for i in range(len(left)):
    acc += abs(left[i] - right[i])

print(acc)

# part 2
score = 0
for l in left:
    acc = 0
    for r in right:
        if l == r:
            acc += 1
    score += acc * l

print(score)
