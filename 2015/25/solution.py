row = 3010
column = 3019

# looking for ordinal for this cell
ordinal = 1
for i in range(row):
    ordinal += i
for i in range(column-1):
    ordinal += row+1+i

start = 20151125
curr = start
for i in range(1, ordinal):
    curr *= 252533
    curr %= 33554393

print(curr)
