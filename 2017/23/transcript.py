# init
reg = dict()

def reset_reg():
    global reg
    reg = dict(
        a = 0,
        b = 0,
        c = 0,
        d = 0,
        e = 0,
        f = 0,
        g = 0,
        h = 0
    )

reset_reg()

# code
def l1():
    reg['b'] = 81 #1
    reg['c'] = reg['b'] #2
    if reg['a'] != 0:
        l5() #3
    else:
        l9() #4

def l5():
    reg['b'] *= 100 #5
    reg['b'] -= -100000 #6
    reg['c'] = reg['b'] #7
    reg['c'] -= -17000 #8
    l9()

def l9():
    reg['f'] = 1 #9
    reg['d'] = 2 #10
    l11()

def l11():
    reg['e'] = 2 #11
    l12()

def l12():
    reg['g'] = reg['d'] #12
    reg['g'] *= reg['e'] #13
    reg['g'] -= reg['b'] #14
    if reg['g'] != 0:
        l17() #15
    else:
        reg['f'] = 0 #16
        l17()

def l17():
    reg['e'] -= -1 #17
    reg['g'] = reg['e'] #18
    reg['g'] -= reg['b'] #19
    if reg['g'] != 0:
        l12() #20
    else:
        reg['d'] -= -1 # 21
        reg['g'] = reg['d'] #22
        reg['g'] -= reg['b'] #23
        if reg['g'] != 0:
            l11() #24
        else:
            if reg['f'] != 0:
                l27() #25
            else:
                reg['h'] -= -1 #26
                l27()

def l27():
    reg['g'] = reg['b'] #27
    reg['g'] -= reg['c'] #28
    if reg['g'] != 0:
        l31() #29
    else:
        l33() #30

def l31():
    reg['b'] -= -17 #31
    l9() #32

def l33():
    pass
