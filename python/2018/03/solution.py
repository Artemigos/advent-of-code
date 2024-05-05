import common
import numpy as np

lines = common.read_file().splitlines()
parsed = [common.extract_numbers(x) for x in lines]

fabric = np.zeros((1000, 1000))

for idd, x, y, w, h in parsed:
    fabric[x:x+w, y:y+h] += 1

print(np.sum(fabric > 1))

for idd, x, y, w, h in parsed:
    if np.all(fabric[x:x+w, y:y+h] == 1):
        print(idd)
