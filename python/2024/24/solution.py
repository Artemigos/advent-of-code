from typing import Callable
from operator import and_, or_, xor
import common

sections = common.read_file().split('\n\n')
GateOp = Callable[[bool, bool], bool]
Gate = tuple[str, str, GateOp, str]
initial_wires: dict[str, bool] = {}
dependencies: dict[str, Gate] = {}
all_wires: set[str] = set()

for line in sections[0].splitlines():
    name, val = line.split(': ')
    initial_wires[name] = val == '1'

for line in sections[1].splitlines():
    left, op, right, _, out = line.split()
    op_func = xor
    if op == 'AND':
        op_func = and_
    elif op == 'OR':
        op_func = or_
    wire = (left, right, op_func, out)
    dependencies[out] = wire
    all_wires.add(left)
    all_wires.add(right)
    all_wires.add(out)

# part 1
def topo_sort(all_wires: set[str], dependencies: dict[str, Gate]) -> list[str]:
    sorted_wires = []
    def put(sorted_wires: list[str], wire: str):
        if wire in sorted_wires:
            return
        gate = dependencies.get(wire)
        if gate is not None:
            put(sorted_wires, gate[0])
            put(sorted_wires, gate[1])
        sorted_wires.append(wire)

    for wire in all_wires:
        put(sorted_wires, wire)

    return sorted_wires


def resolve_values(initial_wires: dict[str, bool], sorted_wires: list[str], dependencies: dict[str, Gate]) -> dict[str, bool]:
    all_wire_values = dict(initial_wires)
    for wire in sorted_wires:
        if wire in all_wire_values:
            continue
        left, right, op, _ = dependencies[wire]
        val = op(all_wire_values[left], all_wire_values[right])
        all_wire_values[wire] = val
    return all_wire_values

sorted_wires = topo_sort(all_wires, dependencies)
all_wire_values = resolve_values(initial_wires, sorted_wires, dependencies)

acc = 0
zeds_count = len([x for x in all_wire_values if x[0] == 'z'])
for i in range(zeds_count-1, -1, -1):
    k = 'z'+str(i).rjust(2, '0')
    val = all_wire_values[k]
    acc <<= 1
    acc |= val
print(acc)

# part 2
# NOTE: the solution involved manual steps, it won't work on arbitrary input data
def stringify_calc(wire: str, dependencies: dict[str, Gate]) -> str:
    gate = dependencies.get(wire)
    if gate is None:
        return wire
    left, right, op_f, _ = gate
    op = '^'
    if op_f == and_:
        op = '&'
    elif op_f == or_:
        op = '|'
    left_s = stringify_calc(left, dependencies)
    right_s = stringify_calc(right, dependencies)
    if len(left_s) > len(right_s) or (len(left_s) == 3 and len(right_s) == 3 and left_s[0] == 'y' and right_s[0] == 'x'):
        left_s, right_s = right_s, left_s
    return f'({left_s} {op} {right_s})'

def stringify_rest(zi: int) -> str:
    assert zi > 0
    if zi == 1:
        return '(x00 & y00)'
    k = str(zi-1).rjust(2, '0')
    rest = stringify_rest(zi-1)
    return f'((x{k} & y{k}) | ((x{k} ^ y{k}) & {rest}))'

def stringify_expected(zi: int) -> str:
    if zi == 0:
        return '(x00 ^ y00)'
    k = str(zi).rjust(2, '0')
    rest = stringify_rest(zi)
    return f'((x{k} ^ y{k}) ^ {rest})'

exprs = [
    stringify_calc('z00', dependencies),
    stringify_calc('z01', dependencies),
    stringify_calc('z02', dependencies),
    stringify_calc('z03', dependencies),
    stringify_calc('z04', dependencies),
    stringify_calc('z05', dependencies),
    stringify_calc('z06', dependencies),
    stringify_calc('z07', dependencies),
    stringify_calc('z08', dependencies),
    stringify_calc('z09', dependencies),
    stringify_calc('z10', dependencies),
    stringify_calc('z11', dependencies),
]

# NOTE:
# The replacements were added manually by finding the first expression
# that didn't match the expecded 'canonical' expression for that
# output bit. When found, I would manualy comb through data to find the
# wires that should be swapped. That would fix that particular output and
# I would move on to the next failing output until finding 4 pairs which
# fixed everything.
replacements = [
    ('z12', 'kth'),
    ('z26', 'gsd'),
    ('z32', 'tbt'),
    ('qnf', 'vpm'),
]

for fro, to in replacements:
    dependencies[fro], dependencies[to] = dependencies[to], dependencies[fro]

# NOTE:
# This is the code I used to find the first failing output.
# It should never fail anymore for my inpput data.
for i in range(45):
    s1 = stringify_calc('z'+str(i).rjust(2, '0'), dependencies)
    s2 = stringify_expected(i)
    if s1 != s2:
        print(i)
        print('got:')
        print(s1)
        print()
        print('expected:')
        print(s2)
        exit(1)

acc = []
for fro, to in replacements:
    acc.append(fro)
    acc.append(to)
acc = list(sorted(acc))
print(','.join(acc))
