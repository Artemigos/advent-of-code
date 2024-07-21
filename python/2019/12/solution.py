import math
import common
from collections import defaultdict

data = common.read_file().splitlines()
positions = list(map(tuple, map(common.extract_numbers, data)))
steps = 1000

def lcm(a, b, c):
    lcm_ab = abs(a*b)//math.gcd(a, b)
    return abs(lcm_ab*c)//math.gcd(lcm_ab, c)

curr_pos = list(positions)
curr_vel = [(0, 0, 0)]*len(curr_pos)

def calc_gravity_center():
    summed = (0, 0, 0)
    for moon in curr_pos:
        summed = summed[0]+moon[0], summed[1]+moon[1], summed[2]+moon[2]
    amount = len(curr_pos)
    summed = summed[0]/amount, summed[1]/amount, summed[2]/amount
    return summed

step = 0
seen_states = defaultdict(lambda: dict())
resolved_loops = dict()

while True:
    new_pos = list(curr_pos)
    for i in range(len(curr_pos)):
        # apply gravity
        for j in range(len(curr_pos)):
            if i == j:
                continue
            m1 = curr_pos[i]
            m2 = curr_pos[j]
            v_change = list(curr_vel[i])
            for k in range(len(v_change)):
                if m2[k] > m1[k]:
                    v_change[k] += 1
                elif m2[k] < m1[k]:
                    v_change[k] -= 1
            curr_vel[i] = tuple(v_change)
        
        # move
        pos = new_pos[i]
        vel = curr_vel[i]
        new_pos[i] = pos[0]+vel[0], pos[1]+vel[1], pos[2]+vel[2]

    # look for loops
    for dim in range(3):
        if dim in resolved_loops:
            continue

        dim_values = []
        for i in range(len(curr_pos)):
            dim_values.append(curr_pos[i][dim])
            dim_values.append(curr_vel[i][dim])
        key = tuple(dim_values)
        if key in seen_states[dim]:
            resolved_loops[dim] = step-seen_states[dim][key]
        else:
            seen_states[dim][key] = step

    if len(resolved_loops) == 3:
        loop_sizes = list(resolved_loops.values())
        print(lcm(loop_sizes[0], loop_sizes[1], loop_sizes[2]))
        break

    # update state
    curr_pos = new_pos

    step += 1
    if step == steps:
        # calculate energy
        energy = 0
        for i in range(len(curr_pos)):
            pos = curr_pos[i]
            vel = curr_vel[i]
            pot = abs(pos[0])+abs(pos[1])+abs(pos[2])
            kin = abs(vel[0])+abs(vel[1])+abs(vel[2])
            energy += pot * kin

        print(energy)
