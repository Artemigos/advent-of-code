import common

alpha = ' abcdefghijklmnopqrstuvwxyz'

for a in alpha:
    data = common.read_file()
    data = data.replace(a, '')
    data = data.replace(a.upper(), '')
    curr_data = data

    while True:
        found = False
        new_data = curr_data
        for b in alpha:
            p1 = b+b.upper()
            p2 = b.upper()+b
            new_data = new_data.replace(p1, '')
            new_data = new_data.replace(p2, '')
        if len(new_data) == len(curr_data):
            break
        curr_data = new_data
    print(a, len(curr_data))

