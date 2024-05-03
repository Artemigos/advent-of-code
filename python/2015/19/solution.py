import common
import queue
import itertools

lines = common.read_file().splitlines()
molecule = lines[-1]
lines = lines[:-2]
mappings = []

for line in lines:
    segments = line.split()
    mappings.append((segments[0], segments[2]))

# part 1
def find_replacements(inp: str):
    replacements = set()

    for i in range(len(inp)):
        for k, v in mappings:
            if inp[i:i+len(k)] == k:
                new_val = inp[:i] + v + inp[i+len(k):]
                replacements.add(new_val)

    return replacements

print(len(find_replacements(molecule)))

# part 2
q = queue.deque([(0, molecule)])
rules = sorted(mappings, key=lambda x: len(x[1]), reverse=True)
seen = set()
target = 'e'

def find_reverse_replacements(inp: str):
    for i in range(len(inp)):
        for k, v in rules:
            if inp.startswith(v, i):
                new_val = inp[:i] + k + inp[i+len(v):]
                yield new_val

while len(q) > 0:
    depth, val = q.popleft()
    if val == target:
        # print()
        print(depth)
        break
    # lucky enough, this finds the right answer
    for i, r in itertools.takewhile(lambda x: x[0] < 3, enumerate(find_reverse_replacements(val))):
        if r not in seen:
            q.append((depth+1, r))
            seen.add(r)
    # common.print_and_return(len(q), len(seen), depth)
