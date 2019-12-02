data = 84601
amount_needed = data + 10

# part 1
tape = [3, 7]
elf1 = 0
elf2 = 1

while len(tape) < amount_needed:
    val1 = tape[elf1]
    val2 = tape[elf2]
    summed = val1+val2
    if summed >= 10:
        tape.append(summed//10)
        tape.append(summed%10)
    else:
        tape.append(summed)
    elf1 = (1+val1+elf1)%len(tape)
    elf2 = (1+val2+elf2)%len(tape)

last_scores = tape[data:data+10]
print(''.join(map(str, last_scores)))

# part 2
data2 = [0, 8, 4, 6, 0, 1]
len_data2 = len(data2)

tape = [3, 7]
elf1 = 0
elf2 = 1

while True:
    val1 = tape[elf1]
    val2 = tape[elf2]
    summed = val1+val2
    if summed >= 10:
        tape.append(summed//10)
        tape.append(summed%10)
    else:
        tape.append(summed)
    elf1 = (1+val1+elf1)%len(tape)
    elf2 = (1+val2+elf2)%len(tape)

    if tape[-len_data2:] == data2:
        print(len(tape)-len_data2)
        break
    elif tape[-len_data2-1:-1] == data2:
        print(len(tape)-len_data2-1)
        break
