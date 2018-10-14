import common
from typing import NamedTuple

class Particle(NamedTuple):
    p: list
    v: list
    a: list

data = common.read_file('2017/20/data.txt')
lines = data.splitlines()

def parse_line(line: str):
    def extract_nums(segment):
        nums_joined = segment[3:-1]
        num_strs = nums_joined.split(',')
        return list(map(int, num_strs))
    segments = line.split(', ')
    p = extract_nums(segments[0])
    v = extract_nums(segments[1])
    a = extract_nums(segments[2])
    return Particle(p, v, a)

def m_len(vec):
    return sum(map(abs, vec))

particles = list(map(parse_line, lines))

min_a_particle = None
min_a = None
min_a_particle_data = None

curr_particle = -1
for particle in particles:
    curr_particle += 1
    a_len = m_len(particle.a)
    if min_a == None or a_len < min_a:
        min_a = a_len
        min_a_particle = [curr_particle]
        min_a_particle_data = [particle]
    elif min_a == a_len:
        min_a_particle.append(curr_particle)
        min_a_particle_data.append(particle)

# NOTE: this result is inconclusive, but gives enough to figure it out manually (or try them all)
print(min_a_particle)
print(min_a)
print(min_a_particle_data)

# part 2
def add(pos, offset):
    pos[0] += offset[0]
    pos[1] += offset[1]
    pos[2] += offset[2]

for _ in range(10000):
    positions = dict()
    for i, p in enumerate(particles):
        if p is None:
            continue
        add(p.v, p.a)
        add(p.p, p.v)
        the_pos = tuple(p.p)
        curr_positions = positions[the_pos] if the_pos in positions.keys() else []
        curr_positions.append(i)
        positions[the_pos] = curr_positions

    for pos, idxs in positions.items():
        if len(idxs) > 1:
            for idx in idxs:
                particles[idx] = None

nones = particles.count(None)
print(len(particles) - nones)
