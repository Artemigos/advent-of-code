import common
year_common = common.import_year_common(2019)

tape = common.extract_numbers(common.read_file('2019/13/data.txt'))

# part 1
mem = year_common.tape_to_mem(tape)
it = year_common.run_intcode(mem, iter([]))

blocks = 0
try:
    while True:
        x = next(it)
        y = next(it)
        tile = next(it)

        if tile == 2:
            blocks += 1
except StopIteration:
    pass

print('part 1:', blocks)

# part 2
mem = year_common.tape_to_mem(tape)
mem[0] = 2
# TODO: display game, display score, take player input
