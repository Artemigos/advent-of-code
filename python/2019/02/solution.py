import common
run_intcode = common.import_year_common(2019).run_intcode
tape_to_mem = common.import_year_common(2019).tape_to_mem

tape = common.extract_numbers(common.read_file())

# part 1
tape[1] = 12
tape[2] = 2
mem = tape_to_mem(tape)
list(run_intcode(mem))
print(str(mem[0]))

# part 2
for i in range(100):
    for j in range(100):
        tape[1] = i
        tape[2] = j
        mem = tape_to_mem(tape)
        list(run_intcode(mem))
        if mem[0] == 19690720:
            print(str(100*i+j))
            exit(0)

print('solution not found')
