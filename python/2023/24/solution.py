import common
from itertools import combinations
import sympy as sp

lines = common.read_file().splitlines()
area_min, area_max = 200000000000000, 400000000000000

# part 1
half_sections: list[tuple[int, int, int, int, int, int]] = []
for line in lines:
    x, y, z, vx, vy, vz = common.extract_numbers(line)
    assert vx != 0 and vy != 0 and vz != 0
    half_sections.append((x, y, z, vx, vy, vz))

acc = 0
for l, r in combinations(half_sections, 2):
    x1, y1, _, vx1, vy1, _ = l
    x2, y2, _, vx2, vy2, _ = r
    a1 = vy1 / vx1
    b1 = y1 - a1*x1
    a2 = vy2 / vx2
    b2 = y2 - a2*x2
    assert (a1, b1) != (a2, b2)
    if a1 == a2:
        continue
    intersection_x = (b2 - b1) / (a1 - a2)
    intersection_y = a1 * intersection_x + b1
    if (intersection_x - x1) / vx1 < 0 or (intersection_y - y1) / vy1 < 0:
        continue
    if (intersection_x - x2) / vx2 < 0 or (intersection_y - y2) / vy2 < 0:
        continue
    if intersection_x < area_min or intersection_x > area_max:
        continue
    if intersection_y < area_min or intersection_y > area_max:
        continue
    acc += 1

print(acc)

# part 2
# NOTE:
# it feels a little bit like cheating to use sympy to solve this,
# but solving this system of 18 equations by hand was a nightmare
x1 = sp.Symbol('x1')
y1 = sp.Symbol('y1')
z1 = sp.Symbol('z1')
x2 = sp.Symbol('x2')
y2 = sp.Symbol('y2')
z2 = sp.Symbol('z2')
x3 = sp.Symbol('x3')
y3 = sp.Symbol('y3')
z3 = sp.Symbol('z3')
t1 = sp.Symbol('t1')
t2 = sp.Symbol('t2')
t3 = sp.Symbol('t3')
ax = sp.Symbol('ax')
bx = sp.Symbol('bx')
ay = sp.Symbol('ay')
by = sp.Symbol('by')
az = sp.Symbol('az')
bz = sp.Symbol('bz')

B1x, B1y, B1z, A1x, A1y, A1z = half_sections[0]
B2x, B2y, B2z, A2x, A2y, A2z = half_sections[1]
B3x, B3y, B3z, A3x, A3y, A3z = half_sections[2]

result = sp.solve([
    sp.Eq(x1, ax*t1 + bx),
    sp.Eq(y1, ay*t1 + by),
    sp.Eq(z1, az*t1 + bz),
    sp.Eq(x1, A1x*t1 + B1x),
    sp.Eq(y1, A1y*t1 + B1y),
    sp.Eq(z1, A1z*t1 + B1z),
    sp.Eq(x2, ax*t2 + bx),
    sp.Eq(y2, ay*t2 + by),
    sp.Eq(z2, az*t2 + bz),
    sp.Eq(x2, A2x*t2 + B2x),
    sp.Eq(y2, A2y*t2 + B2y),
    sp.Eq(z2, A2z*t2 + B2z),
    sp.Eq(x3, ax*t3 + bx),
    sp.Eq(y3, ay*t3 + by),
    sp.Eq(z3, az*t3 + bz),
    sp.Eq(x3, A3x*t3 + B3x),
    sp.Eq(y3, A3y*t3 + B3y),
    sp.Eq(z3, A3z*t3 + B3z),
])[0]

print(result[bx] + result[by] + result[bz])
