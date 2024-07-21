import common
import multiprocessing as mp
import os

data = [x.split(' ') for x in common.read_file().splitlines()]

def calc_pos(start, deck_size, curr_mul, const_add):
    return (start*curr_mul+const_add)%deck_size

def calc_muls(deck_size):
    curr_mul = 1
    const_add = 0

    for move in data:
        if move[0] == 'cut':
            const_add -= int(move[-1])
        elif move[1] == 'with':
            val = int(move[-1])
            curr_mul *= val
            const_add *= val
        else:
            curr_mul *= -1
            const_add *= -1
            const_add -= 1

    curr_mul %= deck_size
    const_add %= deck_size

    return curr_mul, const_add

def compound_muls(curr_mul, const_add, repetitions):
    def compound_10(curr_mul, const_add):
        repeating_mul = 1
        repeating_add = 0
        for _ in range(10):
            repeating_mul *= curr_mul
            repeating_add *= curr_mul
            repeating_add += const_add

            repeating_mul %= deck_size
            repeating_add %= deck_size
        return repeating_mul, repeating_add

    muls = {1: (curr_mul, const_add)}
    current_repeats = 1
    while current_repeats < repetitions:
        current_repeats *= 10
        curr_mul, const_add = compound_10(curr_mul, const_add)
        muls[current_repeats] = curr_mul, const_add

    known_muls = list(sorted(muls.keys(), reverse=True))
    curr_mul = 1
    const_add = 0

    for m in known_muls:
        mul, add = muls[m]
        while m <= repetitions:
            curr_mul *= mul
            const_add *= mul
            const_add += add

            curr_mul %= deck_size
            const_add %= deck_size

            repetitions -= m

    return curr_mul, const_add

# part 1
deck_size = 10007
curr_mul, const_add = calc_muls(deck_size)
curr = calc_pos(2019, deck_size, curr_mul, const_add)
print(curr)

# part 2 - it's not the prettiest, but if you have time it does the job
repetitions = 101741582076661
deck_size = 119315717514047

curr_mul, const_add = calc_muls(deck_size)
curr_mul, const_add = compound_muls(curr_mul, const_add, repetitions)
target = 2020

def check_range(rng, finished):
    interval = 10000000
    total = 0
    curr = calc_pos(rng.start, deck_size, curr_mul, const_add)
    for i in range(rng.start+1, rng.stop):
        curr += curr_mul
        curr %= deck_size
        if curr == target:
            with finished.get_lock():
                print(i)
                break

        total += 1
        if total == interval:
            with finished.get_lock():
                finished.value += interval
                total = 0

process_count = os.cpu_count()-2
chunk_size = deck_size//process_count
processes = []
finished = mp.Value('L', 0)

for i in range(process_count):
    rng = range(i*chunk_size, (i+1)*chunk_size)
    p = mp.Process(target=check_range, args=(rng, finished))
    p.start()
    processes.append(p)

for p in processes:
    p.join()
