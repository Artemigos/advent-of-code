import numpy as np
import common

data = int(common.read_file().strip())

step = 0
dist = 0
num = 1

# part 1
while True:
    # right
    step += 1
    num += step
    dist += 1
    if num >= data:
        break

    # up
    num += step
    dist += 1
    if num >= data:
        break

    # left
    step += 1
    num += step
    if num >= data:
        break

    # down
    num += step
    if num >= data:
        break

step_back = (step + 1) // 2
dist_back = num - data
if dist_back <= step_back:
    dist -= dist_back
else:
    dist -= step_back
    dist += dist_back - step_back

print(dist)

# part 2
step = 0
board = np.zeros((501, 501))
pos_x = 250
pos_y = 250
board[pos_x, pos_y] = 1


def update_field(x, y):
    board_slice = board[x - 1:x + 2, y - 1:y + 2]
    board[x, y] = np.sum(board_slice)


while True:
    # right
    step += 1
    for i in range(step):
        pos_x += 1
        update_field(pos_x, pos_y)
        if board[pos_x, pos_y] > data:
            print(int(board[pos_x, pos_y]))
            exit()

    # up
    for i in range(step):
        pos_y -= 1
        update_field(pos_x, pos_y)
        if board[pos_x, pos_y] > data:
            print(int(board[pos_x, pos_y]))
            exit()

    # left
    step += 1
    for i in range(step):
        pos_x -= 1
        update_field(pos_x, pos_y)
        if board[pos_x, pos_y] > data:
            print(int(board[pos_x, pos_y]))
            exit()

    # down
    for i in range(step):
        pos_y += 1
        update_field(pos_x, pos_y)
        if board[pos_x, pos_y] > data:
            print(int(board[pos_x, pos_y]))
            exit()
