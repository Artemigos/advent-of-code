import common

data = common.read_file()

def read_marker(start, data=data):
    end = data.index(')', start)
    offset = end-start+1
    marker_segments = data[start+1:end].split('x')
    return (int(marker_segments[0]), int(marker_segments[1]), offset)

# part 1
output = ''
i = 0
while i < len(data):
    if data[i] == '(':
        length, repetitions, offset = read_marker(i)
        i += offset
        data_slice = data[i:i+length]
        i += length
        for _ in range(repetitions):
            output += data_slice
    else:
        output += data[i]
        i += 1

print(len(output)-1)

# part 2
def calc_length(data):
    result_len = 0
    i = 0
    while i < len(data):
        if data[i] == '(':
            length, repetitions, offset = read_marker(i, data)
            i += offset
            data_slice = data[i:i+length]
            i += length
            inner_len = calc_length(data_slice)
            result_len += inner_len*repetitions
        else:
            result_len += 1
            i += 1
    return result_len

result = calc_length(data)
print(result-1)
