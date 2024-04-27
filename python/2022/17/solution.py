import common

jet = [ord(c)-61 for c in common.read_file().strip()]

def gen_check(pixels):
    pixels = [f'(x+({p[0]}),y+({p[1]})) in board' for p in pixels]
    return ' or '.join(pixels)

def gen_fun(pixels, pre_check):
    pcheck = gen_check(pixels)
    s = f'def _f(board, x, y): return not (({pre_check}) or ({pcheck}))'
    exec(s)
    return locals()['_f']

class Rock:
    def __init__(self, pixels):
        self.pixels = pixels
        self.top_point = max(pixels, key=lambda x: x[1])
        right_point = max(pixels, key=lambda x: x[0])
        self.start_x = 3
        self.start_dy = 4
        self.min_x = 1
        self.max_x = 7 - right_point[0]
        self.min_y = 1
        self.test_pos = gen_fun(
                pixels,
                f'x < {self.min_x} or x > {self.max_x} or y < {self.min_y}')
    def spawn_point(self, highest_point):
        return (self.start_x, highest_point+self.start_dy)
    def move_left(self, board, x, y):
        new_x = x - 1
        if new_x < self.min_x or new_x > self.max_x:
            return False
        for p in self.pixels:
            if (new_x+p[0], y+p[1]) in board:
                return False
        return True
    def move_right(self, board, x, y):
        new_x = x + 1
        if new_x < self.min_x or new_x > self.max_x:
            return False
        for p in self.pixels:
            if (new_x+p[0], y+p[1]) in board:
                return False
        return True
    def move_down(self, board, x, y):
        new_y = y - 1
        if new_y < self.min_y:
            return False
        for p in self.pixels:
            if (x+p[0], new_y+p[1]) in board:
                return False
        return True
    def get_top_y(self, y):
        return y+self.top_point[1]
    def test_pos_(self, board, x, y):
        if x < self.min_x or x > self.max_x:
            return False
        if y < self.min_y:
            return False
        for p in self.pixels:
            if (x+p[0], y+p[1]) in board:
                return False
        return True

rocks = [
    Rock([(0, 0), (1, 0), (2, 0), (3, 0)]),
    Rock([(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)]),
    Rock([(2, 2), (2, 1), (0, 0), (1, 0), (2, 0)]),
    Rock([(0, 0), (0, 1), (0, 2), (0, 3)]),
    Rock([(0, 0), (1, 0), (0, 1), (1, 1)]),
]

def simulate(moves):
    ji = 0
    highest = 0
    board = set()
    seen = dict()
    jumped = 0

    for i in range(moves):
        if i+jumped >= moves:
            break

        ri = i%len(rocks)

        # cycle detection
        if jumped == 0:
            k = (ri, ji)
            if k in seen:
                prev = seen[k][-1]
                dh = highest - prev[0]
                di = i - prev[2]
                if prev[1] == dh and prev[3] == di: # cycle detected - move up
                    remaining_moves = moves-i-1
                    loops = remaining_moves//di
                    gained_h = loops*dh
                    jumped = loops*di
                    highest += gained_h
                    new_board = set()
                    for x, y in board:
                        new_board.add((x, y+gained_h))
                    board = new_board
                seen[k].append((highest, dh, i, di))
            else:
                seen[k] = [(highest, highest, i, i)]

        rock = rocks[ri]
        x, y = rock.spawn_point(highest)

        while True:
            jet_move = jet[ji]
            ji += 1
            ji %= len(jet)

            if rock.test_pos(board, x+jet_move, y):
                x += jet_move

            if rock.test_pos(board, x, y-1):
                y -= 1
            else:
                highest = max(highest, rock.get_top_y(y))
                for p in rock.pixels:
                    board.add((x+p[0], y+p[1]))
                break

    print(highest)

# part 1
simulate(2022)

# part 2
simulate(1000000000000)
