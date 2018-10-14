import common
import re

data = common.read_file('2017/18/data.txt')
lines = data.splitlines()

registers = dict()
instruction = 0
last_sound = -1

def ensure_reg(reg):
    if not reg in registers.keys():
        registers[reg] = 0

def find_val(val):
    m = re.match('-?\\d+', val)
    if m:
        return int(val)
    ensure_reg(val)
    return registers[val]

def set(reg, val):
    global instruction
    ensure_reg(reg)
    val = find_val(val)
    registers[reg] = val
    instruction += 1

def add(reg, val):
    global instruction
    ensure_reg(reg)
    val = find_val(val)
    registers[reg] += val
    instruction += 1

def mul(reg, val):
    global instruction
    ensure_reg(reg)
    val = find_val(val)
    registers[reg] *= val
    instruction += 1

def mod(reg, val):
    global instruction
    ensure_reg(reg)
    val = find_val(val)
    registers[reg] %= val
    instruction += 1

def snd(val):
    global instruction
    global last_sound
    val = find_val(val)
    last_sound = val
    instruction += 1

def rcv(val):
    global instruction
    val = find_val(val)
    instruction += 1
    if val == 0:
        return None
    return last_sound

def jgz(cmp, val):
    global instruction
    cmp = find_val(cmp)
    val = find_val(val)
    if cmp > 0:
        instruction += val
    else:
        instruction += 1

while True:
    instr = lines[instruction]
    print(instruction, ':', instr)
    segments = instr.split(' ')
    code = segments[0]
    if code == 'set':
        set(segments[1], segments[2])
    elif code == 'add':
        add(segments[1], segments[2])
    elif code == 'mul':
        mul(segments[1], segments[2])
    elif code == 'mod':
        mod(segments[1], segments[2])
    elif code == 'snd':
        snd(segments[1])
    elif code == 'rcv':
        if rcv(segments[1]) is not None:
            break
    elif code == 'jgz':
        jgz(segments[1], segments[2])
        if instruction < 0 or instruction >= len(lines):
            break
    else:
        print('unknown instruction ', code)
        exit(1)

print(last_sound)