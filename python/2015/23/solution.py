import common

lines = common.read_file('2015/23/data.txt').splitlines()
instructions = [line.split() for line in lines]

def run(registers):
    i = 0

    while i >= 0 and i < len(instructions):
        instr = instructions[i]
        if instr[0] == 'hlf':
            registers[instr[1]] = int(registers[instr[1]]/2)
            i += 1
        elif instr[0] == 'tpl':
            registers[instr[1]] *= 3
            i += 1
        elif instr[0] == 'inc':
            registers[instr[1]] += 1
            i += 1
        elif instr[0] == 'jmp':
            i += int(instr[1])
        elif instr[0] == 'jie':
            if registers[instr[1][0]]%2 == 0:
                i += int(instr[2])
            else:
                i += 1
        else: # jio
            if registers[instr[1][0]] == 1:
                i += int(instr[2])
            else:
                i += 1

    print(registers['b'])

run(dict(a=0, b=0))
run(dict(a=1, b=0))
