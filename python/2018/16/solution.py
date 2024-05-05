import common

registers = {
    0: 0,
    1: 0,
    2: 0,
    3: 0
}

def addr(a, b, c):
    registers[c] = registers[a] + registers[b]

def addi(a, b, c):
    registers[c] = registers[a] + b

def mulr(a, b, c):
    registers[c] = registers[a] * registers[b]

def muli(a, b, c):
    registers[c] = registers[a] * b

def banr(a, b, c):
    registers[c] = registers[a] & registers[b]

def bani(a, b, c):
    registers[c] = registers[a] & b

def borr(a, b, c):
    registers[c] = registers[a] | registers[b]

def bori(a, b, c):
    registers[c] = registers[a] | b

def setr(a, b, c):
    registers[c] = registers[a]

def seti(a, b, c):
    registers[c] = a

def gtir(a, b, c):
    registers[c] = 1 if a > registers[b] else 0

def gtri(a, b, c):
    registers[c] = 1 if registers[a] > b else 0

def gtrr(a, b, c):
    registers[c] = 1 if registers[a] > registers[b] else 0

def eqir(a, b, c):
    registers[c] = 1 if a == registers[b] else 0

def eqri(a, b, c):
    registers[c] = 1 if registers[a] == b else 0

def eqrr(a, b, c):
    registers[c] = 1 if registers[a] == registers[b] else 0

instructions = [
    'addr', 'addi', 'mulr', 'muli',
    'banr', 'bani', 'borr', 'bori',
    'setr', 'seti',
    'gtir', 'gtri', 'gtrr',
    'eqir', 'eqri', 'eqrr'
]

def run_instruction(instr, a, b, c):
    globals()[instr](a, b, c)

def set_registers(vals):
    for i in range(len(vals)):
        registers[i] = vals[i]

def registers_equal(vals):
    return list(registers.values()) == vals

lines = common.read_file().split('\n\n\n\n')[0].splitlines()

match3 = 0
for i in range(0, len(lines), 4):
    before = common.extract_numbers(lines[i])
    after = common.extract_numbers(lines[i+2])
    op = common.extract_numbers(lines[i+1])

    matches = 0
    for instr in instructions:
        set_registers(before)
        run_instruction(instr, *op[1:])
        if registers_equal(after):
            matches += 1
    if matches >= 3:
        match3 += 1

print(match3)

# part 2 - figure out op numbers
ops = {}
prev_len = -1
while len(ops) != prev_len:
    prev_len = len(ops)
    for i in range(0, len(lines), 4):
        before = common.extract_numbers(lines[i])
        after = common.extract_numbers(lines[i+2])
        op = common.extract_numbers(lines[i+1])
        if op[0] in ops:
            continue

        matches = []
        for instr in instructions:
            if instr in ops.values():
                continue
            set_registers(before)
            run_instruction(instr, *op[1:])
            if registers_equal(after):
                matches.append(instr)
        if len(matches) == 1:
            ops[op[0]] = matches[0]

# print(ops)
# print(len(set(ops.values())))

# part 2 - run program
program = [common.extract_numbers(x) for x in common.read_file().split('\n\n\n\n')[1].splitlines()]

set_registers([0, 0, 0, 0])
for op in program:
    instr = ops[op[0]]
    run_instruction(instr, *op[1:])

print(registers[0])
