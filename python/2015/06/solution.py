import common

lines = common.read_file().splitlines()
ranges = []

for line in lines:
    segments = line.split()
    variant = 'toggle'
    i_offset = 0
    if segments[0] != 'toggle':
        variant = segments[1]
        i_offset = 1
    start = segments[i_offset+1]
    end = segments[i_offset+3]
    start_segments = start.split(',')
    end_segments = end.split(',')
    ranges.append((variant, int(start_segments[0]), int(start_segments[1]), int(end_segments[0]), int(end_segments[1])))
    assert int(start_segments[0]) <= int(end_segments[0])
    assert int(start_segments[1]) <= int(end_segments[1])

# part 1
ranges.reverse()

lit = 0
for x in range(1000):
    for y in range(1000):
        mod = 0
        for r in ranges:
            if r[1] <= x <= r[3] and r[2] <= y <= r[4]:
                if r[0] == 'toggle':
                    mod = 1-mod
                    continue
                if r[0] == 'on' and mod == 0:
                    lit += 1
                elif r[0] == 'off' and mod == 1:
                    lit += 1
                break
        else:
            lit += mod

print(lit)

# part 2
ranges.reverse()

total_brightness = 0
for x in range(1000):
    for y in range(1000):
        brightness = 0
        for r in ranges:
            if r[1] <= x <= r[3] and r[2] <= y <= r[4]:
                if r[0] == 'toggle':
                    brightness += 2
                elif r[0] == 'on':
                    brightness += 1
                else:
                    brightness -= 1
                    if brightness < 0:
                        brightness = 0
        total_brightness += brightness

print(total_brightness)
