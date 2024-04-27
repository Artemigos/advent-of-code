import common

lines = common.read_file().splitlines()
times = common.extract_numbers(lines[0])
distances = common.extract_numbers(lines[1])

# part 1
aboves = []
for i in range(len(times)):
    time = times[i]
    distance = distances[i]
    above = 0
    for pressed in range (1, time):
        dist = pressed * (time - pressed)
        if dist > distance:
            above += 1
    aboves.append(above)

acc = 1
for above in aboves:
    acc *= above
print(acc)

# part 2
time = common.extract_numbers(lines[0].replace(' ', ''))[0]
distance = common.extract_numbers(lines[1].replace(' ', ''))[0]

above = 0
for pressed in range (1, time):
    dist = pressed * (time - pressed)
    if dist > distance:
        above += 1
print(above)
