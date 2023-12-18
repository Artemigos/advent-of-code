import common

lines = common.read_file().splitlines()

HIGH_CARD = 1
PAIR = 2
TWO_PAIRS = 3
THREE = 4
FULL_HOUSE = 5
FOUR = 6
FIVE = 7

CARD_MAP = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14,
}

# part 1
hands = []

def parse_hand(hand: str, bid: int):
    clumps = []
    prev_c = ''
    curr_size = 0
    for c in sorted(hand):
        if c != prev_c:
            if prev_c != '':
                clumps.append((curr_size, prev_c))
            prev_c = c
            curr_size = 1
        else:
            curr_size += 1
    clumps.append((curr_size, prev_c))
    clumps = list(reversed(sorted(clumps)))

    if clumps[0][0] == 5:
        hand_str = FIVE
    elif clumps[0][0] == 4:
        hand_str = FOUR
    elif clumps[0][0] == 3:
        if clumps[1][0] == 2:
            hand_str = FULL_HOUSE
        else:
            hand_str = THREE
    elif clumps[0][0] == 2:
        if clumps[1][0] == 2:
            hand_str = TWO_PAIRS
        else:
            hand_str = PAIR
    else:
        hand_str = HIGH_CARD

    cards_str = tuple(map(lambda x: CARD_MAP[x], hand))
    return (hand_str, cards_str, hand, bid, clumps)

for line in lines:
    segments = line.split(' ')
    hand = segments[0]
    bid = int(segments[1])
    hands.append(parse_hand(hand, bid))

by_str = list(sorted(hands))
acc = 0
for i in range(len(by_str)):
    rank = i + 1
    bid = by_str[i][3]
    acc += rank * bid

print(acc)

# part 2
CARD_MAP['J'] = 0
hands = []
for line in lines:
    segments = line.split(' ')
    hand = segments[0]
    bid = int(segments[1])
    clumps = []
    prev_c = ''
    curr_size = 0
    for c in sorted(hand):
        if c != prev_c:
            if prev_c != '':
                clumps.append((curr_size, prev_c))
            prev_c = c
            curr_size = 1
        else:
            curr_size += 1
    clumps.append((curr_size, prev_c))
    clumps = list(reversed(sorted(clumps)))

    # joker handling
    joker_clump = None
    for cl in clumps:
        if cl[1] == 'J':
            joker_clump = cl
            break
    if joker_clump is not None and len(clumps) > 1:
        clumps.remove(joker_clump)
        big_cl = clumps[0]
        clumps[0] = (big_cl[0] + joker_clump[0], big_cl[1])

    if clumps[0][0] == 5:
        hand_str = FIVE
    elif clumps[0][0] == 4:
        hand_str = FOUR
    elif clumps[0][0] == 3:
        if clumps[1][0] == 2:
            hand_str = FULL_HOUSE
        else:
            hand_str = THREE
    elif clumps[0][0] == 2:
        if clumps[1][0] == 2:
            hand_str = TWO_PAIRS
        else:
            hand_str = PAIR
    else:
        hand_str = HIGH_CARD

    cards_str = tuple(map(lambda x: CARD_MAP[x], hand))
    hands.append((hand_str, cards_str, hand, bid, clumps))

by_str = list(sorted(hands))
acc = 0
for i in range(len(by_str)):
    rank = i + 1
    bid = by_str[i][3]
    acc += rank * bid

print(acc)
