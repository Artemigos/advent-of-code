data = '.^^^.^.^^^^^..^^^..^..^..^^..^.^.^.^^.^^....^.^...^.^^.^^.^^..^^..^.^..^^^.^^...^...^^....^^.^^^^^^^'
amount_needed = 40
amount_needed = 400000 # part 2

rows = []

def add_row(row):
    rows.append([True]+row+[True])

add_row(list(map(lambda x: x == '.', data)))

for i in range(amount_needed-1):
    row = []
    for j in range(len(data)):
        row.append(rows[i][j] == rows[i][j+2])
    add_row(row)

amount = sum(map(lambda row: sum(map(lambda x: 1 if x else 0, row))-2, rows))
print(amount)
