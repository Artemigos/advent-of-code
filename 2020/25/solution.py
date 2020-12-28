SUBJECT_NUM = 7
MOD_NUM = 20201227
PUB1 = 12092626
PUB2 = 4707356
LOOP_SIZE1 = 0
LOOP_SIZE2 = 0

found1 = False
found2 = False
acc = 1

while not found1 or not found2:
    acc *= SUBJECT_NUM
    acc %= MOD_NUM

    if not found1:
        LOOP_SIZE1 += 1
        if acc == PUB1:
            found1 = True

    if not found2:
        LOOP_SIZE2 += 1
        if acc == PUB2:
            found2 = True

acc = 1
for _ in range(LOOP_SIZE2):
    acc *= PUB1
    acc %= MOD_NUM

print(acc)
