import common
import itertools as it
run_intcode = common.import_year_common(2019).run_intcode

tape = common.extract_numbers(common.read_file('2019/07/data.txt'))

class IterGlue:
    def __init__(self):
        self.forward_to = None

    def iterate(self):
        yield from self.forward_to

def prepend(values, iterator):
    yield from iter(values)
    yield from iterator

def solve(phases):
    max_result = 0
    for perm in it.permutations(phases, 5):
        glue = IterGlue()
        i1 = run_intcode(list(tape), prepend([perm[0], 0], glue.iterate()))
        i2 = run_intcode(list(tape), prepend([perm[1]], i1))
        i3 = run_intcode(list(tape), prepend([perm[2]], i2))
        i4 = run_intcode(list(tape), prepend([perm[3]], i3))
        i5 = run_intcode(list(tape), prepend([perm[4]], i4))
        i5_1, i5_2 = it.tee(i5)
        glue.forward_to = i5_2

        for result in i5_1:
            pass
        if result > max_result:
            max_result = result

    return max_result

# part 1
max_result = solve(range(5))
print('part 1:', max_result)

# part 2
max_result = solve(range(5, 10))
print('part 2:', max_result)
