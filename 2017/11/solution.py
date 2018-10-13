import common

data = common.read_file('2017/11/data.txt').strip().split(',')

offset_x = 0
offset_y = 0

def dist():
    def sign(x):
        if x > 0: return 1
        if x < 0: return -1
        return 0
    if sign(offset_x) != sign(offset_y):
        return max([abs(offset_x), abs(offset_y)])
    return abs(offset_x) + abs(offset_y)

max_dist = 0

#   |nw|n
# sw|  |ne
# s |se|
for move in data:
    if move == 'sw' or move == 's':
        offset_x -= 1
    elif move == 'n' or move == 'ne':
        offset_x += 1

    if move == 'nw' or move == 'n':
        offset_y -= 1
    elif move == 's' or move == 'se':
        offset_y += 1

    curr_dist = dist()
    if curr_dist > max_dist:
        max_dist = curr_dist

last_dist = dist()
print(last_dist)
print(max_dist)
