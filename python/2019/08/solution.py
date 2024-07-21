import common

data = common.read_file().strip()
width = 25
height = 6

layer_size = width*height

# part 1
min_zeros = None
min_result = None
for layer_offset in range(0, len(data), layer_size):
    values = {'0': 0, '1': 0, '2': 0}
    for layer_i in range (layer_offset, layer_offset+layer_size):
        c = data[layer_i]
        values[c] += 1

    if min_zeros is None or values['0'] < min_zeros:
        min_zeros = values['0']
        min_result = values['1']*values['2']

print(min_result)

# part 2
image = ['2'] * layer_size

for layer_offset in reversed(range(0, len(data), layer_size)):
    for layer_i in range(layer_offset, layer_offset+layer_size):
        c = data[layer_i]
        if c != '2':
            image[layer_i-layer_offset] = c

for y in range(height):
    for x in range(width):
        c = '!'
        image_c = image[width*y+x]
        if image_c == '0':
            c = ' '
        elif image_c == '1':
            c = '▓'
        print(c, end='')
    print()
