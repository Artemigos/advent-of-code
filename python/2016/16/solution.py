import common

data = common.read_file().strip()

def solve(data, desired_size):
    bits = list(map(int, data))

    # generate data
    while len(bits) < desired_size:
        b = list(bits)
        b.reverse()
        b = list(map(lambda x: 1-x, b))
        bits.append(0)
        for bit in b:
            bits.append(bit)

    # checksum
    checksum = list(bits[:desired_size])
    while len(checksum)%2 == 0:
        result = []
        for i in range(0, len(checksum), 2):
            result.append(1-(checksum[i]^checksum[i+1]))
        checksum = result

    checksum_str = ''.join(map(str, checksum))
    print(checksum_str)

solve(data, 272)
solve(data, 35651584)
