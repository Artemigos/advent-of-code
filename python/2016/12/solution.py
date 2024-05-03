import common

lines = common.read_file().splitlines()

def get_val(registers, val_spec):
    if val_spec in registers.keys():
        return registers[val_spec]
    return int(val_spec)

def solve(registers):
    i = 0
    while i < len(lines):
        segments = lines[i].split(' ')
        code = segments[0]
        if code == 'cpy':
            registers[segments[2]] = get_val(registers, segments[1])
            i += 1
        elif code == 'inc':
            registers[segments[1]] += 1
            i += 1
        elif code == 'dec':
            registers[segments[1]] -= 1
            i += 1
        else: # jnz
            if get_val(registers, segments[1]) != 0:
                i += int(segments[2])
            else:
                i += 1

    print(registers['a'])

# part 1
solve(dict(a=0, b=0, c=0, d=0))
# part 2
solve(dict(a=0, b=0, c=1, d=0))
