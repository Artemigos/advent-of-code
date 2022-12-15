import common

lines = common.read_file('2022/10/data.txt').splitlines()

# parse
instructions = []
for line in lines:
    segments = line.split(' ')
    if len(segments) == 2:
        instructions.append((segments[0], int(segments[1])))
    else:
        instructions.append((segments[0], 0))

# common
class Interpreter:
    def __init__(self, instructions):
        self.instructions = instructions
        self.cycle = 1
        self.x = 1
        self.instr = 0
        self._last_instr = 0

    def tick(self):
        instruction, val = self.instructions[self.instr]
        if instruction == 'addx':
            if self._last_instr == self.instr:
                self.x += val
                self.instr += 1
            else:
                self._last_instr = self.instr
        else:
            self._last_instr = self.instr
            self.instr += 1

        self.cycle += 1

    def run_cycles(self, amount, acc, handler):
        for _ in range(amount):
            acc = handler(self.cycle, self.x, acc)
            self.tick()
        return acc

# part 1
score_cycles = [20, 60, 100, 140, 180, 220]
def part1_handler(cycle, x, acc):
    if cycle in score_cycles:
        acc += cycle * x
    return acc

print(Interpreter(instructions).run_cycles(220, 0, part1_handler))


# part 2
def part2_handler(cycle, x, points):
    scan_x = (cycle-1) % 40
    if abs(scan_x - x) <= 1:
        points.add(cycle)
    return points

points = Interpreter(instructions).run_cycles(240, set(), part2_handler)

for y in range(6):
    for x in range(40):
        cycle = y * 40 + x + 1
        if cycle in points:
            print('#', end='')
        else:
            print(' ', end='')
    print()
