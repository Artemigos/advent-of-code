import sys
from typing import NamedTuple
import itertools
import queue

class Unit:
    def __init__(self, unit_type: str):
        self.unit_type = unit_type
        self.hp = 200
        self.attack = 3

class Elf(Unit):
    def __init__(self):
        super().__init__('E')

class Goblin(Unit):
    def __init__(self):
        super().__init__('G')

class WorldMap:
    def __init__(self, lines):
        self.h = len(lines)
        self.w = len(lines[0])
        self.board = []
        self.lines = lines

        for y in range(self.h):
            line = lines[y]
            ln = []
            self.board.append(ln)
            for x in range(self.w):
                c = line[x]
                ln.append(c != '#')

    def can_walk_at(self, x, y):
        return self.board[y][x]

class GameState:
    def __init__(self, lines):
        self.map = WorldMap(lines)
        self.elves = self._read_elves(self.map)
        self.goblins = self._read_goblins(self.map)

    def can_walk_at(self, x, y):
        if not self.map.can_walk_at(x, y):
            return False
        if (y, x) in self.elves.keys():
            return False

        if (y, x) in self.goblins.keys():
            return False

        return True

    def move_unit(self, source_pos, target_pos):
        unit = self._pop_unit(source_pos)
        self._push_unit(unit, target_pos)

    def remove_unit(self, source_pos):
        return self._pop_unit(source_pos)

    def try_get_unit(self, source_pos):
        if source_pos in self.elves:
            return self.elves[source_pos]
        elif source_pos in self.goblins:
            return self.goblins[source_pos]
        else:
            return None

    def both_unit_types_exist(self):
        return len(self.elves) > 0 and len(self.goblins) > 0

    def print_state(self):
        for y in range(self.map.h):
            for x in range(self.map.w):
                unit = self.try_get_unit((y, x))
                if unit is not None:
                    print(unit.unit_type, end='')
                elif self.map.can_walk_at(x, y):
                    print('.', end='')
                else:
                    print('#', end='')
            print()

    def _pop_unit(self, pos):
        if pos in self.elves:
            elf = self.elves[pos]
            del self.elves[pos]
            return elf
        elif pos in self.goblins:
            goblin = self.goblins[pos]
            del self.goblins[pos]
            return goblin
        else:
            raise Exception('no unit found at pos')

    def _push_unit(self, unit: Unit, pos):
        if not self.can_walk_at(pos[1], pos[0]):
            raise Exception('cannot walk on pos')

        if unit.unit_type == 'E':
            self.elves[pos] = unit
        else:
            self.goblins[pos] = unit

    @staticmethod
    def _read_elves(m: WorldMap):
        result = {}
        for y in range(m.h):
            for x in range(m.w):
                c = m.lines[y][x]
                if c == 'E':
                    result[y, x] = Elf()
        return result

    @staticmethod
    def _read_goblins(m: WorldMap):
        result = {}
        for y in range(m.h):
            for x in range(m.w):
                c = m.lines[y][x]
                if c == 'G':
                    result[y, x] = Goblin()
        return result

board = 'data'
if len(sys.argv) > 1:
    board = sys.argv[1]

with open(f'2018/15/{board}.txt') as f:
    data = f.read()

lines = data.splitlines()
state = GameState(lines)

def iter_units():
    seen = set()
    for y in range(state.map.h):
        for x in range(state.map.h):
            unit = state.try_get_unit((y, x))
            if unit is not None and unit not in seen:
                seen.add(unit)
                yield unit, (y, x)

def find_target(unit: Unit, pos):
    def get_neighbors(pos):
        y, x = pos
        return [
            (y-1, x),
            (y, x-1),
            (y, x+1),
            (y+1, x)
        ]
    def create_paths(start_path, steps):
        for s in steps:
            base = list(start_path)
            base.append(s)
            yield base
    seen = set()
    q = queue.deque([[pos]])
    target_type = 'G' if unit.unit_type == 'E' else 'E'

    while len(q) > 0:
        path = q.popleft()
        last_pos = path[-1]
        y, x = last_pos
        if last_pos in seen:
            continue
        if len(path) > 1 and not state.can_walk_at(x, y):
            continue
        seen.add(last_pos)
        neighbors = get_neighbors(last_pos)
        for n in neighbors:
            found_unit = state.try_get_unit(n)
            if found_unit is not None and found_unit.unit_type == target_type:
                path.append(n)
                path = path[1:]
                return found_unit, path
        for p in create_paths(path, neighbors):
            q.append(p)

    return None, None

rnd = 0
while state.both_unit_types_exist():
    for unit, pos in iter_units():
        if not state.both_unit_types_exist():
            break
        target, path = find_target(unit, pos)
        if target is not None:
            if len(path) > 1:
                state.move_unit(pos, path[0])
            if len(path) <= 2:
                target.hp -= unit.attack
                if target.hp <= 0:
                    state.remove_unit(path[-1])
        # state.print_state()
    else:
        rnd += 1

state.print_state()
elves_hp = sum(map(lambda x: x.hp, state.elves.values()))
goblins_hp = sum(map(lambda x: x.hp, state.goblins.values()))
sum_hp = elves_hp + goblins_hp

print(rnd, sum_hp, rnd*sum_hp)
