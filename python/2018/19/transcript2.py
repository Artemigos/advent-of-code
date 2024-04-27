def run(r0=0):
    r3 = 10551374 if r0 == 1 else 974
    r0 = 0

    for r4 in range(1, r3+1):
        for r5 in range(1, r3+1):
            if r4*r5 == r3:
                r0 += r4
    return r0

def run_better(r0=0):
    r3 = 10551374 if r0 == 1 else 974
    r0 = 0

    for r4 in range(1, r3+1):
        if r3%r4 == 0:
            r0 += r4

    return r0
