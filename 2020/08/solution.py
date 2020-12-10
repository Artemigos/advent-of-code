import common

instructions = common.pipe_map(
    lambda x: (x[:3], int(x[4:])),
    common.read_file('2020/08/data.txt').splitlines()
)

def try_execute(instructions):
    i = 0
    acc = 0
    seen = set()
    while i not in seen and i < len(instructions):
        seen.add(i)
        cmd, par = instructions[i]
        if cmd == 'nop':
            i += 1
        elif cmd == 'acc':
            acc += par
            i += 1
        else:
            i += par
    return (i >= len(instructions), acc)

# part 1
_, acc = try_execute(instructions)
print(acc)

# part 2
for i in range(len(instructions)):
    cmd, par = instructions[i]
    current_instructions = list(instructions)
    if cmd == 'nop':
        current_instructions[i] = 'jmp', par
    elif cmd == 'jmp':
        current_instructions[i] = 'nop', par
    else:
        continue
    finished, acc = try_execute(current_instructions)
    if finished:
        print(acc)
        break
