import numpy as np
import common

lines = common.read_file('2016/08/data.txt').splitlines()

display = np.zeros((6, 50))
for l in lines:
    segments = l.split(' ')
    if segments[0] == 'rect':
        coords_strs = segments[1].split('x')
        coords = (int(coords_strs[0]), int(coords_strs[1]))
        display[0:coords[1], 0:coords[0]] = 1
    else:
        direction = segments[1]
        shift = int(segments[4])
        which = int(segments[2].split('=')[1])
        if direction == 'row':
            display[which, :] = np.roll(display[which, :], shift)
        else:
            display[:, which] = np.roll(display[:, which], shift)

print(sum(sum(display)))

for y in range(6):
    for x in range(50):
        print('#' if display[y, x] > 0 else '.', end='')
    print()
