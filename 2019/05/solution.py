import common
run_intcode = common.import_year_common(2019).run_intcode

tape = common.extract_numbers(common.read_file('2019/05/data.txt'))

# part 1
print('part 1:')
result = run_intcode(tape, [1])

# part 2
print('part 2:')
result = run_intcode(tape, [5])
