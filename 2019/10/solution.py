import common
import math

def run(file):
    data = list(map(list, common.read_file('2019/10/'+file+'.txt').splitlines()))
    width = len(data[0])
    height = len(data)

    def sees_asteroid_in_direction(x, y, ox, oy):
        cx, cy = x+ox, y+oy
        while cx >= 0 and cx < width and cy >= 0 and cy < height:
            if data[cy][cx] == '#':
                return True, cx, cy
            cx += ox
            cy += oy
        return False, None, None

    max_amount = 0
    max_pos = None
    angles = set()

    for ox in range(-width, width):
        for oy in range(-height, height):
            if math.gcd(ox, oy) == 1:
                angles.add((ox, oy))

    for y in range(height):
        for x in range(width):
            c = data[y][x]
            if c != '#':
                continue

            amount = 0
            for ox, oy in iter(angles):
                success, _, _ = sees_asteroid_in_direction(x, y, ox, oy)
                if success:
                    amount += 1

            if amount > max_amount:
                max_amount = amount
                max_pos = (x, y)

    print(file+':')
    print('part 1:', max_amount)

    # part 2
    mod_angles = []
    for ox, oy in iter(angles):
        theta = (math.atan2(oy, ox)+(math.pi/2)) % (2*math.pi)
        mod_angles.append((theta, ox, oy))
    mod_angles = sorted(mod_angles)
    x, y = max_pos
    removed = 0
    for theta, ox, oy in iter(mod_angles):
        success, cx, cy = sees_asteroid_in_direction(x, y, ox, oy)
        if success:
            data[cy][cx] = '.'
            removed += 1
            # print('asteroid no.', removed, 'removed at', cx, cy)
            if removed == 200:
                print('part 2:', cx*100+cy)
                break

# print('expecting part 1: 8')
# run('sample')
# print('expecting part 1: 33')
# run('sample2')
# print('expecting part 1: 35')
# run('sample3')
# print('expecting part 1: 41')
# run('sample4')
# print('expecting part 1: 210')
# run('sample5')
run('data')
