import common
import operator
import re

lines = common.read_file('2015/07/data.txt').splitlines()

values = dict()
gates = []

def bit_not(val):
    return val ^ 0b1111111111111111

def passthrough(val):
    return val

def get_val(val_spec):
    if re.match('\\d+', val_spec):
        return int(val_spec)
    if val_spec in values.keys():
        return values[val_spec]
    return None

def set_val(name, val):
    values[name] = val
    if name == 'a':
        print(val)

seen = set()

def propagate_val(name):
    fulfilled = []
    for g in gates:
        if name in g[0] and g[2] not in values.keys():
            vals = list(map(get_val, g[0]))
            vals_not_none = list(map(lambda x: x is not None, vals))
            if not all(vals_not_none):
                continue
            result = g[1](*vals)
            set_val(g[2], result)
            fulfilled.append(g)

    for g in fulfilled:
        propagate_val(g[2])

def op_for_name(name):
    if name == 'AND':
        return operator.and_
    elif name == 'OR':
        return operator.or_
    elif name == 'LSHIFT':
        return operator.lshift
    else: # RSHIFT
        return operator.rshift

for line in lines:
    segments = line.split()
    name = segments[-1]
    if len(segments) == 3: # just a value provided
        gates.append((( segments[0], ), passthrough, name))
        val = get_val(segments[0])
        if val is not None:
            set_val(name, val)
            propagate_val(name)
    elif len(segments) == 4: # NOT
        gates.append((( segments[1], ), bit_not, name))
        val = get_val(segments[1])
        if val is not None:
            set_val(name, bit_not(val))
            propagate_val(name)
    else: # two-arg operators
        op = op_for_name(segments[1])
        gates.append((( segments[0], segments[2] ), op, name))
        val1 = get_val(segments[0])
        val2 = get_val(segments[2])
        if val1 is not None and val2 is not None:
            set_val(name, op(val1, val2))
            propagate_val(name)

# part 2
values = dict(b=values['a'])

for g in gates:
    if g[2] not in values:
        vals = list(map(get_val, g[0]))
        vals_not_none = list(map(lambda x: x is not None, vals))
        if not all(vals_not_none):
            continue
        result = g[1](*vals)
        set_val(g[2], result)
        propagate_val(g[2])
