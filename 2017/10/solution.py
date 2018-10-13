import itertools

data = [192,69,168,160,78,1,166,28,0,83,198,2,254,255,41,12]
string = list(range(256))

skip = 0
pos = 0

def inc_pos(amount):
    global pos
    pos += amount
    while pos >= len(string):
        pos -= len(string)

for l in data:
    start_pos = pos
    elements = list()
    for i in range(l):
        elements.append(string[pos])
        inc_pos(1)
    elements.reverse()
    pos = start_pos
    for i in range(l):
        string[pos] = elements[i]
        inc_pos(1)
    inc_pos(skip)
    skip += 1

print(string[0] * string[1])
