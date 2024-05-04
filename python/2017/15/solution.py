import common

lines = common.read_file().splitlines()

data_a = common.extract_numbers(lines[0])[0]
data_b = common.extract_numbers(lines[1])[0]

mul_a = 16807
mul_b = 48271
mod = 2147483647
criteria_a = 4
criteria_b = 8

repetitions_1 = 40000000
repetitions_2 = 5000000
cmp_mask = 256*256-1


def create_gen(init, mul, criteria=1):
    prev = init
    while True:
        prev = (prev*mul) % mod
        if not prev % criteria == 0:
            continue
        yield prev


# part 1
gen_a = create_gen(data_a, mul_a)
gen_b = create_gen(data_b, mul_b)

matches = 0
for i in range(repetitions_1):
    a = next(gen_a)
    b = next(gen_b)
    if (a & cmp_mask) == (b & cmp_mask):
        matches += 1

print(matches)

# part 2
gen_a = create_gen(data_a, mul_a, criteria_a)
gen_b = create_gen(data_b, mul_b, criteria_b)

matches = 0

for i in range(repetitions_2):
    a = next(gen_a)
    b = next(gen_b)
    if (a & cmp_mask) == (b & cmp_mask):
        matches += 1

print(matches)
