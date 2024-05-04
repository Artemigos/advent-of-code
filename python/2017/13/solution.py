import common

data = common.read_file()
lines = data.splitlines()


def parse_line(line):
    segments = line.split(':')
    return int(segments[0]), int(segments[1].strip())


layers = list(map(parse_line, lines))

# part 1
severity = 0
for depth, rng in layers:
    if rng == 1 or (rng != 0 and depth % ((rng-1)*2) == 0):
        severity += depth * rng

print(severity)

# part 2
delay = 0
while True:
    delay += 1
    found = False
    for depth, rng in layers:
        if rng == 1 or (rng != 0 and (depth+delay) % ((rng-1)*2) == 0):
            found = True
            break

    if not found:
        break

print(delay)
