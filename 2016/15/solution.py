data = [
    (13, 11),
    (5, 0),
    (17, 11),
    (3, 0),
    (7, 2),
    (19, 17),
    (11, 0) # part 2
]

status = list(data)

# time offset alignment
for i in range(len(status)):
    curr = status[i]
    status[i] = curr[0], (curr[1]+i+1)%curr[0]

max_loop = status[5]
time = 0

def offset(amount=max_loop[0]):
    global time
    time += amount
    for i in range(len(status)):
        curr = status[i]
        status[i] = curr[0], (curr[1]+amount)%curr[0]

offset(max_loop[0]-max_loop[1])

def is_aligned_at_zero():
    return all(map(lambda x: x[1] == 0, status))

while not is_aligned_at_zero():
    offset()

print(time)
