import common

alpha = ' abcdefghijklmnopqrstuvwxyz'

data = common.read_file().strip()
min_len = len(data)

for a in alpha:
    curr_data = data.replace(a, '')
    curr_data = curr_data.replace(a.upper(), '')

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

    if len(curr_data) < min_len:
        min_len = len(curr_data)
    if a == ' ':
        print(len(curr_data))
print(min_len)
