def run_intcode(tape, noun, verb):
    mem = list(tape)
    mem[1] = noun
    mem[2] = verb

    ip = 0
    while True:
        op = mem[ip]
        if op == 1:
            mem[mem[ip+3]] = mem[mem[ip+1]] + mem[mem[ip+2]]
            ip += 4
        elif op == 2:
            mem[mem[ip+3]] = mem[mem[ip+1]] * mem[mem[ip+2]]
            ip += 4
        elif op == 99:
            break
        else:
            raise "unknown op code: " + str(op)

    return mem[0]
