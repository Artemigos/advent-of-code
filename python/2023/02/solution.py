import common

lines = common.read_file().splitlines()

# parse data
games: list[list[dict]] = []
for line in lines:
    segments = line.split(': ')
    segments = segments[1].split('; ')
    rounds = []
    for round_data in segments:
        groups_data = round_data.split(', ')
        groups = {}
        for group_data in groups_data:
            group_segments = group_data.split(' ')
            count = int(group_segments[0])
            groups[group_segments[1]] = count
        rounds.append(groups)
    games.append(rounds)

# part 1
sum = 0
for i in range(len(games)):
    game = games[i]
    num = i+1
    for round in game:
        if ('red' in round and round['red'] > 12) or ('green' in round and round['green'] > 13) or ('blue' in round and round['blue'] > 14):
            break
    else:
        sum += num

print(sum)

# part 2
sum = 0
for game in games:
    mins = {'red': 0, 'green': 0, 'blue': 0}
    for round in game:
        for col in ['red', 'green', 'blue']:
            val = round.get(col)
            if val is not None:
                mins[col] = max(mins[col], val)
    sum += common.product(mins.values())

print(sum)
