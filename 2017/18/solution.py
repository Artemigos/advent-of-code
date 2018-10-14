import common
import re
import queue

data = common.read_file('2017/18/data.txt')
lines = data.splitlines()
instructions = list(map(lambda x: x.split(' '), lines))

class Runtime:
    def __init__(self, instructions):
        self.instructions = instructions
        self.registers = dict()
        self.instruction = 0
        self.last_sound = None
        self.received_sound = None

    def ensure_reg(self, reg):
        if not reg in self.registers.keys():
            self.registers[reg] = 0

    def find_val(self, val):
        m = re.match('-?\\d+', val)
        if m:
            return int(val)
        self.ensure_reg(val)
        return self.registers[val]

    def current_instruction(self):
        if self.instruction_out_of_bounds():
            return None
        return self.instructions[self.instruction]

    def instruction_out_of_bounds(self):
        return self.instruction < 0 or self.instruction >= len(self.instructions)

    def set(self, reg, val):
        self.ensure_reg(reg)
        val = self.find_val(val)
        self.registers[reg] = val
        self.instruction += 1

    def add(self, reg, val):
        self.ensure_reg(reg)
        val = self.find_val(val)
        self.registers[reg] += val
        self.instruction += 1

    def mul(self, reg, val):
        self.ensure_reg(reg)
        val = self.find_val(val)
        self.registers[reg] *= val
        self.instruction += 1

    def mod(self, reg, val):
        self.ensure_reg(reg)
        val = self.find_val(val)
        self.registers[reg] %= val
        self.instruction += 1

    def snd_sound(self, val):
        val = self.find_val(val)
        self.last_sound = val
        self.instruction += 1

    def rcv_sound(self, val):
        val = self.find_val(val)
        self.instruction += 1
        if val != 0:
            self.received_sound = self.last_sound

    def jgz(self, cmp, val):
        cmp = self.find_val(cmp)
        val = self.find_val(val)
        if cmp > 0:
            self.instruction += val
        else:
            self.instruction += 1

    def advance(self):
        self.instruction += 1

    def process_instr(self, instr=None):
        instr = instr or self.current_instruction()
        code = instr[0]
        if code == 'set':
            self.set(instr[1], instr[2])
        elif code == 'add':
            self.add(instr[1], instr[2])
        elif code == 'mul':
            self.mul(instr[1], instr[2])
        elif code == 'mod':
            self.mod(instr[1], instr[2])
        elif code == 'snd':
            self.snd_sound(instr[1])
        elif code == 'rcv':
            self.rcv_sound(instr[1])
        elif code == 'jgz':
            self.jgz(instr[1], instr[2])
        else:
            print('unknown instruction ', code)
            exit(1)

# part 1
rt1 = Runtime(instructions)
while True:
    rt1.process_instr()
    if rt1.received_sound is not None:
        break
    if rt1.instruction_out_of_bounds():
        break

print(rt1.last_sound)

# part 2
rt21 = Runtime(instructions)
rt22 = Runtime(instructions)
rt21.registers['p'] = 0
rt22.registers['p'] = 1
q1 = queue.Queue()
q2 = queue.Queue()
p1_sent_count = 0
p2_sent_count = 0
while True:
    instr1 = rt21.current_instruction()
    instr2 = rt22.current_instruction()
    code1 = instr1[0] if instr1 else None
    code2 = instr2[0] if instr2 else None

    locked1 = (code1 == 'rcv' and q1.empty()) or code1 == None
    locked2 = (code2 == 'rcv' and q2.empty()) or code2 == None
    if locked1 and locked2:
        break # deadlock

    if code1:
        if code1 == 'snd':
            val = rt21.find_val(instr1[1])
            q2.put(str(val))
            p1_sent_count += 1
            rt21.advance()
        elif code1 == 'rcv':
            if not q1.empty():
                el = q1.get()
                rt21.set(instr1[1], el)
        else:
            rt21.process_instr(instr1)

    if code2:
        if code2 == 'snd':
            val = rt22.find_val(instr2[1])
            q1.put(str(val))
            p2_sent_count += 1
            rt22.advance()
        elif code2 == 'rcv':
            if not q2.empty():
                el = q2.get()
                rt22.set(instr2[1], el)
        else:
            rt22.process_instr(instr2)

print(p1_sent_count)
print(p2_sent_count)
