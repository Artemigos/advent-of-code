import common

trees = common.read_file('2022/08/data.txt').splitlines()
h = len(trees)
w = len(trees[0])

# part 1
visible = set()
for x in range(w):
    occluded = -1
    for y in range(h):
        val = int(trees[y][x])
        if val > occluded:
            occluded = val
            visible.add((x, y))
    occluded = -1
    for y in range(h-1, -1, -1):
        val = int(trees[y][x])
        if val > occluded:
            occluded = val
            visible.add((x, y))
for y in range(h):
    occluded = -1
    for x in range(w):
        val = int(trees[y][x])
        if val > occluded:
            occluded = val
            visible.add((x, y))
    occluded = -1
    for x in range(w-1, -1, -1):
        val = int(trees[y][x])
        if val > occluded:
            occluded = val
            visible.add((x, y))

print(len(visible))

# part 2
max_vis = 0

def find_score(x, y):
    curr = int(trees[y][x])

    # left
    left = 0
    for xx in range(x-1, -1, -1):
        val = int(trees[y][xx])
        left += 1
        if val >= curr:
            break

    # right
    right = 0
    for xx in range(x+1, w):
        val = int(trees[y][xx])
        right += 1
        if val >= curr:
            break

    # up
    up = 0
    for yy in range(y-1, -1, -1):
        val = int(trees[yy][x])
        up += 1
        if val >= curr:
            break

    # down
    down = 0
    for yy in range(y+1, h):
        val = int(trees[yy][x])
        down += 1
        if val >= curr:
            break

    return left * right * up * down

for x in range(w):
    for y in range(h):
        score = find_score(x, y)
        if score > max_vis:
            max_vis = score

print(max_vis)
