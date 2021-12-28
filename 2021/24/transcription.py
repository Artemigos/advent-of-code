def run(data: list):
    stack = []

    stack.append(data[0]+4)         # +1
    stack.append(data[1]+16)        # +2
    stack.append(data[2]+14)        # +3

    x = stack.pop()-13              # -3
    if x != data[3]:
        stack.append(data[3]+3)     # want to skip

    stack.append(data[4]+11)        # +3
    stack.append(data[5]+13)        # +4

    x = stack.pop()-7               # -4
    if x != data[6]:
        stack.append(data[6]+11)    # want to skip

    stack.append(data[7]+7)         # +4

    x = stack.pop()-12              # -4
    if x != data[8]:
        stack.append(data[8]+12)    # want to skip

    stack.append(data[9]+15)        # +4

    x = stack.pop()-16              # -4
    if x != data[10]:
        stack.append(data[10]+13)   # want to skip

    x = stack.pop()-9               # -3
    if x != data[11]:
        stack.append(data[11]+1)    # want to skip

    x = stack.pop()-8               # -2
    if x != data[12]:
        stack.append(data[12]+15)   # want to skip

    x = stack.pop()-8               # -1 - balanced, everything must be skipped
    if x != data[13]:
        stack.append(data[13]+4)

    acc = 0
    for i in range(len(stack)):
        acc *= 26
        acc += stack[i]
    return acc