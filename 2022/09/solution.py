import common

lines = common.read_file().splitlines()
moves = []

# parse
for line in lines:
    segments = line.split(' ')
    moves.append((segments[0], int(segments[1])))

# common
def sgn(x):
    if x == 0:
        return 0
    return -1 if x < 0 else 1

def solve(knots):
    def offset(i, dx, dy):
        knots[i] = (knots[i][0] + dx, knots[i][1] + dy)

    seen = set([knots[-1]])
    for direction, amount in moves:
        for _ in range(amount):
            if direction == 'L':
                offset(0, -1, 0)
            elif direction == 'R':
                offset(0, 1, 0)
            elif direction == 'U':
                offset(0, 0, 1)
            else:
                offset(0, 0, -1)

            for i in range(1, len(knots)):
                dx = knots[i-1][0] - knots[i][0]
                dy = knots[i-1][1] - knots[i][1]
                if abs(dx) > 1 or abs(dy) > 1:
                    offset(i, sgn(dx), sgn(dy))

            seen.add(knots[-1])

    print(len(seen))

# part 1
solve([(0, 0)] * 2)

# part 2
solve([(0, 0)] * 10)
