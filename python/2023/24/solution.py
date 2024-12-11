import common
from itertools import combinations

lines = common.read_file().splitlines()
area_min, area_max = 200000000000000, 400000000000000

# part 1
half_sections: list[tuple[int, int, int, int, int, int, float, float]] = []
for line in lines:
    x, y, z, vx, vy, vz = common.extract_numbers(line)
    assert vx != 0 and vy != 0 and vz != 0
    a = vy / vx
    b = y - a*x
    half_sections.append((x, y, z, vx, vy, vz, a, b))

acc = 0
for l, r in combinations(half_sections, 2):
    x1, y1, _, vx1, vy1, _, a1, b1 = l
    x2, y2, _, vx2, vy2, _, a2, b2 = r
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
