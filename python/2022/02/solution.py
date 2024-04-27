import common

guide = []
lines = common.read_file().splitlines()
for line in lines:
    segments = line.split(' ')
    guide.append((segments[0], segments[1]))

# part 1
def c_score(l, r):
    score = 0
    if r == 'X':
        score += 1
        if l == 'A':
            score += 3
        elif l == 'C':
            score += 6
    elif r == 'Y':
        score += 2
        if l == 'B':
            score += 3
        elif l == 'A':
            score += 6
    else: # r == 'Z'
        score += 3
        if l == 'C':
            score += 3
        elif l == 'B':
            score += 6
    return score

score = 0
for l, r in guide:
    score += c_score(l, r)

print(score)

# part 2
score = 0
for l, r in guide:
    if r == 'X':
        if l == 'A':
            r = 'Z'
        elif l == 'B':
            r = 'X'
        else:
            r = 'Y'
    elif r == 'Y':
        if l == 'A':
            r = 'X'
        elif l == 'B':
            r = 'Y'
        else:
            r = 'Z'
    else:
        if l == 'A':
            r = 'Y'
        elif l == 'B':
            r = 'Z'
        else:
            r = 'X'

    score += c_score(l, r)

print(score)
