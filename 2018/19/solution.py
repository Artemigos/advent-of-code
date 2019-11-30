import common

lines = common.read_file('2018/19/data.txt').splitlines()
ip = 2

lines_with_words = map(common.extract_words, lines)
instructions = [(x[0], int(x[1]), int(x[2]), int(x[3])) for x in lines_with_words]

registers = {
    0: 0,
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0
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

def run_instruction(instr, a, b, c):
    globals()[instr](a, b, c)

def set_registers(vals):
    for i in range(len(vals)):
        registers[i] = vals[i]

def registers_equal(vals):
    return list(registers.values()) == vals

def run_program():
    while True:
        curr_ip = registers[ip]
        if curr_ip < 0 or curr_ip >= len(instructions):
            break
        run_instruction(*instructions[curr_ip])
        registers[ip] += 1
        # print(registers)

# part 1
set_registers([0]*6)
run_program()
print('part 1:', registers)

# part 2
set_registers([1]+[0]*5)
run_program()
print('part 2:', registers)
