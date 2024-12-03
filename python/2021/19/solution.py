from dataclasses import dataclass, field
from itertools import product
from typing import List, Tuple
import common

REQ_INTERSECT = 12
lines = common.read_file().splitlines()

# parse data

Vector3 = Tuple[int, int, int]

@dataclass
class Beacon:
    positions: List[Vector3]
    other_beacons_relative_positions: List[List[Vector3]] = field(default_factory=lambda: [])

@dataclass
class Scanner:
    beacons: List[Beacon]

scanners = []
beacons = []
for line in lines:
    if line == '':
        scanners.append(Scanner(beacons))
        beacons = []
        continue
    if line[:3] == '---':
        continue
    x, y, z = map(int, line.split(','))
    rots = list(common.all_rotations(x, y, z))
    beacons.append(Beacon(rots))
scanners.append(Scanner(beacons))

# index beacon data

for scanner in scanners:
    for i in range(len(scanner.beacons)):
        b1 = scanner.beacons[i]
        for rot in range(24):
            rotated_beacons: List[Vector3] = []
            for j in range(len(scanner.beacons)):
                b2 = scanner.beacons[j]
                x = b2.positions[rot][0] - b1.positions[rot][0]
                y = b2.positions[rot][1] - b1.positions[rot][1]
                z = b2.positions[rot][2] - b1.positions[rot][2]
                rotated_beacons.append((x, y, z))
            b1.other_beacons_relative_positions.append(rotated_beacons)

# part 1 and 2

connections = []

for scanner in scanners:
    for scanner2 in scanners:
        if scanner == scanner2:
            continue
        for beacon in scanner.beacons:
            positions = set(beacon.other_beacons_relative_positions[0])
            for beacon2 in scanner2.beacons:
                for rotation in beacon2.other_beacons_relative_positions:
                    if len(set(rotation).intersection(positions)) >= REQ_INTERSECT:
                        rotation_i = beacon2.other_beacons_relative_positions.index(rotation)
                        beacon_pos = beacon.positions[0]
                        beacon2_pos = beacon2.positions[rotation_i]
                        connections.append((
                            scanners.index(scanner), scanners.index(scanner2),
                            beacon_pos[0] - beacon2_pos[0], beacon_pos[1] - beacon2_pos[1], beacon_pos[2] - beacon2_pos[2],
                            rotation_i))
                        break
                else:
                    continue
                break
            else:
                continue
            break

def get_beacon_points(scanner):
    return [(b.positions[0][0], b.positions[0][1], b.positions[0][2]) for b in scanner.beacons]

def get_all_points(point_selector, scanner_i, skip_scanners):
    scanner = scanners[scanner_i]
    points = point_selector(scanner)
    skip_scanners.append(scanner_i)
    for conn in connections:
        s1, s2, dx, dy, dz, rot = conn
        if s1 != scanner_i or s2 in skip_scanners:
            continue
        for pt in get_all_points(point_selector, s2, skip_scanners):
            x, y, z = common.rotation_functions[rot](*pt)
            points.append((x+dx, y+dy, z+dz))
    return list(set(points))

pts = get_all_points(get_beacon_points, 0, [])
print(len(pts))

scanner_pts = get_all_points(lambda _: [(0, 0, 0)], 0, [])
distances = [common.manhattan_dist(p1, p2) for p1, p2 in product(scanner_pts, scanner_pts)]
print(max(distances))
