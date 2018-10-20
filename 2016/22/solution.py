import numpy as np
import common

lines = common.read_file('2016/22/data.txt').splitlines()[2:]

def parse_line(line: str):
    segments = line.split()
    name_segments = segments[0].split('-')
    x = int(name_segments[-2][1:])
    y = int(name_segments[-1][1:])
    used = int(segments[2][:-1])
    avail = int(segments[3][:-1])
    return (x, y, used, avail)

nodes_lst = list(map(parse_line, lines))

# part 1
found = 0
for i in range(len(nodes_lst)):
    for j in range(i+1, len(nodes_lst)):
        x1, y1, used1, avail1 = nodes_lst[i]
        x2, y2, used2, avail2 = nodes_lst[j]
        if used1 > 0 and used1 <= avail2:
            found += 1
        if used2 > 0 and used2 <= avail1:
            found += 1

print(found)

# part 2
# w = max(nodes_lst, key=lambda x: x[0])[0]+1
# h = max(nodes_lst, key=lambda x: x[1])[1]+1
# grid = np.zeros((w, h), dtype=(np.int, 2))
# for x, y, used, avail in nodes_lst:
#     grid[x, y] = (used, used+avail)
