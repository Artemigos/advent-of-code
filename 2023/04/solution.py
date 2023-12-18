import common

lines = common.read_file().splitlines()

cards = []
for i in range(len(lines)):
    line = lines[i]
    segments = line.split('|')
    winning = set(common.extract_numbers(segments[0])[1:])
    got = set(common.extract_numbers(segments[1]))
    inter = winning.intersection(got)
    cards.append((i+1, len(inter)))

# part 1
sum = 0
for card in cards:
    if card[1] > 0:
        sum += pow(2, card[1]-1)

print(sum)

# part 2
i = 0
while i < len(cards):
    num, count = cards[i]
    for to_copy in cards[num:num+count]:
        cards.append(to_copy)
    i += 1

print(len(cards))
