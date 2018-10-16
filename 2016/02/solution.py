import common

lines = common.read_file('2016/02/data.txt').splitlines()

# part 1
keypad = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9']
]
can_i = [
    [True, True, True],
    [True, True, True],
    [True, True, True]
]
x = 1
y = 1
size = 3

# part 2
keypad = [
    [' ', ' ', '1', ' ', ' '],
    [' ', '2', '3', '4', ' '],
    ['5', '6', '7', '8', '9'],
    [' ', 'A', 'B', 'C', ' '],
    [' ', ' ', 'D', ' ', ' ']
]
can_i = [
    [False, False, True, False, False],
    [False, True , True, True , False],
    [True , True , True, True , True ],
    [False, True , True, True , False],
    [False, False, True, False, False]
]
x = 0
y = 2
size = 5

code = []
for l in lines:
    for m in l:
        if m == 'L':
            if x > 0 and can_i[y][x-1]:
                x -= 1
        elif m == 'R':
            if x < size-1 and can_i[y][x+1]:
                x += 1
        elif m == 'U':
            if y > 0 and can_i[y-1][x]:
                y -= 1
        else:
            if y < size-1 and can_i[y+1][x]:
                y += 1
    code.append(keypad[y][x])

print(''.join(map(str, code)))
