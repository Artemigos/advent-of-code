import common

rules_data, ticket_data, nearby_tickets_data = common.read_file().split('\n\n')
ticket_data = ticket_data.splitlines()[1]
nearby_tickets_data = nearby_tickets_data.splitlines()[1:]

rules = {}
for l in rules_data.splitlines():
    name, ranges = l.split(': ')
    ranges = ranges.split(' or ')
    for i in range(len(ranges)):
        left, right = ranges[i].split('-')
        ranges[i] = range(int(left), int(right)+1)
    rules[name] = ranges

ticket = list(map(int, ticket_data.split(',')))
nearby_tickets = []
for l in nearby_tickets_data:
    nearby_tickets.append(list(map(int, l.split(','))))

# part 1
flat_ranges = [x for v in rules.values() for x in v]
flat_values = [x for t in nearby_tickets for x in t]
invalid_values = []
for v in flat_values:
    for rng in flat_ranges:
        if v in rng:
            break
    else:
        invalid_values.append(v)

print(sum(invalid_values))

# part 2
possible_fields = []
for i in range(len(ticket)):
    names = list(rules.keys())
    possible_fields.append(names)
valid_tickets = []
for t in nearby_tickets:
    for v in t:
        if v in invalid_values:
            break
    else:
        valid_tickets.append(t)

for t in valid_tickets:
    for i in range(len(t)):
        for k in rules:
            for rng in rules[k]:
                if t[i] in rng:
                    break
            else:
                if k in possible_fields[i]:
                    possible_fields[i].remove(k)

while any(map(lambda x: len(x) > 1, possible_fields)):
    for fields in possible_fields:
        if len(fields) == 1:
            for fields2 in possible_fields:
                if fields[0] in fields2 and fields is not fields2:
                    fields2.remove(fields[0])

field_map = {x[0]: i for i, x in enumerate(possible_fields)}

mul = 1
for k in field_map:
    if k.startswith('departure'):
        mul *= ticket[field_map[k]]

print(mul)
