boss = dict(
    hp = 109,
    dmg = 8,
    armor = 2
)

player = dict(
    hp = 100,
    dmg = 0,
    armor = 0
)

weapon_choices = [
    (8, 4, 0),
    (10, 5, 0),
    (25, 6, 0),
    (40, 7, 0),
    (74, 8, 0)
]

armor_choices = [
    (0, 0, 0),
    (13, 0, 1),
    (31, 0, 2),
    (53, 0, 3),
    (75, 0, 4),
    (102, 0, 5)
]

ring_choices = [
    (0, 0, 0),
    (0, 0, 0),
    (25, 1, 0),
    (50, 2, 0),
    (100, 3, 0),
    (20, 0, 1),
    (40, 0, 2),
    (80, 0, 3)
]

def calc_win(iw, ia, ir1, ir2):
    player_dmg = max([weapon_choices[iw][1] + ring_choices[ir1][1] + ring_choices[ir2][1] - boss['armor'], 1])
    player_armor = armor_choices[ia][2] + ring_choices[ir1][2] + ring_choices[ir2][2]
    boss_dmg = max([boss['dmg'] - player_armor, 1])

    player_hp = player['hp']
    boss_hp = boss['hp']
    while True:
        player_hp -= boss_dmg
        boss_hp -= player_dmg
        if boss_hp <= 0:
            return True
        if player_hp <= 0:
            return False

min_cost = None
max_cost = 0
for iw in range(len(weapon_choices)):
    for ia in range(len(armor_choices)):
        for ir1 in range(len(ring_choices)):
            for ir2 in range(len(ring_choices)):
                if ir1 == ir2:
                    continue
                cost = weapon_choices[iw][0] + armor_choices[ia][0] + ring_choices[ir1][0] + ring_choices[ir2][0]
                if calc_win(iw, ia, ir1, ir2):
                    if min_cost is None or cost < min_cost:
                        min_cost = cost
                else:
                    if cost > max_cost:
                        max_cost = cost

print(min_cost)
print(max_cost)
