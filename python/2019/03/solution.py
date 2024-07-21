import common

data = common.read_file().splitlines()
moves1 = data[0].split(',')
moves2 = data[1].split(',')

def generate_positions(moves):
    at = [0, 0]

    for move in moves:
        direction = move[0]
        amount = int(move[1:])

        for i in range(amount):
            if direction == 'R':
                at[0] += 1
            elif direction == 'L':
                at[0] -= 1
            elif direction == 'U':
                at[1] += 1
            elif direction == 'D':
                at[1] -= 1
            else:
                raise Exception('unknown direction')
            yield tuple(at)

# part 1
line1_points = set(generate_positions(moves1))
line2_points = set(generate_positions(moves2))

intersection = line1_points.intersection(line2_points)

min_dist = None
for pos in intersection:
    dist = abs(pos[0]) + abs(pos[1])
    if min_dist is None or dist < min_dist:
        min_dist = dist

print(min_dist)

# part 2
line1_points = list(generate_positions(moves1))
line2_points = list(generate_positions(moves2))

min_steps = None
for pos in intersection:
    steps1 = line1_points.index(pos)+1
    steps2 = line2_points.index(pos)+1
    all_steps = steps1 + steps2

    if min_steps is None or all_steps < min_steps:
        min_steps = all_steps

print(min_steps)
