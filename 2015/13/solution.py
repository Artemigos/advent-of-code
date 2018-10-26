import itertools
import common

lines = common.read_file('2015/13/data.txt').splitlines()

ppl = set()
ratings = dict()

for line in lines:
    segments = line.split()
    person1 = segments[0]
    person2 = segments[-1][:-1]
    val = int(segments[3])
    if segments[2] == 'lose':
        val = -val
    ppl.add(person1)
    ppl.add(person2)
    ratings[person1, person2] = val

def find_max_score():
    max_score = None
    for p in itertools.permutations(ppl):
        score = 0
        score += ratings[p[-1], p[0]]
        score += ratings[p[0], p[-1]]
        for i in range(len(p)-1):
            score += ratings[p[i], p[i+1]]
            score += ratings[p[i+1], p[i]]
        if max_score is None or score > max_score:
            max_score = score
    return max_score

# part 1
max_score = find_max_score()
print(max_score)

# part 2
for person in ppl:
    ratings['me', person] = 0
    ratings[person, 'me'] = 0
ppl.add('me')

max_score = find_max_score()
print(max_score)
