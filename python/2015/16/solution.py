import common

lines = common.read_file().splitlines()

target = dict(
    children=3,
    cats=7,
    samoyeds=2,
    pomeranians=3,
    akitas=0,
    vizslas=0,
    goldfish=5,
    trees=3,
    cars=2,
    perfumes=1
)

# part 1
for line in lines:
    segments = line.split()
    num = int(segments[1][:-1])
    known_compunds_num = int((len(segments)-2)/2)
    for i in range(known_compunds_num):
        name = segments[2+i*2][:-1]
        amount = int(segments[3+i*2].rstrip(','))
        if target[name] != amount:
            break
    else:
        print(num)

# part 2
for line in lines:
    segments = line.split()
    num = int(segments[1][:-1])
    known_compunds_num = int((len(segments)-2)/2)
    for i in range(known_compunds_num):
        name = segments[2+i*2][:-1]
        amount = int(segments[3+i*2].rstrip(','))
        if name == 'cats' or name == 'trees':
            if amount <= target[name]:
                break
        elif name == 'pomeranians' or name == 'goldfish':
            if amount >= target[name]:
                break
        elif target[name] != amount:
            break
    else:
        print(num)
