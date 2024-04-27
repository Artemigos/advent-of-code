import common

# run_program = common.import_year_common(2018).run_program
# program = common.read_file('2018/19/data.txt')
# ip = 2

# def hook(curr_ip, instruction, registers):
#     if curr_ip == 1:
#         print('pre-loop state:', registers)

# # part 1
# result = run_program(program, ip, hook=hook)
# print('part 1:', result)

# # part 2
# result = run_program(program, ip, 1, hook)
# print('part 2:', result)

# --------------------------

transcript2 = common.import_from_day(2018, 19, 'transcript2')

# part 1
result = transcript2.run_better()
print('part 1:', result)

# part 2
result = transcript2.run_better(1)
print('part 2:', result)
