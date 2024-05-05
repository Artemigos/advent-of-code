import queue
import common

class Unit:
    def __init__(self, unit_type: str, power=3):
        self.unit_type = unit_type
        self.hp = 200
        self.attack = power

class Elf(Unit):
    def __init__(self, power):
        super().__init__('E', power)

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
    def __init__(self, lines, elf_power):
        self.map = WorldMap(lines)
        self.elves = self._read_elves(self.map, elf_power)
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
    def _read_elves(m: WorldMap, elf_power):
        result = {}
        for y in range(m.h):
            for x in range(m.w):
                c = m.lines[y][x]
                if c == 'E':
                    result[y, x] = Elf(elf_power)
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

lines = common.read_file().splitlines()
state: GameState = None

def iter_units():
    seen = set()
    for y in range(state.map.h):
        for x in range(state.map.h):
            unit = state.try_get_unit((y, x))
            if unit is not None and unit not in seen:
                seen.add(unit)
                yield unit, (y, x)

def get_neighbors(pos):
    y, x = pos
    return [
        (y-1, x),
        (y, x-1),
        (y, x+1),
        (y+1, x)
    ]

def find_move_target(unit: Unit, pos):
    def create_paths(start_path, steps):
        for s in steps:
            base = list(start_path)
            base.append(s)
            yield base
    seen = set()
    q = queue.deque([[pos]])
    target_type = 'G' if unit.unit_type == 'E' else 'E'
    found = []

    while len(q) > 0:
        path = q.popleft()
        last_pos = path[-1]
        y, x = last_pos
        if last_pos in seen:
            continue
        if len(path) > 1 and not state.can_walk_at(x, y):
            continue
        if len(found) > 0 and len(path) > len(found[0][1]):
            continue
        seen.add(last_pos)
        neighbors = get_neighbors(last_pos)
        for n in neighbors:
            found_unit = state.try_get_unit(n)
            if found_unit is not None and found_unit.unit_type == target_type:
                cp = path[1:]
                cp.append(n)
                found.append((found_unit, cp))
        for p in create_paths(path, neighbors):
            q.append(p)

    if len(found) > 0:
        return min(found, key=lambda x: x[1][-1])

    return None, None

def find_attack_target(unit, pos):
    target_type = 'G' if unit.unit_type == 'E' else 'E'
    min_hp = 300
    min_unit = None
    min_pos = None
    for n in get_neighbors(pos):
        unit = state.try_get_unit(n)
        if unit is not None and unit.unit_type == target_type and unit.hp < min_hp:
            min_hp = unit.hp
            min_unit = unit
            min_pos = n
    return min_unit, min_pos

def play(elf_attack_powah=3):
    global state
    state = GameState(lines, elf_attack_powah)
    rnd = 0
    while state.both_unit_types_exist():
        for unit, pos in iter_units():
            if not state.both_unit_types_exist():
                break
            curr_pos = pos
            target, path = find_move_target(unit, pos)
            if target is not None:
                if len(path) > 1:
                    state.move_unit(pos, path[0])
                    curr_pos = path[0]
                if len(path) <= 2:
                    target, target_pos = find_attack_target(unit, curr_pos)
                    target.hp -= unit.attack
                    if target.hp <= 0:
                        state.remove_unit(target_pos)
            # state.print_state()
        else:
            rnd += 1

    # state.print_state()
    elves_hp = sum(map(lambda x: x.hp, state.elves.values()))
    goblins_hp = sum(map(lambda x: x.hp, state.goblins.values()))
    sum_hp = elves_hp + goblins_hp

    return rnd*sum_hp

# part 1
print(play())

# part 2
elves_before = 0
for l in lines:
    elves_before += sum(map(lambda x: 1 if x == 'E' else 0, l))

atk = 3
while True:
    atk += 1
    r = play(atk)
    if len(state.elves) == elves_before:
        break
    # else:
    #     print('elves left:', len(state.elves))
print(r)
