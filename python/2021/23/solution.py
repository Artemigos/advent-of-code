from dataclasses import dataclass, field
from queue import PriorityQueue
from typing import Any
import common

board = common.read_file().splitlines()
ROOMS_COUNT = 4
HALLWAY_LEN = len(list(filter(lambda x: x == '.', board[1]))) - ROOMS_COUNT

costs = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000,
}

# part 1

def available_moves(hallway, rooms):
    moves = []
    for room_i in range(len(rooms)):
        room = rooms[room_i]
        expected_c = chr(ord('A')+room_i)
        for i in range(len(room)):
            if room[i] is not None:
                if any(filter(lambda x: x != expected_c, room[i:])):
                    break
        else:
            continue
        hallway_start = room_i+1
        for hallway_i in range(hallway_start, -1, -1):
            if hallway[hallway_i] is not None:
                break
            move_len = i+2
            moved_across = hallway_start-hallway_i
            move_len += min(room_i, moved_across)
            move_len += moved_across
            cost = move_len*costs[room[i]]
            moves.append(('out', room_i, i, hallway_i, cost))
        hallway_start = room_i+2
        for hallway_i in range(hallway_start, len(hallway)):
            if hallway[hallway_i] is not None:
                break
            move_len = i+2
            moved_across = hallway_i-hallway_start
            move_len += min(len(rooms)-room_i-1, moved_across)
            move_len += moved_across
            cost = move_len*costs[room[i]]
            moves.append(('out', room_i, i, hallway_i, cost))
    for hallway_i in range(len(hallway)):
        el = hallway[hallway_i]
        if el is None:
            continue
        room_i = ord(el)-ord('A')
        room = rooms[room_i]
        if room[0] is not None:
            continue
        last_empty = 0
        for i in range(len(room)):
            if room[i] is None:
                last_empty = i
            elif room[i] != el:
                break
        else:
            move_len = 2+last_empty
            cost = move_len*costs[el]
            if hallway_i in [room_i+1, room_i+2]:
                moves.append(('in', hallway_i, room_i, last_empty, cost))
            elif hallway_i < room_i+1:
                moved_across = room_i+1-hallway_i
                move_len += moved_across
                move_len += min(room_i, moved_across)
                cost = move_len*costs[el]
                for i in range(hallway_i+1, room_i+2):
                    if hallway[i] is not None:
                        break
                else:
                    moves.append(('in', hallway_i, room_i, last_empty, cost))
            else: # to the right
                moved_across = hallway_i-(room_i+2)
                move_len += moved_across
                move_len += min(len(rooms)-room_i-1, moved_across)
                cost = move_len*costs[el]
                for i in range(room_i+2, hallway_i):
                    if hallway[i] is not None:
                        break
                else:
                    moves.append(('in', hallway_i, room_i, last_empty, cost))
    return moves

def splice(source, i, item):
    return source[:i] + [item] + source[i+1:]

@dataclass(order=True)
class PrioritizedItem:
    dist: int
    hallway: Any=field(compare=False)
    rooms: Any=field(compare=False)

def solve(rooms):
    hallway = [None]*HALLWAY_LEN
    seen = {}
    q = PriorityQueue()
    q.put(PrioritizedItem(0, hallway, rooms))
    while not q.empty():
        item = q.get()
        dist = item.dist
        hallway = item.hallway
        rooms = item.rooms
        k = tuple(hallway), tuple(map(tuple, rooms))
        if k in seen and seen[k] <= dist:
            continue
        seen[k] = dist
        for room_i in range(len(rooms)):
            c = chr(ord('A')+room_i)
            for el in rooms[room_i]:
                if el != c:
                    break
            else:
                continue
            break
        else:
            return dist
        moves = available_moves(hallway, rooms)
        for move in moves:
            if move[0] == 'out':
                _, room_i, i, hallway_i, cost = move
                room = rooms[room_i]
                item = room[i]
                new_room = splice(room, i, None)
                new_rooms = splice(rooms, room_i, new_room)
                new_hallway = splice(hallway, hallway_i, item)
                q.put(PrioritizedItem(dist+cost, new_hallway, new_rooms))
            else:
                _, hallway_i, room_i, i, cost = move
                item = hallway[hallway_i]
                new_hallway = splice(hallway, hallway_i, None)
                room = rooms[room_i]
                new_room = splice(room, i, item)
                new_rooms = splice(rooms, room_i, new_room)
                q.put(PrioritizedItem(dist+cost, new_hallway, new_rooms))

board_rooms = []
for i in range(ROOMS_COUNT):
    board_rooms.append([])
for line in board[2:4]:
    idx = 0
    for c in line:
        if c != ' ' and c != '#':
            board_rooms[idx].append(c)
            idx += 1

print(solve(board_rooms))

# part 2
board_rooms[0].insert(1, 'D')
board_rooms[0].insert(2, 'D')
board_rooms[1].insert(1, 'C')
board_rooms[1].insert(2, 'B')
board_rooms[2].insert(1, 'B')
board_rooms[2].insert(2, 'A')
board_rooms[3].insert(1, 'A')
board_rooms[3].insert(2, 'C')
print(solve(board_rooms))
