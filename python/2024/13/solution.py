import common

# parse
machines_data = common.read_file().split('\n\n')
machines: list[tuple[int, int, int, int, int, int]] = []
for machine_data in machines_data:
    ba_data, bb_data, prize_data = machine_data.splitlines()
    ax, ay = common.extract_numbers(ba_data)
    bx, by = common.extract_numbers(bb_data)
    x, y = common.extract_numbers(prize_data)
    machines.append((ax, ay, bx, by, x, y))

# part 1
acc = 0
for machine in machines:
    ax, ay, bx, by, px, py = machine
    solutions: list[tuple[int, int]] = []
    for a_presses in range(1, 101):
        x = ax * a_presses
        if x > px:
            break
        b_presses, remainder = divmod(px - x, bx)
        if remainder != 0:
            continue
        y = ay * a_presses + by * b_presses
        if y != py:
            continue
        solutions.append((a_presses, b_presses))
    assert len(solutions) <= 1
    if solutions:
        acc += min(map(lambda x: x[0]*3 + x[1], solutions))
print(acc)

# part 2
# NOTE:
# a_presses * ax[given] + b_presses * bx[given] = px[given]
# a_presses * ay[given] + b_presses * by[given] = py[given]
# 2 equations, 2 unknowns -> solvable
# from equation 1: b_presses = (px - a_presses * ax) / bx
# substitute it in equation 2: a_presses * ay + (px - a_presses * ax) / bx * by = py
# solve for a_presses: a_presses * ay + px / bx * by - a_presses * ax / bx * by = py
# a_presses * (ay - ax / bx * by) = py - px / bx * by
# a_presses = (py - px / bx * by) / (ay - ax / bx * by)
# additionally, the solutions must be integers
acc = 0
for machine in machines:
    ax, ay, bx, by, px, py = machine
    px += 10000000000000
    py += 10000000000000
    # round to compensate for floating point imprecision
    a_presses = round((py - px / bx * by) / (ay - ax / bx * by))
    b_presses = round((px - a_presses * ax) / bx)
    if a_presses < 0 or b_presses < 0:
        continue
    if a_presses * ax + b_presses * bx != px or a_presses * ay + b_presses * by != py: # happens when solution is not an integer
        continue
    acc += a_presses * 3 + b_presses
print(acc)
