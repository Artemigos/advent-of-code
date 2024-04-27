def run_intcode(mem: dict, input_data=None):
    ip = 0
    rel_base = 0

    while True:
        op = mem[ip]%100

        # read parameter modes
        parameter_modes = [0, 0, 0]
        param_specifier = mem[ip]//100
        param_i = 0
        while param_specifier > 0:
            parameter_modes[param_i] = param_specifier%10
            param_specifier //= 10
            param_i += 1

        def mem_get(i):
            return 0 if i not in mem else mem[i]

        def mem_set(i, val):
            mem[i] = val

        def read_param(i):
            if parameter_modes[i] == 0:
                return mem_get(mem_get(ip+i+1))
            elif parameter_modes[i] == 1:
                return mem_get(ip+i+1)
            elif parameter_modes[i] == 2:
                return mem_get(mem_get(ip+i+1)+rel_base)
            else:
                raise Exception("unsupported parameter mode for get: " + str(parameter_modes[i]))

        def set_at_param(i, val):
            if parameter_modes[i] == 0:
                mem_set(mem_get(ip+i+1), val)
            elif parameter_modes[i] == 2:
                mem_set(mem_get(ip+i+1)+rel_base, val)
            else:
                raise Exception("unsupported parameter mode for set: " + str(parameter_modes[i]))

        # execute
        if op == 1:
            set_at_param(2, read_param(0) + read_param(1))
            ip += 4
        elif op == 2:
            set_at_param(2, read_param(0) * read_param(1))
            ip += 4
        elif op == 3:
            set_at_param(0, next(input_data))
            ip += 2
        elif op == 4:
            yield read_param(0)
            ip += 2
        elif op == 5:
            if read_param(0) != 0:
                ip = read_param(1)
            else:
                ip += 3
        elif op == 6:
            if read_param(0) == 0:
                ip = read_param(1)
            else:
                ip += 3
        elif op == 7:
            result = 1 if read_param(0) < read_param(1) else 0
            set_at_param(2, result)
            ip += 4
        elif op == 8:
            result = 1 if read_param(0) == read_param(1) else 0
            set_at_param(2, result)
            ip += 4
        elif op == 9:
            rel_base += read_param(0)
            ip += 2
        elif op == 99:
            break
        else:
            raise Exception("unknown op code: " + str(op))

def tape_to_mem(tape):
    mem = {}
    for i, num in enumerate(tape):
        mem[i] = num
    return mem
