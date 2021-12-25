rotation_functions = [
    lambda x, y, z: (x, y, z),
    lambda x, y, z: (z, y, -x),
    lambda x, y, z: (-x, y, -z),
    lambda x, y, z: (-z, y, x),
    lambda x, y, z: (y, z, x),
    lambda x, y, z: (y, x, -z),
    lambda x, y, z: (y, -z, -x),
    lambda x, y, z: (y, -x, z),
    lambda x, y, z: (-x, -y, z),
    lambda x, y, z: (z, -y, x),
    lambda x, y, z: (x, -y, -z),
    lambda x, y, z: (-z, -y, -x),
    lambda x, y, z: (-y, z, -x),
    lambda x, y, z: (-y, -x, -z),
    lambda x, y, z: (-y, -z, x),
    lambda x, y, z: (-y, x, z),
    lambda x, y, z: (z, x, y),
    lambda x, y, z: (x, -z, y),
    lambda x, y, z: (-z, -x, y),
    lambda x, y, z: (-x, z, y),
    lambda x, y, z: (x, z, -y),
    lambda x, y, z: (z, -x, -y),
    lambda x, y, z: (-x, -z, -y),
    lambda x, y, z: (-z, x, -y),
]

def rot_x(x, y, z):
    return (x, z, -y)

def rot_y(x, y, z):
    return (z, y, -x)

def rot_z(x, y, z):
    return (y, -x, z)

def all_rotations(x, y, z):
    for i in range(24):
        yield rotation_functions[i](x, y, z)