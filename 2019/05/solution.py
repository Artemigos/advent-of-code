import common
run_intcode = common.import_year_common(2019).run_intcode

tape = common.extract_numbers(common.read_file('2019/05/data.txt'))

# part 1
mem = list(tape)
output = list(run_intcode(mem, iter([1])))
print('part 1:', output)

# part 2
mem = list(tape)
output = next(run_intcode(mem, iter([5])))
print('part 2:', output)
