import common
from queue import PriorityQueue
import math

lines = common.read_file().splitlines()

blueprints = []
for line in lines:
    blueprints.append(common.extract_numbers(line)[1:])

# safe max points calculation - when buying a geo robot every turn
def calc_potential(time, geo, geo_r):
    return geo + sum(range(geo_r, geo_r+time))

# prioritise paths with more of more advanced robots
def fill_priority(item):
    _, _, _, _, _, ore_r, clay_r, obsid_r, geo_r = item
    return (-geo_r, -obsid_r, -clay_r, -ore_r), *item

def new_state(
        turns,
        state,
        d_ore=0,
        d_clay=0,
        d_obsid=0,
        d_ore_r=0,
        d_clay_r=0,
        d_obsid_r=0,
        d_geo_r=0):
    _, time, ore, clay, obsid, geo, ore_r, clay_r, obsid_r, geo_r = state
    n_state = (
        time - turns,
        ore + turns * ore_r + d_ore,
        clay + turns * clay_r + d_clay,
        obsid + turns * obsid_r + d_obsid,
        geo + turns * geo_r,
        ore_r + d_ore_r,
        clay_r + d_clay_r,
        obsid_r + d_obsid_r,
        geo_r + d_geo_r,
    )
    return fill_priority(n_state)

def solve(blueprint, max_time):
    ore_r_ore_c, clay_r_ore_c, obsid_r_ore_c, obsid_r_clay_c, \
            geo_r_ore_c, geo_r_obsid_c = blueprint
    max_ore_c = max(ore_r_ore_c, clay_r_ore_c, obsid_r_ore_c, geo_r_ore_c)
    max_clay_c = obsid_r_clay_c
    max_obsid_c = geo_r_obsid_c
    q = PriorityQueue()
    q.put(fill_priority((max_time, 0, 0, 0, 0, 1, 0, 0, 0)))
    max_geo = 0
    while not q.empty():
        state = q.get()
        _, time, ore, clay, obsid, geo, ore_r, clay_r, obsid_r, geo_r = state

        # too much time spent
        if time < 0:
            continue

        # skip if can't reach better score
        potential = calc_potential(time, geo, geo_r)
        if potential <= max_geo:
            continue

        # buying those robots can't help anymore
        if ore_r > max_ore_c:
            continue
        if clay_r > max_clay_c:
            continue
        if obsid_r > max_obsid_c:
            continue

        # update max if at the end of time will have more geo
        curr_end_geo = geo+time*geo_r
        if curr_end_geo > max_geo:
            max_geo = curr_end_geo

        # path where buying a geo robot
        if obsid_r > 0:
            needed_ore_turns = max(math.ceil((geo_r_ore_c-ore)/ore_r), 0)
            needed_obsid_turns = max(math.ceil((geo_r_obsid_c-obsid)/obsid_r), 0)
            turns = max(needed_ore_turns, needed_obsid_turns) + 1
            q.put(new_state(
                turns,
                state,
                d_ore=-geo_r_ore_c,
                d_obsid=-geo_r_obsid_c,
                d_geo_r=1))

        # path where buying an obsidian robot
        if clay_r > 0:
            needed_ore_turns = max(math.ceil((obsid_r_ore_c-ore)/ore_r), 0)
            needed_clay_turns = max(math.ceil((obsid_r_clay_c-clay)/clay_r), 0)
            turns = max(needed_ore_turns, needed_clay_turns) + 1
            q.put(new_state(
                turns,
                state,
                d_ore=-obsid_r_ore_c,
                d_clay=-obsid_r_clay_c,
                d_obsid_r=1))

        # path where buying a clay robot
        turns = max(math.ceil((clay_r_ore_c-ore)/ore_r), 0) + 1
        q.put(new_state(turns, state, d_ore=-clay_r_ore_c, d_clay_r=1))

        # path where buying an ore robot
        turns = max(math.ceil((ore_r_ore_c-ore)/ore_r), 0) + 1
        q.put(new_state(turns, state, d_ore=-ore_r_ore_c, d_ore_r=1))

    return max_geo

def part1():
    results = []
    acc = 0
    for i in range(len(blueprints)):
        blueprint = blueprints[i]
        result = solve(blueprint, 24)
        results.append(result)
        acc += (i+1)*result

    print(acc)

def part2():
    amo = min(len(blueprints), 3)
    results = []
    acc = 1
    for i in range(amo):
        blueprint = blueprints[i]
        result = solve(blueprint, 32)
        results.append(result)
        acc *= result

    print(acc)

part1()
part2()
