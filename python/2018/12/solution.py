import common
import collections as coll
import queue
import itertools
import functools
import numpy as np
import re

def parse_line(line: str):
    segments = line.split(' ')
    return (list(segments[0]), segments[2])

def run_simulation(rules_path, initial, generations, label, padding_left = 50, padding_right = 100):
    data = common.read_file('2018/12/data.txt').splitlines()
    parsed = [parse_line(x) for x in data]

    size = len(initial)+padding_left+padding_right
    i0 = -padding_left
    state = '.'*padding_left+initial+'.'*padding_right
    state = list(state)

    seen_trim_states = {}

    g = 0
    while g < generations:
        # calculate new state
        print(g/generations, end='\r')
        new_state = '.'*size
        new_state = list(new_state)
        for i in range(2, len(state)-2):
            for rule in parsed:
                if state[i-2:i+3] == rule[0]:
                    new_state[i] = rule[1]
                    break
            else:
                new_state[i] = '.'
        state = new_state

        # diagnostics
        if g%1000 == 0:
            for i in range(-1, -7, -1):
                if state[i] == '#':
                    print('right end reached!')
                    break
            for i in range(0, 6):
                if state[i] == '#':
                    print('left end reached!')
                    break

        # detect travelling loops
        hashable_state = ''.join(state)
        trimmed_state = hashable_state.strip('.')
        start = hashable_state.index('#')
        if trimmed_state in seen_trim_states:
            print('travelling loop!', seen_trim_states[trimmed_state], g, start)
            print(trimmed_state)
            loop_size = g-seen_trim_states[trimmed_state][0]
            loop_relocation = start-seen_trim_states[trimmed_state][1]
            print('loop size', loop_size)
            print('loop relocation', loop_relocation)
            print('at generation', g)
            diff = generations-1-g
            skipped_loops = diff // loop_size
            print('skipping', skipped_loops, 'loops')
            move = skipped_loops * loop_size
            g += move
            print('moved to generation', g)
            print('current offset', i0)
            i0 += loop_relocation*skipped_loops
            print('moved to offset', i0)
            seen_trim_states.clear()
        else:
            seen_trim_states[trimmed_state] = (g, start)

        g += 1

    # calculate puzzle result
    acc = 0
    for i in range(len(state)):
        if state[i] == '#':
            acc += (i+i0)
    print()
    print(label, acc)

# part 1
run_simulation(
    '2018/12/data.txt',
    '..##.#######...##.###...#..#.#.#..#.##.#.##....####..........#..#.######..####.#.#..###.##..##..#..#',
    20,
    'part 1:',
    1000,
    1000)

# part 2
run_simulation(
    '2018/12/data.txt',
    '..##.#######...##.###...#..#.#.#..#.##.#.##....####..........#..#.######..####.#.#..###.##..##..#..#',
    50000000000,
    'part 2:',
    1000,
    2000)

# sample
# initial = '#..#.#..##......###...###'