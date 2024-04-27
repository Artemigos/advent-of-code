from collections import deque
import common

deck1 = common.to_int(common.read_file('2020/22/p1.txt').splitlines())
deck2 = common.to_int(common.read_file('2020/22/p2.txt').splitlines())

# part 1
p1 = deque(deck1)
p2 = deque(deck2)

while len(p1) > 0 and len(p2) > 0:
    play1 = p1.popleft()
    play2 = p2.popleft()

    if play1 > play2:
        p1.append(play1)
        p1.append(play2)
    else:
        p2.append(play2)
        p2.append(play1)

winner = p1 if len(p1) > 0 else p2

def calculate_score(cards):
    acc = 0
    for i in range(len(cards)):
        acc += cards[-i-1] * (i+1)
    return acc

print(calculate_score(winner))

# part 2
def play_rec_game(p1, p2):
    p1 = deque(p1)
    p2 = deque(p2)
    seen = set()

    while len(p1) > 0 and len(p2) > 0:
        state = tuple(p1), tuple(p2)
        if state in seen:
            return p1, p2, 1
        seen.add(state)

        play1 = p1.popleft()
        play2 = p2.popleft()

        if len(p1) >= play1 and len(p2) >= play2:
            _, _, winner = play_rec_game(list(p1)[:play1], list(p2)[:play2])
        else:
            winner = 1 if play1 > play2 else 2

        if winner == 1:
            p1.append(play1)
            p1.append(play2)
        else:
            p2.append(play2)
            p2.append(play1)

    return p1, p2, 1 if len(p2) == 0 else 2

p1, p2, winner = play_rec_game(deck1, deck2)
winner = p1 if winner == 1 else p2
print(calculate_score(winner))
