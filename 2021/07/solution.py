import common

positions = common.to_int(common.read_file('2021/07/data.txt').split(','))
min_pos = min(positions)
max_pos = max(positions)

# part 1 and 2

fuel_cost = [0]*(max_pos-min_pos+1)
fuel_cost2 = [0]*(max_pos-min_pos+1)

for crab in positions:
    for i in range(min_pos, max_pos+1):
        diff = abs(i-crab)
        fuel_cost[i] += diff
        fuel_cost2[i] += sum(range(diff+1))

print(min(fuel_cost))
print(min(fuel_cost2))
