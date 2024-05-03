import common

lines = common.read_file().splitlines()

reindeer = {}
for line in lines:
    name = line.split(' ')[0]
    nums = common.extract_numbers(line)
    assert len(nums) == 3
    reindeer[name] = tuple(nums)

race_len = 2503

# part 1
max_dist = 0
for name, params in reindeer.items():
    speed, run_len, break_len = params
    cycle_len = run_len + break_len
    full_cycle_dist = run_len*speed
    full_cycles = int(race_len/cycle_len)
    rest = race_len%cycle_len
    rest_run_len = min([rest, run_len])
    rest_dist = rest_run_len*speed
    dist = full_cycles*full_cycle_dist+rest_dist

    if dist > max_dist:
        max_dist = dist

print(max_dist)

distances = dict()
points = dict()
for name, params in reindeer.items():
    distances[name] = 0
    points[name] = 0

for i in range(race_len):
    curr_winner = []
    curr_winning_dist = 0
    for name, dist in distances.items():
        params = reindeer[name]
        speed, run_len, break_len = params
        cycle_len = run_len + break_len
        if i%cycle_len < run_len:
            dist += speed
            distances[name] = dist
        if dist > curr_winning_dist:
            curr_winning_dist = dist
            curr_winner = [name]
        elif dist == curr_winning_dist:
            curr_winner.append(name)
    for w in curr_winner:
        points[w] += 1

print(max(points.values()))
