import common

data = common.to_int(common.read_file().split(','))

# part 1
def find_num(limit):
    last_seen = {}
    last_num = -1

    for i in range(limit):
        if i < len(data):
            new_num = data[i]
        elif last_num not in last_seen:
            new_num = 0
        else:
            new_num = i - last_seen[last_num]
        last_seen[last_num] = i
        last_num = new_num

    return last_num

print(find_num(2020))

# part 2
print(find_num(30000000))
