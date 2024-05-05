import common
transcript2 = common.import_from_day(2018, 21, 'transcript2')

# part 1
def hook1(r0, r2, r3):
    print(str(r3))
    return False
transcript2.run(hook1)

# part 2
seen_states = set()
seen_possible_solutions = set()
last_unique = 0

def hook2(r0, r2, r3):
    global seen_states
    global seen_possible_solutions
    global last_unique

    key = (r2, r3)

    if key in seen_states:
        print(str(last_unique))
        return False

    seen_states.add(key)
    if r3 not in seen_possible_solutions:
        last_unique = r3
    seen_possible_solutions.add(r3)
    return True
transcript2.run(hook2)
