import numpy as np
import common

data = int(common.read_file().strip())
powers = np.zeros((300, 300))

for x in range(1, 301):
    for y in range(1, 301):
        rack_id = x+10
        powa = rack_id*y + data
        powa *= rack_id
        powa %=1000
        powa //= 100
        powa -= 5
        powers[x-1, y-1] = powa

def find_max_pow(sizes):
    maxp = -100000
    maxx=0
    maxy=0
    maxn = 0

    for n in sizes:
        for x in range(300-n+1):
            for y in range(300-n+1):
                p = np.sum(powers[x:x+n, y:y+n])
                if p > maxp:
                    maxp = p
                    maxx = x+1
                    maxy = y+1
                    maxn = n

    return (maxp, maxx, maxy, maxn)

print(find_max_pow([3]))
print(find_max_pow(range(1, 301)))
