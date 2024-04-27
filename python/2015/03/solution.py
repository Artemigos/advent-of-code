import common

data = common.read_file('2015/03/data.txt')

pos1 = 0, 0
pos2 = [(0, 0), (0, 0)]
pos_i = 0
seen1 = set([pos1])
seen2 = set([pos2[pos_i]])

for move in data:
    if move == '<':
        pos1 = pos1[0]-1, pos1[1]
        pos2[pos_i] = pos2[pos_i][0]-1, pos2[pos_i][1]
    elif move == '>':
        pos1 = pos1[0]+1, pos1[1]
        pos2[pos_i] = pos2[pos_i][0]+1, pos2[pos_i][1]
    elif move == 'v':
        pos1 = pos1[0], pos1[1]+1
        pos2[pos_i] = pos2[pos_i][0], pos2[pos_i][1]+1
    else:
        pos1 = pos1[0], pos1[1]-1
        pos2[pos_i] = pos2[pos_i][0], pos2[pos_i][1]-1
    seen1.add(pos1)
    seen2.add(pos2[pos_i])
    pos_i = 1 - pos_i

print(len(seen1))
print(len(seen2))
