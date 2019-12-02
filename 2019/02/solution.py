import common
run_intcode = common.import_year_common(2019).run_intcode

sample1 = [1,9,10,3,2,3,11,0,99,30,40,50]
sample2 = [1,0,0,0,99]
sample3 = [2,3,0,3,99]
sample4 = [2,4,4,5,99,0]
sample5 = [1,1,1,4,99,5,6,0,99]

tape = common.extract_numbers(common.read_file('2019/02/data.txt'))

# part 1
print('part 1: ' + str(run_intcode(tape, 12, 2)))

# part 2
for i in range(100):
    for j in range(100):
        result = run_intcode(tape, i, j)
        if result == 19690720:
            print('part 2: ' + str(100*i+j))
            exit(0)

print('part 2: solution not found')
