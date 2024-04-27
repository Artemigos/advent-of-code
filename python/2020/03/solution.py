import common

m = common.read_file('2020/03/data.txt').splitlines()
w = len(m[0])

def count_trees(dx, dy):
    x, y = 0, 0
    trees = 0
    while y < len(m):
        if m[y][x] == '#':
            trees += 1
        x += dx
        x %= w
        y += dy
    return trees

# part 1
print(count_trees(3, 1))

# part 2
t1 = count_trees(1, 1)
t2 = count_trees(3, 1)
t3 = count_trees(5, 1)
t4 = count_trees(7, 1)
t5 = count_trees(1, 2)
print(t1 * t2 * t3 * t4 * t5)
