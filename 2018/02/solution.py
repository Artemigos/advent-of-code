import common
from collections import Counter
import numpy as np

data = common.read_file('2018/02/data.txt').splitlines()

twos = 0
threes = 0
for line in data:
    cnt = Counter(line)
    is2 = False
    is3 = False
    for _, num in cnt.items():
        if num == 2 and not is2:
            twos += 1
            is2 = True
        if num == 3 and not is3:
            threes += 1
            is3 = True

print(twos*threes)

for i1 in range(len(data)):
    for i2 in range(i1+1, len(data)):
        l1 = data[i1]
        l2 = data[i2]
        common = ''
        for il in range(len(l1)):
            if l1[il] == l2[il]:
                common += l1[il]
        if len(common)+1 == len(l1):
            print(common)
