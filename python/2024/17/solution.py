import common

lines = common.read_file().splitlines()
start_a = common.extract_numbers(lines[0])[0]
start_b = common.extract_numbers(lines[1])[0]
start_c = common.extract_numbers(lines[2])[0]
program = common.extract_numbers(lines[4])

# part 1
def run(a: int, b: int, c: int) -> list[int]:
    instr = 0
    def get_combo(val: int) -> int:
        if val < 4:
            return val
        if val == 4:
            return a
        if val == 5:
            return b
        if val == 6:
            return c
        raise Exception('invalid combo value')

    out: list[int] = []
    while instr < len(program):
        opcode, operand = program[instr:instr+2]
        if opcode == 0:
            a >>= get_combo(operand)
        elif opcode == 1:
            b ^= operand
        elif opcode == 2:
            b = get_combo(operand) & 0b111
        elif opcode == 3:
            if a != 0:
                instr = operand
                continue
        elif opcode == 4:
            b ^= c
        elif opcode == 5:
            out.append(get_combo(operand) & 0b111)
        elif opcode == 6:
            b = a >> get_combo(operand)
        elif opcode == 7:
            c = a >> get_combo(operand)
        else:
            raise Exception('unknown opcode')
        instr += 2

    return out

print(','.join(map(str, run(start_a, start_b, start_c))))

# part 2
# reverse engineered
def run_rev_eng(a: int, b: int, c: int) -> list[int]:
    out = []

    while True:
        b = a & 0b111 # bst 4
        b ^= 1 # bxl 1
        c = a >> b # cdv 5
        a = a >> 3 # adv 3
        b ^= c # bxc 3
        b ^= 6 # bxl 6
        out.append(b & 0b111) # out 5
        if a == 0: # jnz 0 (loop when a != 0)
            break

    return out

# NOTE: from analysis of reverse engineered program:
# - we're operating on triplets (like bytes, but 3 bits instead)
# - the solution will have as many triplets as the program
# - looking at output triplets from right to left, given triplet is a result of a triplet in the same position in the input + up to 3 previous triplets
# - so search for a triplet that produces a valid output triplet 3 positions further - then it can't change anymore
# - need to seed the search with all possible sets of 3 triplets (there's only 8**3 = 512 of them)

def actualize(num: list[int]) -> int:
    acc = 0
    for n in reversed(num):
        acc <<= 3
        acc |= n
    return acc

seed: list[list[int]] = []
for i in range(8):
    for j in range(8):
        for k in range(8):
            seed.append([i, j, k])

off = 1
while True:
    new_seed = []
    for s in seed:
        for i in range(8):
            ns = [i] + s
            out = run_rev_eng(actualize(ns), start_b, start_c)
            if out == program:
                print(actualize(ns))
                exit(0)
            if len(out) >= off and out[-off] == program[-off]:
                new_seed.append(ns)
    seed = new_seed
    off += 1
