import itertools

data = [192,69,168,160,78,1,166,28,0,83,198,2,254,255,41,12]
string = list(range(256))
print(string)

skip = 0
pos = 0

def roller():
    i = 0
    while True:
        yield string[i]
        i += 1
        if i >= 256:
            i = 0

string_gen = roller()

for l in data:
    elements = list(itertools.islice(string_gen, l))
    elements.reverse()
    for i in range(l):
        string[pos] = elements[i]
        pos += 1
        if pos >= 256:
            pos = 0
    pos += skip
    skip += 1
    while pos >= 256:
        pos -= 256
    print(string)

# TODO: result wasn't accepted
print(string[0] * string[1])
