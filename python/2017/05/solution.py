import common

data = common.read_file()
lines = data.splitlines()

# part 1
instructions = list(map(lambda x: int(x), lines))
instructions_len = len(instructions)
position = 0
steps = 0

while True:
    if position < 0 or position >= instructions_len:
        break
    steps += 1
    jump = instructions[position]
    instructions[position] += 1
    position += jump

print(steps)

# part 2
instructions = list(map(lambda x: int(x), lines))
instructions_len = len(instructions)
position = 0
steps = 0

while True:
    if position < 0 or position >= instructions_len:
        break
    steps += 1
    jump = instructions[position]
    instructions[position] += 1 if jump < 3 else -1
    position += jump

print(steps)
