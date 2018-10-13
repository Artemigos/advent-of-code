import common

data = common.read_file('2017/11/data.txt').strip().split(',')

offset_x = 0
offset_y = 0

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

print(offset_x, offset_y)
# NOTE: with this data I calculated the distance manually
