import common

data = common.read_file('2017/5/data.txt')
lines = data.splitlines()

instructions = list(map(lambda x: int(x), lines))
instructions_len = len(instructions)
position = 0
steps = 0

while True:
    if position < 0 or position >= instructions_len:
        break
    steps += 1
    jump = instructions[position]
    # part 1
    # instructions[position] += 1
    # part 2
    instructions[position] += 1 if jump < 3 else -1
    position += jump

print(steps)
