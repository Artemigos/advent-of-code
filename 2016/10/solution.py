import common

lines = common.read_file('2016/10/data.txt').splitlines()

values = dict()
bots = dict()
bots_values = dict()
outputs = dict()
for l in lines:
    segments = l.split(' ')
    if segments[0] == 'value':
        values[int(segments[1])] = int(segments[5])
    else:
        bots[int(segments[1])] = (
            int(segments[6]) if segments[5] == 'bot' else -int(segments[6])-1,
            int(segments[11]) if segments[10] == 'bot' else -int(segments[11])-1
        )

def propagate_value(bot, val):
    if bot not in bots_values.keys():
        bots_values[bot] = [val]
    else:
        vals = bots_values[bot]
        vals.append(val)
        vals.sort()

        # part 1
        if vals == [17, 61]:
            print(bot)

        children = bots[bot]
        if children[0] >= 0:
            propagate_value(children[0], vals[0])
        else:
            outputs[children[0]] = vals[0]
        if children[1] >= 0:
            propagate_value(children[1], vals[1])
        else:
            outputs[children[1]] = vals[1]

for val, bot in values.items():
    propagate_value(bot, val)

# part 2
prod = 1
for k in [-1, -2, -3]:
    prod *= outputs[k]

print(prod)
