import common

lines = common.read_file('2021/11/data.txt').splitlines()
w = len(lines[0])
h = len(lines)
board = {}

for x in range(w):
    for y in range(h):
        board[(x, y)] = ord(lines[y][x]) - ord('0')

# part 1 and 2

curr = dict(board)

def increase_at(x, y):
    curr[(x, y)] += 1
    if curr[(x, y)] == 10:
        if (x-1, y-1) in curr:
            increase_at(x-1, y-1)
        if (x, y-1) in curr:
            increase_at(x, y-1)
        if (x+1, y-1) in curr:
            increase_at(x+1, y-1)
        if (x-1, y) in curr:
            increase_at(x-1, y)
        if (x+1, y) in curr:
            increase_at(x+1, y)
        if (x-1, y+1) in curr:
            increase_at(x-1, y+1)
        if (x, y+1) in curr:
            increase_at(x, y+1)
        if (x+1, y+1) in curr:
            increase_at(x+1, y+1)

flashed = 0
i = 0
while(True):
    for x in range(w):
        for y in range(h):
            increase_at(x, y)

    curr_flashed = 0
    for x in range(w):
        for y in range(h):
            if curr[(x, y)] > 9:
                curr[(x, y)] = 0
                curr_flashed += 1
                flashed += 1
    if i == 99:
        print(flashed)
    i += 1
    if curr_flashed == w*h:
        print(i)
        break
