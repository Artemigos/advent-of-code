import common

commands = common.read_file().splitlines()
commands = [(a, int(b)) for a, b in (x.split(' ') for x in commands)]

# part 1
x, y = 0, 0
for cmd, num in commands:
    if cmd == 'forward':
        x += num
    elif cmd == 'down':
        y += num
    elif cmd == 'up':
        y -= num
    else:
        raise 'wut'

print(x*y)

# part 2
x, y, aim = 0, 0, 0
for cmd, num in commands:
    if cmd == 'forward':
        x += num
        y += num*aim
    elif cmd == 'down':
        aim += num
    elif cmd == 'up':
        aim -= num
    else:
        raise 'wut'

print(x*y)
