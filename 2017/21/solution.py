import common
import numpy as np

data = common.read_file('2017/21/data.txt')
lines = data.splitlines()
repetitions = 5  # part 1
repetitions = 18  # part 2


def parse_rule(rule):
    segments = rule.split(' ')
    pattern_lines = segments[0].split('/')
    result_lines = segments[2].split('/')

    def interpret_characters(lines):
        return [
            [1 if x == '#' else 0 for x in line]
            for line in lines
        ]

    pattern_lines = interpret_characters(pattern_lines)
    result_lines = interpret_characters(result_lines)
    return len(pattern_lines), np.array(pattern_lines), np.array(result_lines)


all_rules = [parse_rule(x) for x in lines]


def transform_rules(rules):
    for rule in rules:
        yield rule
        rot = np.rot90(rule[1])
        yield (rule[0], rot, rule[2])
        rot = np.rot90(rot)
        yield (rule[0], rot, rule[2])
        rot = np.rot90(rot)
        yield (rule[0], rot, rule[2])
        flipped = np.fliplr(rule[1])
        yield (rule[0], flipped, rule[2])
        rot = np.rot90(flipped)
        yield (rule[0], rot, rule[2])
        rot = np.rot90(rot)
        yield (rule[0], rot, rule[2])
        rot = np.rot90(rot)
        yield (rule[0], rot, rule[2])


all_rules = list(transform_rules(all_rules))

rules_2 = [x for x in all_rules if x[0] == 2]
rules_3 = [x for x in all_rules if x[0] == 3]


def eq(w1: np.ndarray, w2: np.ndarray):
    return (w1 == w2).all()


board = np.array([[0, 1, 0], [0, 0, 1], [1, 1, 1]])
for i in range(repetitions):
    print(i)
    side = 2 if (len(board) % 2) == 0 else 3
    rules = rules_2 if side == 2 else rules_3
    new_side = side + 1
    new_len = len(board) + int(len(board) / side)
    result = np.zeros((new_len, new_len))
    for y in range(0, int(len(board) / side)):
        for x in range(0, int(len(board) / side)):
            _y = y * side
            _x = x * side
            __y = y * new_side
            __x = x * new_side
            slc = board[_y:_y + side, _x:_x + side]
            # NOTE: this is kinda slow, bot got me the result in under 5min, so I'm leaving it
            for r in rules:
                if eq(r[1], slc):
                    result[__y:__y + new_side, __x:__x + new_side] = r[2]
                    break
    board = result

print(np.count_nonzero(board))
