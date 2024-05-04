import common
from typing import NamedTuple


class Particle(NamedTuple):
    p: list
    v: list
    a: list


data = common.read_file()
lines = data.splitlines()


def parse_line(line: str):
    def extract_nums(segment):
        nums_joined = segment[3:-1]
        num_strings = nums_joined.split(',')
        return list(map(int, num_strings))
    segments = line.split(', ')
    return Particle(
        p=extract_nums(segments[0]),
        v=extract_nums(segments[1]),
        a=extract_nums(segments[2]))


def m_len(vec):
    return sum(map(abs, vec))


particles = list(map(parse_line, lines))

min_particle = None
min_a = None
min_v = None

curr_particle = -1
for particle in particles:
    curr_particle += 1
    a_len = m_len(particle.a)
    v_len = m_len(particle.v)
    if min_a is None or a_len < min_a or (a_len == min_a and v_len < min_v):
        min_a = a_len
        min_v = v_len
        min_particle = curr_particle

print(min_particle)


# part 2
def add(position, offset):
    position[0] += offset[0]
    position[1] += offset[1]
    position[2] += offset[2]


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

    for pos, indices in positions.items():
        if len(indices) > 1:
            for idx in indices:
                particles[idx] = None

nones = particles.count(None)
print(len(particles) - nones)
