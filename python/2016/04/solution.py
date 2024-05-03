import common

lines = common.read_file().splitlines()

def parse_line(line: str):
    segments = line.rstrip(']').split('[')
    segments = segments[0].split('-') + [segments[1]]
    return segments

rooms = list(map(parse_line, lines))
real_rooms = []

for r in rooms:
    checksum = r[-1]
    name_segments = r[:-2]

    scores = dict()
    for s in name_segments:
        for c in s:
            if c in scores.keys():
                scores[c] +=1
            else:
                scores[c] = 1

    sorted_result = list(
        sorted(
            sorted(
                scores.items(),
                key=lambda x: x[0]
            ),
            key=lambda x: x[1],
            reverse=True
        )
    )
    valid = True
    for i in range(5):
        if checksum[i] != sorted_result[i][0]:
            valid = False
            break

    if valid:
        real_rooms.append(r)

print(sum(map(lambda x: int(x[-2]), real_rooms)))

# part 2
for r in real_rooms:
    name_segments = r[:-2]
    segment_id = int(r[-2])
    orda = ord('a')
    char_num = ord('z')-orda+1

    def decrypt(s: str):
        result = ''
        for c in s:
            num = (ord(c)-orda+segment_id)%char_num
            result += chr(num+orda)
        return result

    name = ' '.join(map(decrypt, name_segments))
    if name == 'northpole object storage':
        print(segment_id)
