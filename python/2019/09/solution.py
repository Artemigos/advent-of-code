import common
year_common = common.import_year_common(2019)

tape = common.extract_numbers(common.read_file())

# part 1
mem = year_common.tape_to_mem(tape)
output = list(year_common.run_intcode(mem, iter([1])))
print(output[0])

# part 2
mem = year_common.tape_to_mem(tape)
output = list(year_common.run_intcode(mem, iter([2])))
print(output[0])
