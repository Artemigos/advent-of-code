import common

data = common.read_file('2019/12/data.txt').splitlines()
positions = list(map(tuple, map(common.extract_numbers, data)))
steps = 1000

# part 1
curr_pos = list(positions)
curr_vel = [(0, 0, 0)]*len(curr_pos)

def calc_gravity_center():
    summed = (0, 0, 0)
    for moon in curr_pos:
        summed = summed[0]+moon[0], summed[1]+moon[1], summed[2]+moon[2]
    amount = len(curr_pos)
    summed = summed[0]/amount, summed[1]/amount, summed[2]/amount
    return summed

gravity_center = 0, 0, 0
for _ in range(steps):
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
    curr_pos = new_pos
    new_center = calc_gravity_center()
    if new_center != gravity_center:
        print('gravity center changed to', new_center)
        gravity_center = new_center

# calculate energy
energy = 0
for i in range(len(curr_pos)):
    pos = curr_pos[i]
    vel = curr_vel[i]
    pot = abs(pos[0])+abs(pos[1])+abs(pos[2])
    kin = abs(vel[0])+abs(vel[1])+abs(vel[2])
    energy += pot * kin

print('part 1:', energy)
