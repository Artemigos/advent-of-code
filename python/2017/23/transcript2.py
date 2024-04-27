def run(part2=False):
    non_prime_count = 0
    start = 81
    end = 81
    if part2:
        start = 108100
        end = 125100
        # c = b + 17000

    for current in range(start, end+1, 17):
        found_factors = False
        for i1 in range(2, current+1):
            for i2 in range(2, current+1):
                if i1*i2 == current:
                    found_factors = True
        if found_factors:
            non_prime_count += 1

    return non_prime_count


if __name__ == '__main__':
    run()
