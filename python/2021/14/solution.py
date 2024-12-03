from collections import defaultdict
import common

lines = common.read_file().splitlines()
polymer = lines[0]
rules = {}
for line in lines[2:]:
    a, b = line.split(' -> ')
    rules[a] = b

# part 1 and 2

def add_dicts(d1, d2):
    d = defaultdict(lambda: 0)
    for k in d1:
        d[k] += d1[k]
    for k in d2:
        d[k] += d2[k]
    return d

all_pairs = list(rules.keys())
sols = defaultdict(lambda: defaultdict(lambda: 0))
for pair in all_pairs:
    c = rules[pair]
    sols[(pair, 1)][c] = 1

for i in range(2, 41):
    for pair in all_pairs:
        c = rules[pair]
        sols[(pair, i)] = add_dicts(sols[(pair[0]+c, i-1)], sols[(c+pair[1], i-1)])
        sols[(pair, i)][c] += 1

def solve(depth):
    results = defaultdict(lambda: 0)
    for i in range(1, len(polymer)):
        counts = sols[(polymer[i-1:i+1], depth)]
        results = add_dicts(results, counts)
    for c in polymer:
        results[c] += 1
    print(max(results.values()) - min(results.values()))

solve(10)
solve(40)
