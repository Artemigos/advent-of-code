def run(solution_hook, r0 = 0):
    r2, r3 = 0, 0

    while True:
        r2 = r3 | 65536
        r3 = 832312

        while True:
            r3 += (r2 & 255)
            r3 &= 16777215
            r3 *= 65899
            r3 &= 16777215

            if r2 < 256:
                break

            r2 //= 256

        # if r3 == r0:
        if not solution_hook(r0, r2, r3):
            break
