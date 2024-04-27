from collections import Counter, defaultdict

p1_start = 3
p2_start = 4

# part 1

rolls = 0
def roll():
    global rolls
    rolls += 1
    return ((rolls-1)%100)+1

p1 = p1_start
p2 = p2_start
p1_points = 0
p2_points = 0

while True:
    p1 += roll()+roll()+roll()
    p1 %= 10
    p1_points += p1+1
    if p1_points >= 1000:
        losing_points = p2_points
        break

    p2 += roll()+roll()+roll()
    p2 %= 10
    p2_points += p2+1
    if p2_points >= 1000:
        losing_points = p1_points
        break

print(rolls*losing_points)

# part 2

triple_roll = Counter()
for i in range(1, 4):
    for j in range(1, 4):
        for k in range(1, 4):
            triple_roll[i+j+k] += 1

ways_to_reach_21 = defaultdict(lambda: (0, 0))
def find_ways_to_reach_21(p1, p2, p1_points, p2_points, p_to_move):
    k = (p1, p2, p1_points, p2_points, p_to_move)
    if k in ways_to_reach_21:
        return ways_to_reach_21[k]
    for roll in triple_roll:
        if p_to_move == 1:
            p1_new = (p1+roll)%10
            p1_new_points = p1_points+p1_new+1
            stored_p1_wins, stored_p2_wins = ways_to_reach_21[k]
            if p1_new_points >= 21:
                ways_to_reach_21[k] = (stored_p1_wins+triple_roll[roll], stored_p2_wins)
            else:
                lower_p1_wins, lower_p2_wins = find_ways_to_reach_21(p1_new, p2, p1_new_points, p2_points, 2)
                ways_to_reach_21[k] = (triple_roll[roll]*lower_p1_wins+stored_p1_wins, triple_roll[roll]*lower_p2_wins+stored_p2_wins)
        else:
            p2_new = (p2+roll)%10
            p2_new_points = p2_points+p2_new+1
            stored_p1_wins, stored_p2_wins = ways_to_reach_21[k]
            if p2_new_points >= 21:
                ways_to_reach_21[k] = (stored_p1_wins, stored_p2_wins+triple_roll[roll])
            else:
                lower_p1_wins, lower_p2_wins = find_ways_to_reach_21(p1, p2_new, p1_points, p2_new_points, 1)
                ways_to_reach_21[k] = (triple_roll[roll]*lower_p1_wins+stored_p1_wins, triple_roll[roll]*lower_p2_wins+stored_p2_wins)
    return ways_to_reach_21[k]

print(max(find_ways_to_reach_21(p1_start, p2_start, 0, 0, 1)))
