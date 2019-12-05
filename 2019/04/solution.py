data = range(193651, 649729 + 1)

# part 1
amount = 0
for a in range(2, 6):
    for b in range(a, 10):
        for c in range(b, 10):
            for d in range(c, 10):
                for e in range(d, 10):
                    for f in range(e, 10):
                        if a == b or b == c or c == d or d == e or e == f:
                            amount += 1

print('part 1:', amount+1) # +1 for the 199999 solution that is skipped in the loops

# part 2
amount = 0
for a in range(2, 6):
    for b in range(a, 10):
        for c in range(b, 10):
            for d in range(c, 10):
                for e in range(d, 10):
                    for f in range(e, 10):
                        if (a == b and b != c) or (b == c and a != b and c != d) or (c == d and b != c and d != e) or (d == e and c != d and e != f) or (e == f and d != e):
                            amount += 1

print('part 2:', amount)
