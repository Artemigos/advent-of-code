r0, r1, r2, r3, r4, r5 = 0, 0 ,0, 0, 0, 0

r2 += 16
r4 = 1
r5 = 1
r1 = r4*r5
r1 = 1 if r1==r3 else 0
r2 += r1
r2 += 1
r0 += r4
r5 += 1
r1 = 1 if r5==r3 else 0
r2 += r1
r2 = 2
