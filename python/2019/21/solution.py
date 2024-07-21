import common
year_common = common.import_year_common(2019)

tape = common.extract_numbers(common.read_file())

def send_program(program):
    for c in program:
        # print(c, end='')
        yield ord(c)

# part 1
program = \
'''NOT A T
OR A T
AND A T
AND B T
AND C T
NOT T T
AND D T
NOT T T
NOT T J
WALK
'''

mem = year_common.tape_to_mem(tape)
it = year_common.run_intcode(mem, send_program(program))

for val in it:
    if val >= 0 and val <= 255:
        # print(chr(val), end='')
        pass
    else:
        print(val)

# part 2
program = \
'''NOT A T
OR A T
AND A T
AND B T
AND C T
NOT T T
AND D T
NOT T T
NOT T J
NOT E T
NOT T T
OR H T
AND T J
RUN
'''

mem = year_common.tape_to_mem(tape)
it = year_common.run_intcode(mem, send_program(program))

for val in it:
    if val >= 0 and val <= 255:
        # print(chr(val), end='')
        pass
    else:
        print(val)
