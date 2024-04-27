import queue

# data
state = 'A'
steps = 12399302
blueprint = dict(
    A=[
        (1, 1, 'B'),
        (0, 1, 'C')
    ],
    B=[
        (0, -1, 'A'),
        (0, 1, 'D')
    ],
    C=[
        (1, 1, 'D'),
        (1, 1, 'A')
    ],
    D=[
        (1, -1, 'E'),
        (0, -1, 'D')
    ],
    E=[
        (1, 1, 'F'),
        (1, -1, 'B')
    ],
    F=[
        (1, 1, 'A'),
        (1, 1, 'E')
    ]
)

tape = queue.deque([0])
pos = 0
for i in range(steps):
    tape[pos], mov, state = blueprint[state][tape[pos]]
    pos += mov
    if pos == -1:
        tape.appendleft(0)
        pos = 0
    elif pos == len(tape):
        tape.append(0)

print(sum(tape))
