import common

lines = common.read_file().splitlines()

# part 1
eggs = 7
# part 2
eggs = 12

registers = dict(a=eggs, b=0, c=0, d=0)

def get_val(val_spec):
    if val_spec in registers.keys():
        return registers[val_spec]
    return int(val_spec)

def is_reg(val_spec):
    return val_spec in registers.keys()

instructions = [x.split(' ') for x in lines]

i = 0
while i < len(instructions) and i >= 0:
    print(registers)
    instr = instructions[i]
    code = instr[0]
    if code == 'cpy':
        if is_reg(instr[2]):
            registers[instr[2]] = get_val(instr[1])
        i += 1
    elif code == 'inc':
        if is_reg(instr[1]):
            registers[instr[1]] += 1
        i += 1
    elif code == 'dec':
        if is_reg(instr[1]):
            registers[instr[1]] -= 1
        i += 1
    elif code == 'jnz':
        if get_val(instr[1]) != 0:
            i += get_val(instr[2])
        else:
            i += 1
    else: # tgl
        instr_offset = get_val(instr[1])
        instr_idx = i + instr_offset
        if 0 <= instr_idx < len(instructions):
            to_tgl = instructions[instr_idx]
            if to_tgl[0] == 'inc':
                to_tgl[0] = 'dec'
            elif to_tgl[0] == 'dec' or to_tgl[0] == 'tgl':
                to_tgl[0] = 'inc'
            elif to_tgl[0] == 'jnz':
                to_tgl[0] = 'cpy'
            else: # cpy
                to_tgl[0] = 'jnz'
        i += 1

print('a=', registers['a'])
