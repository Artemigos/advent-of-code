import queue
import common

# data
lines = common.read_file().splitlines()
state = lines[0][-2]
steps = common.extract_numbers(lines[1])[0]
blueprint = {}

for i in range(3, len(lines), 10):
    st = lines[i][-2]
    def read_points(i: int) -> tuple[int, int, str]:
        w = common.extract_numbers(lines[i])[0]
        m = -1 if 'left' in lines[i+1] else 1
        n = lines[i+2][-2]
        return (w, m, n)
    p0 = read_points(i+2)
    p1 = read_points(i+6)
    blueprint[st] = [p0, p1]

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
