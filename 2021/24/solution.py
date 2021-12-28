import common
run = common.import_from_day('2021', '24', 'transcription').run

# part 1 - solution found by reverse engineering the data

num = [9, 1, 8, 9, 7, 3, 9, 9, 4, 9, 8, 9, 9, 5]
assert run(num) == 0
print(''.join(map(str, num)))

# part 2 - solution found by reverse engineering the data

num = [5, 1, 1, 2, 1, 1, 7, 6, 1, 2, 1, 3, 9, 1]
assert run(num) == 0
print(''.join(map(str, num)))
