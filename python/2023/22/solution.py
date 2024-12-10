import common
from collections import deque

lines = common.read_file().splitlines()

Brick = tuple[range, range, range]
falling_bricks: list[Brick] = []
for line in lines:
    x1, y1, z1, x2, y2, z2 = common.extract_numbers(line)
    assert x1 <= x2 and y1 <= y2 and z1 <= z2
    falling_bricks.append((range(x1, x2+1), range(y1, y2+1), range(z1, z2+1)))

# part 1
def bot(b: Brick) -> int:
    return b[2].start
def top(b: Brick) -> int:
    return b[2].stop
def collision(b1: Brick, b2: Brick) -> bool:
    return common.range_intersects(b1[0], b2[0]) and common.range_intersects(b1[1], b2[1])
def move_onto(place: Brick, onto: int) -> Brick:
    offset = onto - bot(place)
    return place[0], place[1], range(place[2].start + offset, place[2].stop + offset)
falling_bricks = list(sorted(falling_bricks, key=bot))
stack: list[Brick] = []
def put(b: Brick):
    global stack
    stack.append(b)
    stack = list(sorted(stack, key=top))

# stack the bricks
for b in falling_bricks:
    for placed in reversed(stack):
        if collision(b, placed):
            new = move_onto(b, top(placed))
            put(new)
            break
    else:
        new = move_onto(b, 0)
        put(new)

# look for multi-supported bricks (and pre-fill lookups for part 2)
requires: dict[Brick, list[Brick]] = {}
supported_by: dict[Brick, list[Brick]] = {}
supports_for: dict[Brick, list[Brick]] = {}
for b in stack:
    supports: list[Brick] = []
    for b2 in stack:
        if collision(b, b2) and top(b2) == bot(b):
            supports.append(b2)
    supports_for[b] = supports
    for s in supports:
        if s not in supported_by:
            supported_by[s] = []
        supported_by[s].append(b)
    if len(supports) == 1:
        for s in supports:
            if s not in requires:
                requires[s] = []
            requires[s].append(b)

print(len(stack) - len(requires))

# part 2
acc = 0
for required in requires:
    falls = deque([required])
    all_fallen: set[Brick] = set()
    while falls:
        r = falls.popleft()
        if r in all_fallen:
            continue
        all_fallen.add(r)
        if r not in supported_by:
            continue
        for b in supported_by[r]:
            supports = supports_for[b]
            if all([s in all_fallen for s in supports]):
                falls.append(b)
    acc += len(all_fallen) - 1 # subtract the disintegrated brick from count

print(acc)
