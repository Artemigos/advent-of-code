def goto(offset):
    pass
def noop():
    pass
def out(val):
    print(val)

def run(a):
    b = 0
    a += 2572

    org = a
    while True:
        if a == 0:
            a = org

        b = a
        a = int(b/2)
        b %= 2

        out(b)

run(158)

def run_org(a):
    b = 0
    c = 0
    d = 0

    d = a # 1
    c = 4 # 2
    b = 643 # 3
    d += 1 # 4
    b -= 1 # 5
    if b != 0:
        goto(-2) # 6
    c -= 1 # 7
    if c != 0:
        goto(-5) # 8
    a = d # 9
    noop() # 10
    b = a # 11
    a = 0 # 12
    c = 2 # 13
    if b != 0:
        goto(2) # 14
    goto(6) # 15
    b -= 1 # 16
    c -= 1 # 17
    if c != 0:
        goto(-4) # 18
    a += 1 # 19
    goto(-7) # 20
    b = 2 # 21
    if c != 0:
        goto(2) # 22
    goto(4) # 23
    b -= 1 # 24
    c -= 1 # 25
    goto(-4) # 26
    noop() # 27
    out(b) # 28
    if a != 0:
        goto(-19) # 29
    goto(-21) # 30
