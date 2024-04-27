def goto(offset):
    pass
def toggle(offset):
    pass

a = 12
b = 0
c = 0
d = 0

b = a # 1
b -= 1 # 2
d = a # 3
a = 0 # 4
c = b # 5
a += 1 # 6
c -= 1 # 7
if c != 0:
    goto(-2) # 8
d -= 1 # 9
if d != 0:
    goto(-5) # 10
b -= 1 # 11
c = b # 12
d = c # 13
d -= 1 # 14
c += 1 # 15
if d != 0:
    goto(-2) # 16
toggle(c) # 17
c = -16 # 18
goto(c) # 19
c = 90 # 20
goto(d) # 21
a += 1 # 22
d += 1 # 23
if d != 0:
    goto(-2) # 24
c += 1 # 25
if c != 0:
    goto(-5) # 26
