from queue import PriorityQueue
import common

lines = common.read_file().splitlines()
rows = []
for line in lines:
    nums = common.extract_numbers(line)
    rows.append(tuple(nums))

X = 0
Y = 1
Z = 2
R = 3

def manhattan_dist(pos1, pos2):
    return abs(pos1[X]-pos2[X])+abs(pos1[Y]-pos2[Y])+abs(pos1[Z]-pos2[Z])

def sees(bot, point):
    return manhattan_dist(bot, point) <= bot[R]

# part 1
max_range_bot = max(rows, key=lambda x: x[R])
max_range_bot_pos = max_range_bot[:R]
max_range_bot_range = max_range_bot[R]

in_range_count = 0
for row in rows:
    dist = manhattan_dist(max_range_bot_pos, row)
    if dist <= max_range_bot_range:
        in_range_count += 1

print('part 1:', in_range_count)

# part 2
minx = min(map(lambda x: x[X], rows))-max_range_bot_range
maxx = max(map(lambda x: x[X], rows))+max_range_bot_range
miny = min(map(lambda x: x[Y], rows))-max_range_bot_range
maxy = max(map(lambda x: x[Y], rows))+max_range_bot_range
minz = min(map(lambda x: x[Z], rows))-max_range_bot_range
maxz = max(map(lambda x: x[Z], rows))+max_range_bot_range
space = (minx, maxx, miny, maxy, minz, maxz)

def search_space(space, evaluator):
    def partition_by(segments, i1, i2):
        new_segments = []
        for segment in segments:
            if segment[i1] == segment[i2]:
                return segments
            middle = (segment[i2]-segment[i1])//2
            if middle == 0:
                copy = list(segment)
                copy[i2] = segment[i1]
                new_segments.append(tuple(copy))
                copy = list(segment)
                copy[i1] = segment[i2]
                new_segments.append(tuple(copy))
            else:
                copy = list(segment)
                copy[i2] = segment[i1]+middle
                new_segments.append(tuple(copy))
                copy = list(segment)
                copy[i1] += middle+1
                new_segments.append(tuple(copy))
        return new_segments

    min_val = None
    min_data = None
    q = PriorityQueue()
    q.put(((0, 0), 0, space))
    while not q.empty():
        _, depth, segment = q.get()
        rank = evaluator(segment, depth)
        if min_val is not None and rank > min_val:
            continue

        is_leaf = segment[0] == segment[1] and segment[2] == segment[3] and segment[4] == segment[5]
        if is_leaf:
            min_val = rank
            min_data = segment
        else:
            segments = partition_by([segment], 0, 1)
            segments = partition_by(segments, 2, 3)
            segments = partition_by(segments, 4, 5)

            for p in segments:
                q.put((rank, depth+1, p))

    return (min_val, min_data)

def segment_corners(segment):
    x1, x2, y1, y2, z1, z2 = segment
    yield (x1, y1, z1)
    yield (x1, y1, z2)
    yield (x1, y2, z1)
    yield (x1, y2, z2)
    yield (x2, y1, z1)
    yield (x2, y1, z2)
    yield (x2, y2, z1)
    yield (x2, y2, z2)

def min_segment_manhattan_dist(point, segment):
    def dimension_dist(pi, si1, si2):
        if point[pi] > segment[si2]:
            return point[pi] - segment[si2]
        elif point[pi] < segment[si1]:
            return segment[si1] - point[pi]
        else:
            return 0

    return dimension_dist(X, 0, 1) + dimension_dist(Y, 2, 3) + dimension_dist(Z, 4, 5)

def eval_segment(segment, depth):
    amount = 0
    for row in rows:
        if row[X] >= segment[0] and row[X] <= segment[1] and row[Y] >= segment[2] and row[Y] <= segment[3] and row[Z] >= segment[4] and row[Z] <= segment[5]:
            amount += 1
        else:
            for corner in segment_corners(segment):
                if sees(row, corner):
                    amount += 1
                    break
    return -amount, -depth, min_segment_manhattan_dist((0, 0, 0), segment)

found_val, found_segment = search_space(space, eval_segment)
found_dist = manhattan_dist((found_segment[0], found_segment[2], found_segment[4]), (0, 0, 0))
print('part 2:', found_dist)
