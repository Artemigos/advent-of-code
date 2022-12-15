use std::collections::HashSet;
use itertools::iproduct;

struct Beacon {
    positions: Vec<(i32, i32, i32)>,
    other_beacons_relative_positions: Vec<Vec<(i32, i32, i32)>>,
}

impl Beacon {
    fn new(positions: Vec<(i32, i32, i32)>) -> Self {
        Self {
            positions,
            other_beacons_relative_positions: vec![],
        }
    }
}

struct Scanner {
    beacons: Vec<Beacon>,
}

fn get_beacon_points(scanner: &Scanner) -> Vec<(i32, i32, i32)> {
    (&scanner.beacons)
        .into_iter()
        .map(|x| x.positions[0])
        .collect()
}

struct Rotations {
    functions: Vec<Box<dyn Fn(i32, i32, i32) -> (i32, i32, i32)>>,
}

impl Rotations {
    fn new() -> Self {
        Self {
            functions: vec![
                Box::new(|x, y, z| (x, y, z)),
                Box::new(|x, y, z| (z, y, -x)),
                Box::new(|x, y, z| (-x, y, -z)),
                Box::new(|x, y, z| (-z, y, x)),
                Box::new(|x, y, z| (y, z, x)),
                Box::new(|x, y, z| (y, x, -z)),
                Box::new(|x, y, z| (y, -z, -x)),
                Box::new(|x, y, z| (y, -x, z)),
                Box::new(|x, y, z| (-x, -y, z)),
                Box::new(|x, y, z| (z, -y, x)),
                Box::new(|x, y, z| (x, -y, -z)),
                Box::new(|x, y, z| (-z, -y, -x)),
                Box::new(|x, y, z| (-y, z, -x)),
                Box::new(|x, y, z| (-y, -x, -z)),
                Box::new(|x, y, z| (-y, -z, x)),
                Box::new(|x, y, z| (-y, x, z)),
                Box::new(|x, y, z| (z, x, y)),
                Box::new(|x, y, z| (x, -z, y)),
                Box::new(|x, y, z| (-z, -x, y)),
                Box::new(|x, y, z| (-x, z, y)),
                Box::new(|x, y, z| (x, z, -y)),
                Box::new(|x, y, z| (z, -x, -y)),
                Box::new(|x, y, z| (-x, -z, -y)),
                Box::new(|x, y, z| (-z, x, -y)),
            ],
        }
    }

    fn all_rotations(&self, x: i32, y: i32, z: i32) -> Vec<(i32, i32, i32)> {
        (&self.functions)
            .into_iter()
            .map(|rot| rot(x, y, z))
            .collect()
    }
}

fn manhattan_dist(p1: (i32, i32, i32), p2: (i32, i32, i32)) -> i32 {
    (p1.0 - p2.0).abs() + (p1.1 - p2.1).abs() + (p1.2 - p2.2).abs()
}

struct State {
    scanners: Vec<Scanner>,
    connections: Vec<(usize, usize, i32, i32, i32, usize)>,
    rotations: Rotations,
}

impl State {
    fn new() -> Self {
        Self {
            scanners: vec![],
            connections: vec![],
            rotations: Rotations::new(),
        }
    }

    fn get_all_points<'a, FSel: Fn(&'a Scanner) -> Vec<(i32, i32, i32)>>(
        &'a self,
        point_selector: &FSel,
        scanner_i: usize,
        skip_scanners: &mut Vec<usize>,
    ) -> Vec<(i32, i32, i32)> {
        let scanner = &self.scanners[scanner_i];
        let mut points = point_selector(&scanner);
        skip_scanners.push(scanner_i);

        for conn in &self.connections {
            let (s1, s2, dx, dy, dz, rot) = *conn;
            if s1 != scanner_i || skip_scanners.contains(&s2) {
                continue;
            }

            for pt in self.get_all_points(point_selector, s2, skip_scanners) {
                let (x, y, z) = self.rotations.functions[rot](pt.0, pt.1, pt.2);
                points.push((x + dx, y + dy, z + dz));
            }
        }

        let points_set: HashSet<(i32, i32, i32)> = HashSet::from_iter(points.into_iter().map(|x| x.clone()));
        points_set.into_iter().collect()
    }
}

fn main() {
    const REQ_INTERSECT: usize = 12;
    let mut state = State::new();

    // parse data
    let data = std::fs::read_to_string("data.txt").unwrap();
    let mut beacons = vec![];
    for line in data.lines() {
        if line == "" {
            state.scanners.push(Scanner { beacons });
            beacons = vec![];
            continue;
        }
        if line.starts_with("---") {
            continue;
        }
        let coordinates: Vec<i32> = line.split(",").map(|x| { x.parse::<i32>().unwrap() }).collect();
        let (x, y, z) = (coordinates[0], coordinates[1], coordinates[2]);
        let rots = state.rotations.all_rotations(x, y, z);
        beacons.push(Beacon::new(rots));
    }

    state.scanners.push(Scanner { beacons });

    // index beacon data
    for scanner in &mut state.scanners {
        // FIXME: inefficient hack (because of clone), don't know how to get around borrow checker to mut-iterate the same vector twice
        let positions: Vec<Vec<(i32, i32, i32)>> = (&scanner.beacons).into_iter().map(|x| x.positions.clone()).collect();

        for b1 in &mut scanner.beacons {
            for rot in 0..24 {
                let mut rotated_beacons = vec![];
                for b2 in &positions {
                    let x = b2[rot].0 - b1.positions[rot].0;
                    let y = b2[rot].1 - b1.positions[rot].1;
                    let z = b2[rot].2 - b1.positions[rot].2;
                    rotated_beacons.push((x, y, z));
                }
                b1.other_beacons_relative_positions.push(rotated_beacons);
            }
        }
    }

    // part 1 and 2
    for scanner_i in 0..state.scanners.len() {
        let scanner = &state.scanners[scanner_i];
        for scanner2_i in 0..state.scanners.len() {
            let scanner2 = &state.scanners[scanner2_i];
            if scanner_i == scanner2_i {
                continue;
            }

            let mut connection_found = false;
            for beacon in &scanner.beacons {
                let positions: HashSet<(i32, i32, i32)> = HashSet::from_iter((&beacon.other_beacons_relative_positions[0]).into_iter().map(|x| x.clone()));
                for beacon2 in &scanner2.beacons {
                    for rotation in &beacon2.other_beacons_relative_positions {
                        let rotation_set: HashSet<(i32, i32, i32)> = HashSet::from_iter(rotation.into_iter().map(|x| x.clone()));
                        if rotation_set.intersection(&positions).collect::<Vec<&(i32, i32, i32)>>().len() >= REQ_INTERSECT {
                            let rotation_i = beacon2.other_beacons_relative_positions.iter().position(|x| x == rotation).unwrap();
                            let beacon_pos = &beacon.positions[0];
                            let beacon2_pos = beacon2.positions[rotation_i];
                            state.connections.push((
                                scanner_i, scanner2_i,
                                beacon_pos.0 - beacon2_pos.0, beacon_pos.1 - beacon2_pos.1, beacon_pos.2 - beacon2_pos.2,
                                rotation_i));
                            connection_found = true;
                            break;
                        }
                    }

                    if connection_found {
                        break;
                    }
                }

                if connection_found {
                    break;
                }
            }
        }
    }

    let pts = state.get_all_points(&get_beacon_points, 0, &mut vec![]);
    println!("{}", pts.len());

    let scanner_pts = state.get_all_points(&|_| vec![(0, 0, 0)], 0, &mut vec![]);
    let distances = iproduct!(&scanner_pts, &scanner_pts).map(|(x, y)| manhattan_dist(*x, *y));
    println!("{}", distances.max().unwrap());
}
