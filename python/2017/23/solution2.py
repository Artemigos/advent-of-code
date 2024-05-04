import common

def run():
    lines = common.read_file('2017/23/primes.txt').splitlines()
    primes = set(map(int, lines))

    count = 0
    for i in range(108100, 125101, 17):
        if i not in primes:
            count += 1

    print(count)
