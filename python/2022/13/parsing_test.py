with open('2022/13/data.txt') as f:
    lines = f.read().splitlines()

def parse(input):
    if input[0] == '[':
        input = input[1:]
        items = []
        while input[0] != ']':
            if input[0] == ',':
                input = input[1:]
            val, input = parse(input)
            items.append(val)
        return items, input[1:]
    for i in range(len(input)):
        if not input[i].isdigit():
            break
    return int(input[:i]), input[i:]

for line in lines:
    if line == '':
        continue

    l1 = eval(line)
    l2, _ = parse(line)
    assert l1 == l2

print('ok')
