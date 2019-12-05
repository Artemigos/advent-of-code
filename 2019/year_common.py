def run_intcode(tape, input_data=None):
    input_data = input_data or []
    mem = list(tape)
    ip = 0

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

        def read_param(i):
            return mem[ip+i+1] if parameter_modes[i] == 1 else mem[mem[ip+i+1]]

        def set_at_param(i, val):
            mem[mem[ip+i+1]] = val

        # execute
        if op == 1:
            set_at_param(2, read_param(0) + read_param(1))
            ip += 4
        elif op == 2:
            set_at_param(2, read_param(0) * read_param(1))
            ip += 4
        elif op == 3:
            if len(input_data) == 0:
                raise "not enough input data"
            set_at_param(0, input_data[0])
            input_data = input_data[1:]
            ip += 2
        elif op == 4:
            print(read_param(0))
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
        elif op == 99:
            break
        else:
            raise Exception("unknown op code: " + str(op))

    return mem
