import common

def run_program(program, ip, r0=0, hook=None):
    lines = program.splitlines()
    lines_with_words = map(common.extract_words, lines)
    instructions = [(x[0], int(x[1]), int(x[2]), int(x[3])) for x in lines_with_words]

    rt = Runtime({
        0: r0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0
    })

    while True:
        curr_ip = rt.registers[ip]
        if curr_ip < 0 or curr_ip >= len(instructions):
            break
        if hook:
            hook(curr_ip, instructions[curr_ip], rt.registers)
        rt.run_instruction(*instructions[curr_ip])
        rt.registers[ip] += 1

    return rt.registers

class Runtime:
    def __init__(self, registers):
        self.registers = registers

    def addr(self, a, b, c):
        self.registers[c] = self.registers[a] + self.registers[b]

    def addi(self, a, b, c):
        self.registers[c] = self.registers[a] + b

    def mulr(self, a, b, c):
        self.registers[c] = self.registers[a] * self.registers[b]

    def muli(self, a, b, c):
        self.registers[c] = self.registers[a] * b

    def banr(self, a, b, c):
        self.registers[c] = self.registers[a] & self.registers[b]

    def bani(self, a, b, c):
        self.registers[c] = self.registers[a] & b

    def borr(self, a, b, c):
        self.registers[c] = self.registers[a] | self.registers[b]

    def bori(self, a, b, c):
        self.registers[c] = self.registers[a] | b

    def setr(self, a, b, c):
        self.registers[c] = self.registers[a]

    def seti(self, a, b, c):
        self.registers[c] = a

    def gtir(self, a, b, c):
        self.registers[c] = 1 if a > self.registers[b] else 0

    def gtri(self, a, b, c):
        self.registers[c] = 1 if self.registers[a] > b else 0

    def gtrr(self, a, b, c):
        self.registers[c] = 1 if self.registers[a] > self.registers[b] else 0

    def eqir(self, a, b, c):
        self.registers[c] = 1 if a == self.registers[b] else 0

    def eqri(self, a, b, c):
        self.registers[c] = 1 if self.registers[a] == b else 0

    def eqrr(self, a, b, c):
        self.registers[c] = 1 if self.registers[a] == self.registers[b] else 0

    def run_instruction(self, instr, a, b, c):
        getattr(self, instr)(a, b, c)