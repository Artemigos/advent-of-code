import common
from functools import cache

sections = common.read_file().split('\n\n')
pieces = sections[0].split(', ')
targets = sections[1].splitlines()

# part 1 and 2
min_piece = min(map(len, pieces))
max_piece = max(map(len, pieces))
pieces_spread = max_piece - min_piece

@cache
def ways_to_advance(target: str) -> int:
    ways = 0
    for i in range(min_piece, min(max_piece+1, len(target)+1)):
        piece = target[:i]
        if piece in pieces:
            if piece == target:
                ways += 1
            else:
                ways += ways_to_advance(target[i:])
    return ways

acc1 = 0
acc2 = 0
for target in targets:
    ways = ways_to_advance(target)
    if ways > 0:
        acc1 += 1
    acc2 += ways
print(acc1)
print(acc2)
