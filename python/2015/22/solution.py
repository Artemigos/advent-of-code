import queue

boss = (55, 8) # hp, dmg
player = (50, 500, 0) # hp, mana, armor
state = (player, boss, True, 0, 0, 0, 0) # player, boss, player's turn, shield turns left, poison turns left, recharge turns left, mana spent

def magic_missile(state):
    mana = state[0][1]
    if mana < 53:
        return None
    return ((state[0][0], mana-53, state[0][2]), (state[1][0]-4, state[1][1]), False, state[3], state[4], state[5], state[6]+53)

def drain(state):
    mana = state[0][1]
    if mana < 73:
        return None
    return ((state[0][0]+2, mana-73, state[0][2]), state[1], False, state[3], state[4], state[5], state[6]+73)

def shield(state):
    mana = state[0][1]
    if mana < 113:
        return None
    if state[3] > 0:
        return None
    return ((state[0][0], mana-113, state[0][2]), state[1], False, 6, state[4], state[5], state[6]+113)

def poison(state):
    mana = state[0][1]
    if mana < 173:
        return None
    if state[4] > 0:
        return None
    return ((state[0][0], mana-173, state[0][2]), state[1], False, state[3], 6, state[5], state[6]+173)

def recharge(state):
    mana = state[0][1]
    if mana < 229:
        return None
    if state[5] > 0:
        return None
    return ((state[0][0], mana-229, state[0][2]), state[1], False, state[3], state[4], 5, state[6]+229)

spells = [magic_missile, drain, shield, poison, recharge]

def apply_effects(state):
    player, boss, players_turn, shield_turns, poison_turns, recharge_turns, mana_spent = state
    if shield_turns > 0:
        player = player[0], player[1], 7
        shield_turns -= 1
    else:
        player = player[0], player[1], 0
    if poison_turns > 0:
        boss = boss[0]-3, boss[1]
        poison_turns -= 1
    if recharge_turns > 0:
        player = player[0], player[1]+101, player[2]
        recharge_turns -= 1

    return player, boss, players_turn, shield_turns, poison_turns, recharge_turns, mana_spent

def boss_attack(state):
    dmg = max([state[1][1]-state[0][2], 1])
    return ((state[0][0]-dmg, state[0][1], state[0][2]), state[1], True, *state[3:])

def do_the_solve(state, part2):
    q = queue.deque([state])
    min_winning_spent = None
    while len(q) > 0:
        state = q.popleft()
        player, boss, players_turn, shield_turns, poison_turns, recharge_turns, mana_spent = state
        boss_hp, boss_dmg = boss
        player_hp, player_mana, player_armor = player

        if min_winning_spent is not None and mana_spent >= min_winning_spent:
            continue

        if boss_hp <= 0:
            min_winning_spent = mana_spent
            continue

        if part2:
            # part 2 - comment out for part 1 solution
            if players_turn:
                player_hp -= 1
                state = (player_hp, player_mana, player_armor), boss, players_turn, shield_turns, poison_turns, recharge_turns, mana_spent
            # end of part 2

        if player_hp <= 0:
            continue

        state = apply_effects(state)
        if players_turn:
            moves = [spell(state) for spell in spells]
            for move in moves:
                if move is not None:
                    q.append(move)
        else:
            q.append(boss_attack(state))

    print(min_winning_spent)

do_the_solve(state, False)
do_the_solve(state, True)
