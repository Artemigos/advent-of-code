a = 12
b = a-1

while True:
    a *= b
    b -= 1
    if b == 1:
        break

a += 90*90
print(a)
