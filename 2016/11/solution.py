import queue

def create_state_hash(e, sg, sm, pg, pm, tg, tm, rg, rm, cg, cm):
    return (e << 0) + \
        (sg << 2) + \
        (sm << 4) + \
        (pg << 6) + \
        (pm << 8) + \
        (tg << 10) + \
        (tm << 12) + \
        (rg << 14) + \
        (rm << 16) + \
        (cg << 18) + \
        (cm << 20)

target = create_state_hash(3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3)
state = [0, 0, 0, 0, 0, 1, 2, 1, 1, 1, 1]

def is_state_valid(state):
    if state[2] != state[1] and (state[2] == state[3] or state[2] == state[5] or state[2] == state[7] or state[2] == state[9]):
        return False
    if state[4] != state[3] and (state[4] == state[1] or state[4] == state[5] or state[4] == state[7] or state[4] == state[9]):
        return False
    if state[6] != state[5] and (state[6] == state[3] or state[6] == state[1] or state[6] == state[7] or state[6] == state[9]):
        return False
    if state[8] != state[7] and (state[8] == state[3] or state[8] == state[5] or state[8] == state[1] or state[8] == state[9]):
        return False
    if state[10] != state[9] and (state[10] == state[3] or state[10] == state[5] or state[10] == state[7] or state[10] == state[1]):
        return False
    return True

seen_states = set()
move_queue = queue.deque([(0, state)])

div = (1 << 22) / 100

while len(move_queue) > 0:
    deepness, move = move_queue.popleft()
    move_hash = create_state_hash(*move)
    if move_hash == target:
        print('found path with deepness', deepness, '; move:', move)
        break
    if move_hash in seen_states:
        continue
    seen_states.add(move_hash)
    if len(seen_states)%20000 == 0:
        print(len(seen_states) / div, '%')
    if not is_state_valid(move):
        continue
    elevator = move[0]
    for a in range(1, 11):
        for b in range(1, 11):
            if a != b and move[a] == elevator and move[b] == elevator:
                if elevator > 0:
                    new_move = list(move)
                    new_move[0] = elevator-1
                    new_move[a] = elevator-1
                    new_move[b] = elevator-1
                    move_queue.append((deepness+1, new_move))
                if elevator < 3:
                    new_move = list(move)
                    new_move[0] = elevator+1
                    new_move[a] = elevator+1
                    new_move[b] = elevator+1
                    move_queue.append((deepness+1, new_move))
        if move[a] == elevator:
            if elevator > 0:
                new_move = list(move)
                new_move[0] = elevator-1
                new_move[a] = elevator-1
                move_queue.append((deepness+1, new_move))
            if elevator < 3:
                new_move = list(move)
                new_move[0] = elevator+1
                new_move[a] = elevator+1
                move_queue.append((deepness+1, new_move))

print(len(seen_states))
