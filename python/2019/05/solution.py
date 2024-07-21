import common

run_intcode = common.import_year_common(2019).run_intcode
tape_to_mem = common.import_year_common(2019).tape_to_mem

tape = common.extract_numbers(common.read_file())

# part 1
mem = tape_to_mem(tape)
output = list(run_intcode(mem, iter([1])))
print(output[-1])

# part 2
mem = tape_to_mem(tape)
output = next(run_intcode(mem, iter([5])))
print(output)
